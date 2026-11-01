# Revised scene composer and first minute

Open `engine/first-minute-revised.html` or play `output/Turag_First_Minute_Revised.mp4`. Editable storyboard: `episodes/ep02-first-minute-revised.json`. These supersede the rejected first-minute preview. The older full-episode example is not rebuilt by this revision.

This revision authors 15 separate cue compositions, adds reusable physical props, and animates articulated hands for writing, phone handling, medical reports, sewing and keyboard work. New scenes are authored by the AI reading the script; the renderer is not a text-to-video model. It does not infer arbitrary stories by itself. A capable AI with file/code/render access uses the supplied references, authors each shot, extends the shared art system and renders it. Script and audio are the user's only creative inputs.

The two source folders were inventoried, hashed and decoded: 19,115 consecutive video-2 JPEGs plus 341 stills from the other reference. All 341 latter stills were visually reviewed in sheets; video-2 visual review used chronological samples and selected scene anchors. Automated frame coverage must not be described as visual inspection of every frame. See `reference/folder_audit/` and `reference/COMPLETE_AUDIT.json`.

The newly rendered minute remains a vector reconstruction. Textures, silhouettes, staging detail and acting are not proven identical to the references. Timing uses the supplied editorial timecodes; the exact 60-second cut truncates the final longer cue. No reference video frames are used as the rendered picture.

Checks: 15 exact cue/beat matches, 75 seek/boundary checks, no repeated structural arrangements in the variety report, local fonts/assets, deterministic seeking, joint-motion measurements and sampled visual action checks. These establish technical correctness and improvements, not automatic semantic understanding or exact style equivalence.

Rebuild:

```sh
python3 tools/author_first_minute_fresh.py
python3 tools/build_episode.py episodes/ep02-first-minute-revised.json --output engine/first-minute-revised.html
node tools/qa_episode.js engine/first-minute-revised.html output/first-minute-fresh-qa
node tools/check_first_minute_actions.js
node tools/render_mp4.js engine/first-minute-revised.html audio/ep02_voiceover.mp3 output/Turag_First_Minute_Revised.mp4 --duration 60 --fps 30 --width 1280 --workers 1
```

For a new script, follow `REFERENCE_FIRST.md`, `01_MASTER_PROMPT.md` and `08_DIRECTOR_RULES.md`; do not reuse the first-minute authoring script for unrelated text.
