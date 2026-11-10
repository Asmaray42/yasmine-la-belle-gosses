# Série vidéo BA1 — Biologie & Embryologie générale (WMEDE1152)

61 épisodes verticaux (9:16) qui couvrent **l'intégralité** du syllabus WMEDE1152 (Prof. Charles De Smet, UCLouvain) : les 7 PDF, 274 pages, Partie I et Partie II.

**Public :** étudiant·e de BA1 à l'UCLouvain, préparation de la session de janvier.
**Principe :** les vidéos reprennent **exactement** les termes, les valeurs et les formulations du cours. Rien n'y est corrigé ni contredit. Les nuances, incohérences et erreurs repérées sont consignées à part, avec la formulation à retenir pour l'examen.

## Ce que contient le dépôt

| Dossier / fichier | Contenu |
|---|---|
| [`00-plan-global.md`](00-plan-global.md) | Sources analysées, ordre pédagogique, **tableau des 61 épisodes** (notions, pièges, durées), règles de production, chaîne technique |
| [`00-grille-couverture.md`](00-grille-couverture.md) | Attribution de **chacune des 274 pages** du syllabus à un épisode |
| [`AUDIT_FINAL_EXHAUSTIVITE.md`](AUDIT_FINAL_EXHAUSTIVITE.md) | Contrôle automatique : termes et chiffres de chaque page retrouvés dans le script de l'épisode |
| [`ANNEXE_CONFIDENTIELLE_ERREURS_ET_INCOHERENCES.md`](ANNEXE_CONFIDENTIELLE_ERREURS_ET_INCOHERENCES.md) | **À ne pas diffuser.** Incohérences entre diapos, formulations discutables, données datées, coquilles — et ce qu'il faut répondre à l'examen |
| `episode-NN-script.md` | Script complet de chaque épisode, avec les **timecodes réels** de la vidéo : objectifs, accroche, séquence par séquence (voix off, visuel, texte incrusté, animation, vigilance QCM), récap, pièges, mnémos, mini-test corrigé, grille de couverture |
| `videos/epNN.mp4` | La vidéo, verticale 1080 × 1920, 30 fps, sous-titres incrustés |
| `sous-titres/epNN.srt` et `.ass` | Sous-titres séparés (SRT pour l'import, ASS pour le rendu stylé) |
| `voix-off/epNN.m4a` | La voix off seule (révision en marchant, en voiture…) |
| `source/episodes/epNN.yaml` | La **source** de l'épisode : tout le contenu, scène par scène |
| `outils/` | La chaîne de fabrication (voix, lexique de prononciation, découpe des diapos, moteur d'animation, montage, audit) |

## Comment réviser avec

1. **Regarder** l'épisode (`videos/`) : la vidéo suit les diapos du cours, avec zoom sur la zone commentée.
2. **Relire** la section « Récapitulatif » du script : elle reprend le cours **mot pour mot**, condensé.
3. **Refaire** le mini-test à la fin du script : chaque proposition, vraie ou fausse, est justifiée avec sa page.
4. **Réviser les pièges** (section « Pièges de QCM ») la veille de l'examen.
5. **Écouter** la voix off (`voix-off/`) en révision passive.

## Refabriquer une vidéo

Les PDF du cours ne sont pas dans le dépôt (contenu protégé) : il faut les remettre aux chemins indiqués dans `outils/config.py`.

```bash
python3 outils/render_episode.py 42          # un épisode
outils/file_rendu.sh $(seq 1 61)             # toute la série
python3 outils/audit.py                      # grille de couverture + audit
```

Voix : **Kokoro v1.0 ONNX**, voix française `ff_siwis`, identique sur toute la série ; la prononciation des sigles, formules et termes scientifiques est pilotée par `outils/lexique.py`.
