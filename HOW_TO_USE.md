# Make a complete video from your script and audio

**Start with `GIVE_THIS_TO_AI.md` for the handoff steps and ready-to-paste prompt.**

## The workflow you asked for

1. Unzip the complete toolkit folder.
2. Give that folder to an AI that can inspect images, edit files and execute code. Open the folder as its workspace.
3. Give it your timestamped script and matching narration audio.
4. Paste this instruction:

> Read REFERENCE_FIRST.md, 01_MASTER_PROMPT.md, 07_SCENE_COMPOSER.md, 08_DIRECTOR_RULES.md, 10_AUTONOMOUS_DIRECTOR.md, 11_ANIMATION_DIRECTOR.md and HOW_TO_USE.md. Use my script and audio to create the complete video. Act as both director and animator: understand the whole argument, create the episode design and cue dossiers, invent a fresh meaningful scene for every cue, preserve the supplied reference style and continuity, stage readable anticipation/contact/follow-through/settling, keep hands attached to props, show weight and gaze, animate relevant objects and secondary motion, add missing artwork, inspect every shot at five motion phases, critique weak results and revise them. Do not recycle the example's layouts or ask me to design scenes. Run tools/director_audit.py, then use tools/finish_episode.py for the complete MP4, offline HTML and editable manifest, with no --duration limit.

The AI does the creative work. This folder is a local drawing/rendering toolkit, not a self-running language model. A chat-only AI without file access and execution cannot produce the MP4. You do not need to choose templates or write scene JSON yourself.

## Input format

Use UTF-8 Markdown with explicit time ranges, or SRT. Example:

```text
[00:00–00:04] Your first narration line.
[00:04–00:09] Your next narration line.
[00:09–00:14] The next idea and action.
```

Continue through the complete narration. A script that ends more than three seconds before the audio requires the missing cues or an AI-authored `tailHoldReason` for a verified silent/outro hold. Use the actual timing of your audio. Multiline narration after a Markdown cue belongs to that cue. An untimed script receives estimated timing, which must be reviewed. The kit does not contain forced speech alignment. A malformed timestamp must be corrected, not silently treated as untimed prose.

## Commands for the AI or a technical operator

Requirements: Python 3, Node 22.12+, Chrome/Chromium and FFmpeg/ffprobe. From the toolkit directory, run `npm ci` once. Set `CHROME_PATH` only if Chrome is outside the supported installation paths.

```sh
python3 tools/prepare_episode.py --script /path/to/script.md --audio /path/to/narration.mp3 --output episodes/my-video.json
python3 tools/create_director_packet.py episodes/my-video.json
```

The importer copies external input files into the toolkit and creates a scaffold. The packet command creates a cue-by-cue directing brief. **The AI must now complete the episode design and every cue dossier, author every shot, inspect references, add missing props/actions and review rendered start/middle/end states.** Mark `planningStatus:"authored"` and `directorStatus:"approved"` only after that work and a passing director audit. Initial keyword suggestions are not finished scene decisions.

Before approval, build the HTML and generate the directing board and five-phase animation board:

```sh
python3 tools/build_episode.py episodes/my-video.json --output engine/my-video.html
node tools/director_review.js engine/my-video.html output/my-video-director-review
node tools/animation_review.js engine/my-video.html output/my-video-animation-review
```

Open `output/my-video-director-review/index.html`. The AI must compare every start/peak/end triplet with its selected references, repair the shot, regenerate the board, and only then approve its review records.

First build and check the complete authored project without encoding:

```sh
python3 tools/finish_episode.py episodes/my-video.json --check-only
```

Final export now requires a review receipt. First run `finish_episode.py` with `--check-only`, inspect both boards, and write JSON notes with a `shots` array. Each record needs its beat `id`, concrete `meaning`, `style`, `motion`, `contact`, and `timing` observations, `unresolved:[]`, and `approved:true` only after repair. Run `python3 tools/review_receipt.py engine/my-video.html notes.json --output output/my-video-review-receipt.json`, then rerun the finish command with `--review-receipt output/my-video-review-receipt.json`. Any change to the player, artwork, audio or manifest invalidates that approval. The receipt records the AI's judgment; it cannot prove aesthetic quality automatically.

```sh
python3 tools/review_receipt.py engine/my-video.html notes.json --output output/my-video-review-receipt.json
python3 tools/finish_episode.py episodes/my-video.json --review-receipt output/my-video-review-receipt.json --workers 2
```

This renders the ENTIRE timeline with narration and checks full video decoding. Use `--workers 1` on a machine with limited memory; the result is the same.

Outputs:

- `output/my-video.mp4` — full video with narration.
- `engine/my-video.html` — offline portable player with audio/fonts embedded.
- `episodes/my-video.json` — editable shots and timestamps.
- `output/my-video-qa/` — screenshots and technical check report.
- `output/my-video-director-report.json` — dossier, repetition and design-gate report.
- `output/my-video-director-review/index.html` — start/action-peak/end review board for every cue.
- `output/my-video-animation-review/index.html` — start/anticipation/peak/settle/end acting board with motion diagnostics.
- `output/my-video.mp4.render.json` — encoding details.

To check before the full render:

```sh
python3 tools/finish_episode.py episodes/my-video.json --check-only
npm test
```

`--check-only` does not render an MP4. Do not deliver a check-only result as a finished video. The normal command has no 60-second limit. The renderer refuses to cover missing narration with silent padding.

## Working on a long episode scene by scene

The AI can split an authored or draft manifest into smaller repair packets:

```sh
python3 tools/scene_workspace.py split episodes/my-video.json output/my-video-scenes
# AI edits each numbered packet's beat and repairNotes.
python3 tools/scene_workspace.py merge episodes/my-video.json output/my-video-scenes --output episodes/my-video-revised.json
```

Each packet retains neighboring script context. Merge protects narration text, cue timing and IDs, detects stale source edits and marks changed scenes unapproved. Rebuild and inspect them before completing the review receipt. No user scene descriptions are needed.

The finish workflow also produces a `-handoff` directory with `captions.srt`, `timeline.csv`, `chapters.json` and `timing-provenance.json`. These are derived from the exact authored manifest, not a new transcription.

Read `13_2026_WORKFLOW_RESEARCH.md` for the current workflow comparison and implemented changes.

## Current examples and limits

`episodes/ep02-full-directed.json` is the current 115-cue full-episode project with individually authored scenes, reviewed repairs and full narration coverage. Its player is `engine/Turag_Full_Episode.html`; the guarded export produces `output/Turag_Full_Episode.mp4`. See `output/Turag_Full_Episode_README.md` for its review scope and limitations. `ep02-composed.json` is the older compatibility example; do not use its repeated layouts as a creative template. The episode-specific `tools/author_full_episode.py` is not a general script-to-video model.

Technical tests cannot certify semantic correctness, exact visual equivalence or perfect lip/word timing. The AI must still visually compare new shots against the bundled references and check narration timing. The style target is the reference; an unseen shot has no identical reference frame to prove pixel equality against.
