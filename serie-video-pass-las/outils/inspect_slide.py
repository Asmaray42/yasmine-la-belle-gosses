"""Outil de préparation : enregistre une diapo recadrée avec une grille de repérage (coordonnées relatives)."""
import sys
from PIL import ImageDraw, ImageFont
import assets, config
out = config.WORK / "inspect"; out.mkdir(exist_ok=True)
f = ImageFont.truetype(config.FONTS["bold"], 26)
for sid in sys.argv[1:]:
    im = assets.slide_image(sid).convert("RGB")
    im = im.resize((900, int(900 * im.height / im.width)))
    d = ImageDraw.Draw(im)
    for k in range(1, 10):
        x = im.width * k / 10; y = im.height * k / 10
        d.line((x, 0, x, im.height), fill=(255, 0, 0), width=1); d.line((0, y, im.width, y), fill=(255, 0, 0), width=1)
        d.text((x + 2, 2), f".{k}", font=f, fill=(255, 0, 0)); d.text((2, y + 2), f".{k}", font=f, fill=(255, 0, 0))
    im.save(out / (sid.replace(":", "_") + ".png"))
print(out)
