"""Outil de préparation : planche-contact de diapos avec grille de repérage (coordonnées relatives 0-1)."""
import sys
from PIL import Image, ImageDraw, ImageFont
import assets, config
out = config.WORK / "inspect"; out.mkdir(exist_ok=True)
f = ImageFont.truetype(config.FONTS["bold"], 18); fl = ImageFont.truetype(config.FONTS["bold"], 24)
ids = sys.argv[2:]; name = sys.argv[1]
TW = 540; cells = []
for sid in ids:
    im = assets.slide_image(sid).convert("RGB")
    im = im.resize((TW, int(TW * im.height / im.width)))
    d = ImageDraw.Draw(im)
    for k in range(1, 10):
        x = im.width * k / 10; y = im.height * k / 10
        d.line((x, 0, x, im.height), fill=(255, 60, 60), width=1); d.line((0, y, im.width, y), fill=(255, 60, 60), width=1)
        d.text((x + 2, 2), f"{k}", font=f, fill=(255, 0, 0)); d.text((2, y + 1), f"{k}", font=f, fill=(255, 0, 0))
    lab = Image.new("RGB", (TW, 30), (20, 20, 20)); ImageDraw.Draw(lab).text((6, 2), sid, font=fl, fill=(255, 255, 0))
    c = Image.new("RGB", (TW, im.height + 30)); c.paste(lab, (0, 0)); c.paste(im, (0, 30)); cells.append(c)
cols = 2; rows = (len(cells) + 1) // 2
rh = [max(c.height for c in cells[r*cols:(r+1)*cols]) for r in range(rows)]
sheet = Image.new("RGB", (TW * cols + 10, sum(rh) + 10 * rows), (60, 60, 60))
y = 0
for r in range(rows):
    for k, c in enumerate(cells[r*cols:(r+1)*cols]):
        sheet.paste(c, (k * (TW + 10), y))
    y += rh[r] + 10
sheet.save(out / f"{name}.png"); print(out / f"{name}.png")
