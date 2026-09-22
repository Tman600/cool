#!/usr/bin/env python3
"""
Pixel-model generator for the dungeon crawler.

Working title: "SANCTIONED"
Premise: You are a Pilgrim walking a dungeon that sits outside sacred time.
Doctrine of the place: you cannot do what you were not meant to do. Every
forbidden act *branches the timeline*: it spawns a Variant of you and risks
you being pulled into that branch or losing (corrupting) the room you stand
in. Christian iconography anchors the "sanctioned" path -- altars, crosses,
a Guardian Angel guide -- while the enforcing authority is the Warden, an
archangel that hunts branches, and the enemies are the Fallen.

Everything here is authored as 16x16 (or 16x24) string grids so the pixels
are deliberate. We export:
  - assets/sprites/<name>.png            native-resolution frames/sheets
  - assets/preview/<name>_x8.png         8x nearest-neighbour previews
  - assets/preview/atlas.png             one contact sheet of everything

Run:  python3 game/tools/gen_sprites.py
"""

from PIL import Image
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SPRITES = os.path.join(ROOT, "assets", "sprites")
PREVIEW = os.path.join(ROOT, "assets", "preview")
os.makedirs(SPRITES, exist_ok=True)
os.makedirs(PREVIEW, exist_ok=True)

# ---------------------------------------------------------------------------
# Palette.  Single letter -> RGBA.  '.' is transparent.
# ---------------------------------------------------------------------------
P = {
    ".": (0, 0, 0, 0),        # transparent
    "K": (26, 22, 34, 255),   # outline / near-black
    "k": (52, 46, 64, 255),   # soft dark

    # skin
    "s": (232, 190, 152, 255),
    "S": (196, 148, 112, 255),

    # pilgrim (sanctioned blue + white robe, gold trim)
    "w": (238, 236, 228, 255),  # robe white
    "W": (198, 200, 210, 255),  # robe shadow
    "b": (74, 108, 176, 255),   # cloak blue
    "B": (48, 74, 132, 255),    # cloak blue shadow
    "g": (226, 186, 92, 255),   # gold
    "G": (176, 138, 58, 255),   # gold shadow

    # variant (branched, corrupted violet + glitch cyan)
    "v": (150, 92, 196, 255),
    "V": (98, 56, 140, 255),
    "c": (120, 224, 226, 255),  # glitch cyan
    "n": (30, 20, 44, 255),     # variant near-black

    # angelic (holy white + halo gold + soft glow)
    "h": (250, 248, 236, 255),  # feather white
    "H": (214, 216, 224, 255),  # feather shadow
    "y": (250, 224, 130, 255),  # halo / light
    "Y": (214, 176, 78, 255),   # halo shadow
    "t": (196, 226, 250, 255),  # holy glow accent

    # fallen / demon
    "r": (176, 54, 54, 255),    # demon red
    "R": (120, 34, 36, 255),    # demon red shadow
    "d": (70, 60, 60, 255),     # fallen steel dark
    "D": (44, 38, 40, 255),     # fallen steel darker
    "e": (232, 96, 72, 255),    # ember
    "o": (250, 176, 84, 255),   # fire / torch

    # props
    "m": (150, 120, 96, 255),   # wood
    "M": (108, 84, 64, 255),    # wood shadow
    "z": (120, 128, 140, 255),  # stone
    "Z": (84, 92, 104, 255),    # stone shadow
    "p": (206, 92, 150, 255),   # rift magenta
    "l": (168, 118, 214, 255),  # rift violet
    "a": (250, 250, 250, 255),  # bright white / spark
}


def grid(rows):
    """Turn a list of equal-length strings into an RGBA Image."""
    h = len(rows)
    w = max(len(r) for r in rows)
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    px = img.load()
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            px[x, y] = P.get(ch, (0, 0, 0, 0))
    return img


def mirror(img):
    return img.transpose(Image.FLIP_LEFT_RIGHT)


def sheet(frames, pad=1):
    """Lay frames left-to-right onto one strip with `pad` transparent px gap."""
    h = max(f.height for f in frames)
    w = sum(f.width for f in frames) + pad * (len(frames) - 1)
    out = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    x = 0
    for f in frames:
        out.paste(f, (x, h - f.height), f)  # bottom-align
        x += f.width + pad
    return out


def scale(img, f):
    return img.resize((img.width * f, img.height * f), Image.NEAREST)


# ===========================================================================
# PILGRIM  -- the player. 3rd-person, 4 facings x 2 walk frames.
# 16x16.  Blue cloak over white robe, gold cross on the chest, staff.
# ===========================================================================
PIL_DOWN_A = [
    "......KK........",
    ".....KssK.......",
    ".....KssK.......",
    "....KsssK.......",
    "...KbwwwbK..g...",
    "...KbwgwbK.KgK..",
    "...KbwgwbK.KgK..",
    "...KbwwwbK.KgK..",
    "...KBwwwBK.KGK..",
    "....KwwwK..KgK..",
    "....KwWwK..KgK..",
    "....Kw.wK..KgK..",
    "....Ks.sK..KgK..",
    "...KK...KK.KgK..",
    "................",
    "................",
]
PIL_DOWN_B = [
    "......KK........",
    ".....KssK.......",
    ".....KssK.......",
    "....KsssK.......",
    "...KbwwwbK..g...",
    "...KbwgwbK.KgK..",
    "...KbwgwbK.KgK..",
    "...KbwwwbK.KgK..",
    "...KBwwwBK.KGK..",
    "....KwwwK..KgK..",
    "....KwWwK..KgK..",
    "...Kw..wK..KgK..",
    "...Ks..sK..KgK..",
    "..KK....KK.KgK..",
    "................",
    "................",
]
PIL_UP_A = [
    "......KK........",
    ".....KbbK.......",
    ".....KbbK.......",
    "....KbbbK.......",
    "...KbbbbbK..g...",
    "...KbbbbbK.KgK..",
    "...KbBbBbK.KgK..",
    "...KbbbbbK.KgK..",
    "...KBbbbBK.KGK..",
    "....KbbbK..KgK..",
    "....KbWbK..KgK..",
    "....Kb.bK..KgK..",
    "....Ks.sK..KgK..",
    "...KK...KK.KgK..",
    "................",
    "................",
]
PIL_UP_B = [
    "......KK........",
    ".....KbbK.......",
    ".....KbbK.......",
    "....KbbbK.......",
    "...KbbbbbK..g...",
    "...KbbbbbK.KgK..",
    "...KbBbBbK.KgK..",
    "...KbbbbbK.KgK..",
    "...KBbbbBK.KGK..",
    "....KbbbK..KgK..",
    "....KbWbK..KgK..",
    "...Kb..bK..KgK..",
    "...Ks..sK..KgK..",
    "..KK....KK.KgK..",
    "................",
    "................",
]
PIL_SIDE_A = [
    "....KK..........",
    "...KssK.........",
    "...KssK.........",
    "...KsssK........",
    "...KbwwK...g....",
    "..KbwgwK..KgK...",
    "..KbwgwK..KgK...",
    "..KbwwwK..KgK...",
    "..KBwwWK..KGK...",
    "...KwwK...KgK...",
    "...KwWK...KgK...",
    "...Kw.K...KgK...",
    "...Ks.K...KgK...",
    "..KK.KK...KgK...",
    "................",
    "................",
]
PIL_SIDE_B = [
    "....KK..........",
    "...KssK.........",
    "...KssK.........",
    "...KsssK........",
    "...KbwwK...g....",
    "..KbwgwK..KgK...",
    "..KbwgwK..KgK...",
    "..KbwwwK..KgK...",
    "..KBwwWK..KGK...",
    "...KwwK...KgK...",
    "...KwWK...KgK...",
    "..Kw..K...KgK...",
    "..Ks..sK..KgK...",
    ".KK...KK..KgK...",
    "................",
    "................",
]

# ===========================================================================
# VARIANT -- your branched self. Same silhouette, corrupted palette + glitch.
# ===========================================================================
VAR_DOWN_A = [
    "......KK........",
    ".....KSSK.......",
    ".....KScK...c...",
    "....KSSSK.......",
    "...KvnnnvK..c...",
    "...KvncnvK.KcK..",
    "...KvnnnvK.KcK..",
    "...KvnnnvK.KcK..",
    "...KVnnnVK.KcK..",
    "..c.KnnnK..KcK..",
    "....KncnK..KcK..",
    "....Kn.nK..KcK..",
    "....KS.SK..KcK..",
    "...KK.c.KK.KcK..",
    "................",
    "................",
]
VAR_DOWN_B = [
    "......KK........",
    ".....KSSK...c...",
    ".....KScK.......",
    "....KSSSK.......",
    "...KvnnnvK..c...",
    "...KvncnvK.KcK..",
    "...KvnnnvK.KcK..",
    "...KvnnnvK.KcK..",
    "...KVnnnVK.KcK..",
    "....KnnnK..KcK..",
    "..c.KncnK..KcK..",
    "...Kn..nK..KcK..",
    "...KS..SK..KcK..",
    "..KK.c..KK.KcK..",
    "................",
    "................",
]

# ===========================================================================
# GUARDIAN ANGEL -- ally / guide. Floating, front only, 2-frame wing beat.
# 16x16. Halo, spread wings, white gown.
# ===========================================================================
ANG_A = [
    ".......yy.......",
    "......yYYy......",
    "......Y..Y......",
    "..h....ss....h..",
    ".hHh..KssK..hHh.",
    "hHHHh.KssK.hHHHh",
    "hHHHhKhhhhKhHHHh",
    ".hHHKhhtthhKHHh.",
    "..hhKhhhhhhKhh..",
    "....KhtHHthK....",
    "....KhhHHhhK....",
    "....KhhhhhhK....",
    ".....KhttHK.....",
    "......KhhK......",
    ".......yy.......",
    "................",
]
ANG_B = [
    ".......yy.......",
    "......yYYy......",
    "......Y..Y......",
    ".......ss.......",
    "h.....KssK.....h",
    "hHh...KssK...hHh",
    "hHHh.KhhhhKhHHh.",
    "hHHHKhhtthhKHHHh",
    ".hhhKhhhhhhKhhh.",
    "....KhtHHthK....",
    "....KhhHHhhK....",
    "....KhhhhhhK....",
    ".....KhttHK.....",
    "......KhhK......",
    ".......yy.......",
    "................",
]

# ===========================================================================
# WARDEN -- the enforcing archangel (TVA-style authority). Taller (16x24).
# Gold armour, great grey wings, a spear, stern helm-halo.
# ===========================================================================
WARDEN_A = [
    "......yYYy......",
    ".....yYggYy.....",
    ".....KggggK.....",
    ".....KgSSgK.....",
    "....HKgSSgKH....",
    "...HHKggggKHH...",
    "..HHHKgGGgKHHH..",
    "..HHKGgggGKHH...",
    "...HKgGggGgK....",
    "....KgGggGgK....",
    "....KgGGGGgK....",
    "....KbGggGbK....",
    "....KbbGGbbK....",
    "....KbBbBbbK....",
    "....KbBbBbbK....",
    "....KbbbbbbK....",
    "....KBb..bBK....",
    "....Kg....gK....",
    "....Kg....gK....",
    "...KK......KK...",
    "................",
    "................",
    "................",
    "................",
]
WARDEN_B = [
    "......yYYy......",
    ".....yYggYy.....",
    ".....KggggK.....",
    ".....KgSSgK.....",
    ".H..HKgSSgKH..H.",
    ".HH.HKggggKH.HH.",
    ".HHHHKgGGgKHHHH.",
    "..HHKGgggGKHH...",
    "...HKgGggGgK....",
    "....KgGggGgK....",
    "....KgGGGGgK....",
    "....KbGggGbK....",
    "....KbbGGbbK....",
    "....KbBbBbbK....",
    "....KbBbBbbK....",
    "....KbbbbbbK....",
    "....KBb..bBK....",
    "....Kg....gK....",
    "...Kg......gK...",
    "..KK........KK..",
    "................",
    "................",
    "................",
    "................",
]

# ===========================================================================
# FALLEN KNIGHT -- corrupted crusader enemy. Front, 2-frame.
# Dark steel, cracked-red visor glow, broken sword.
# ===========================================================================
FALLEN_A = [
    "......KK........",
    ".....KddK.......",
    ".....KdDK.......",
    "....KdeedK......",
    "....KdDDdK...D..",
    "...KdddddK..KDK.",
    "...KdRRRdK..KDK.",
    "...KddddK...KDK.",
    "...KDddDK...KeK.",
    "....KdddK...KDK.",
    "....KdDdK...KDK.",
    "....Kd.dK...KDK.",
    "....Kd.dK...KDK.",
    "...KK...KK..KDK.",
    "................",
    "................",
]
FALLEN_B = [
    "......KK........",
    ".....KddK.......",
    ".....KdDK.......",
    "....KdeedK......",
    "....KdDDdK...D..",
    "...KdddddK..KDK.",
    "...KdRRRdK..KDK.",
    "...KddddK...KeK.",
    "...KDddDK...KDK.",
    "....KdddK...KDK.",
    "....KdDdK...KDK.",
    "...Kd..dK...KDK.",
    "...Kd..dK...KDK.",
    "..KK....KK..KDK.",
    "................",
    "................",
]

# ===========================================================================
# DEMON -- lesser enemy. Horns, wings, ember eyes. Front, 2-frame hover.
# ===========================================================================
DEMON_A = [
    "...K........K...",
    "...Kr......rK...",
    "r...KrK..KrK...r",
    "rRr..KrrrrK..rRr",
    "rRRr.KraarK.rRRr",
    "rRRrKrrrrrrKrRRr",
    ".RRKrreerreeKRR.",
    "..KrrrrrrrrrrK..",
    "..KrRrKooKrRrK..",
    "...KrrKooKrrK...",
    "...KrRrrrrRrK...",
    "....KrRRRRrK....",
    "....Krr..rrK....",
    "...KrK....KrK...",
    "..KK........KK..",
    "................",
]
DEMON_B = [
    "...K........K...",
    "...Kr......rK...",
    "....KrK..KrK....",
    "rRr..KrrrrK..rRr",
    "rRRr.KraarK.rRRr",
    "rRRrKrrrrrrKrRRr",
    "rRRKrreerreeKRRr",
    ".RKrrrrrrrrrrKR.",
    "..KrRrKooKrRrK..",
    "...KrrKooKrrK...",
    "...KrRrrrrRrK...",
    "....KrRRRRrK....",
    "....Krr..rrK....",
    "....KrK..KrK....",
    "...KK....KK.....",
    "................",
]

# ===========================================================================
# PROPS / OBJECTS
# ===========================================================================
# Altar of Anchor -- your save / "sanctioned checkpoint". 16x16.
ALTAR = [
    "................",
    ".......gg.......",
    ".......gg.......",
    ".....g.gg.g.....",
    "......gggg......",
    ".......gg.......",
    ".....yyggyy.....",
    "....zzzzzzzz....",
    "...KzwwwwwwzK...",
    "...KzzzzzzzzK...",
    "...KZzzzzzzZK...",
    "...KZZZZZZZZK...",
    "...KZZzzzzZZK...",
    "...KZZZZZZZZK...",
    "..KKZZZZZZZZKK..",
    "................",
]
# Standing cross
CROSS = [
    ".......gg.......",
    ".......gg.......",
    ".......gg.......",
    "....gggGGggg....",
    "....gggGGggg....",
    ".......GG.......",
    ".......gg.......",
    ".......gg.......",
    ".......gg.......",
    ".......gg.......",
    ".......GG.......",
    ".......gg.......",
    "......KggK......",
    ".....KZZZZK.....",
    "....KZZZZZZK....",
    "................",
]
# Chest
CHEST = [
    "................",
    "................",
    "...KKKKKKKK.....",
    "..KmmmmmmmmK....",
    "..KmMmMmMmMK....",
    "..KmmmmmmmmK....",
    "..KKKKgggKKK....",
    "..KMMMKgKMMM....",
    "..KmmmmmmmmK....",
    "..KmMmMmMmMK....",
    "..KmmmmmmmmK....",
    "..KMMMMMMMMK....",
    "..KKKKKKKKKK....",
    "................",
    "................",
    "................",
]
# Torch (wall) -- 2-frame flicker, 8x16
TORCH_A = [
    "...oo...",
    "..oaao..",
    "..oooo..",
    "...eo...",
    "...KK...",
    "...mK...",
    "...mK...",
    "...mK...",
    "...mK...",
    "..KKK...",
    "........",
    "........",
    "........",
    "........",
    "........",
    "........",
]
TORCH_B = [
    "...o....",
    "..oao...",
    "..ooao..",
    "..oeo...",
    "...KK...",
    "...mK...",
    "...mK...",
    "...mK...",
    "...mK...",
    "..KKK...",
    "........",
    "........",
    "........",
    "........",
    "........",
    "........",
]
# Timeline Rift -- forbidden branch portal. 3-frame pulse. 16x16.
RIFT_A = [
    "................",
    "......pp........",
    ".....pllp.......",
    "....pl..lp......",
    "...pl.aa.lp.....",
    "...pl.aa.lp.....",
    "..pl.a..a.lp....",
    "..pl.a..a.lp....",
    "..pl.a..a.lp....",
    "...pl.aa.lp.....",
    "...pl.aa.lp.....",
    "....pl..lp......",
    ".....pllp.......",
    "......pp........",
    "................",
    "................",
]
RIFT_B = [
    "......pp........",
    ".....pllp.......",
    "....pl..lp......",
    "...pla..alp.....",
    "..pl.acca.lp....",
    "..pla.cc.alp....",
    ".pl.ac..ca.lp...",
    ".pla.c..c.alp...",
    ".pl.ac..ca.lp...",
    "..pla.cc.alp....",
    "..pl.acca.lp....",
    "...pla..alp.....",
    "....pl..lp......",
    ".....pllp.......",
    "......pp........",
    "................",
]
RIFT_C = [
    ".....pp.pp......",
    "....pllplp......",
    "...pl.ccl.p.....",
    "..pl.acca.lp....",
    ".pl.ac..ca.lp...",
    ".plac.aa.calp...",
    "pl.c.a..a.c.lp..",
    "pla.c.aa.c.alp..",
    "pl.c.a..a.c.lp..",
    ".plac.aa.calp...",
    ".pl.ac..ca.lp...",
    "..pl.acca.lp....",
    "...pl.ccl.p.....",
    "....pllplp......",
    ".....pp.pp......",
    "................",
]

# ---------------------------------------------------------------------------
# Build table:  name -> (list_of_frame_grids, is_character_facings)
# ---------------------------------------------------------------------------
def G(rows):
    return grid(rows)


builds = {}

# Pilgrim: down, up, side-right, side-left (mirrored)  x2 frames each
p_down = [G(PIL_DOWN_A), G(PIL_DOWN_B)]
p_up = [G(PIL_UP_A), G(PIL_UP_B)]
p_right = [G(PIL_SIDE_A), G(PIL_SIDE_B)]
p_left = [mirror(f) for f in p_right]
builds["pilgrim_down"] = p_down
builds["pilgrim_up"] = p_up
builds["pilgrim_right"] = p_right
builds["pilgrim_left"] = p_left

# Variant: down + up(mirror-derived not accurate, so reuse down palette).
v_down = [G(VAR_DOWN_A), G(VAR_DOWN_B)]
v_right = [G(VAR_DOWN_A), G(VAR_DOWN_B)]  # placeholder side = front for now
builds["variant_down"] = v_down

builds["guardian_angel"] = [G(ANG_A), G(ANG_B)]
builds["warden"] = [G(WARDEN_A), G(WARDEN_B)]
builds["fallen_knight"] = [G(FALLEN_A), G(FALLEN_B)]
builds["demon"] = [G(DEMON_A), G(DEMON_B)]

builds["altar"] = [G(ALTAR)]
builds["cross"] = [G(CROSS)]
builds["chest"] = [G(CHEST)]
builds["torch"] = [G(TORCH_A), G(TORCH_B)]
builds["rift"] = [G(RIFT_A), G(RIFT_B), G(RIFT_C)]

# ---------------------------------------------------------------------------
# Export
# ---------------------------------------------------------------------------
manifest = {}
for name, frames in builds.items():
    strip = sheet(frames) if len(frames) > 1 else frames[0]
    strip.save(os.path.join(SPRITES, f"{name}.png"))
    scale(strip, 8).save(os.path.join(PREVIEW, f"{name}_x8.png"))
    manifest[name] = {
        "frames": len(frames),
        "frame_w": frames[0].width,
        "frame_h": frames[0].height,
        "file": f"assets/sprites/{name}.png",
    }

# One big contact-sheet atlas (labels omitted; just the art, tidy grid).
cols = 4
cell = 16 * 8 + 16  # 8x sprite + margin
labels = list(builds.keys())
rows_n = (len(labels) + cols - 1) // cols
# tallest 8x sprite is the warden strip; give generous cell height
cell_h = 24 * 8 + 24
atlas = Image.new("RGBA", (cols * cell, rows_n * cell_h), (18, 16, 24, 255))
for i, name in enumerate(labels):
    strip = sheet(builds[name]) if len(builds[name]) > 1 else builds[name][0]
    big = scale(strip, 8)
    if big.width > cell - 8:
        f = (cell - 8) / big.width
        big = strip.resize((int(strip.width * f * 8 / 8), int(strip.height * f)), Image.NEAREST)
        big = scale(strip, max(1, int((cell - 8) / strip.width)))
    cx = (i % cols) * cell + (cell - big.width) // 2
    cy = (i // cols) * cell_h + (cell_h - big.height) // 2
    atlas.alpha_composite(big, (cx, max(cy, (i // cols) * cell_h + 8)))
atlas.save(os.path.join(PREVIEW, "atlas.png"))

# Write a small JSON manifest for the eventual game loader.
import json
with open(os.path.join(ROOT, "assets", "sprites", "manifest.json"), "w") as fh:
    json.dump({"tile": 16, "sprites": manifest}, fh, indent=2)

print(f"Generated {len(builds)} sprite sets -> {SPRITES}")
for n, m in manifest.items():
    print(f"  {n:18} {m['frames']} frame(s)  {m['frame_w']}x{m['frame_h']}")
print(f"Atlas -> {os.path.join(PREVIEW, 'atlas.png')}")
