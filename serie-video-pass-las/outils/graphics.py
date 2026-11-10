"""Primitives graphiques (Pillow) : fond, texte riche avec mots-clés colorés, cartes, badges."""
import functools
import re
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np

import config
from config import W, H, C


@functools.lru_cache(maxsize=256)
def font(name, size):
    return ImageFont.truetype(config.FONTS[name], size)


@functools.lru_cache(maxsize=4)
def background(variant=0):
    """Fond dégradé sombre avec halos lumineux (sans grain, pour une compression efficace)."""
    y = np.linspace(0, 1, H)[:, None]
    x = np.linspace(0, 1, W)[None, :]
    c0, c1 = np.array(C["bg0"], float), np.array(C["bg1"], float)
    base = c0[None, None, :] * (1 - y[..., None]) + c1[None, None, :] * y[..., None]
    base = np.broadcast_to(base, (H, W, 3)).copy()
    glows = [((0.15, 0.12), (40, 90, 200), 0.55), ((0.95, 0.55), (130, 60, 200), 0.5), ((0.3, 0.95), (20, 120, 160), 0.45)]
    if variant == 1:
        glows = [((0.85, 0.1), (200, 40, 80), 0.5), ((0.1, 0.6), (120, 30, 90), 0.45)]
    if variant == 2:
        glows = [((0.8, 0.12), (20, 160, 110), 0.5), ((0.1, 0.7), (30, 90, 140), 0.45)]
    for (gx, gy), col, r in glows:
        d = np.sqrt((x - gx) ** 2 + ((y - gy) * H / W) ** 2)
        a = np.clip(1 - d / r, 0, 1) ** 2 * 0.55
        base += a[..., None] * (np.array(col, float)[None, None, :] - base) * 0.6
    return Image.fromarray(np.clip(base, 0, 255).astype(np.uint8)).convert("RGBA")


def rounded(size, radius, fill, outline=None, width=0):
    im = Image.new("RGBA", size, (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, size[0] - 1, size[1] - 1), radius=radius, fill=fill, outline=outline, width=width)
    return im


def shadow(im, radius=18, alpha=110, offset=(0, 10)):
    sh = Image.new("RGBA", (im.width + radius * 4, im.height + radius * 4), (0, 0, 0, 0))
    mask = im.split()[3].point(lambda v: alpha if v > 0 else 0)
    sh.paste((0, 0, 0, 255), (radius * 2 + offset[0], radius * 2 + offset[1]), mask)
    return sh.filter(ImageFilter.GaussianBlur(radius)), radius * 2


TOKEN = re.compile(r"(\*[^*]+\*)")


def rich_tokens(text, base_color, accent):
    """Découpe « mot *clé* » en mots stylés : (mot, couleur, gras, collé_au_précédent)."""
    out = []
    pos = 0
    hl = False
    i = 0
    buf = ""
    segs = []                      # (texte, en_relief)
    for part in TOKEN.split(text):
        if not part:
            continue
        if part.startswith("*") and part.endswith("*") and len(part) > 1:
            segs.append((part[1:-1], True))
        else:
            segs.append((part, False))
    prev_space = True
    for seg, hl in segs:
        for m in re.finditer(r"(\s*)(\S+)", seg):
            sp, w = m.group(1), m.group(2)
            glued = not sp and not prev_space and out
            out.append((w, accent if hl else base_color, hl, bool(glued)))
            prev_space = False
        prev_space = seg[-1:].isspace() if seg else prev_space
    return out


def layout_rich(text, size, max_w, base_color=C["text"], accent=C["num"], weight="semibold", bold="bold"):
    """Renvoie (lignes, hauteur_ligne) ; chaque ligne = liste de (x, mot, couleur, police)."""
    fr, fb = font(weight, size), font(bold, size)
    space = fr.getlength(" ")
    lines, cur, x = [], [], 0
    for w, colr, b, glued in rich_tokens(text, base_color, accent):
        f = fb if b else fr
        wl = f.getlength(w)
        if glued and cur:
            x -= space
        if cur and x + wl > max_w:
            if glued:
                # déplacer le groupe collé (ex. « (mot » + « ) ») sur la ligne suivante
                grp = [cur.pop()]
                while cur and grp and cur and getattr(cur[-1], "__len__", None) and False:
                    pass
                if cur:
                    lines.append(cur)
                x0 = grp[0][0]
                cur = [(gx - x0, gw, gc, gf) for gx, gw, gc, gf in grp]
                x = cur[-1][0] + cur[-1][3].getlength(cur[-1][1])
            else:
                lines.append(cur)
                cur, x = [], 0
        cur.append((x, w, colr, f))
        x += wl + space
    if cur:
        lines.append(cur)
    return lines, int(size * 1.28)


def rich_size(text, size, max_w, **kw):
    lines, lh = layout_rich(text, size, max_w, **kw)
    wmax = 0
    for ln in lines:
        x, w, col, f = ln[-1]
        wmax = max(wmax, x + f.getlength(w))
    return int(wmax), lh * len(lines)


def draw_rich(img, xy, text, size, max_w, align="left", **kw):
    lines, lh = layout_rich(text, size, max_w, **kw)
    d = ImageDraw.Draw(img)
    x0, y = xy
    for ln in lines:
        lw = ln[-1][0] + ln[-1][3].getlength(ln[-1][1])
        off = (max_w - lw) / 2 if align == "center" else 0
        for x, w, col, f in ln:
            d.text((x0 + off + x, y), w, font=f, fill=col)
        y += lh
    return y - xy[1]


def fit_size(text, max_w, max_h, sizes=(56, 52, 48, 44, 40, 36, 33, 30, 27, 24), **kw):
    for s in sizes:
        w, h = rich_size(text, s, max_w, **kw)
        if h <= max_h:
            return s
    return sizes[-1]


def badge(text, color, size=30):
    f = font("bold", size)
    tw = int(f.getlength(text))
    im = rounded((tw + 44, size + 26), (size + 26) // 2, fill=color + (255,))
    d = ImageDraw.Draw(im)
    d.text((22, 11), text, font=f, fill=(10, 12, 24))
    return im


def ease(p):
    p = max(0.0, min(1.0, p))
    return 1 - (1 - p) ** 3


def ease_io(p):
    p = max(0.0, min(1.0, p))
    return 4 * p ** 3 if p < 0.5 else 1 - (-2 * p + 2) ** 3 / 2


def with_alpha(im, a):
    if a >= 0.999:
        return im
    im = im.copy()
    al = im.split()[3].point(lambda v: int(v * a))
    im.putalpha(al)
    return im
