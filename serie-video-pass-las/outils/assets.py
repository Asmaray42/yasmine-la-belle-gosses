"""Accès aux diapositives du syllabus : rendu haute définition, recadrage automatique,
recherche de texte (pour zoomer et surligner exactement ce que dit la voix off),
floutage des photos de personnes réelles."""
import functools
import fitz  # PyMuPDF
from PIL import Image, ImageFilter

import config

DPI = 220
SCALE = DPI / 72.0


@functools.lru_cache(maxsize=16)
def doc(code):
    return fitz.open(str(config.PDFS[code]))


def parse(slide_id):
    """'S1-1:5h' → ('S1-1', 5, 'h') ; 'S2-3:8' → ('S2-3', 8, '')."""
    code, rest = slide_id.split(":")
    half = rest[-1] if rest[-1] in "hb" else ""
    page = int(rest[:-1] if half else rest)
    return code, page, half


def slide_rect(slide_id):
    code, page, half = parse(slide_id)
    p = doc(code)[page - 1]
    r = p.rect
    if code in config.LANDSCAPE or not half:
        base = fitz.Rect(r)
    elif half == "h":
        base = fitz.Rect(r.x0, r.y0, r.x1, r.y0 + r.height / 2)
    else:
        base = fitz.Rect(r.x0, r.y0 + r.height / 2, r.x1, r.y1)
    # rognage automatique sur le contenu réel de la diapo
    boxes = []
    for b in p.get_text("blocks"):
        rr = fitz.Rect(b[:4])
        if rr.intersects(base) and rr.get_area() > 4:
            boxes.append(rr & base)
    for info in p.get_image_info():
        rr = fitz.Rect(info["bbox"])
        if rr.intersects(base):
            boxes.append(rr & base)
    for d in p.get_drawings():
        rr = fitz.Rect(d["rect"])
        if rr.intersects(base) and rr.width < base.width * 0.98:
            boxes.append(rr & base)
    if boxes:
        u = fitz.Rect(boxes[0])
        for b in boxes[1:]:
            u |= b
        u = fitz.Rect(u.x0 - 8, u.y0 - 8, u.x1 + 8, u.y1 + 8) & base
        if u.width > 50 and u.height > 50:
            base = u
    return p, base


@functools.lru_cache(maxsize=64)
def slide_image(slide_id, blur=()):
    """Image PIL RGB de la diapo, recadrée. `blur` = tuple de boîtes relatives (x0,y0,x1,y1) à flouter."""
    p, rect = slide_rect(slide_id)
    pix = p.get_pixmap(clip=rect, dpi=DPI, alpha=False)
    im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    for bx in blur:
        x0, y0, x1, y1 = [int(v * s) for v, s in zip(bx, (im.width, im.height, im.width, im.height))]
        region = im.crop((x0, y0, x1, y1)).filter(ImageFilter.GaussianBlur(28))
        im.paste(region, (x0, y0))
    return im


def find(slide_id, needle):
    """Boîte relative (0-1) de la 1re occurrence du texte `needle` dans la diapo, ou None."""
    p, rect = slide_rect(slide_id)
    hits = p.search_for(needle, clip=rect)
    if not hits:
        # recherche tolérante : premier mot significatif
        words = [w for w in needle.split() if len(w) > 3]
        for w in words:
            hits = p.search_for(w, clip=rect)
            if hits:
                break
    if not hits:
        return None
    u = fitz.Rect(hits[0])
    # occurrences adjacentes (texte sur plusieurs lignes)
    for h in hits[1:]:
        if abs(h.y0 - u.y1) < 14 and abs(h.x0 - u.x0) < 200:
            u |= h
    return ((u.x0 - rect.x0) / rect.width, (u.y0 - rect.y0) / rect.height,
            (u.x1 - rect.x0) / rect.width, (u.y1 - rect.y0) / rect.height)


def images(slide_id, min_frac=0.02):
    """Boîtes relatives des images (figures) de la diapo, triées en ordre de lecture."""
    p, rect = slide_rect(slide_id)
    out = []
    for info in p.get_image_info():
        rr = fitz.Rect(info["bbox"]) & rect
        if rr.is_empty or rr.get_area() < min_frac * rect.get_area():
            continue
        out.append(((rr.x0 - rect.x0) / rect.width, (rr.y0 - rect.y0) / rect.height,
                    (rr.x1 - rect.x0) / rect.width, (rr.y1 - rect.y0) / rect.height))
    out.sort(key=lambda b: (round(b[1], 1), b[0]))
    return out
