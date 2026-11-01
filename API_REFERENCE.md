# API Reference — Turag Video Kit Engine

All engine code lives in `engine/`. Coordinates use design space **960×540**, uniformly scaled at render time. Drawing is a pure function of absolute time `t` and stable data — deterministic, seekable, no randomness.

## Global Objects

- `TuragScenes.palette` / `P` — color tokens: `paper #E9E4D2`, `ink #12141C`, `red #FF3D17`, `blue #2F3BFF`, `green #216E50`, `grey #8A8CA0`, `slate #4A4D63`, `pale #C8C1AB`
- `TuragScenes.helpers` / `H` — drawing primitives: `rect`, `line`, `poly`, `oval`, `text`, `mono`, `wrap`, `panel`, `tag`, `hero`, `dots`, `monitor`, `desk`, `bed`, `skyline`, `palm`, `check`, `shield`, `robot`, `paperStack`, `building`, `ticks`, `heading`, `val`, `progress`, `orb`, `ceilingFans`
- `TuragCharacters` — shared articulated rig (`draw`, `seated`, `icon`, `socket`, `actionNames`)
- `TuragComposer` — prop registry (`register`, `propNames`)
- `TuragScenes` — backdrop/scene draw functions (`drawStreet`, `titleOffice`, `nightCity`, `professionRooms`, `survey`, `phoneChat`, `engineGarage`, `aiWorkflow`, `shopfronts`, `taskTiles`, `doctors`, `headcount`, `riceField`, `nightDesk`, `ledger`, `newspaper`, `compare`, `garment`, `robotCost`, `robotHand`, `digitalCopies`, `government`, `queue`, `village`, `demandFunnel`, `evidenceChart`, `podium`, `ranking`, `emptyChair`, `bankATM`, `mobileMoney`, `conveyor`, `hammock`, `laptopTasks`)

---

## Drawing Helpers (`runtime.js`)

### `rect(c, x, y, w, h, col, stroke?)`
Filled rectangle with optional stroke.

### `line(c, x, y, x1, y1, col=ink, w=1)`
Straight line.

### `poly(c, pts, col, stroke?, w=1.5)`
Closed polygon from points array.

### `oval(c, x, y, rx, ry, col)`
Filled ellipse.

### `text(c, s, x, y, size=25, col=ink, align='left', max=840, font='Anek Bangla', weight=800)`
Text with auto-shrink to fit `max` width. Bengali-aware font stack.

### `mono(c, s, x, y, size=9, col=slate, align='left', max=800)`
Monospace metadata text (Space Mono).

### `wrap(c, s, x, y, max, size=24, col=ink, lineHeight=size*1.3)`
Multi-line wrapped Bengali text (Hind Siliguri). Returns row count.

### `panel(c, x, y, w, h, col=paper)`
Card with ink offset shadow.

### `tag(c, s, x, y, col=ink)`
Pill-shaped tag with monospace text.

### `hero(c, value, label, x=65, y=110, size=76)`
Large numeric evidence in ink box with red offset edge.

### `dots(c, x, y, w, h, col, spacing=7, r=1.2)`
Halftone dot grid.

### `bg(c, dark=false)`
Cached background: seeded paper texture (day) or night pattern with dots. Drawn once, cached.

### `floor(c, y=455, dark=false)`
Ground baseline stroke.

### `person(c, x, y, h, t=0, role='extra', pose='stand', variant=0, extra={})`
Draws a character via `TuragCharacters.draw`.

### `icon(c, x, y, h, col=ink)`
Tiny symbolic figure for crowds/grids.

### `orb(c, x, y, r, t)`
Animated blue orb with dots.

### `monitor(c, x, y, w=70, blue=false)`
Computer monitor with dark bezel, screen, stem, foot.

### `desk(c, x, y, s=1, t=0, col=grey, variant=0, blue=false, empty=false)`
Desk with seated person, monitor, rails.

### `bed(c, x, y, w=95)`
Simple bed frame + pillow.

### `skyline(c, y=345, col=#B8B19C, nightMode=false)`
City silhouette with optional night windows.

### `palm(c, x, y, h=170, t=0)`
Animated palm tree.

### `check(c, x, y, s=20, col=green)`
Green check mark.

### `shield(c, x, y, s=70, t=0, cracked=false)`
Shield shape, optional crack.

### `robot(c, x, y, h=140, t=0)`
Robot figure with arm and head.

### `paperStack(c, x, y, n=8, w=36)`
Stack of paper sheets.

### `building(c, x, y, w=145, h=190, label='অফিস', blue=false)`
Building with windows and door.

### `ticks(c, x, y, w, h)`
Grid tick marks for charts.

### `heading(c, b, dark=false)`
Chapter heading text.

### `progress(t, b)`
Normalized beat progress 0–1.

---

## Characters API (`characters.js`)

### `TuragCharacters.draw(ctx, opts)`

Renders an articulated faceless person.

| Option | Type | Default | Description |
|---|---|---|---|
| `x, y` | number | required | Ground anchor (feet position) |
| `h` | number | required | Total height (hair to sole) |
| `t` | number | 0 | Absolute time for motion sampling |
| `role` | string | 'extra' | 'guide' \| 'extra' \| 'doctor' \| 'vendor' |
| `pose` | string | 'stand' | stand, walk, phone, point, raise, sit, type, sew, examine, take, etc. |
| `variant` | number | 0 | Visual variant (hair, clothing) |
| `dir` | number | 1 | Facing direction (1=right, -1=left) |
| `visor` | bool\|string | false | Optional face strip color |
| `color` | string | — | Top/tunic color override |
| `legColor` | string | — | Trousers color override |
| `alpha` | number | 1 | Opacity |
| `actionTime` | number | t | Action clock for action tracks |
| `action` | string | — | Single action name |
| `actions` | array | — | Action track list `[{at, action, blend}]` |
| `phase` | number | 0 | Gait phase offset for walk |
| `look` | string | — | Gaze target |
| `bodyLean` | number | — | Body lean angle |
| `breathe` | bool | — | Breathing motion |
| `autoProps` | bool | — | Suppress default carried items |
| `rightHandFrames` / `leftHandFrames` | — | — | Hand keyframes for prop contact |

### `TuragCharacters.seated(ctx, options)`
Seated variant (thigh horizontal, shin vertical, shoe on floor).

### `TuragCharacters.icon(ctx, x, y, h, color)`
Tiny symbolic crowd figure.

### `TuragCharacters.socket(character, socketName)`
Resolves hand/torso/head/pelvis attachment point in character-local coordinates, accounting for lean, facing, scale, rotation, gait, seated posture.

### `TuragCharacters.actionNames()`
Returns list of supported action names: typing, sew, phone, explain, raise, write, carry, examine, take, point, wave, handover, push, pull, lift, place, drink, read, listen, operate.

---

## Composer API (`composer.js`)

### `TuragComposer.register(name, drawFn)`
Registers a reusable prop drawing function. `drawFn(ctx, absoluteTime, object)` draws at local origin (0,0 = ground anchor). Throws on invalid arguments.

### `TuragComposer.propNames()`
Returns array of registered prop type names.

### Shot Object Schema

```json
{
  "id": "unique-id",
  "type": "person\|desk\|chair\|...\|\|vector",
  "x": 400,
  "y": 455,
  "scale": 1,
  "rotation": 0,
  "z": 0,
  "opacity": 1,
  "enter": 0,
  "exit": undefined,
  "reveal": 0.35,
  "revealFrom": 0,
  "enterStyle": "slideLeft\|slideRight\|rise\|scale",
  "exitStyle": "slideLeft\|slideRight\|drop\|scale",
  "enterDistance": 80,
  "exitDistance": 80,
  "instant": false,
  "motion": { "kind": "walk\|float\|bob\|shake\|pendulum\|pulse\|orbit", "speed": 18, "amplitude": 4, "phase": 0, "radiusX": ..., "radiusY": ... },
  "keyframes": [ { "at": 0, "x": 100, ... }, ... ],
  "actions": [ { "at": 0, "action": "stand", "blend": 0.2 }, ... ],
  "attachTo": "person-id",
  "hand": "right\|left",
  "socket": "rightHand\|leftHand\|head\|torso\|pelvis",
  // person-specific:
  "role": "guide\|extra\|doctor\|vendor",
  "pose": "stand\|walk\|phone\|point\|raise\|sit...",
  "variant": 0,
  "dir": 1,
  "visor": false,
  "color": "...",
  "legColor": "...",
  // label-specific:
  "text": "...", "size": 32, "color": "...", "align": "center", "maxWidth": 400
}
```

### Shot Schema

```json
{
  "backdrop": "paper\|night\|city\|street\|office\|field",
  "floor": true,
  "floorY": 465,
  "camera": { "x": 480, "y": 270, "zoom": 1, "keyframes": [...] },
  "objects": [ ShotObject, ... ],
  "links": [ { "from": "id", "to": "id", "fromDy": -60, "toDy": -60, "color": "#2F3BFF", "width": 2, "dashed": true } ]
}
```

### Vector Primitive Shapes

Used inside `{ "type": "vector", "shapes": [...] }`:

| Kind | Fields |
|---|---|
| `path` | `d` (SVG path data), `fill`, `stroke`, `width`, `fillRule` |
| `rect` | `x, y, w, h`, `fill`, `stroke` |
| `ellipse` | `x, y, rx, ry`, `fill` |
| `line` | `x, y, x2, y2`, `stroke`, `width` |
| `polygon` | `points` array, `fill`, `stroke`, `width` |
| `text` | `x, y, text, size, maxWidth, align`, `fill` |

Shape options: `translateX, translateY, rotation, scale, opacity, enter, exit, keyframes`.

### Validation Rules (thrown as errors)

- Each object needs unique `id`, finite `x`/`y`, registered `type`
- Person actions must be in `actionNames()`
- Vector shapes need valid kind and path data
- Keyframes need finite unique `at`, no duplicate times
- Links must reference existing object IDs
- Attachments must target root `person`, valid hand/socket
- Exit must be after enter

---

## Custom Props (`custom-props.js`)

AI-authored props registered at load (~50 total). Key examples:

| Prop | Purpose |
|---|---|
| `custom_machine` | AI machine with active cells |
| `asset_bubble` | Expanding red bubble with label |
| `direction_arrow` | Bidirectional arrow |
| `cross_mark` | Animated red X |
| `survey_scale` | 0–100% slider with moving indicator |
| `percent_column` | Filling percentage bar |
| `chat_screen` | AI chat interface |
| `road_sign` | Green directional sign |
| `workflow_strip` | 3-stage process panel |
| `stage_curtain` | Opening/closing curtain |
| `scaffold` | Construction scaffolding |
| `task_bundle` | Splitting task blocks |
| `timebar` | Vertical time bar |
| `patient` | Medical patient icon |
| `task_matrix` | Activating task grid |
| `rice_patch` | Rice field with cut line |
| `rice_bundles` | Rice bundles |
| `combine_live` | Combine harvester |
| `editing_timeline` | Video editing timeline |
| `code_panel` | Code editor panel |
| `spotlight` | Spotlight beam |
| `ledger` | Two-column accounting ledger |
| `newspaper` | Newspaper front page |
| `four_cells` | 4-cell activation |
| `cloth_gripper` | Sewing machine cloth feed |
| `copy_network` | Copy distribution network |
| `recruitment_notice` | Hiring notice with closure |
| `demand_flow` | Demand flow diagram |
| `history_ledger` | History/accounting comparison |
| `village_hut` | Rural hut |
| `health_route` | Healthcare route lines |
| `bounded_requests` | Request grid with active subset |
| `magnifier` | Magnifying glass |
| `podium` | Speaker podium |
| `attribution_folder` | Attribution folder |
| `rank_list` | Ranked list (AI at #4) |
| `partial_picture` | Partial picture reveal |
| `late_report_wave` | Late data wave |
| `mobile_shop` | Mobile money shop |
| `speed_bump` | Speed bump |
| `audit_tasks` | Task audit with AI/human split |

Register new props in this file; they are bundled automatically by `build_episode.py`.

---

## Player API (`engine/player.js`)

### `window.seek(t)`
Seek to absolute time `t` (seconds). Renders frame deterministically.

### `window.DURATION`
Total episode duration in seconds.

### Readiness
`window.__ready === true` when fonts loaded and first frame rendered.

### Player Features
- Chapter chrome (top-left boxed number + label)
- Subtitle band (y 486–518, near-black with vermilion left edge)
- Progress rule (top, vermilion, proportional to time)
- Scene counter (lower right, mono)
- Font loading: all fonts embedded as data URLs, blocks first frame
- Remote asset blocking: all `https:` requests aborted at render
- Resize: `window.resize(width)` sets canvas output width

---

## Build Tool APIs

### `build_episode.py`
```
python3 tools/build_episode.py <episode.json> --output <out.html>
```
- Validates manifest, resolves cast, rejects `planningStatus != "authored"` for compose scenes
- Embeds fonts (base64), audio (base64), engine source into portable HTML
- Output: self-contained `episode.html`

### `render_mp4.js`
```
node tools/render_mp4.js episode.html audio.mp3 out.mp4 [--fps 30 --width 1280 --workers 1 --start 0 --duration 10 --crf 18]
```
- Launches headless Chrome, captures canvas frames as JPEG pipe
- FFmpeg encodes H.264 + AAC, validates frame count/dimensions/duration
- Output: MP4 + `.render.json` sidecar

### `qa_episode.js`
```
node tools/qa_episode.js episode.html <output-dir>
```
- Runs QA checks on built HTML, produces validation report

### `prepare_episode.py`
```
python3 tools/prepare_episode.py --script script.md --audio audio.mp3 --output episodes/new.json
```
- Creates scaffold manifest with timing cues from script/audio
- Supports Markdown and SRT input

### `director_audit.py`
```
python3 tools/director_audit.py <episode.json>
```
- Structural audit of director dossier: `directorStatus`, per-cue dossiers, review records

### `director_review.js`
- Per-cue start/middle/end review recorder
