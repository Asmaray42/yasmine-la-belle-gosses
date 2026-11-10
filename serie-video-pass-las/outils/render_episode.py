"""Production d'un épisode : voix off → minutage → sous-titres → animation → MP4 vertical.

Usage :  python3 render_episode.py 1 [2 3 ...]   (ou « all »)
Options : --audio-only  (voix off, sous-titres et minutage, sans vidéo)
          --preview S   (rend seulement quelques images PNG de contrôle)
"""
import json
import re
import subprocess
import sys
import time
import numpy as np
import soundfile as sf
import yaml
from PIL import Image

import config
import voice
import graphics as G
from config import W, H, FPS, SR
from scenes import Scene

GAP_SENT, GAP_BEAT, GAP_SCENE, XFADE = 0.14, 0.26, 0.42, 0.22


def load(n):
    with open(config.EPISODES_DIR / f"ep{n:02d}.yaml", encoding="utf-8") as f:
        ep = yaml.safe_load(f)
    ep["episode"] = n
    for sc in ep["scenes"]:
        sc.setdefault("beats", [])
        if not sc["beats"]:
            sc["beats"] = [{"say": ""}]
    return ep


# ---------------------------------------------------------------------------- sous-titres
def caption_chunks(text, maxc=34):
    """Découpe une phrase (avec *mots-clés*) en sous-titres courts façon TikTok."""
    toks = []
    for part in re.split(r"(\*[^*]+\*)", text):
        if not part:
            continue
        hl = part.startswith("*") and part.endswith("*")
        for w in (part[1:-1] if hl else part).split():
            toks.append((w, hl))
    chunks, cur, n = [], [], 0
    for i, (w, hl) in enumerate(toks):
        if cur and n + len(w) + 1 > maxc:
            chunks.append(cur)
            cur, n = [], 0
        cur.append((w, hl))
        n += len(w) + 1
        if re.search(r"[,;:]$", w) and n > maxc * 0.55 and i < len(toks) - 2:
            chunks.append(cur)
            cur, n = [], 0
    if cur:
        if chunks and len(cur) == 1 and len(cur[0][0]) < 8:
            chunks[-1].extend(cur)
        else:
            chunks.append(cur)
    return chunks


def chunk_plain(ch):
    return " ".join(w for w, _ in ch)


def chunk_ass(ch):
    out = []
    for w, hl in ch:
        w = w.replace("{", "(").replace("}", ")")
        out.append("{\\c&H66D1FF&}" + w + "{\\c&HFFFFFF&}" if hl else w)
    return " ".join(out)


def ts_ass(t):
    h, r = divmod(t, 3600)
    m, s = divmod(r, 60)
    return f"{int(h)}:{int(m):02d}:{s:05.2f}"


def ts_srt(t):
    h, r = divmod(t, 3600)
    m, s = divmod(r, 60)
    return f"{int(h):02d}:{int(m):02d}:{int(s):02d},{int((s - int(s)) * 1000):03d}"


# ---------------------------------------------------------------------------- effets sonores (synthétisés)
def sfx_bank():
    t = lambda d: np.arange(int(d * SR)) / SR
    rng = np.random.default_rng(1)
    pop = np.sin(2 * np.pi * (700 + 500 * np.exp(-t(0.09) * 40)) * t(0.09)) * np.exp(-t(0.09) * 38)
    n = rng.standard_normal(int(0.28 * SR))
    env = np.sin(np.pi * np.linspace(0, 1, len(n))) ** 2
    k = np.ones(18) / 18
    whoosh = np.convolve(n, k, "same") * env * 0.9
    tick = np.sin(2 * np.pi * 1250 * t(0.03)) * np.exp(-t(0.03) * 120)
    ding = (np.sin(2 * np.pi * 1320 * t(0.6)) + 0.6 * np.sin(2 * np.pi * 1980 * t(0.6))) * np.exp(-t(0.6) * 7)
    buzz = np.sign(np.sin(2 * np.pi * 150 * t(0.22))) * np.exp(-t(0.22) * 9) * 0.5
    bank = {"pop": pop * 0.10, "whoosh": whoosh * 0.07, "tick": tick * 0.16, "ding": ding * 0.10, "buzz": buzz * 0.07}
    return {k: v.astype(np.float32) for k, v in bank.items()}


# ---------------------------------------------------------------------------- minutage
def build(ep):
    parts, subs, sfx = [], [], []
    t = 0.3
    for si, sc in enumerate(ep["scenes"]):
        sc["_t0"] = t
        if si:
            sfx.append(("whoosh", t - 0.12))
        if sc.get("kind") == "trap":
            sfx.append(("buzz", t + 0.05))
        for bi, b in enumerate(sc["beats"]):
            b["_t0"] = t
            if b.get("show") and bi:
                sfx.append(("pop", t))
            if b.get("reveal"):
                sfx.append(("ding", t))
            sents = voice.split_sentences(b.get("say", "") or "")
            for s in sents:
                audio, sp, ph = voice.synth(s)
                d = len(audio) / SR
                parts.append((t, audio))
                chs = caption_chunks(s)
                weights = [max(1, len(voice.spoken(chunk_plain(c)))) for c in chs]
                tot = sum(weights)
                tc = t
                for c, wgt in zip(chs, weights):
                    dc = d * wgt / tot
                    subs.append((tc, tc + dc, c))
                    tc += dc
                t += d + GAP_SENT
            if b.get("countdown"):
                b["_cd0"] = t
                for k in range(int(b["countdown"])):
                    sfx.append(("tick", t + k))
                t += float(b["countdown"])
            t += float(b.get("hold", 0))
            if not sents and not b.get("countdown") and not b.get("hold"):
                t += 1.3
            t += GAP_BEAT
            b["_t1"] = t
        t += GAP_SCENE - GAP_BEAT
        sc["_t1"] = t
    total = t + 0.5
    audio = np.zeros(int(total * SR) + SR, np.float32)
    for t0, a in parts:
        i = int(t0 * SR)
        audio[i:i + len(a)] += a
    vo_only = audio.copy()
    bank = sfx_bank()
    for name, t0 in sfx:
        a = bank[name]
        i = max(0, int(t0 * SR))
        audio[i:i + len(a)] += a[: len(audio) - i]
    return total, audio, vo_only, subs


def write_subs(ep, subs, n):
    config.SUBS_DIR.mkdir(exist_ok=True)
    srt, ass = [], []
    for k, (a, b, c) in enumerate(subs, 1):
        srt.append(f"{k}\n{ts_srt(a)} --> {ts_srt(b)}\n{chunk_plain(c)}\n")
        ass.append(f"Dialogue: 0,{ts_ass(a)},{ts_ass(b)},Sub,,0,0,0,,{{\\fscx94\\fscy94\\t(0,90,\\fscx100\\fscy100)}}{chunk_ass(c)}")
    (config.SUBS_DIR / f"ep{n:02d}.srt").write_text("\n".join(srt), encoding="utf-8")
    head = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Sub,Inter Display,62,&H00FFFFFF,&H00FFFFFF,&H00100A08,&H90000000,-1,0,0,0,100,100,0,0,1,6,2,2,80,150,350,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    path = config.SUBS_DIR / f"ep{n:02d}.ass"
    path.write_text(head + "\n".join(ass) + "\n", encoding="utf-8")
    return path


# ---------------------------------------------------------------------------- images
def locate(ep, t):
    sc_list = ep["scenes"]
    si = 0
    for k, sc in enumerate(sc_list):
        if sc["_t0"] <= t:
            si = k
    sc = sc_list[si]
    bi = 0
    for k, b in enumerate(sc["beats"]):
        if b["_t0"] <= t:
            bi = k
    b = sc["beats"][bi]
    return si, bi, t - b["_t0"], b["_t1"] - b["_t0"]


def frames(ep, total, scenes):
    n = int(total * FPS)
    last_key, last_bytes = None, None
    prev_last = None
    cur_si = -1
    for i in range(n):
        t = i / FPS
        t = max(t, ep["scenes"][0]["_t0"])
        si, bi, tb, bd = locate(ep, t)
        if si != cur_si:
            if cur_si >= 0:
                prev_last = last_img
            cur_si = si
        sc = scenes[si]
        ts = t - ep["scenes"][si]["_t0"]
        xf = si > 0 and ts < XFADE
        static = sc.is_static(bi, tb) and not xf
        if sc.kind == "figure" and not xf and tb > 0.75:
            key = (si, bi, "kb", int(tb * FPS) // 3)    # Ken Burns : nouvelle image toutes les 3 trames
        else:
            key = (si, bi, "s") if static else (si, bi, i)
        if key == last_key:
            yield last_bytes
            continue
        img = sc.render(bi, tb, bd, fast=not static)
        if xf and prev_last is not None:
            a = G.ease(ts / XFADE)
            img = Image.blend(prev_last, img, a)
        last_img = img
        last_key = key
        last_bytes = img.convert("RGB").tobytes()
        yield last_bytes


def encode(ep, n, total, audio, ass_path, scenes, crf=26):
    config.VIDEOS_DIR.mkdir(exist_ok=True)
    wav = config.WORK / f"ep{n:02d}_mix.wav"
    sf.write(wav, audio, SR)
    out = config.VIDEOS_DIR / f"ep{n:02d}.mp4"
    accent = "0x4DA3FF"
    vf = (f"[0:v][2:v]overlay=x='-W+W*t/{total:.3f}':y=34:shortest=1[v1];"
          f"[v1]ass='{ass_path}'[v]")
    cmd = ["ffmpeg", "-y", "-loglevel", "error",
           "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
           "-i", str(wav),
           "-f", "lavfi", "-i", f"color=c={accent}:s={W}x10:r={FPS}",
           "-filter_complex", vf, "-map", "[v]", "-map", "1:a",
           "-c:v", "libx264", "-preset", "veryfast", "-crf", str(crf), "-tune", "animation",
           "-pix_fmt", "yuv420p", "-r", str(FPS),
           "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", "48000", "-ac", "1", "-c:a", "aac", "-b:a", "80k",
           "-movflags", "+faststart", "-shortest", str(out)]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for fb in frames(ep, total, scenes):
        p.stdin.write(fb)
    p.stdin.close()
    if p.wait() != 0:
        raise RuntimeError("ffmpeg a échoué")
    return out


def export_voice(vo, n):
    config.VOICE_DIR.mkdir(exist_ok=True)
    wav = config.WORK / f"ep{n:02d}_vo.wav"
    sf.write(wav, vo, SR)
    out = config.VOICE_DIR / f"ep{n:02d}.m4a"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(wav), "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
                    "-ar", "44100", "-ac", "1", "-c:a", "aac", "-b:a", "48k", str(out)], check=True)
    return out


def save_timing(ep, n, total):
    data = {"episode": n, "duration": round(total, 2), "scenes": []}
    for sc in ep["scenes"]:
        data["scenes"].append({"t0": round(sc["_t0"], 2), "t1": round(sc["_t1"], 2),
                               "beats": [[round(b["_t0"], 2), round(b["_t1"], 2)] for b in sc["beats"]]})
    p = config.EPISODES_DIR / f"ep{n:02d}.timing.json"
    p.write_text(json.dumps(data, ensure_ascii=False, indent=0), encoding="utf-8")


def run(n, audio_only=False, preview=None):
    t0 = time.time()
    ep = load(n)
    total, audio, vo, subs = build(ep)
    save_timing(ep, n, total)
    ass = write_subs(ep, subs, n)
    if preview is not None:
        scenes = [Scene(ep, sc, k, len(ep["scenes"])) for k, sc in enumerate(ep["scenes"])]
        outdir = config.WORK / "preview"
        outdir.mkdir(exist_ok=True)
        for si in preview:
            sc = ep["scenes"][si]
            b = len(sc["beats"]) - 1
            bt = sc["beats"][b]
            img = scenes[si].render(b, (bt["_t1"] - bt["_t0"]) * 0.9, bt["_t1"] - bt["_t0"])
            img.convert("RGB").save(outdir / f"ep{n:02d}_s{si:02d}.png")
        print("preview ok", outdir)
        return
    export_voice(vo, n)
    if audio_only:
        print(f"ep{n:02d} audio {total:.1f}s en {time.time() - t0:.0f}s")
        return
    scenes = [Scene(ep, sc, k, len(ep["scenes"])) for k, sc in enumerate(ep["scenes"])]
    out = encode(ep, n, total, audio, ass, scenes)
    print(f"ep{n:02d} OK {total / 60:.1f} min -> {out} en {time.time() - t0:.0f}s", flush=True)


if __name__ == "__main__":
    args = sys.argv[1:]
    audio_only = "--audio-only" in args
    preview = None
    if "--preview" in args:
        k = args.index("--preview")
        preview = [int(x) for x in args[k + 1].split(",")]
        args = args[:k] + args[k + 2:]
    args = [a for a in args if not a.startswith("--")]
    eps = range(1, 62) if args == ["all"] else [int(a) for a in args]
    for e in eps:
        run(e, audio_only, preview)
