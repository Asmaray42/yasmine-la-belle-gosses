#!/usr/bin/env python3
"""Vérifie la prononciation d'un texte : texte écran → texte prononcé → phonèmes (API).

    python3 outils/verif_prononciation.py "L'ADN contient 10⁻⁷ mole de Na+/K+"
    python3 outils/verif_prononciation.py --lexique      # contrôle tout le lexique
    python3 outils/verif_prononciation.py --episode 42   # contrôle un épisode entier

Rien n'est synthétisé : seule la chaîne texte → phonèmes est affichée, pour relire
ce que la voix va réellement dire. Les entrées de `lexique.IPA` sont imposées telles
quelles (elles court-circuitent la phonémisation automatique).
"""
import sys, re, yaml
import lexique, voice, config


def montre(texte):
    dit = voice.spoken(texte)
    pho = voice.phonemes(dit)
    print(f"  écran : {texte}")
    print(f"  dit   : {dit}")
    print(f"  API   : {pho}")
    print()


def lexique_complet():
    print(f"— {len(lexique.IPA)} prononciations imposées (API) —")
    for mot, ipa in sorted(lexique.IPA.items()):
        print(f"  {mot:<28} {ipa}")
    print(f"\n— {len(lexique.SIGLES_EPELES)} sigles épelés —")
    print("  " + ", ".join(f"{s} → {lexique.epele(s)}" for s in lexique.SIGLES_EPELES))


def episode(n):
    d = yaml.safe_load(open(config.EPISODES / f"ep{int(n):02d}.yaml"))
    for sc in d["scenes"]:
        for b in sc.get("beats", []):
            if b.get("say"):
                montre(b["say"])


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a:
        print(__doc__)
    elif a[0] == "--lexique":
        lexique_complet()
    elif a[0] == "--episode":
        episode(a[1])
    else:
        montre(" ".join(a))
