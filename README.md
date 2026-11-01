# Turag video kit · script-driven scene composer

Read `CHANNEL_GOAL.md` for the channel-wide production objective and reference channel. The toolkit must support fresh episodes from script and audio while preserving the supplied visual language.

The current research update is documented in `13_2026_WORKFLOW_RESEARCH.md`: persistent cast IDs, editable scene packets, curved vector artwork with animated parts, event-based QA, and subtitle/editor handoff exports.

**Start with [GIVE_THIS_TO_AI.md](GIVE_THIS_TO_AI.md).** It explains what to give an AI and includes the copy-and-paste prompt. [HOW_TO_USE.md](HOW_TO_USE.md) contains the guarded full-video commands. Direction and acting are defined in `10_AUTONOMOUS_DIRECTOR.md` and `11_ANIMATION_DIRECTOR.md`.

The current full episode is `output/Turag_Full_Episode.mp4`: 115 cues, 10:37, 1280×720 at 30 fps with complete narration. Its editable project is `episodes/ep02-full-directed.json` and its offline player is `engine/Turag_Full_Episode.html`. Read `output/Turag_Full_Episode_README.md` for the actual review scope and remaining limitations. Older examples below are retained for history, not as the current delivery.

Read `REFERENCE_FIRST.md` first. The actual supplied videos and images define the visual target. The AI invents scene content from the timestamped script and audio, and extends or corrects the renderer to match those references. Existing templates, style-token guesses and the example reconstruction must not limit new scenes or preserve visual mismatches.

Give the complete folder or ZIP to an AI that can read images, edit files and run Python, Node, Chrome and FFmpeg. Supply just **your timestamped script and narration audio**. Say:

> Read 01_MASTER_PROMPT.md and 07_SCENE_COMPOSER.md. Analyze my timestamped script and audio. Compose a fresh shot for every line, create any missing props in the shared style, check consistency, and deliver the complete MP4 plus editable project. Make routine creative decisions yourself.

The AI is the scene planner. You do not supply scene descriptions, object lists or layout instructions. The kit provides the drawing system, reference evidence, characters, props, compositor and exporter. It does not contain a language model or call an AI service on its own. A text-only AI without code execution cannot render a video.

## Contents

- `01_MASTER_PROMPT.md`: complete autonomous AI handoff.
- `02_STYLE_CARD.md`, `04_CHARACTER_SPEC.md`: consistent drawing and character rules.
- `07_SCENE_COMPOSER.md`: per-line composition format, prop API, unseen-object workflow.
- `11_ANIMATION_DIRECTOR.md`: acting, hand contact, weight, gait, secondary motion and five-phase inspection.
- `engine/animation-lab.html`: interactive action/sequence inspection, mirrored cast, seated and standing figures, wrist markers and a held prop.
- `05_NEW_SCENES.md`, `03_SCENE_LIBRARY.md`: visual reasoning and reference scene examples.
- `engine/composer.js`: draws arbitrary object arrangements, not a fixed-template selector.
- `engine/custom-props.js`: new reusable objects drawn for the example script.
- `engine/characters.js`, `runtime.js`: shared rig, material and drawing helpers. Legacy full-scene handlers are examples, not the primary pipeline.
- `episodes/ep02-composed.json`: 115 timestamped lines and 115 composed shots.
- `engine/episode.html`: portable preview with embedded narration, fonts and engine.
- `reference/analysis/index.html`: every-frame source atlas. 19,115 decoded frames, CSV measurements, full-resolution frame hashes, 192 atlas sheets and corrected PTS overview sheets.
- `output/Turag_EP02_composed.mp4`: rendered composition example, when render completes.
- `output/Turag_EP02_reference_with_audio.mp4`: supplied original picture with supplied narration added; original decoded picture verified identical. This is a reference mux.

The legacy 41-second and stage-zero HTML files are historical material. Use the composer and current master prompt for new work. Old small contact-sheet labels have timing offsets; use `reference/analysis/` for actual source PTS.

## Build and render

Requirements: Python 3, FFmpeg/ffprobe, Node 22.12+, Chrome/Chromium. Install Node dependencies using `npm ci`. Set `CHROME_PATH` if Chrome is not at a common installation path. Pillow and NumPy are used by the optional source analysis tool; normal composition/build/render requires neither.

```sh
python3 tools/prepare_episode.py --script script/new.md --audio audio/new.mp3 --output episodes/new.json
# The AI now authors/refines every shot from the script and adds missing props.
python3 tools/build_episode.py episodes/new.json --output engine/new.html
node tools/qa_episode.js engine/new.html output/new-qa
node tools/render_mp4.js engine/new.html audio/new.mp3 output/new.mp4 --workers 1
```

`prepare_episode.py` makes an editable scaffold. Its initial noun matching is a convenience and does not understand arbitrary scripts. The AI must analyze the script and replace inappropriate suggestions before rendering. Timestamped Markdown and SRT are supported. Supplied timestamps are retained; untimed timing is explicitly estimated. Silence detection does not align words.

For the shipped example:

```sh
npm run build
npm run qa
npm run render
```

## What is consistent and what is approximate

Every shot uses the same palette, paper/night material, fonts, subtitle chrome and articulated character rig. New props use the same vocabulary and are bundled into the portable player. One line owns one shot; environments may continue while their action changes.

The code-rendered example is a reconstruction. Its composition, motion and characters differ from original pixels, and the supplied transcript timings have not been independently forced-aligned. No kit can prove a pixel-identical match for a new scene that has no corresponding reference frame. Use the source atlas and visual QA to judge resemblance. See `06_QA.md` and actual reports under `output/`.

## Expanded image-folder evidence

Read `09_REFERENCE_KNOWLEDGE.md` for the mechanisms observed across both supplied image folders and `08_DIRECTOR_RULES.md` for autonomous scene decisions. All 341 stills from the second folder are bundled full-size, alongside contact sheets, file hashes and measurements. The large video-image folder is represented by its audit, overview sheets, existing source video and every-frame atlas. `style-lock.json` fixes the shared aesthetic and cast identity. Object and camera keyframes allow script-specific actions and framing.

The importer now marks plans `planningStatus:"scaffold"`; the AI must author/refine the shots and mark them `authored` before building. This prevents initial noun suggestions from being delivered as a finished storyboard.

The complete video-1 source is now included under `reference/video1/original/`, with a full 10,243-frame audit and atlas. Together the two source videos contain 29,358 decoded frames. Open `reference/index.html` for the consolidated library. `reference/COMPLETE_AUDIT.json` records the counts and evidence levels.
