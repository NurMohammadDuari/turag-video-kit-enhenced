# Workflow — End-to-End Episode Production

Complete pipeline from timestamped script + narration audio to delivered MP4.

## Phase 0 — Prerequisites

**Tools required:** Python 3, Node 22.12+, Chrome/Chromium, FFmpeg/ffprobe, Pillow + NumPy (optional analysis).

```
npm ci                          # install puppeteer-core
export CHROME_PATH=/path/to/chrome   # if not at common path
```

## Phase 1 — Inspect Inputs

1. Read the timestamped script (`script/*.md` or `script/*.srt`).
2. Probe narration audio: `ffprobe -v error -show_streams -show_format -of json audio/ep02_voiceover.mp3`
3. Confirm duration, stream count, decodability.
4. Preserve all wording, names, numbers, units, uncertainty from the script.

## Phase 2 — Prepare Timing

```
python3 tools/prepare_episode.py \
  --script script/ep02.md \
  --audio audio/ep02_voiceover.mp3 \
  --output episodes/ep02-new.json
```

- Timecoded scripts retain cue boundaries.
- Untimed scripts use approximate duration allocation.
- `timing.verified = false` for estimated alignment — never label as verified.
- Audio duration controls the final timeline.

## Phase 3 — Plan the Full Episode

Author one beat per narration cue in the episode JSON:

```json
{
  "id": "b001", "t0": 0, "t1": 4,
  "scene": "compose", "cueIndex": 0, "scriptLine": "exact narration text",
  "visualIntent": "who does what, to what, what changes, what viewer understands",
  "chapter": 1, "chapterTitle": "...", "heading": "...",
  "shot": { "backdrop": "office", "objects": [...] },
  "planningStatus": "authored"
}
```

Rules:
- Every cue maps to exactly one `scene:"compose"` shot.
- Match `cueIndex` and `scriptLine` exactly.
- `visualIntent` must preserve negation, causation, uncertainty.
- Reuse environments across lines; one shot per line ≠ one location per line.
- `planningStatus: "scaffold"` builds are rejected — must be `"authored"`.

## Phase 4 — Build Assets & New Scenes

1. Reuse shared character rig (`engine/characters.js`) — no oversized heads, short legs, missing necks.
2. Add unseen props to `engine/custom-props.js` or use `type:"vector"` with `shapes`.
3. All drawing at 960×540 design coordinates.
4. No `Math.random`, no accumulating state, no wall-clock — pure `f(t, data)`.
5. Expose `window.seek(t)`, `window.DURATION` via player.

## Phase 5 — Build Portable HTML

```
python3 tools/build_episode.py episodes/ep02-new.json --output engine/episode.html
```

- Bundles local fonts, audio, complete engine into self-contained HTML.
- Rejects scaffolds (planningStatus must be "authored").
- Refuses if narration shorter than episode duration (no silent padding).

## Phase 6 — QA

```
node tools/qa_episode.js engine/episode.html output/ep02-qa
```

Checks:
- Cues ordered, in bounds, full timeline coverage
- No negative lengths, overlaps, unsupported IDs
- Bengali text shaped, readable, wrapped, inside safe areas
- Character silhouettes: slender, small head, visible neck, grounded shoes
- Literal grids: bars/percentages/data labels agree
- First/final frames, chapter boundaries — no black flashes
- Deterministic seek: seek t → seek another → seek t again matches
- Fonts load locally, no external requests

## Phase 7 — Director Review

Per cue, record start/middle/end review:

```
tools/director_review.js
```

- `review.start`, `review.middle`, `review.end` — actual frame observations
- `review.issues`, `review.fixes` — concrete findings and corrections
- `review.approved` — only after visual inspection

Set `directorStatus: "approved"` only after:
- `tools/director_audit.py` passes
- Rendered contact sheets inspected
- `06_QA.md` checklist complete

## Phase 8 — Render MP4

```
node tools/render_mp4.js engine/episode.html audio/ep02_voiceover.mp3 \
  output/ep02.mp4 --workers 1
```

Validation:
- ffmpeg exit code 0
- Frame count matches expected
- Dimensions 1280×720, fps 30
- Duration within 0.15s of expected
- Audio stream present, AAC 192k
- Output metadata written to `.render.json`

## Phase 9 — Finish & Deliver

Deliverables:
1. Final MP4 with narration
2. Editable episode JSON + timed cue/beat data
3. Portable HTML preview (functioning audio + seeking)
4. New reusable props in `engine/custom-props.js`
5. Validation summary: passed, timing confidence, unsupported claims, stylistic limits

Honesty rules:
- Do not label source footage + added audio as newly generated animation.
- Do not claim pixel-exact clone for unseen scenes.
- Mark approximate timing as `verified: false`.
- Report material limitations visibly.

## Reproducible Commands (Shipped Example)

```sh
npm run build    # python3 tools/build_episode.py episodes/ep02-composed.json --output engine/episode.html
npm run qa       # node tools/qa_episode.js engine/episode.html output/composer-qa
npm run render   # node tools/render_mp4.js engine/episode.html audio/ep02_voiceover.mp3 output/Turag_EP02_composed.mp4 --workers 1
npm run test     # full test suite
```

## Failure Modes to Avoid

| Problem | Fix |
|---|---|
| `planningStatus: "scaffold"` build rejected | Author every shot, set `"authored"` |
| Narration shorter than video | Refuse to pad; shorten video or get longer audio |
| Unknown prop type | Register in `custom-props.js` or use `vector` shapes |
| Non-finite coordinates / duplicate keyframes | Validate shot data |
| Remote asset blocked | All assets must be local/embedded |
| Black flash at chapter boundary | Inspect first/final frames, fix enter/exit |
| Bengali glyph boxes | Check fonts loaded, test চাকরি, স্বাস্থ্য, সংখ্যা |
