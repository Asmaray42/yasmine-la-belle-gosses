#!/bin/bash
# File de rendu : rend dans l'ordre les épisodes passés en argument (journal dans $SERIE_WORK/rendu.log)
cd "$(dirname "$0")"
LOG=${SERIE_WORK:-/tmp/serie-wmede1152-work}/rendu.log
for e in "$@"; do
  echo "$(date +%T) début ep$e" >> "$LOG"
  python3 -W ignore render_episode.py "$e" >> "$LOG" 2>&1 && python3 -W ignore build_scripts.py "$e" >> "$LOG" 2>&1 || echo "ÉCHEC ep$e" >> "$LOG"
done
echo "$(date +%T) file terminée : $*" >> "$LOG"
