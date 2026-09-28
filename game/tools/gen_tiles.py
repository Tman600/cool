#!/usr/bin/env python3
"""Generate the 16x16 dungeon tileset for SANCTIONED (floor/wall/door/etc).

Kept separate from gen_sprites.py so the character art and the environment
art can be regenerated independently. Run: python3 game/tools/gen_tiles.py
"""
from PIL import Image
import os, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SPRITES = os.path.join(ROOT, "assets", "sprites")
PREVIEW = os.path.join(ROOT, "assets", "preview")
os.makedirs(SPRITES, exist_ok=True)
os.makedirs(PREVIEW, exist_ok=True)

P = {
    ".": (0, 0, 0, 0),
    "K": (26, 22, 34, 255),
    # stone floor
    "f": (58, 54, 70, 255),
    "F": (48, 44, 58, 255),
    "g": (66, 62, 80, 255),   # floor speck light
    # wall
    "w": (92, 84, 104, 255),
    "W": (68, 62, 80, 255),
    "e": (112, 104, 126, 255),  # wall highlight edge
    # door wood
    "m": (150, 120, 96, 255),
    "M": (108, 84, 64, 255),
    "i": (226, 186, 92, 255),   # iron/gold stud
    # corrupted floor (branch decay)
    "c": (74, 44, 88, 255),
    "C": (52, 30, 64, 255),
    "p": (150, 92, 196, 255),
    # stairs
    "s": (84, 92, 104, 255),
    "S": (60, 66, 78, 255),
}


def grid(rows):
    img = Image.new("RGBA", (len(rows[0]), len(rows)), (0, 0, 0, 0))
    px = img.load()
    for y, r in enumerate(rows):
        for x, ch in enumerate(r):
            px[x, y] = P.get(ch, (0, 0, 0, 0))
    return img


FLOOR = [
    "ffffffffffffffff",
    "fFffffffgfffffFf",
    "ffffffffffffffff",
    "ffgfffffffffffff",
    "ffffffffffffgfff",
    "fffffffFffffffff",
    "fffgffffffffffff",
    "ffffffffffffffff",
    "ffffffffffgfffff",
    "fFfffffffffffffF",
    "ffffffgfffffffff",
    "ffffffffffffffff",
    "fffffffffffFffff",
    "ffgffffffffffgff",
    "ffffffffffffffff",
    "fFffffffffgfffff",
]
WALL = [
    "eeeeeeeeeeeeeeee",
    "wwwwwwwwwwwwwwww",
    "wWwwWwwwWwwwWwww",
    "wwwwwwwwwwwwwwww",
    "wwWwwwWwwwWwwwWw",
    "wwwwwwwwwwwwwwww",
    "WwwwWwwwWwwwWwww",
    "wwwwwwwwwwwwwwww",
    "wwwWwwwWwwwWwwwW",
    "wwwwwwwwwwwwwwww",
    "wWwwWwwwWwwwWwww",
    "wwwwwwwwwwwwwwww",
    "wwwwWwwwWwwwWwww",
    "wwwwwwwwwwwwwwww",
    "WwwwwwWwwwwwWwww",
    "KKKKKKKKKKKKKKKK",
]
DOOR = [
    "KKKKKKKKKKKKKKKK",
    "KMMMMMMMMMMMMMMK",
    "KMmmmmmmmmmmmmMK",
    "KMmMmmmMmmMmmmMK",
    "KMmmmmmmmmmmmmMK",
    "KMmmmMmmmmMmmmMK",
    "KMmmmmmmimmmmmMK",
    "KMmMmmmimimmMmMK",
    "KMmmmmmmimmmmmMK",
    "KMmmmMmmmmMmmmMK",
    "KMmmmmmmmmmmmmMK",
    "KMmMmmmMmmMmmmMK",
    "KMmmmmmmmmmmmmMK",
    "KMmmmmmmmmmmmmMK",
    "KMMMMMMMMMMMMMMK",
    "KKKKKKKKKKKKKKKK",
]
CORRUPT = [
    "cccccccccccccccc",
    "cCccpcccccccCccc",
    "ccccccccpccccccc",
    "ccpccccccccccccc",
    "ccccccccccccpccc",
    "cccccccCcccccccc",
    "cccpccccccccccpc",
    "cccccccccccccccc",
    "ccccpcccccCccccc",
    "cCccccccccccccpc",
    "ccccccpccccccccc",
    "ccpccccccccccccc",
    "ccccccccccCppccc",
    "ccpcccccccccccpc",
    "cccccccccccccccc",
    "cCcccccccpcccccc",
]
STAIRS = [
    "ssssssssssssssss",
    "SSSSSSSSSSSSSSSS",
    "ssssssssssssssss",
    "SSSSSSSSSSSSSSSS",
    "ssssssssssssssss",
    "SSSSSSSSSSSSSSSS",
    "ssssssssssssssss",
    "SSSSSSSSSSSSSSSS",
    "ssssssssssssssss",
    "SSSSSSSSSSSSSSSS",
    "ssssssssssssssss",
    "SSSSSSSSSSSSSSSS",
    "ssssssssssssssss",
    "SSSSSSSSSSSSSSSS",
    "ssssssssssssssss",
    "SSSSSSSSSSSSSSSS",
]

tiles = {
    "tile_floor": FLOOR,
    "tile_wall": WALL,
    "tile_door": DOOR,
    "tile_corrupt": CORRUPT,
    "tile_stairs": STAIRS,
}

made = {}
for name, rows in tiles.items():
    img = grid(rows)
    img.save(os.path.join(SPRITES, f"{name}.png"))
    img.resize((128, 128), Image.NEAREST).save(os.path.join(PREVIEW, f"{name}_x8.png"))
    made[name] = {"frames": 1, "frame_w": 16, "frame_h": 16,
                  "file": f"assets/sprites/{name}.png", "solid": name == "tile_wall"}

# merge into manifest.json
mpath = os.path.join(SPRITES, "manifest.json")
manifest = json.load(open(mpath))
manifest.setdefault("tiles", {}).update(made)
json.dump(manifest, open(mpath, "w"), indent=2)

print(f"Generated {len(made)} tiles and merged into manifest.json")
for n in made:
    print(" ", n)
