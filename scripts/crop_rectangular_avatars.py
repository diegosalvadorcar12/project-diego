from pathlib import Path
from PIL import Image, ImageDraw

# Final Project Diego grids with solid #050d18-ish app background.
# Order verified visually by progression strength, not just filename.
SHEETS = [
    Path('/Users/salvador/.hermes/document_cache/doc_e299f9f264d7_1.__bronze_-_black_gold__final_picture_Project_Diego.png'),
    Path('/Users/salvador/.hermes/document_cache/doc_7405d5b1cdcb_2.__legend_-_heavenly_axis__final_picture__Project_Diego..png'),
    Path('/Users/salvador/.hermes/document_cache/doc_a7cbb6a2e445_3.__dao_of_dragon_-_emperor__final_picture_Project_Diego.png'),
]
REALMS = [
    'bronze','silver','gold','blackgold',
    'legend','heavenlyfate','heavenlystar','heavenlyaxis',
    'daoofdragon','martialancestor','deity','emperor',
]
OUT = Path('/Users/salvador/ProjectDiego/assets/avatars')
PREVIEW = Path('/Users/salvador/ProjectDiego/assets/avatar_preview.png')
LISTING = Path('/Users/salvador/ProjectDiego/assets/avatar_listing.txt')
OUT.mkdir(parents=True, exist_ok=True)
for p in OUT.glob('*.png'):
    p.unlink()

outputs = []
level = 1
for sheet_path in SHEETS:
    img = Image.open(sheet_path).convert('RGB')
    W, H = img.size
    cell_w = W / 5
    cell_h = H / 4
    for row in range(4):
        for col in range(5):
            left = int(round(col * cell_w))
            top = int(round(row * cell_h))
            right = int(round((col + 1) * cell_w))
            bottom = int(round((row + 1) * cell_h))
            # Plain rectangular crop. No alpha processing, no background removal, no color keying.
            # Rows below the first can contain glow/wing spillover from the row above at
            # the very top of their grid cell, so trim a small top strip while keeping a rectangle.
            if row > 0:
                top += 24
            sprite = img.crop((left, top, right, bottom))
            realm = REALMS[(level - 1) // 5]
            star = ((level - 1) % 5) + 1
            out = OUT / f'{realm}-{star}.png'
            sprite.save(out)
            outputs.append((level, realm, star, out.name, sprite.size))
            level += 1

# Preview on same app navy background around cards.
thumb_w, thumb_h, label_h = 140, 190, 30
cols, rows = 10, 6
preview = Image.new('RGB', (cols * thumb_w, rows * (thumb_h + label_h)), (5, 13, 24))
d = ImageDraw.Draw(preview)
for idx, (level, realm, star, name, size) in enumerate(outputs):
    r, c = divmod(idx, cols)
    x = c * thumb_w
    y = r * (thumb_h + label_h)
    card = Image.new('RGB', (thumb_w, thumb_h), (5, 13, 24))
    av = Image.open(OUT / name).convert('RGB')
    av.thumbnail((thumb_w, thumb_h), Image.LANCZOS)
    card.paste(av, ((thumb_w - av.width) // 2, (thumb_h - av.height) // 2))
    preview.paste(card, (x, y))
    d.text((x + 4, y + thumb_h + 6), f'{level:02d} {realm}-{star}', fill=(230, 238, 255))
preview.save(PREVIEW)
LISTING.write_text('\n'.join(f'{level:02d}: {name} {size[0]}x{size[1]}' for level, realm, star, name, size in outputs) + '\n')
print(f'Saved {len(outputs)} rectangular avatar crops to {OUT}')
print(f'Preview: {PREVIEW}')
print(f'Listing: {LISTING}')
for level, realm, star, name, size in outputs:
    print(f'{level:02d}: {name} {size[0]}x{size[1]}')
