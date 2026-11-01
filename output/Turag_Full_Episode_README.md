# Full episode delivery

This episode uses the supplied Bengali narration and all 115 supplied script cues, covering 637.257143 seconds. The MP4 rounds to 19,118 frames at 30 fps (637.266667 seconds), with 1280 × 720 picture and AAC narration. All illustrations are rendered by the local engine; this is not the source video with replacement audio.

## Files

- `output/Turag_Full_Episode.mp4`: complete video after the guarded finish workflow succeeds.
- `engine/Turag_Full_Episode.html`: portable offline player with embedded fonts and narration.
- `episodes/ep02-full-directed.json`: editable scene manifest and director dossier.
- `output/Turag_Full_Episode-handoff/`: SRT subtitles, scene CSV, chapter metadata and timing provenance.
- `output/Turag_Full_Episode-director-review/index.html`: start, action peak and end of every shot, plus selected supplied reference images.
- `output/Turag_Full_Episode-animation-review/index.html`: five-phase animation samples and motion measurements.
- `output/Turag_Full_Episode-visual-observations.txt`: specific observations for every shot, including the corrected failures.
- `output/Turag_Full_Episode-review-receipt.json`: inspection record bound to the exact HTML by SHA-256.

## Review and limits

All 115 shots were visually inspected at start, action peak and end. Repairs include background/window occlusion, surplus default carried props, farm crop bundles, writing-hand placement, night furniture contrast, count labels and recruitment-notice placement. The seven chapters use the office opening plus six blue chapter resets. Two structural repetitions are intentional: returning to the never-hired editor and comparing the same workforce before/after arithmetic.

The engine is a reference-informed reconstruction. It does not reproduce every fine silhouette, detail density or motion of the original footage. The supplied editorial timecodes are approximate and have not been forced-aligned to individual spoken words. Script claims were retained, not independently fact-checked. The end card identifies the supplied script as provenance rather than inventing missing citations. The one-second transcript gap at 630–631 seconds holds the existing conversation, and the closing card covers the complete audio tail.

Automated checks cover deterministic seeking, local fonts/assets, blank-frame detection, subtitle width and authored event boundaries. Five-phase motion warnings were inspected alongside the three-frame boards; quiet evidence and listening shots retain restrained motion. This is not a claim of manually inspecting all 19,118 encoded frames.

## Rebuild or edit

Open the HTML directly to play or seek. Edit the JSON to revise individual shots. The operating AI should read the project instructions, preserve exact script coverage, create missing art, inspect the changed shots and record a fresh review.

```sh
python3 tools/build_episode.py episodes/ep02-full-directed.json --output engine/Turag_Full_Episode.html
python3 tools/director_audit.py episodes/ep02-full-directed.json
python3 tools/finish_episode.py episodes/ep02-full-directed.json --name Turag_Full_Episode --check-only
# After inspecting the rebuilt boards, author concrete review notes and bind them:
python3 tools/review_receipt.py engine/Turag_Full_Episode.html output/Turag_Full_Episode-review-notes.json --output output/Turag_Full_Episode-review-receipt.json
python3 tools/finish_episode.py episodes/ep02-full-directed.json --name Turag_Full_Episode --review-receipt output/Turag_Full_Episode-review-receipt.json --workers 2
```

Do not reuse old review notes for changed pictures. `tools/author_full_episode.py` is the episode-specific authoring source; running it recreates the draft and deliberately resets review approval. The final editable JSON retains the completed review.
