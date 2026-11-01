# Manifest Schema — Episode JSON Contract

The episode manifest is the editable source of truth. It drives `build_episode.py` → portable HTML → MP4 render. Located in `episodes/*.json`. Version 2.

## Top-Level Structure

```json
{
  "version": 2,
  "id": "ep03",
  "title": "Episode title",
  "duration": 90,
  "fps": 30,
  "width": 1280,
  "height": 720,
  "audio": "audio/current.mp3",
  "script": "script/current.md",
  "planningStatus": "authored",
  "directorStatus": "approved",
  "cast": { "host": { "role": "guide", "variant": 0, ... } },
  "continuity": { ... },
  "timing": { "method": "...", "verified": false, "note": "..." },
  "cues": [ { "t0": 0, "t1": 4, "text": "..." } ],
  "beats": [ { ... } ]
}
```

### Top-Level Fields

| Field | Type | Required | Description |
|---|---|---|---|
| `version` | integer | yes | Manifest version (2) |
| `id` | string | yes | Episode identifier (e.g. "ep03") |
| `title` | string | yes | Human-readable title |
| `duration` | number | yes | Total duration in seconds (audio-driven) |
| `fps` | integer | yes | Frame rate (30) |
| `width` | integer | yes | Output width (1280) |
| `height` | integer | yes | Output height (720) |
| `audio` | string | yes | Relative path to narration MP3 |
| `script` | string | yes | Relative path to source script |
| `planningStatus` | string | yes | `"scaffold"` (draft) or `"authored"` (AI-reviewed) |
| `directorStatus` | string | yes | `"approved"` only after audit + review pass |
| `cast` | object | no | Episode-level cast identity map |
| `continuity` | object | no | Cross-shot continuity notes |
| `timing` | object | yes | Timing method + verification status |
| `cues` | array | yes | Ordered narration cues |
| `beats` | array | yes | One beat per cue |

### `timing` Object

```json
{
  "method": "user_supplied_timecodes",
  "verified": false,
  "note": "Timecodes are supplied editorial cues, not independently forced-aligned to speech."
}
```

- `method`: source of timing ("user_supplied_timecodes", "estimated", "forced_aligned")
- `verified`: boolean — true only after listening/alignment review
- `note`: human explanation of timing provenance

## Cues Array

One entry per narration line, ordered, non-overlapping, inside duration.

```json
{
  "t0": 0.0,
  "t1": 4.0,
  "text": "(টাইটেল কার্ড): আপনার চাকরি কি আসলেই সেফ?"
}
```

| Field | Type | Description |
|---|---|---|
| `t0` | number | Start time (seconds) |
| `t1` | number | End time (seconds) |
| `text` | string | Exact narration text (Bengali) |

## Beats Array

One beat per cue. `cueIndex` and `scriptLine` must match the cue exactly.

```json
{
  "id": "b001",
  "t0": 0,
  "t1": 4,
  "scene": "compose",
  "cueIndex": 0,
  "scriptLine": "exact narration excerpt",
  "visualIntent": "who does what, to what, what changes, what viewer understands",
  "chapter": 1,
  "chapterTitle": "short label",
  "heading": "on-screen summary",
  "label": "optional metadata",
  "value": "",
  "values": [],
  "items": [],
  "mode": "",
  "shot": { ... },
  "planningStatus": "authored",
  "continuity": { ... },
  "styleRefs": [ "reference/folder_audit/frames/fullsize/f_0001.jpg" ],
  "referenceUse": "what evidence this shot borrows",
  "animationPlan": { ... },
  "designDecision": { ... },
  "semanticAnalysis": { ... },
  "review": { "start": ..., "middle": ..., "end": ..., "approved": false },
  "copyLedger": [ ... ],
  "factBasis": { ... }
}
```

### Beat Fields

| Field | Type | Required | Description |
|---|---|---|---|
| `id` | string | yes | Unique beat ID |
| `t0, t1` | number | yes | Start/end time (seconds) |
| `scene` | string | yes | `"compose"` |
| `cueIndex` | integer | yes | Index into cues array |
| `scriptLine` | string | yes | Exact narration text |
| `visualIntent` | string | yes | Semantic description of the image |
| `chapter` | integer | no | Chapter number |
| `chapterTitle` | string | no | Chapter label |
| `heading` | string | no | Designed on-screen summary (not full subtitle) |
| `shot` | object | yes | Scene graph (backdrop, objects, camera, links) |
| `planningStatus` | string | yes | `"scaffold"` or `"authored"` |
| `styleRefs` | array | no | Reference image paths |
| `referenceUse` | string | no | What evidence is borrowed |
| `animationPlan` | object | no | 5-phase acting plan |
| `designDecision` | object | no | Chosen visual approach + rationale |
| `semanticAnalysis` | object | no | Actors, action, facts, negation, tone |
| `continuity` | object | no | Cast/place/props continuity |
| `review` | object | no | start/middle/end inspection record |
| `copyLedger` | array | no | Every on-screen phrase accounted |
| `factBasis` | object | no | Data-like number basis: script/derived/editorial/decorative |

## Shot Object

```json
{
  "backdrop": "office",
  "floor": true,
  "floorY": 455,
  "camera": { "x": 480, "y": 270, "zoom": 1, "keyframes": [...] },
  "objects": [ ... ],
  "links": [ ... ]
}
```

| Field | Type | Default | Description |
|---|---|---|---|
| `backdrop` | string | "paper" | paper, night, city, street, office, field |
| `floor` | boolean | true | Draw ground baseline |
| `floorY` | number | 465 | Floor baseline Y |
| `camera` | object | {x:480,y:270,zoom:1} | Camera position + zoom (+keyframes) |
| `objects` | array | required | Shot object list |
| `links` | array | [] | Connector lines between objects |

### Shot Object Fields

| Field | Type | Description |
|---|---|---|
| `id` | string | Unique within shot |
| `type` | string | Registered prop type |
| `x, y` | number | Anchor coordinates (finite) |
| `scale` | number | Scale factor (>=0, default 1) |
| `rotation` | number | Degrees (default 0) |
| `z` | number | Painter order (default 0) |
| `opacity` | number | 0–1 (default 1) |
| `enter` | number | Seconds relative to beat start (default 0) |
| `exit` | number | Seconds when object leaves |
| `reveal` | number | Reveal duration (default 0.35) |
| `revealFrom` | number | Vertical reveal offset |
| `enterStyle` | string | slideLeft, slideRight, rise, scale |
| `exitStyle` | string | slideLeft, slideRight, drop, scale |
| `enterDistance` | number | Entrance travel distance |
| `exitDistance` | number | Exit travel distance |
| `instant` | boolean | Render fully at entry (no fade) |
| `motion` | object | {kind, speed, amplitude, phase, ...} |
| `keyframes` | array | [{at, prop, ...}, ...] |
| `actions` | array | Person action tracks [{at, action, blend}] |
| `attachTo` | string | Parent person ID for held props |
| `hand` | string | "right" or "left" |
| `socket` | string | rightHand, leftHand, head, torso, pelvis |
| `role` | string | guide, extra, doctor, vendor |
| `pose` | string | stand, walk, phone, point, raise, sit, ... |
| `variant` | number | Visual variant (default 0) |
| `dir` | number | Facing (1=right, -1=left) |
| `visor` | bool\|string | Face strip |
| `color` | string | Top color override |
| `legColor` | string | Trousers color override |
| `text` | string | Label/card text |
| `size` | number | Text size |
| `color` (label) | string | Text color |

### Motion Kinds

| Kind | Description | Options |
|---|---|---|
| `walk` | Horizontal walking | `speed`, `offset` |
| `float` | Vertical sine bobbing | `speed`, `amplitude` |
| `bob` | Same as float | — |
| `shake` | Horizontal+vertical shake | `speed`, `amplitude` |
| `pendulum` | Rotational swing | `speed`, `amplitude` |
| `pulse` | Scale pulsing | `speed`, `amplitude` |
| `orbit` | Elliptical orbit | `speed`, `radiusX`, `radiusY` |

## Camera Keyframes

```json
{
  "x": 480, "y": 270, "zoom": 1,
  "keyframes": [
    { "at": 0, "x": 480, "y": 270, "zoom": 1 },
    { "at": 2, "x": 600, "y": 330, "zoom": 1.35 }
  ]
}
```

Camera changes the illustrated world; chapter chrome and subtitles remain fixed outside world transforms.

## Links

```json
{
  "from": "object-id",
  "to": "other-id",
  "fromDy": -60,
  "toDy": -60,
  "color": "#2F3BFF",
  "width": 2,
  "dashed": true
}
```

Links draw behind objects. Only connect objects with meaningful relationships.

## Vector Objects

```json
{
  "id": "vec-1",
  "type": "vector",
  "x": 400, "y": 455,
  "shapes": [
    { "kind": "path", "d": "M0 0 L50 50", "fill": "#216E50", "stroke": "#12141C" }
  ],
  "keyframes": [ { "at": 0, "scale": 0 }, { "at": 1, "scale": 1 } ]
}
```

## Validation Rules (enforced by build_episode.py + composer.js)

1. `planningStatus` must be `"authored"` if any beat has `scene: "compose"` — scaffolds rejected.
2. Cues ordered, `t0 < t1`, inside duration, no overlaps.
3. Every beat `cueIndex` matches its cue position; `scriptLine` matches cue text exactly.
4. Every object: unique `id`, finite `x`/`y`, registered `type`.
5. Person actions must be in `TuragCharacters.actionNames()`.
6. Keyframes: finite unique `at`, no duplicates, numeric values finite.
7. Links reference existing object IDs.
8. Attachments target root `person`, valid `hand`/`socket`.
9. `exit` must be after `enter`.
10. Audio duration must be >= episode duration (no silent padding).

## Cast Map (Episode Level)

```json
{
  "cast": {
    "host": {
      "role": "guide",
      "variant": 0,
      "top": "#FF3D17",
      "trousers": "#272A3A",
      "identityMustPersist": true
    }
  }
}
```

A person with `castId: "host"` inherits these fields. Shot identity (stage position, height, action, facing, camera) remains scene-specific. Recurring extras keep identity; do not change guide hair/clothing between lines.

## Example Beat

```json
{
  "id": "line-001",
  "t0": 0,
  "t1": 6,
  "scene": "compose",
  "cueIndex": 0,
  "scriptLine": "নিয়োগ না হলে চেয়ারটা খালিই থাকে।",
  "visualIntent": "নিয়োগ না হলে: an empty chair beside an unattended desk; a worker leaves the frame.",
  "chapter": 1,
  "chapterTitle": "চাকরি",
  "heading": "নিয়োগ বন্ধ",
  "shot": {
    "backdrop": "office",
    "objects": [
      { "id": "vacancy", "type": "chair", "x": 520, "y": 455 },
      { "id": "workstation", "type": "desk", "x": 640, "y": 455 },
      { "id": "departing", "type": "person", "x": 240, "y": 455, "role": "extra", "pose": "walk", "variant": 2, "motion": { "kind": "walk", "speed": -30 } },
      { "id": "notice", "type": "label", "x": 620, "y": 210, "text": "নিয়োগ বন্ধ", "size": 35, "enter": 0.4 }
    ],
    "links": []
  },
  "planningStatus": "authored"
}
```
