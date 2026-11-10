"""Synthèse vocale de la série : voix neuronale Kokoro v1.0 (ONNX), voix française ff_siwis.

- Le texte de voix off est écrit « pour l'écran » (ADN, Na+, 10⁻⁷…). Il est converti
  en texte « pour l'oreille » par le lexique de prononciation (lexique.py).
- Les mots délicats peuvent recevoir une prononciation imposée en API (phonèmes).
- Chaque phrase est mise en cache (WAV) : un nouveau rendu ne resynthétise que ce qui change.
"""
import hashlib
import re
import numpy as np
import soundfile as sf

import config
import lexique

_KOKORO = None


def engine():
    global _KOKORO
    if _KOKORO is None:
        from kokoro_onnx import Kokoro
        _KOKORO = Kokoro(str(config.MODELS / "kokoro-v1.0.onnx"), str(config.MODELS / "voices-v1.0.bin"))
    return _KOKORO


MARK = re.compile(r"\*([^*]+)\*")


def strip_marks(text: str) -> str:
    return MARK.sub(r"\1", text)


def _num_fr(s: str) -> str:
    from num2words import num2words
    s = s.replace(" ", " ").replace("\xa0", " ")
    neg = s.startswith("-") or s.startswith("–")
    s = s.lstrip("-–")
    if "," in s:
        a, b = s.split(",", 1)
        a = a.replace(" ", "").replace(".", "")
        words = num2words(int(a), lang="fr") + " virgule " + (
            " ".join(num2words(int(d), lang="fr") for d in b) if b.startswith("0") else num2words(int(b), lang="fr"))
    else:
        words = num2words(int(s.replace(" ", "").replace(".", "")), lang="fr")
    return ("moins " if neg else "") + words


NUM = re.compile(r"(?<![\w'])[-–]?\d{1,3}(?:[ . \xa0]\d{3})+(?:,\d+)?(?![\w])|(?<![\w'])[-–]?\d+(?:,\d+)?(?![\w])")


def spoken(text: str) -> str:
    """Texte d'affichage → texte prononcé."""
    t = strip_marks(text)
    t = lexique.appliquer(t)
    t = NUM.sub(lambda m: _num_fr(m.group(0)), t)
    t = t.replace("%", " pour cent")
    t = re.sub(r"\s+", " ", t).strip()
    return t


def phonemes(text_spoken: str) -> str:
    """Phonémisation espeak-ng (fr-fr) + prononciations imposées du lexique."""
    k = engine()
    parts = []
    pos = 0
    keys = sorted(lexique.IPA, key=len, reverse=True)
    if keys:
        pat = re.compile(r"(?<!\w)(" + "|".join(re.escape(x) for x in keys) + r")(?!\w)", re.I)
        for m in pat.finditer(text_spoken):
            if m.start() > pos:
                parts.append(("t", text_spoken[pos:m.start()]))
            parts.append(("p", lexique.IPA[next(x for x in keys if x.lower() == m.group(1).lower())]))
            pos = m.end()
    parts.append(("t", text_spoken[pos:]))
    out = []
    for kind, val in parts:
        if kind == "p":
            out.append(val)
        elif val.strip():
            out.append(k.tokenizer.phonemize(val, lang="fr-fr").strip())
        elif val:
            out.append(" ")
    ph = " ".join(x.strip() for x in out if x.strip())
    ph = re.sub(r"\((?:en|fr|de|it|es)\)", "", ph)
    # ponctuation conservée par espeak : on garde la ponctuation finale du texte
    return ph


def synth(text_display: str):
    """Renvoie (audio float32 24 kHz, texte prononcé, phonèmes)."""
    sp = spoken(text_display)
    ph = phonemes(sp)
    key = hashlib.sha1(f"{config.VOICE}|{config.SPEED}|{ph}".encode()).hexdigest()[:20]
    cache = config.WORK / "tts" / f"{key}.wav"
    cache.parent.mkdir(parents=True, exist_ok=True)
    if cache.exists():
        audio, _ = sf.read(cache, dtype="float32")
        return audio, sp, ph
    k = engine()
    audio, sr = k.create(ph, voice=config.VOICE, speed=config.SPEED, lang="fr-fr", is_phonemes=True)
    assert sr == config.SR
    audio = trim(audio.astype(np.float32))
    sf.write(cache, audio, sr)
    return audio, sp, ph


def trim(a, thr=0.004, pad=0.03):
    idx = np.where(np.abs(a) > thr)[0]
    if len(idx) == 0:
        return a
    p = int(pad * config.SR)
    return a[max(0, idx[0] - p): min(len(a), idx[-1] + p)]


def split_sentences(text: str):
    text = re.sub(r"\s+", " ", text.strip())
    if not text:
        return []
    parts = re.split(r"(?<=[.!?…])\s+(?=[«“A-ZÀ-Ý0-9*])", text)
    out = []
    for p in parts:
        p = p.strip()
        if not p:
            continue
        # phrases très longues : découpe aux points-virgules / deux-points
        if len(p) > 260:
            sub = re.split(r"(?<=[;:])\s+", p)
            out.extend(s for s in sub if s.strip())
        else:
            out.append(p)
    return out
