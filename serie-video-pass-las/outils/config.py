"""Configuration commune du pipeline de production de la série vidéo WMEDE1152."""
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent          # serie-video-pass-las/
EPISODES_DIR = ROOT / "source" / "episodes"
VIDEOS_DIR = ROOT / "videos"
VOICE_DIR = ROOT / "voix-off"
SUBS_DIR = ROOT / "sous-titres"

# Dossier de travail (cache audio, rendus de diapos) : hors dépôt.
WORK = Path(os.environ.get("SERIE_WORK", "/tmp/serie-wmede1152-work"))
WORK.mkdir(parents=True, exist_ok=True)

# Emplacement des 7 PDF du syllabus (non versionnés). Surchargeable avec SERIE_PDF_DIR.
_UP = Path(os.environ.get("SERIE_PDF_DIR", "/root/.claude/uploads/bc6c7609-8820-509d-bddf-452f8bbe0c3c"))
_ZIP = Path(os.environ.get("SERIE_ZIP_DIR",
            "/tmp/claude-0/-home-user-yasmine-la-belle-gosses/bc6c7609-8820-509d-bddf-452f8bbe0c3c/scratchpad/zip"))
PDFS = {
    "S1-1": _ZIP / "WMEDE1152-Syllabus-1-1 (3)_compressed.pdf",
    "S1-2": _ZIP / "WMEDE1152-Syllabus-1-2 (1)_compressed.pdf",
    "S1-3": _UP / "e1fa30ee-WMEDE1152-Syllabus-1-3_1.pdf",
    "S1-4": _UP / "aacfd81f-WMEDE1152-Syllabus-1-4.pdf",
    "S2-1": _UP / "743365f8-WMEDE1152-Syllabus-2-1.pdf",
    "S2-2": _UP / "ab9b15a6-WMEDE1152-Syllabus-2-2.pdf",
    "S2-3": _UP / "ca8808c6-WMEDE1152-Syllabus-2-3.pdf",
}
PAGES = {"S1-1": 60, "S1-2": 51, "S1-3": 32, "S1-4": 26, "S2-1": 25, "S2-2": 38, "S2-3": 42}
LANDSCAPE = {"S2-3"}   # 1 diapo par page

# Voix : moteur neuronal Kokoro (v1.0, ONNX), voix française « ff_siwis ».
MODELS = Path(os.environ.get("SERIE_MODELS",
              "/tmp/claude-0/-home-user-yasmine-la-belle-gosses/bc6c7609-8820-509d-bddf-452f8bbe0c3c/scratchpad/models"))
VOICE = "ff_siwis"
SPEED = 1.08
SR = 24000

# Vidéo verticale TikTok
W, H, FPS = 1080, 1920, 30
FONT_DIR = Path("/usr/share/fonts/opentype/inter")
FONTS = {
    "display": str(FONT_DIR / "InterDisplay-Bold.otf"),
    "displayx": str(FONT_DIR / "InterDisplay-ExtraBold.otf"),
    "bold": str(FONT_DIR / "Inter-Bold.otf"),
    "semibold": str(FONT_DIR / "Inter-SemiBold.otf"),
    "regular": str(FONT_DIR / "Inter-Regular.otf"),
    "medium": str(FONT_DIR / "Inter-Medium.otf"),
    "symbols": "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
}

# Palette (code couleur fixe de la série)
C = {
    "bg0": (9, 12, 28), "bg1": (24, 16, 58),
    "text": (245, 247, 255), "muted": (170, 178, 214),
    "card": (255, 255, 255, 20), "card2": (255, 255, 255, 34),
    "def": (77, 163, 255),       # bleu : définition / intitulé du cours
    "num": (255, 209, 102),      # jaune : chiffre à retenir
    "trap": (255, 92, 122),      # rouge : piège
    "mnemo": (46, 229, 157),     # vert : mnémotechnique
    "extra": (183, 148, 246),    # violet : complément hors cours
    "ok": (46, 229, 157), "ko": (255, 92, 122),
}

KIND_STYLE = {
    "hook":    ("ACCROCHE", "num"),
    "intro":   ("LE COURS", "def"),
    "list":    ("À RETENIR", "def"),
    "figure":  ("LA DIAPO DU COURS", "def"),
    "table":   ("TABLEAU", "def"),
    "flow":    ("MÉCANISME", "def"),
    "compare": ("COMPARAISON", "def"),
    "cards":   ("À RETENIR", "def"),
    "big":     ("CHIFFRE CLÉ", "num"),
    "trap":    ("PIÈGE D'EXAMEN", "trap"),
    "mnemo":   ("MNÉMO", "mnemo"),
    "quiz":    ("QUIZ EXPRESS", "num"),
    "recap":   ("RÉCAP", "mnemo"),
    "outro":   ("LA SUITE", "num"),
}
