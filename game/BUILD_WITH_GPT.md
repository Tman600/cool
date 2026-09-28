# SANCTIONED — Build Kit (hand this whole `game/` folder to GPT)

This folder is a complete, self-contained spec + assets for a **3rd-person
(top-down) dungeon crawler**. A model or developer should be able to build a
playable prototype from the files here without any other context.

> **Premise:** You are a **Pilgrim** in a dungeon outside sacred time. Its one
> law: *you cannot do what you were not meant to do.* Every forbidden act
> **branches the timeline** — spawning a **Variant** of you and risking either
> being pulled into the branch or corrupting the room you stand in. Christian
> iconography (altars, crosses, a Guardian Angel) marks the sanctioned path;
> the **Warden**, an archangel, hunts branches. (Think Marvel/TVA "sacred
> timeline," reframed through faith and restraint.)

---

## What's in here

```
game/
├── BUILD_WITH_GPT.md        ← you are here (the brief)
├── data/                    ← all game data as JSON (the "content")
│   ├── game.json            ← title, pillars, global config
│   ├── mechanics.json       ← the rules: divergence, forbidden actions, faith, combat, endings
│   ├── entities.json        ← player / enemies / npcs / props + which sprite each uses
│   ├── rooms.json           ← the dungeon: 6 rooms as tile grids + placements + exits
│   └── dialogue.json        ← Guardian Angel lines + ending text
├── assets/
│   ├── sprites/             ← ready-to-use PNGs (16px pixel art) + manifest.json
│   │   ├── manifest.json    ← every sprite/tile: file, frame size, frame count
│   │   ├── pilgrim_down.png … (4 facings, 2-frame walk strips)
│   │   ├── variant_down.png, guardian_angel.png, warden.png,
│   │   ├── fallen_knight.png, demon.png,
│   │   ├── altar.png, cross.png, chest.png, torch.png, rift.png,
│   │   └── tile_floor.png, tile_wall.png, tile_door.png, tile_corrupt.png, tile_stairs.png
│   └── preview/             ← 8× zoomed previews + atlas.png (human reference only)
└── tools/                   ← the Python generators that produced the art (optional)
    ├── gen_sprites.py        (characters + props)   requires: pillow
    └── gen_tiles.py          (dungeon tiles)        requires: pillow
```

**Sprite sheets are horizontal strips.** For a sprite with N frames, the PNG is
`N × frame_w` wide; slice it into N frames of `frame_w × frame_h`. There is a
**1px transparent gap between frames** — read exact frame boxes from
`manifest.json` (each frame starts at `x = i * (frame_w + 1)`). Single-frame
sprites/tiles have no gap.

---

## Recommended build target

Pick whichever is easiest for you; the data is engine-agnostic:

- **Web / fastest to run:** plain HTML5 Canvas + JavaScript (single `index.html`
  + `main.js`), or **Phaser 3**. No build step; loads the PNGs and JSON directly.
- **Desktop:** **Python + pygame** (matches the asset generators already here),
  or **Godot 4** (import PNGs, parse the JSON in GDScript).

Default recommendation if unspecified: **HTML5 Canvas + vanilla JS**, so the
result opens in a browser with zero install.

---

## Build order (do it in this sequence)

1. **Loader** — read `assets/sprites/manifest.json`; load every PNG; slice each
   into frames using `frame_w/frame_h` and the 1px gap. Expose `getSprite(key)`.
2. **Tilemap renderer** — read a room from `data/rooms.json`, draw the tile layer
   using the `_format.legend` mapping (char → tile sprite). Cell = 16px, then
   apply `game.json.render_scale` (default 3×) with **nearest-neighbour** scaling
   (keep pixels crisp — disable image smoothing).
3. **Player** — spawn the Pilgrim at `player_spawn`. Implement 4-direction
   movement + walk animation (`entities.player.sprites` + `anim_fps`). Collide
   with `#` walls.
4. **Props & interaction** — place props from each room; implement `interact`
   verbs from `entities.props` (pray, light_cross, open, enter_rift).
5. **Divergence system** — implement `mechanics.divergence`: the meter, the
   forbidden-action costs (`mechanics.forbidden_actions`), the threshold effects,
   and passive decay. Show it as a UI bar.
6. **Enemies** — implement the behaviors in `entities.enemies` (variant ghost-
   pursuit, kneeling fallen knight, demon swoop, warden enforcer).
7. **Faith** — altar prayer + cross lighting from `mechanics.faith` (reset
   divergence, checkpoint, seal rifts, despawn variants).
8. **Rooms & exits** — connect rooms via each room's `exits` (door `+`, stairs
   `>`); handle rift `branch_to` travel into `*__branch` rooms.
9. **Dialogue** — Guardian Angel lines from `data/dialogue.json`, triggered by
   `npcs[].on` / `dialogue` id and by divergence thresholds.
10. **Endings** — route via `mechanics.endings` using final divergence + whether
    sealed relics were taken; show `dialogue.endings.<id>`.

---

## The one rule that makes this game *this* game

Divergence is the whole hook. Keep these true:

- Doing the **sanctioned** thing (only what a room permits) is calm and free.
- Every **forbidden** action has an immediate, legible cost and a visible
  consequence (a Variant appears, the floor starts turning to `tile_corrupt`,
  the Warden stirs). The player must always feel *why* restraint pays.
- **Altars are mercy:** prayer wipes divergence, seals the rift, and banishes the
  Variant. Faith is the undo button. Make it feel like relief.

Rooms declare their own `forbidden` list, so the *same* action (e.g. striking a
knight) is sanctioned in one room and a timeline branch in another. Honor the
per-room list.

---

## Regenerating / editing the art (optional)

The PNGs are already built — you don't need Python to ship. To change the art,
edit the string-grid pixel maps in `tools/gen_sprites.py` / `tools/gen_tiles.py`
and rerun (`pip install pillow` first). They rewrite the PNGs and
`manifest.json` deterministically.

## Missing pieces / good first extensions (be honest with the player)

Not yet authored — safe to add:
- Variant only has a `down` facing; give it the other 3 (mirror `right`).
- Warden / angels are front-facing only.
- No player attack/hurt frames yet (combat uses the walk sprite for now).
- No audio, title screen, or HUD art — add as desired.
