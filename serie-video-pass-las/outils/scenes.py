"""Mise en page et animation des scènes (format vertical 1080×1920).

Chaque scène est un ensemble d'« éléments » (images RGBA positionnées) qui apparaissent
au rythme des « beats » de la voix off, plus des parties dynamiques (zoom sur la diapo,
compte à rebours, correction de quiz)."""
import math
from PIL import Image, ImageDraw

import config
import assets
import graphics as G
from config import W, H, C, KIND_STYLE

X0, X1 = 70, 1010
CW = X1 - X0
Y_END = 1330          # bas de la zone de contenu (sous-titres en dessous)
ANIM = 0.32


def col(name):
    return C[name]


def norm_marks(m):
    if m is None:
        return []
    if isinstance(m, str):
        return [m]
    if isinstance(m, list) and len(m) == 4 and all(isinstance(v, (int, float)) for v in m):
        return [m]
    return list(m)


class Scene:
    def __init__(self, ep, sc, idx, total_scenes):
        self.ep, self.sc, self.idx = ep, sc, idx
        self.kind = sc.get("kind", "list")
        tag, colname = KIND_STYLE.get(self.kind, ("", "def"))
        self.tag = sc.get("tag", tag)
        self.accent = col(sc.get("color", colname))
        self.beats = sc["beats"]
        self.elements = []          # (img, x, y, beat_index, anim)
        self.dyn = None
        self.bg = G.background({"trap": 1, "mnemo": 2, "recap": 2}.get(self.kind, 0))
        self._header()
        getattr(self, "lay_" + self.kind, self.lay_list)()
        self._static_cache = {}

    # ------------------------------------------------------------------ en-tête
    def _header(self):
        base = self.bg.copy()
        d = ImageDraw.Draw(base)
        ep_tag = f"ÉP. {self.ep['episode']:02d} / 61  ·  {self.ep['title']}"
        f = G.font("semibold", 28)
        while f.getlength(ep_tag) > 700 and len(ep_tag) > 20:
            ep_tag = ep_tag[:-2].rstrip() + "…"
            ep_tag = ep_tag.replace("……", "…")
        d.text((X0, 72), ep_tag, font=f, fill=C["muted"])
        ref = self.sc.get("ref", "")
        if ref:
            fr = G.font("medium", 27)
            d.text((X1 - fr.getlength(ref), 72), ref, font=fr, fill=C["muted"])
        y = 140
        b = G.badge(self.tag, self.accent, 28)
        base.alpha_composite(b, (X0, y))
        y += b.height + 22
        title = self.sc.get("title", "")
        if title:
            s = G.fit_size(title, CW, 170, sizes=(64, 58, 52, 48, 44), weight="display", bold="displayx",
                           accent=self.accent)
            h = G.draw_rich(base, (X0, y), title, s, CW, weight="display", bold="displayx", accent=self.accent)
            y += h + 10
        self.header = base
        self.y0 = y + 34

    def add(self, img, x, y, beat, anim="up", page=None):
        self.elements.append((img, int(x), int(y), beat, anim, page))

    def show_beats(self):
        return [(i, b["show"]) for i, b in enumerate(self.beats) if b.get("show")]

    # ------------------------------------------------------------------ cartes de texte
    def text_card(self, text, w, size, color, fill=(255, 255, 255, 22), icon=None, pad=26, label=None,
                  text_color=None, bar=True):
        icon_w = 0
        if icon:
            icon_w = int(size * 1.15)
        tw, th = G.rich_size(text, size, w - 2 * pad - icon_w - (12 if bar else 0), accent=color)
        lab_h = 0
        if label:
            lab_h = 34
        h = th + 2 * pad - 8 + lab_h
        card = G.rounded((w, h), 26, fill=fill)
        d = ImageDraw.Draw(card)
        xo = pad
        if bar:
            d.rounded_rectangle((0, 0, 10, h - 1), radius=5, fill=color + (255,))
            xo += 12
        if label:
            d.text((xo, pad - 6), label, font=G.font("bold", 24), fill=color)
        if icon:
            fi = G.font("symbols", int(size * 0.95))
            d.text((xo, pad - 4 + lab_h), icon, font=fi, fill=color)
            xo += icon_w
        G.draw_rich(card, (xo, pad - 4 + lab_h), text, size, w - xo - pad, accent=color,
                    base_color=text_color or C["text"])
        return card

    def stack(self, items, top, bottom, w=CW, x=X0, gap=20, sizes=(48, 45, 42, 39, 36, 33, 30, 28, 26),
              maker=None, min_size=34):
        """Empile des cartes ; prend la plus grande police qui tient. Si rien ne tient au-dessus de
        `min_size`, les cartes sont réparties en « pages » successives (lisibilité sur smartphone)."""
        maker = maker or (lambda txt, s: self.item_card(txt, w, s))
        sizes = [s for s in sizes if s >= min_size] or [min_size]
        paged = False
        for s in sizes:
            cards = [maker(t, s) for _, t in items]
            tot = sum(c.height for c in cards) + gap * (len(cards) - 1)
            if tot <= bottom - top:
                break
        else:
            paged = True
        y, page = top, 0
        out = []
        for (bi, _), c in zip(items, cards):
            if paged and y > top and y + c.height > bottom:
                page += 1
                y = top
            out.append((c, x, y, bi, page if paged else None))
            y += c.height + gap
        return out, y

    def item_card(self, text, w, s):
        color, icon, label, fill = self.accent, None, None, (255, 255, 255, 22)
        if text.startswith("[C] "):
            text, color, label = text[4:], C["extra"], "COMPLÉMENT (hors cours)"
        elif text.startswith("✗ "):
            text, color, icon, fill = text[2:], C["ko"], "✗", (255, 92, 122, 34)
        elif text.startswith("✓ "):
            text, color, icon, fill = text[2:], C["ok"], "✓", (46, 229, 157, 30)
        elif text.startswith("! "):
            text, color = text[2:], C["trap"]
        elif text.startswith("# "):
            text, color = text[2:], C["num"]
        return self.text_card(text, w, s, color, fill=fill, icon=icon, label=label)

    # ------------------------------------------------------------------ dispositions
    def lay_list(self):
        items = self.show_beats()
        if not items:
            return
        els, _ = self.stack(items, self.y0, Y_END)
        for c, x, y, bi, pg in els:
            self.add(c, x, y, bi, page=pg)

    lay_intro = lay_list

    def lay_recap(self):
        items = [(i, "✓ " + t if not t.startswith(("✓", "✗")) else t) for i, t in self.show_beats()]
        els, _ = self.stack(items, self.y0, Y_END, gap=16)
        for c, x, y, bi, pg in els:
            self.add(c, x, y, bi, page=pg)

    def lay_trap(self):
        stamp = G.badge("⚠  PIÈGE D'EXAMEN", C["trap"], 44)
        self.add(stamp, (W - stamp.width) // 2, self.y0, 0, "pop")
        items = self.show_beats()
        els, _ = self.stack(items, self.y0 + stamp.height + 34, Y_END)
        for c, x, y, bi, pg in els:
            self.add(c, x, y, bi, page=pg)

    def lay_hook(self):
        y = self.y0 + 10
        num = self.sc.get("big")
        if num:
            s = G.fit_size(num, CW, 330, sizes=(170, 150, 130, 110, 96, 84), weight="displayx", bold="displayx")
            im = Image.new("RGBA", (CW, int(s * 1.35)), (0, 0, 0, 0))
            G.draw_rich(im, (0, 0), num, s, CW, align="center", weight="displayx", bold="displayx",
                        base_color=self.accent, accent=C["text"])
            self.add(im, X0, y, 0, "pop")
            y += im.height + 30
        items = self.show_beats()
        if items:
            els, _ = self.stack(items, y, Y_END, sizes=(56, 52, 48, 44, 40, 36))
            for c, x, yy, bi, pg in els:
                self.add(c, x, yy, bi, page=pg)

    lay_outro = lay_hook

    def lay_big(self):
        items = self.show_beats()
        if not items:
            return
        first_i, first = items[0]
        s = G.fit_size(first, CW, 380, sizes=(190, 170, 150, 130, 112, 96, 84, 72, 64), weight="displayx",
                       bold="displayx")
        tw, th = G.rich_size(first, s, CW, weight="displayx", bold="displayx")
        im = Image.new("RGBA", (CW, th + 20), (0, 0, 0, 0))
        G.draw_rich(im, (0, 0), first, s, CW, align="center", weight="displayx", bold="displayx",
                    base_color=C["num"], accent=C["text"])
        y = self.y0 + 30
        self.add(im, X0, y, first_i, "pop")
        y += im.height + 40
        rest = items[1:]
        if rest:
            els, _ = self.stack(rest, y, Y_END)
            for c, x, yy, bi, pg in els:
                self.add(c, x, yy, bi, page=pg)

    def lay_cards(self):
        items = self.show_beats()
        n = len(items)
        cols = 2 if n >= 3 else 1
        cw = (CW - 24) // cols if cols == 2 else CW
        rows = math.ceil(n / cols)
        avail = Y_END - self.y0
        for s in (44, 40, 37, 34, 32, 30):
            cards = [self.item_card(t, cw, s) for _, t in items]
            rh = []
            for r in range(rows):
                rh.append(max(c.height for c in cards[r * cols:(r + 1) * cols]))
            if sum(rh) + 20 * (rows - 1) <= avail:
                break
        y = self.y0
        for r in range(rows):
            for cidx in range(cols):
                k = r * cols + cidx
                if k >= n:
                    break
                c = cards[k]
                self.add(c, X0 + cidx * (cw + 24), y, items[k][0])
            y += rh[r] + 20

    def lay_mnemo(self):
        y = self.y0
        phrase = self.sc.get("phrase")
        if phrase:
            card = self.text_card(phrase, CW, G.fit_size(phrase, CW - 80, 260, sizes=(52, 48, 44, 40, 36),
                                                         accent=C["mnemo"]),
                                  C["mnemo"], fill=(46, 229, 157, 38), label="MNÉMO")
            self.add(card, X0, y, 0, "pop")
            y += card.height + 30
        items = self.show_beats()
        if items:
            els, _ = self.stack(items, y, Y_END, gap=14, sizes=(44, 41, 38, 36))
            for c, x, yy, bi, pg in els:
                self.add(c, x, yy, bi, page=pg)

    def lay_table(self):
        header = self.sc.get("header", [])
        rows = [(i, [c.strip() for c in t.split("|")]) for i, t in self.show_beats()]
        ncol = max([len(header)] + [len(r) for _, r in rows])
        lens = [max([len(header[k]) if k < len(header) else 0] + [len(r[k]) if k < len(r) else 0 for _, r in rows])
                for k in range(ncol)]
        tot = sum(max(6, l) for l in lens)
        widths = [int(CW * max(6, l) / tot) for l in lens]
        widths[-1] = CW - sum(widths[:-1])
        avail = Y_END - self.y0
        for s in (40, 37, 34, 32, 30, 28):
            def rowimg(cells, head=False):
                hs = []
                for k in range(ncol):
                    txt = cells[k] if k < len(cells) else ""
                    hs.append(G.rich_size(txt, s, widths[k] - 28, weight="bold" if head else "semibold",
                                          accent=self.accent)[1])
                h = max(hs) + 30
                im = G.rounded((CW, h), 18, fill=(self.accent + (70,)) if head else (255, 255, 255, 20))
                x = 0
                for k in range(ncol):
                    txt = cells[k] if k < len(cells) else ""
                    G.draw_rich(im, (x + 14, 13), txt, s, widths[k] - 28, weight="bold" if head else "semibold",
                                accent=C["num"])
                    if k:
                        ImageDraw.Draw(im).line((x, 10, x, h - 10), fill=(255, 255, 255, 50), width=2)
                    x += widths[k]
                return im
            himg = rowimg(header, True) if header else None
            rimgs = [rowimg(r) for _, r in rows]
            total = (himg.height + 12 if himg else 0) + sum(r.height for r in rimgs) + 10 * len(rimgs)
            if total <= avail:
                break
        y = self.y0
        if himg:
            self.add(himg, X0, y, 0, "fade")
            y += himg.height + 12
        top = y
        paged = total > avail
        page = 0
        for (bi, _), im in zip(rows, rimgs):
            if paged and y > top and y + im.height > Y_END:
                page += 1
                y = top
            self.add(im, X0, y, bi, page=page if paged else None)
            y += im.height + 10

    lay_compare = lay_table

    def lay_flow(self):
        items = self.show_beats()
        n = len(items)
        avail = Y_END - self.y0
        for s in (42, 39, 36, 34, 32):
            cards = [self.step_card(k + 1, t, s) for k, (_, t) in enumerate(items)]
            arrow = 34
            tot = sum(c.height for c in cards) + arrow * (n - 1)
            if tot <= avail:
                break
        paged = tot > avail
        y, page = self.y0, 0
        for k, ((bi, _), c) in enumerate(zip(items, cards)):
            if paged and k and y + arrow + c.height > Y_END:
                page += 1
                y = self.y0
            elif k:
                a = Image.new("RGBA", (60, arrow), (0, 0, 0, 0))
                d = ImageDraw.Draw(a)
                d.line((30, 2, 30, arrow - 10), fill=self.accent + (255,), width=6)
                d.polygon([(18, arrow - 14), (42, arrow - 14), (30, arrow - 1)], fill=self.accent + (255,))
                self.add(a, X0 + 20, y, bi, "fade", page=page if paged else None)
                y += arrow
            self.add(c, X0, y, bi, page=page if paged else None)
            y += c.height

    def step_card(self, k, text, s):
        num_w = int(s * 1.7)
        tw, th = G.rich_size(text, s, CW - num_w - 56, accent=self.accent)
        h = max(th + 34, num_w + 10)
        card = G.rounded((CW, h), 24, fill=(255, 255, 255, 22))
        d = ImageDraw.Draw(card)
        cy = h // 2
        r = num_w // 2 - 4
        d.ellipse((18, cy - r, 18 + 2 * r, cy + r), fill=self.accent + (255,))
        fn = G.font("displayx", int(s * 0.9))
        lab = str(k)
        d.text((18 + r - fn.getlength(lab) / 2, cy - s * 0.55), lab, font=fn, fill=(10, 12, 24))
        G.draw_rich(card, (num_w + 34, (h - th) // 2 - 2), text, s, CW - num_w - 56, accent=self.accent)
        return card

    # ------------------------------------------------------------------ diapo du cours
    def lay_figure(self):
        sid = self.sc["fig"]
        blur = tuple(tuple(b) for b in self.sc.get("blur", []))
        self.slide = assets.slide_image(sid, blur)
        sw, sh = self.slide.size
        items = self.show_beats()
        aspect = sw / sh
        avail = Y_END - self.y0
        sizes = (38, 36, 34, 32, 30)
        chosen = None
        for s in sizes:
            caps = [self.item_card(tx, CW, s) for _, tx in items]
            hc = sum(c.height for c in caps) + 14 * max(0, len(caps) - 1) + (26 if caps else 0)
            ph = min(int(CW / aspect), avail - hc)
            if ph >= 0.6 * avail or s == sizes[-1]:
                chosen = s
                break
        self.cap_size = chosen
        ph = max(int(0.6 * avail), min(int(CW / aspect), avail - hc))
        pw = min(CW, int(ph * aspect))
        ph = int(pw / aspect)
        self.panel = (X0 + (CW - pw) // 2, self.y0, pw, ph)
        # vues : une par beat (zoom sur un texte ou une zone de la diapo)
        self.views, self.marks = [], []
        view = (0, 0, 1, 1)
        for b in self.beats:
            f = b.get("focus")
            marks = []
            for mm in norm_marks(b.get("mark")):
                bx = assets.find(sid, mm) if isinstance(mm, str) else tuple(mm)
                if bx:
                    marks.append(bx)
            if f is not None:
                view = self.view_for(sid, f, pw / ph)
            elif marks and self.sc.get("autozoom", True):
                u = (min(m[0] for m in marks), min(m[1] for m in marks), max(m[2] for m in marks), max(m[3] for m in marks))
                view = self.view_for(sid, list(u), pw / ph)
            self.views.append(view)
            self.marks.append(marks)
        if items:
            top = self.y0 + ph + 26
            els, _ = self.stack(items, top, Y_END, gap=14, sizes=(self.cap_size, 32, 30), min_size=30)
            for c, x, y, bi, pg in els:
                self.add(c, x, y, bi, page=pg)
        self.dyn = self.dyn_figure

    def view_for(self, sid, f, aspect):
        if f == "all":
            return (0, 0, 1, 1)
        if isinstance(f, str) and f.startswith("img"):
            ims = assets.images(sid)
            k = int(f[3:] or 1) - 1 if f[3:] else None
            if not ims:
                return (0, 0, 1, 1)
            if k is None:
                bx = (min(b[0] for b in ims), min(b[1] for b in ims), max(b[2] for b in ims), max(b[3] for b in ims))
            else:
                bx = ims[min(k, len(ims) - 1)]
        elif isinstance(f, str):
            bx = assets.find(sid, f) or (0, 0, 1, 1)
        else:
            bx = tuple(f)
        sw, sh = self.slide.size
        x0, y0, x1, y1 = bx[0] * sw, bx[1] * sh, bx[2] * sw, bx[3] * sh
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        w, h = (x1 - x0) * 1.12 + 30, (y1 - y0) * 1.12 + 30
        w = max(w, sw * 0.5)
        if w / h > aspect:
            h = w / aspect
        else:
            w = h * aspect
        w, h = min(w, sw), min(h, sh)
        if w / h > aspect:
            w = h * aspect
        else:
            h = w / aspect
        x0 = min(max(0, cx - w / 2), sw - w)
        y0 = min(max(0, cy - h / 2), sh - h)
        return (x0 / sw, y0 / sh, (x0 + w) / sw, (y0 + h) / sh)

    def dyn_figure(self, img, bi, tb, t_in_beat, beat_dur, fast):
        """Panneau de diapo : transition de vue (0,7 s) puis léger zoom continu (effet Ken Burns)."""
        x, y, pw, ph = self.panel
        sw, sh = self.slide.size
        cur = self.views[bi]
        prev = self.views[bi - 1] if bi > 0 else cur
        p = G.ease_io(t_in_beat / 0.7) if cur != prev else 1.0
        v = [a + (b - a) * p for a, b in zip(prev, cur)]
        # Ken Burns : zoom de 4 % sur la durée du beat
        k = 0.04 * min(1.0, t_in_beat / max(beat_dur, 0.1))
        cxv, cyv = (v[0] + v[2]) / 2, (v[1] + v[3]) / 2
        hw, hh = (v[2] - v[0]) / 2 * (1 - k), (v[3] - v[1]) / 2 * (1 - k)
        box = (int((cxv - hw) * sw), int((cyv - hh) * sh), int((cxv + hw) * sw), int((cyv + hh) * sh))
        crop = self.slide.crop(box).resize((pw, ph), Image.BILINEAR if fast else Image.LANCZOS)
        panel = Image.new("RGBA", (pw, ph), (0, 0, 0, 0))
        mask = G.rounded((pw, ph), 26, fill=(255, 255, 255, 255))
        panel.paste(crop.convert("RGBA"), (0, 0), mask)
        d = ImageDraw.Draw(panel)
        # surlignage de ce qui est dit (beats courant et précédents de la même vue)
        a = G.ease(t_in_beat / 0.45)
        for mb in self.marks[bi]:
            mx0 = (mb[0] * sw - box[0]) / (box[2] - box[0]) * pw - 10
            my0 = (mb[1] * sh - box[1]) / (box[3] - box[1]) * ph - 8
            mx1 = (mb[2] * sw - box[0]) / (box[2] - box[0]) * pw + 10
            my1 = (mb[3] * sh - box[1]) / (box[3] - box[1]) * ph + 8
            cxm, cym = (mx0 + mx1) / 2, (my0 + my1) / 2
            gx = (mx1 - mx0) / 2 * (0.6 + 0.4 * a)
            gy = (my1 - my0) / 2 * (0.6 + 0.4 * a)
            d.rounded_rectangle((cxm - gx, cym - gy, cxm + gx, cym + gy), radius=12,
                                outline=C["num"] + (int(255 * a),), width=7)
        frame = G.rounded((pw + 8, ph + 8), 30, fill=(255, 255, 255, 40))
        img.alpha_composite(frame, (x - 4, y - 4))
        img.alpha_composite(panel, (x, y))
        return img

    # ------------------------------------------------------------------ quiz
    def lay_quiz(self):
        q = self.sc["question"]
        s = G.fit_size(q, CW, 260, sizes=(50, 46, 42, 39, 36, 33, 30))
        qim = Image.new("RGBA", (CW, G.rich_size(q, s, CW)[1] + 10), (0, 0, 0, 0))
        G.draw_rich(qim, (0, 0), q, s, CW, weight="bold", bold="displayx", accent=C["num"])
        self.add(qim, X0, self.y0, 0, "fade")
        top = self.y0 + qim.height + 30
        opts = self.sc["options"]
        ans = set(self.sc.get("answer", []))
        letters = "ABCDEFG"
        self.reveal_beat = next((i for i, b in enumerate(self.beats) if b.get("reveal")), None)
        self.cd = [(i, b) for i, b in enumerate(self.beats) if b.get("countdown")]
        avail = Y_END - top
        for sz in (44, 41, 38, 35, 32, 30, 28, 26, 24):
            neutral = [self.opt_card(letters[k], o, sz, None) for k, o in enumerate(opts)]
            if sum(c.height for c in neutral) + 16 * (len(opts) - 1) <= avail - 10:
                break
        revealed = [self.opt_card(letters[k], o, sz, k in ans) for k, o in enumerate(opts)]
        self.opt_pos = []
        y = top
        for k, c in enumerate(neutral):
            self.add(c, X0, y, 0, "up")
            self.opt_pos.append((X0, y))
            y += c.height + 16
        self.revealed = revealed
        self.dyn = self.dyn_quiz

    def opt_card(self, letter, text, s, ok):
        if ok is None:
            colr, fill, icon = C["def"], (255, 255, 255, 22), letter
        elif ok:
            colr, fill, icon = C["ok"], (46, 229, 157, 60), "✓"
        else:
            colr, fill, icon = C["ko"], (255, 92, 122, 28), "✗"
        lw = int(s * 1.6)
        tw, th = G.rich_size(text, s, CW - lw - 60)
        h = th + 36
        card = G.rounded((CW, h), 24, fill=fill, outline=colr + (200,), width=3)
        d = ImageDraw.Draw(card)
        r = int(s * 0.72)
        cy = h // 2
        d.ellipse((20, cy - r, 20 + 2 * r, cy + r), fill=colr + (255,))
        fi = G.font("symbols" if ok is not None else "displayx", int(s * 0.85))
        d.text((20 + r - fi.getlength(icon) / 2, cy - s * 0.55), icon, font=fi, fill=(10, 12, 24))
        G.draw_rich(card, (lw + 40, 16), text, s, CW - lw - 60, base_color=C["text"] if ok is not False else C["muted"])
        return card

    def dyn_quiz(self, img, bi, tb, t_in_beat, beat_dur, fast):
        # correction
        if self.reveal_beat is not None and bi >= self.reveal_beat:
            a = G.ease(t_in_beat / 0.35) if bi == self.reveal_beat else 1.0
            for (x, y), c in zip(self.opt_pos, self.revealed):
                img.alpha_composite(G.with_alpha(c, a), (x, y))
        # compte à rebours
        for i, b in self.cd:
            if bi == i:
                t0 = b["_cd0"] - b["_t0"]
                tc = t_in_beat - t0
                if 0 <= tc <= b["countdown"]:
                    self.ring(img, b["countdown"] - tc, b["countdown"])
        return img

    def ring(self, img, remaining, total):
        R = 92
        cx, cy = X1 - R - 6, 152 + R // 2
        im = Image.new("RGBA", (2 * R + 20, 2 * R + 20), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        d.ellipse((10, 10, 10 + 2 * R, 10 + 2 * R), fill=(10, 12, 30, 230), outline=(255, 255, 255, 60), width=8)
        frac = max(0.0, remaining / total)
        d.arc((10, 10, 10 + 2 * R, 10 + 2 * R), -90, -90 + 360 * frac, fill=C["num"] + (255,), width=12)
        n = str(max(1, math.ceil(remaining)))
        f = G.font("displayx", 92)
        d.text((10 + R - f.getlength(n) / 2, 10 + R - 58), n, font=f, fill=C["text"])
        img.alpha_composite(im, (cx - R - 10, cy - R - 10))

    # ------------------------------------------------------------------ rendu
    def render(self, bi, t_in_beat, beat_dur, fast=False):
        """Image RGBA de la scène au beat `bi`, `t_in_beat` secondes après son début."""
        anim_p = t_in_beat / ANIM
        static_key = bi
        if anim_p >= 1 and static_key in self._static_cache:
            img = self._static_cache[static_key].copy()
        else:
            img = self.header.copy()
            pages = [e[5] for e in self.elements if e[5] is not None and e[3] <= bi]
            cur_page = max(pages) if pages else 0
            for (im, x, y, b, anim, pg) in self.elements:
                if pg is not None and pg != cur_page:
                    continue
                if b < bi or (b == bi and anim_p >= 1):
                    img.alpha_composite(im, (x, y))
                elif b == bi:
                    p = G.ease(anim_p)
                    if anim == "pop":
                        sc = 0.82 + 0.18 * p
                        w2, h2 = max(1, int(im.width * sc)), max(1, int(im.height * sc))
                        im2 = G.with_alpha(im.resize((w2, h2), Image.BILINEAR), min(1, p * 1.4))
                        img.alpha_composite(im2, (x + (im.width - w2) // 2, y + (im.height - h2) // 2))
                    elif anim == "fade":
                        img.alpha_composite(G.with_alpha(im, p), (x, y))
                    else:
                        img.alpha_composite(G.with_alpha(im, p), (x, int(y + 46 * (1 - p))))
            if anim_p >= 1:
                self._static_cache[static_key] = img.copy()
        if self.dyn:
            img = self.dyn(img, bi, None, t_in_beat, beat_dur, fast)
        return img

    def is_static(self, bi, t_in_beat):
        if t_in_beat < ANIM:
            return False
        if self.kind == "figure":
            return False
        if self.kind == "quiz":
            b = self.beats[bi]
            if b.get("countdown"):
                return False
            if self.reveal_beat is not None and bi == self.reveal_beat and t_in_beat < 0.4:
                return False
        return True
