"""Lexique de prononciation de la série (texte écran → texte prononcé).

Ordre d'application : (1) formules, ions et expressions spécifiques ; (2) sigles épelés
« à la française » ; (3) unités ; (4) symboles génériques.
IPA : prononciations imposées (phonèmes) pour les mots que la phonémisation automatique
lit mal. Chaque entrée a été contrôlée en lisant la transcription phonétique produite
(voir verif_prononciation.py et PRONONCIATION.md).
"""
import re

LETTRES = {"A": "a", "B": "bé", "C": "cé", "D": "dé", "E": "eu", "F": "èf", "G": "gé", "H": "ache",
           "I": "i", "J": "ji", "K": "ka", "L": "èl", "M": "èm", "N": "ène", "O": "o", "P": "pé",
           "Q": "ku", "R": "èr", "S": "èss", "T": "té", "U": "u", "V": "vé", "W": "doublevé",
           "X": "ixe", "Y": "igrec", "Z": "zède"}


def epele(sigle):
    """« ADN » → « adéène » (épellation lisible par la phonémisation, élision comprise)."""
    out = "".join(LETTRES.get(ch, ch) for ch in sigle.upper() if ch.isalpha())
    return out.replace("ée", "éé")


# Sigles épelés lettre par lettre (le reste est lu comme un mot).
SIGLES_EPELES = ["ADN", "ARN", "ATP", "ADP", "GTP", "RER", "REL", "RE", "MEC", "SRP", "SGLT", "LDL", "AQP",
                 "CFTR", "INS", "ADA", "SCID", "HSPA", "NCBI", "AP", "ETS", "OCT", "EGR", "HES", "FSH",
                 "LH", "GnRH", "hCG", "CGP", "ZP", "SED", "CD", "TEM", "ES", "OPC", "iPS", "KLF", "RA",
                 "Lrd", "FGF", "BMP", "CEA", "IgG", "DPI", "ICM", "EPI", "TP", "CIB", "MEB", "UCL", "QCM",
                 "SNC", "SNE", "FIV", "NADH", "NAD", "FAD", "FADH", "dGTP", "HCl", "NaOH", "NaCl", "BA",
                 "Fgfr", "MCI", "PMA", "IUPAC", "SHH"]

REGLES = [
    # --- formules, ions, expressions spécifiques (avant tout le reste) ---
    (r"\bNa\+/K\+", "sodium potassium"), (r"\bNa\+", "Na plus"), (r"\bK\+", "K plus"),
    (r"\bCa2\+|\bCa\+\+|\bCa\b", "calcium"), (r"\bCl[-–]", "chlorure"), (r"\bH\+", "H plus"),
    (r"\bOH[–-]", "O H moins"), (r"\bH3O\+", "H trois O plus"), (r"\bHCO3[–-]", "ion bicarbonate"),
    (r"\bH2CO3\b", "H deux C O trois"), (r"\bH2O\b", "H deux O"), (r"\bCO2\b", "C O deux"), (r"\bO2\b", "O deux"),
    (r"\bC6H12O6\b", "C six H douze O six"), (r"\bC3H8\b", "C trois H huit"),
    (r"\bNAD\+", "NAD plus"), (r"\bFADH2\b", "FADH deux"),
    (r"[–-]NH3\+", "N H trois plus"), (r"[–-]NH2\b", "N H deux"), (r"[–-]COOH\b", "C O O H"),
    (r"\bCOO[–-]", "C O O moins"), (r"[–-]OH\b", "O H"), (r"[–-]SH\b", "S H"), (r"[–-]OPO3²⁻", "phosphate"),
    (r"C=O", "C double liaison O"), (r"C[–-]H\b", "C H"), (r"C[–-]C\b", "C C"), (r"C=C", "C double liaison C"),
    (r"N[–-]H\b", "N H"),
    (r"\b10\^(\d+)", r"dix puissance \1"),
    (r"\bARNm\b", "ARN messager"), (r"\bARNt\b", "ARN de transfert"), (r"\bARNr\b", "ARN ribosomal"),
    (r"\bmicroARNs?\b", "micro ARN"), (r"\bGLUT(\d)\b", r"glut \1"), (r"\bMYOC\b", "myoc"), (r"\bCREB\b", "creb"),
    (r"\bIZUMO\+?", "izoumo"), (r"\bSOX2\b", "sox deux"), (r"\bMYC\b", "mic"), (r"\bShh\b", "sonic hedgehog"),
    (r"\bPitx2\b", "pitx deux"), (r"\bLefty2\b", "lefty deux"), (r"\bBcd\b", "bicoïde"), (r"\bBtd\b", "buttonhead"),
    (r"\bHOXD(\d+)\b", r"hox D \1"), (r"\bHOXD\b", "hox D"), (r"\bE2F1?\b", "E deux F"),
    (r"\bRh\+", "rhésus positif"), (r"\bRh[-–]", "rhésus négatif"), (r"\bRh\b", "rhésus"),
    (r"\bICSI\b", "icsi"), (r"\bFIVETE\b", "fivète"),
    (r"\bWMEDE1152\b", "W M E D E onze cinquante-deux"), (r"\bBA1\b", "BA un"),
    (r"\bS1-(\d)\b", r"syllabus un tiret \1"), (r"\bS2-(\d)\b", r"syllabus deux tiret \1"),
    (r"\bG1/S\b", "G un S"), (r"\bG2/M\b", "G deux M"), (r"\bG1\b", "G un"), (r"\bG2\b", "G deux"),
    (r"\b2n\b", "deux n"), (r"\bn = 23\b", "n égale vingt-trois"), (r"\bXXY\b", "X X Y"), (r"\bX0\b", "X zéro"),
    (r"\bC\. elegans\b", "C elegans"), (r"α", " alpha"), (r"β", " bêta"), (r"δ", "delta"),
    (r"[ΔΔ∆]G\b", "delta G"), (r"\bpH\b", "pé hache"),
    (r"\bIA\b", "I A"), (r"\bIB\b", "I B"), (r"\bIO\b", "I O"),
    (r"(\d)'", r"\1 prime"),
    (r"\bJ(\d+)", r"jour \1"), (r"\bp\.\s?(\d+)", r"page \1"), (r"\bex\.", "par exemple"),
]

UNITES = [
    (r"(\d)\s?µm\b", r"\1 micromètres"), (r"\bµm\b", "micromètres"), (r"(\d)\s?nm\b", r"\1 nanomètres"),
    (r"(\d)\s?Gb\b", r"\1 gigabases"), (r"(\d)\s?bp\b", r"\1 paires de bases"), (r"\bbp\b", "paires de bases"),
    (r"(\d)\s?cM\b", r"\1 centimorgans"), (r"(\d)\s?°C\b", r"\1 degrés"), (r"(\d)\s?ml\b", r"\1 millilitres"),
    (r"kcal/mole?", "kilocalories par mole"), (r"mol/L|moles/litre", "moles par litre"),
    (r"(\d)\s?h\b", r"\1 heures"), (r"(\d)\s?min\b", r"\1 minutes"), (r"(\d)\s?s\b", r"\1 secondes"),
]

SYMBOLES = [
    (r"→|⇒|->", ", donne "), (r"⇌", " équilibre "), (r"\bvs\.?", "versus"),
    (r"≈|~|±", "environ "), (r"\s<\s?", " moins de "), (r"\s>\s?", " plus de "),
    (r"&", " et "), (r"(?<=\w)/(?=\w)", " sur "), (r"[«»“”\"]", ""), (r"—", ", "), (r"\(|\)", ", "),
]


SUP = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹", "0123456789")


def _puissance(m):
    return "dix puissance " + ("moins " if m.group(1) else "") + m.group(2).translate(SUP)


def _sigle(m, s):
    apos = m.group(1)
    num = m.group(2)
    if apos:                      # élision : l'ADN → l'adéène (un seul mot)
        out = apos + epele(s)
    else:                         # sinon lettres séparées : la M E C
        out = " ".join(ch.upper() for ch in s if ch.isalpha())
    return out + (" " + num if num else "")


def appliquer(t):
    t = re.sub(r"10(⁻?)([⁰¹²³⁴⁵⁶⁷⁸⁹]+)", _puissance, t)
    t = re.sub(r"\bUCLouvain\b", "U C Louvain", t)
    for pat, rep in REGLES:
        t = re.sub(pat, rep, t)
    for s in sorted(SIGLES_EPELES, key=len, reverse=True):
        t = re.sub(r"(?<![\w-])((?:[lLdDnNsSjJ]|[qQ]u)['’])?" + re.escape(s) + r"(\d*)(?![\w])",
                   lambda m, s=s: _sigle(m, s), t)
    for pat, rep in UNITES:
        t = re.sub(pat, rep, t)
    for pat, rep in SYMBOLES:
        t = re.sub(pat, rep, t)
    t = re.sub(r"\s*,\s*,", ",", t)
    return t


# Prononciations imposées (API utilisée par Kokoro / espeak-ng).
IPA = {
    "Naegleria": "nɛɡlˈeʁja",
    "Floweri": "flˈɔweʁi",
    "Moodle": "mˈudœl",
    "case report": "kˈɛjz ʁipˈɔʁt",
    "case reports": "kˈɛjz ʁipˈɔʁts",
    "Viridiplantae": "viʁidiplˈɑ̃te",
    "elegans": "eleɡˈɑ̃s",
    "archées": "aʁkˈe",
    "archée": "aʁkˈe",
    "phosphatidylcholine": "fɔsfatidilkɔlˈin",
    "choline": "kɔlˈin",
    "izoumo": "izumˈo",
    "glut": "ɡlˈyt",
    "Ehlers-Danlos": "elˈɛʁs dɑ̃lˈɔs",
    "Tay-Sachs": "tˈɛ saks",
    "Krebs": "kʁˈɛbs",
    "Graaf": "ɡʁˈaf",
    "Sertoli": "sɛʁtolˈi",
    "Leydig": "lɛjdˈiɡ",
    "Heuser": "øzˈɛʁ",
    "Spemann": "ʃpˈeman",
    "Mangold": "manɡˈɔld",
    "Kartagener": "kaʁtaʒenˈɛʁ",
    "Klinefelter": "klinfɛltˈɛʁ",
    "Carnegie": "kaʁnəɡˈi",
    "Janssens": "ʒɑ̃sˈɛns",
    "Mendel": "mɛ̃dˈɛl",
    "Pfeiffer": "pfajfˈɛʁ",
    "Ensembl": "ɑ̃sˈɑ̃bl",
    "Duve": "dˈyv",
    "Hooke": "ˈuk",
    "cellulae": "selylˈe",
    "Sucraid": "sykʁˈɛd",
    "buttonhead": "bœtœnˈɛd",
    "sonic hedgehog": "sɔnˈik ɛdʒɔɡ",
    "lefty": "lɛftˈi",
    "Wood": "wˈud",
    "Stemagen": "stɛmaʒˈɛn",
    "Turner": "tyʁnˈɛʁ",
    "Victoria": "viktɔʁjˈa",
}
