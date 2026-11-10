"""Génère les scripts de production Markdown (episode-NN-script.md) à partir des sources YAML
et du minutage réel issu du rendu (epNN.timing.json).

Usage : python3 build_scripts.py all | 1 2 3
"""
import json
import re
import sys
import yaml

import config
from config import KIND_STYLE

KIND_DESC = {
    "hook": ("Carte d'accroche plein écran : grand mot-titre en jaune, puis phrases-chocs qui apparaissent une à une.",
             "Le mot-titre « pop » (agrandissement 82 % → 100 %), puis chaque phrase glisse vers le haut au moment où elle est dite."),
    "intro": ("Cartes empilées (barre de couleur à gauche) avec les informations d'organisation du cours.",
              "Chaque carte glisse vers le haut et apparaît en fondu au moment exact où la voix off la cite."),
    "list": ("Cartes numérotées empilées ; les mots-clés du cours sont colorés.",
             "Révélation progressive, une carte par phrase de voix off (glissement + fondu, 0,3 s), avec un petit son « pop »."),
    "recap": ("Fond vert : liste de contrôle ✓ des notions de l'épisode.", "Chaque ligne ✓ apparaît au rythme de la voix off."),
    "trap": ("Fond rouge : tampon « ⚠ PIÈGE D'EXAMEN », puis cartes ✗ (formulation fausse) et ✓ (formulation du cours).",
             "Le tampon « pop » avec un son d'alerte ; chaque carte ✗ puis ✓ glisse vers le haut au moment où elle est dite."),
    "mnemo": ("Fond vert : la phrase mnémotechnique en grand (initiales en vert), puis une carte par lettre ou par élément.",
              "La phrase « pop », puis chaque correspondance apparaît au rythme de la voix off."),
    "table": ("Tableau du cours recréé : ligne d'en-tête colorée, puis les lignes.", "Les lignes apparaissent l'une après l'autre, synchronisées avec la voix off."),
    "compare": ("Tableau comparatif à deux (ou plusieurs) colonnes.", "Une ligne de comparaison par phrase de voix off."),
    "flow": ("Mécanisme en étapes numérotées reliées par des flèches.", "Chaque étape apparaît avec sa flèche au moment où elle est expliquée : on suit le mécanisme pas à pas."),
    "cards": ("Grille de cartes (2 colonnes).", "Les cartes apparaissent une à une."),
    "big": ("Chiffre clé géant au centre de l'écran (jaune), puis ses explications.", "Le chiffre « pop », puis les cartes d'explication glissent."),
    "quiz": ("Quiz express : question en haut, propositions A, B, C… en cartes ; compte à rebours circulaire en haut à droite.",
             "Les propositions apparaissent ; le compte à rebours tourne avec un tic par seconde ; à la correction, les bonnes réponses passent en vert (✓) et les fausses en rouge (✗), avec un son « ding »."),
    "outro": ("Carte « La suite » : teaser de l'épisode suivant avec un chiffre-énigme.", "Le chiffre « pop », puis la phrase-teaser."),
    "figure": ("Diapo originale du cours affichée dans un cadre arrondi (proportions conservées) ; légendes en cartes sous la diapo.",
               "Zoom et recadrage animés (0,7 s) vers la zone dont parle la voix off, léger zoom continu ; surlignage jaune animé du texte cité ; les légendes apparaissent au rythme de la voix off."),
}


def mmss(t):
    return f"{int(t // 60):02d}:{int(t % 60):02d}"


def md_marks(s):
    return re.sub(r"\*([^*]+)\*", r"**\1**", s or "")


def clean_show(s):
    s = s or ""
    for p in ("[C] ", "! ", "# "):
        if s.startswith(p):
            s = ("💡 Complément (hors cours) : " if p == "[C] " else "") + s[len(p):]
    return md_marks(s)


def focus_txt(f):
    if f is None:
        return None
    if f == "all":
        return "vue d'ensemble de la diapo"
    if isinstance(f, str):
        return f"zoom sur « {f} »"
    return f"zoom sur la zone ({f[0]:.2f}, {f[1]:.2f}) → ({f[2]:.2f}, {f[3]:.2f}) de la diapo"


def marks_txt(m):
    if m is None:
        return []
    if isinstance(m, str):
        return [m]
    if isinstance(m, list) and len(m) == 4 and all(isinstance(v, (int, float)) for v in m):
        return ["une zone de la diapo"]
    return [x if isinstance(x, str) else "une zone de la diapo" for x in m]


def build(n):
    src = config.EPISODES_DIR / f"ep{n:02d}.yaml"
    ep = yaml.safe_load(src.read_text(encoding="utf-8"))
    tpath = config.EPISODES_DIR / f"ep{n:02d}.timing.json"
    timing = json.loads(tpath.read_text(encoding="utf-8")) if tpath.exists() else None
    L = []
    A = L.append
    A(f"# ÉPISODE {n} — « {ep['title']} »\n")
    A("> Série vidéo BA1 UCLouvain — Biologie & Embryologie générale (WMEDE1152) · Préparation de l'examen de janvier · Script de production intégral (généré depuis la source `source/episodes/ep%02d.yaml`)\n" % n)
    dur = f"{timing['duration'] / 60:.1f} min ({mmss(timing['duration'])})" if timing else "—"
    A("| Livrable | Fichier |\n|---|---|")
    A(f"| Vidéo verticale 9:16 (1080×1920, 30 i/s, sous-titres incrustés) | [`videos/ep{n:02d}.mp4`](videos/ep{n:02d}.mp4) |")
    A(f"| Voix off seule | [`voix-off/ep{n:02d}.m4a`](voix-off/ep{n:02d}.m4a) |")
    A(f"| Sous-titres | [`sous-titres/ep{n:02d}.srt`](sous-titres/ep{n:02d}.srt) · [`.ass`](sous-titres/ep{n:02d}.ass) |")
    A(f"| Durée réelle | {dur} |\n")
    A("## 1. Titre de l'épisode\n")
    A(f"**{ep['title']}**" + (f"  \n*{ep['subtitle']}*" if ep.get("subtitle") else "") + "\n")
    A("## 2. Position dans le cours\n")
    A(f"- **Pages du PDF :** {ep['source']}")
    A(f"- **Chapitre :** {ep.get('chapter', '')}\n")
    A("## 3. Objectifs pédagogiques\n\nÀ la fin de l'épisode, tu sais :\n")
    for k, o in enumerate(ep.get("objectives", []), 1):
        A(f"{k}. {o}")
    A("")
    A("## 4. Hook d'introduction\n")
    hook = " ".join(b.get("say", "") for b in ep["scenes"][0].get("beats", []))
    A(f"> « {md_marks(hook)} »\n")
    A("## 5. Script audiovisuel intégral\n")
    A("**Charte commune :** format vertical 9:16 (1080×1920) ; voix neuronale française unique pour toute la série ; sous-titres "
      "synchronisés incrustés (gros caractères blancs contour noir, mots-clés en jaune) au-dessus de la zone d'interface TikTok ; "
      "barre de progression en haut ; référence de page en haut à droite. Code couleur : bleu = intitulé du cours ; jaune = chiffre ; "
      "rouge = piège ; vert = mnémo ; violet = complément hors cours.\n")
    for si, sc in enumerate(ep["scenes"]):
        kind = sc.get("kind", "list")
        tag = sc.get("tag", KIND_STYLE.get(kind, ("", ""))[0])
        A(f"### SÉQUENCE {si + 1} — {sc.get('title', '').upper()}  ·  *{tag}*\n")
        tsc = timing["scenes"][si] if timing and si < len(timing["scenes"]) else None
        A("| | |\n|---|---|")
        if tsc:
            A(f"| **A. Durée** | {tsc['t1'] - tsc['t0']:.0f} s ({mmss(tsc['t0'])} → {mmss(tsc['t1'])}) |")
        A(f"| **Source** | {sc.get('ref', '')}" + (f" — diapo `{sc['fig']}`" if sc.get("fig") else "") + " |\n")
        A("**B. Voix off**\n")
        for b in sc.get("beats", []):
            if b.get("say"):
                A(f"> {md_marks(b['say'])}\n>")
        if L[-1] == ">":
            L.pop()
        A("")
        vis, anim = KIND_DESC.get(kind, KIND_DESC["list"])
        A("**C. Visuel à l'écran**\n")
        A(f"- {vis}")
        if kind == "figure":
            A(f"- Diapo affichée : **{sc['fig']}** (rendu haute définition du PDF du cours).")
            if sc.get("blur"):
                A("- Les photos de personnes réelles présentes sur la diapo sont **floutées** (protection de la vie privée).")
        if kind == "mnemo" and sc.get("phrase"):
            A(f"- Phrase mnémotechnique : {md_marks(sc['phrase'])}")
        if kind == "quiz":
            A(f"- Question : {md_marks(sc['question'])}")
            for k, o in enumerate(sc["options"]):
                ok = "✓" if k in sc.get("answer", []) else "✗"
                A(f"  - {'ABCDEFG'[k]}. {md_marks(o)} ({ok})")
        if sc.get("visual"):
            A(f"- {sc['visual']}")
        A("")
        A("**D. Texte incrusté**\n")
        A(f"- Titre : **{md_marks(sc.get('title', ''))}**")
        for b in sc.get("beats", []):
            if b.get("show"):
                A(f"- {clean_show(b['show'])}")
        A("")
        A("**E. Animation et mise en scène**\n")
        A(f"- {anim}")
        for bi, b in enumerate(sc.get("beats", [])):
            steps = []
            ft = focus_txt(b.get("focus"))
            if ft:
                steps.append(ft)
            mk = marks_txt(b.get("mark"))
            if mk:
                steps.append("surlignage de " + ", ".join(f"« {m} »" for m in mk))
            if b.get("show") and kind != "figure":
                steps.append("apparition de la carte « " + clean_show(b["show"])[:70] + ("…" if len(b["show"]) > 70 else "") + " »")
            if b.get("countdown"):
                steps.append(f"compte à rebours de {b['countdown']} s")
            if b.get("reveal"):
                steps.append("correction (vert/rouge)")
            if steps:
                tc = f"{mmss(tsc['beats'][bi][0])}" if tsc and bi < len(tsc["beats"]) else f"beat {bi + 1}"
                A(f"- **{tc}** : " + " ; ".join(steps))
        A("")
        A("**F. Point de vigilance QCM**\n")
        A(f"- {md_marks(sc.get('trap', '—'))}\n")
        A("---\n")
    A("## 6. Récapitulatif des notions essentielles (fidèle au cours)\n")
    for r in ep.get("recap", []):
        A(f"- {md_marks(r)}")
    A("")
    A("## 7. Pièges de QCM à connaître\n")
    A("| # | Piège | Ce qu'il faut retenir | Source |\n|---|---|---|---|")
    for k, t in enumerate(ep.get("traps", []), 1):
        A(f"| {k} | {t[0]} | {t[1]} | {t[2] if len(t) > 2 else ''} |")
    A("")
    A("## 8. Mnémotechniques\n")
    A("| Ce qu'il faut retenir | Mnémotechnique | Correspondance exacte |\n|---|---|---|")
    for m in ep.get("mnemonics", []):
        A(f"| {m[0]} | {m[1]} | {m[2]} |")
    A("")
    A("## 9. Mini-test de récupération active (corrigé détaillé)\n")
    A("> Une ou plusieurs propositions exactes. Réponds **avant** de lire le corrigé, puis refais le test 24 h plus tard.\n")
    for qk, q in enumerate(ep.get("quiz", []), 1):
        A(f"### Question {qk}\n\n{md_marks(q['q'])}\n")
        for k, p in enumerate(q["props"]):
            A(f"- **{'ABCDEFG'[k]}.** {md_marks(p[0])}")
        good = ", ".join("ABCDEFG"[k] for k, p in enumerate(q["props"]) if p[1]) or "aucune"
        A(f"\n**✅ Réponse(s) : {good}**\n")
        for k, p in enumerate(q["props"]):
            A(f"- **{'ABCDEFG'[k]} — {'VRAI' if p[1] else 'FAUX'}.** {md_marks(p[2])}")
        A("")
    A("## 10. Contrôle qualité — couverture de l'épisode\n")
    A("| Fichier | Page | Notion ou information du PDF | Séquence | Statut |\n|---|---|---|---|---|")
    for c in ep.get("coverage", []):
        A(f"| {c[0]} | p.{c[1]} | {c[2]} | {c[3]} | ✅ Intégrée |")
    A("")
    out = config.ROOT / f"episode-{n:02d}-script.md"
    out.write_text("\n".join(L) + "\n", encoding="utf-8")
    return out


if __name__ == "__main__":
    args = sys.argv[1:]
    eps = sorted(int(p.stem[2:4]) for p in config.EPISODES_DIR.glob("ep[0-9][0-9].yaml")) if args == ["all"] else [int(a) for a in args]
    for e in eps:
        print(build(e))
