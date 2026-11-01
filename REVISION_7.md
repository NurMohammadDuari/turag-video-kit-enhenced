# Revision 7: visual and full-pipeline audit

## Fixed

- Report count labels collided with the report header; archive count covered its own header. Separate layout bands now keep them readable.
- Character feet were above several scene floor lines. Shot baselines now match the cast and furniture, including the teacher.
- The offer and payment moved independently of the hand. Reusable hand attachments now follow the rig's actual reachable wrist, including rotation, scale, handedness, visibility and motion.
- Keyboard hands sat below the keyboard. Corrected contact height and typing movement.
- Chalk appeared away from the hand. Marks now follow the actual chalk-tip path; the teacher and board share the corrected baseline.
- Cream doctor/employer clothing disappeared against the cream background. Added a slightly darker coat tone while retaining the reference palette family.
- Hospital/sewing headings intersected window details. Repositioned the windows.
- The fan only rocked slightly. Added a deterministic rotating three-blade silhouette.
- Unrelated keyframes reset earlier animated properties. Interpolation now retains each property's own last keyed value.
- Zero scale and zero walking speed were treated as missing values. Explicit zero now works.
- Links could show before their endpoint objects. They now follow endpoint visibility and opacity.
- Unknown props and invalid attachments could fail deep into a long export. Every shot is preflighted on player load.
- Malformed timestamps could fall back silently to estimated timing; multiline Markdown narration was dropped. The importer now rejects malformed timecodes and retains continuation text.
- Cue ownership, duplicate object IDs, non-finite values, invalid keyframe timing and out-of-range cues were insufficiently checked. Added validation and regression tests.
- External script/audio paths made handoffs fragile. The importer copies external inputs into the toolkit.
- Long exports could silently pad missing narration. Builder/finalizer/renderer now check available audio duration.
- Widths giving odd H.264 frame heights were accepted. Render widths must be multiples of 32.
- Renderer could overwrite an input path, use remote assets or wait unhelpfully after a player failure. Added guards, network blocking and clearer early failures.
- Episode identity was hardcoded in player chrome. It now uses episodeNumber, with a neutral fallback.
- First-minute authoring depended on its own previous output. It now starts from the stable input example.
- Existing blue card and exact transition fixes from revision 6 remain in place.

## Full-video operation

`python3 tools/finish_episode.py episodes/my-video.json` builds, checks, renders the complete authored manifest and verifies decoding. No 60-second cap is applied. `HOW_TO_USE.md` provides the user-facing handoff and commands.

Regression suite: 13 Python tests plus shared-engine tests for property persistence, zero values, transformed wrist attachments, visibility, boundary timing and articulated movement. Both the 15-cue sample and the 115-cue 637.257143-second example are exercised. Render reports and QA folders are included with the package.

The full-episode example is a compatibility test fixture, not a claim that its older artwork has been redesigned. Its older repeated arrangements are reported by the variety checker. The revised first minute is the current visual sample. No test suite proves that all possible bugs, semantic mistakes or stylistic differences have been eliminated. Supplied editorial timecodes remain unverified against word-level speech alignment.

Final scope of verification: 120 frames sampled at 0.5-second intervals were visually reviewed from the encoded first minute, then the remaining pale employer clothing was corrected. The 1,800-frame render decoded successfully. The full-length project passed 577 time-point checks, and a separate 218-frame MP4 was successfully rendered from 630s through its end. This tests long timeline export, not a redesigned full episode.
