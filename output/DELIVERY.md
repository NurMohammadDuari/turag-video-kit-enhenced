# Toolkit changes and validation

The primary engine is now a script-driven object composer. The AI authors one scene graph per timestamped line, reusing the same characters, paper/night material, typography, palette and chrome. New nouns can be drawn as reusable props or declarative vectors. The user only needs to supply the timestamped script and narration audio to a capable AI.

The example has 115 cues and 115 composed shots. `episodes/ep02-composed.json` records the exact line, cue index, intent and objects. `engine/custom-props.js` includes episode-specific engine, car, harvester, chalkboard, task, clock, hammock, sewing machine, envelope and chart props. The guide's hair variant is fixed across scenes.

Source evidence: all 19,115 original frames were decoded and fingerprinted. The all-frame atlas has 192 sheets. Eleven chronological overview sheets at two-second intervals were visually reviewed; this is sampled visual review, not a claim of manual full-resolution examination of all 19,115 frames. Old overview labels were offset; corrected PTS data is under `reference/analysis/`.

Validation completed before full encoding: 577 boundary/midpoint checks, no blank scenes, no browser errors, no nondeterministic backward seeks, no network requests, four bundled font faces loaded. All 115 shot midpoint images were inspected in six contact sheets. Maximum measured subtitle width was 808.19 design pixels. One peak draw took 77.3 ms while rendering concurrently; this is an offline renderer, and no real-time performance guarantee is made.

The extension test draws a lighthouse absent from the reference using vector primitives without a new scene template. It verifies deterministic seeking and rejects unknown props. See `composer-proof.json` and `unseen-prop-proof.png`.

The source-picture-with-audio output was checked against every original decoded frame hash: all 19,115 are identical. That output preserves the original picture and adds narration; it is not generated animation.

The composed output is an approximate reconstruction, with different composition density, prop detail, motion and character geometry from the original. Supplied script timing is retained but not independently forced-aligned; factual claims are user-provided. Some adjacent lines deliberately continue the same environment or composition. The kit provides a reusable method and shared art grammar; it does not guarantee that every AI model can render or that unseen scenes can be pixel-identical to nonexistent references.

For final encode counts, dimensions and duration, see the adjacent MP4 `.render.json` generated only after successful encoding and ffprobe validation.

## Expanded reference edition

Both user image folders were audited: 19,115 JPEGs at 1280×720 and 341 JPEGs at 1920×1080, with no decode errors. Every image file was hashed and decoded at JPEG reduced resolution for measurements. All 341 stills and 160 chronological samples from the other folder were visually reviewed. The original videos have separate full-resolution frame hashes: 10,243 + 19,115 = 29,358 decoded source frames, indexed across 295 atlas sheets. These figures describe computational coverage, not manual visual examination of every original-resolution frame.

The reference guide now maps observed scene mechanisms to concrete image evidence. The director contract separates decisions the AI makes from the palette, cast identity and visual grammar it must preserve. Added independent supporting props bring the registry to 42; all rendered in a smoke check. Camera/object keyframes, a stable-guide check and an authored-plan build gate were exercised. The gate rejects unreviewed importer scaffolds; semantic and style judgments still require the AI's actual review.

The previously rendered sample MP4 remains included. The expanded edition updates the toolkit, reference library and portable preview; it is not a claim of a newly rerendered or pixel-identical sample video. New production work uses the supplied timestamped script and audio through the revised director workflow.
