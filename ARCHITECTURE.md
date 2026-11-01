# Architecture — Turag Video Kit

Offline Bengali canvas explainer toolkit and reference evidence. A script-driven scene composer that renders deterministic, seekable MP4 videos from a timestamped script and narration audio using a shared canvas engine, custom props, and a portable HTML player.

## System Purpose

The kit lets an AI director compose one shot per narration line from a timestamped script, draw it with a shared flat-illustration grammar, and render a complete MP4 with embedded audio and local fonts — no external model API, no CDN assets, no network calls during render.

## Directory Layout

```
turag-video-kit/
├── README.md                    # Working commands, deliverables, honesty policy
├── AGENTS.md                    # AI operating instructions (read first)
├── style-lock.json              # Enforceable aesthetic limits + palette
├── 01_MASTER_PROMPT.md          # Complete autonomous AI handoff contract
├── 02_STYLE_CARD.md             # Visual grammar, palette, typography, composition
├── 03_SCENE_LIBRARY.md          # Visual reasoning + reference scene examples
├── 04_CHARACTER_SPEC.md         # Character rig proportions, poses, cast variants
├── 05_NEW_SCENES.md             # How to author unseen scenes
├── 06_QA.md                     # Validation checklist + evidence levels
├── 07_SCENE_COMPOSER.md         # Per-line composition format + prop API
├── 08_DIRECTOR_RULES.md         # Autonomous scene decision rules
├── 09_REFERENCE_KNOWLEDGE.md    # Evidence mechanisms from supplied frames
├── 10_AUTONOMOUS_DIRECTOR.md    # Director loop: design, analysis, decision, review
├── 11_ANIMATION_DIRECTOR.md     # 5-phase acting plan + action profiles
├── CHANNEL_GOAL.md              # Channel-wide production objective
├── GIVE_THIS_TO_AI.md           # Copy-paste prompt for new AI operators
├── HOW_TO_USE.md                # Guarded full-video commands
├── REFERENCE_FIRST.md           # Reference evidence precedence note
├── REVISION_*.md                # Revision history
├── START_HERE.txt               # Entry point
├── package.json                 # Node project (puppeteer-core dependency)
├── engine/                      # Deterministic canvas renderer (all JS)
│   ├── runtime.js               # Drawing helpers (bg, floor, person, props, backdrops)
│   ├── characters.js            # Shared articulated character rig
│   ├── composer.js              # Scene graph composer, prop registry, validation
│   ├── custom-props.js          # AI-authored reusable vector props
│   ├── player.js                # Portable HTML player (seek, chapters, subtitles)
│   ├── player-template.html     # Build-time HTML template
│   ├── episode.html             # Shipped portable preview
│   └── ...                      # Historical V0–V11 HTML examples
├── tools/                       # Python + Node build/QA/render tooling
│   ├── build_episode.py         # Bundles engine + fonts + audio into offline HTML
│   ├── render_mp4.js            # Puppeteer + ffmpeg deterministic MP4 renderer
│   ├── qa_episode.js            # QA runner for built HTML
│   ├── prepare_episode.py       # Creates episode manifest scaffold from script+audio
│   ├── director_audit.py        # Director dossier structural audit
│   ├── director_review.js       # Per-cue start/middle/end review recorder
│   ├── author_*.py              # Episode authoring helpers
│   ├── package_*.py             # Delivery packaging scripts
│   └── ...                      # QA, review, audit, export tools
├── episodes/                    # Editable episode JSON manifests
├── audio/                       # Narration MP3 sources
├── script/                      # Source scripts (Markdown + SRT)
├── assets/fonts/                # Bundled local Bengali/Latin fonts
├── output/                      # Rendered MP4s, QA reports, director reviews
├── tests/                       # Python unittest + Node regression tests
├── reference/                   # Supplied source evidence (videos, images, audits)
│   ├── analysis/                # Every-frame metrics, scene atlas, index
│   ├── folder_audit/            # 341 supplied stills inventory + full-size copies
│   ├── video1/original/video.mp4# Large source video (Git LFS tracked)
│   ├── video2/                  # Second source episode frames
│   ├── characters/              # Character reference crops
│   └── index.html               # Consolidated reference library
```

## Core Engine Architecture

### Runtime (`engine/runtime.js`)

Pure drawing functions operating on a 2D canvas context at design resolution **960×540**, uniformly scaled to output (1280×720). Key primitives:

- `bg(c, dark)` — cached seeded paper texture (day) or night pattern
- `floor(c, y, dark)` — ground baseline
- `person(c, x, y, h, t, role, pose, variant, extra)` — articulated character via `TuragCharacters.draw`
- Backdrop drawers: `drawStreet`, `titleOffice`, `nightCity`, `professionRooms`, `survey`, `phoneChat`, `engineGarage`, `aiWorkflow`, `shopfronts`, `taskTiles`, `doctors`, `headcount`, `riceField`, `nightDesk`, `skylineWindow`, `ledger`, `newspaper`, `compare`, `ceilingFans`, `garment`, `robotCost`, `robotHand`, `digitalCopies`, `government`, `queue`, `village`, `demandFunnel`, `evidenceChart`, `podium`, `ranking`, `emptyChair`, `bankATM`, `mobileMoney`, `conveyor`, `hammock`, `laptopTasks`
- All drawing is a pure function of absolute time `t` and stable data — no `Math.random`, no accumulating state, no wall-clock dependence.

### Characters (`engine/characters.js`)

Shared articulated rig. `TuragCharacters.draw(ctx, opts)` renders a faceless slender person with jointed limbs, small head, visible neck, long torso, grounded shoes. Supported options: `x, y, h, role, pose, t, variant, dir, visor, color, legColor, alpha, actionTime, action, actions, phase, look, bodyLean, breathe, autoProps, rightHandFrames, leftHandFrames`. Poses: stand, walk, phone, point, raise, sit, type, sew, examine, take, etc. `TuragCharacters.icon` draws tiny symbolic crowd marks. `TuragCharacters.socket` resolves hand attachment points for held props.

### Composer (`engine/composer.js`)

Registers prop drawing functions via `TuragComposer.register(name, drawFn)`. Validates shot objects (unique IDs, finite coordinates, known prop types, valid keyframes, valid action tracks, attachment sockets). Resolves object local time, enter/exit fades, motion (walk, float, bob, shake, pendulum, pulse, orbit), entrance/exit styles, camera interpolation, and hand socket attachment. Draw order: backdrop → camera transform → objects → chrome/subtitles (by player).

### Custom Props (`engine/custom-props.js`)

AI-authored reusable vector prop drawing functions registered at module load (~50 props including `custom_machine`, `asset_bubble`, `survey_scale`, `percent_column`, `chat_screen`, `workflow_strip`, `ledger`, `newspaper`, `combine_live`, `recruitment_notice`, `rank_list`, `mobile_shop`, `speed_bump`, `audit_tasks`, `magnifier`, `spotlight`, etc.).

### Player (`engine/player.js`)

Portable HTML player exposing `window.seek(t)`, `window.DURATION`, readiness state. Handles chapter chrome, subtitle bands, progress rule, scene counter, font loading, and deterministic seeking. All fonts embedded as data URLs at build time.

## Build Pipeline

```
script + audio
    │
    ▼
prepare_episode.py          → scaffold episode JSON (timing, cues)
    │
    ▼  (AI authors/refines every shot; sets planningStatus="authored")
episodes/*.json
    │
    ▼
build_episode.py            → engine/episode.html (fonts+audio+engine embedded)
    │
    ▼
qa_episode.js               → validation report
    │
    ▼
render_mp4.js               → output/*.mp4 (puppeteer captures canvas frames,
                               ffmpeg encodes H.264 + AAC)
    │
    ▼
director_audit.py /         → structural + QA sign-off
director_review.js
    │
    ▼
Deliverables: MP4, editable JSON, portable HTML, QA report
```

### Determinism Guarantees

- Every frame is `f(t, data)` — pure function of absolute time.
- Seeking backward/forward reproduces identical frames.
- No `Math.random`, `Date.now()`, frame-count accumulation, or physics integration.
- Fonts bundled locally; remote asset requests blocked at render time.

## Output Contract

- Resolution: 1280×720 (design 960×540, uniform 4:3 scale)
- FPS: 30 (configurable)
- Codec: H.264 video + AAC audio
- Embedded: narration audio, local fonts, complete engine source
- Metadata comment marks output as "code-rendered reconstruction, not original reference pixels"

## Tests

- `tests/test_episode.py` — Python manifest validation
- `tests/test_cast_registry.py` — Cast identity resolution
- `tests/test_director_audit.py` — Director dossier structure
- `tests/test_export_handoff.py` — Delivery export
- `tests/test_pipeline_regressions.py` — End-to-end pipeline
- `tests/test_review_receipt.py` — Review receipt validation
- `tests/test_scene_workspace.py` — Scene workspace
- `tools/test_scene_engine.js` — Node engine regression
- `tools/test_vector_browser.js` — Vector primitive browser test

Run with `npm test`.
