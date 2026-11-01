# Current workflow research — 31 October 2026

## What already exists

The user was right: closely related workflows already exist. The following are inspected public projects and firsthand accounts, not a claim that their demos match the supplied Turag references. No third-party code or skills were installed or copied during this pass.

| Source | Useful evidence | Decision for this toolkit |
|---|---|---|
| [stickman-video](https://github.com/nispa/stickman-video) | Script/SRT inputs, articulated action engine, narration retiming, contact-sheet review. | Keep narration-led timing and shared acting; do not adopt its stickman aesthetic. |
| [Whiteboard Video Orchestrator](https://github.com/dujudini/whiteboard-video-orchestrator) | Scene components plus newly generated line-art assets and drawing events. | Add richer vector artwork and independently animated parts for unfamiliar objects. Its silence-based timing is an estimate, not verified word alignment. |
| [Flick](https://github.com/Creatorberry/flick) | Timestamped transcripts, separate named scenes, reusable assets, targeted scene revisions. | Add per-scene workspaces with adjacent script context and safe merge. User approval checkpoints are not imported: this user delegates routine direction to the AI. |
| [Will Chen's production system](https://www.wcdc.io/writing/animated-product-video-system) | Shared geometry/timing, rendered repair rounds and boundary checks. | Expand QA around actual authored events rather than only midpoint screenshots. |
| [paper2video](https://github.com/Lunamos/paper2video) | Research-driven animation and editor handoff with subtitles and markers. | Export exact-cue SRT, scene CSV, chapter JSON and timing provenance. |
| [anything2explainer](https://github.com/Vincentwei1021/anything2explainer) | Per-shot code, explicit style specification and quantitative QC. | Retain original local implementation; its README identifies a noncommercial license and its black-canvas aesthetic is not our target. |
| [Remotion's official animation docs](https://www.remotion.dev/docs/animating-properties) | Frame-driven interpolation avoids render-time animation drift. | Preserve our deterministic time-based Canvas engine. Migrating frameworks alone would not fix the artwork or scene meaning. |
| [Runway's long-film guide](https://help.runwayml.com/hc/en-us/articles/26871350018835-How-to-create-longer-videos-and-films) | Persistent character/environment references and shot planning. | Add machine-enforced cast identity; retain source reference images for visual decisions. |

## Community evidence and caveats

[This Reddit architecture report](https://www.reddit.com/r/reactjs/comments/1qzadb5/used_remotion_claude_to_produce_13_min_of_clean/) describes reusable components, style guidance and scene-specific specs for a longer film. It links a repository; it is a creator report, not an independent quality evaluation.

[This firsthand animation breakdown](https://www.reddit.com/r/StableDiffusion/comments/1to7uzx/i_built_a_full_ai_animation_pipeline_and_made_a/) describes style training, character/background preparation, multiple generations and manual layered edits. It reinforces that visual consistency needs prepared assets and iteration. We did not install its models, train a LoRA or verify its performance claims.

An automatically generated r/ClaudeWorkflows summary was also inspected but was not treated as primary technical evidence.

### X follow-up

Direct X search redirected to login in the browser; a specific indexed post returned HTTP 403. An [indexed X topic](https://x.com/i/trending/2045371480712843352) supplied a useful lead, which was checked against the primary [browser-use/video-use repository](https://github.com/browser-use/video-use) and its README. The X topic is an automated summary, not independent verification. The repository describes narration-led editing, animation overlays, rendered cut-boundary review, bounded repair attempts and persistent project notes. These are relevant workflow ideas, but its footage-editing pipeline does not demonstrate matching our supplied character artwork. No code was installed, no social account was accessed, and no claim of exhaustive X coverage is made. Preserve our source timestamps, autonomous direction and visual review requirements rather than importing its approval or transcription setup.

## Concrete changes from this pass

- `tools/scene_workspace.py`: one editable packet per cue, neighboring narration, episode design, source hashes, protected timing/text and review invalidation on changed scenes.
- `tools/cast_registry.py`: named identity reused across shots, with conflicts rejected by the builder.
- `engine/composer.js`: SVG path curves and strokes, plus shape-level keyframes/transforms/visibility for new multi-part artwork.
- `tools/qa_episode.js`: event-adjacent samples around entrances, exits, camera/object keyframes, hand trajectories and action blends.
- `tools/export_handoff.py`: exact manifest subtitles, editing timeline and chapter metadata. Runs in the finish workflow.

## What is still not solved automatically

The AI must still understand and direct every cue, author the missing drawing, inspect actual motion and correct style mismatches. None of these sources establishes an unlimited one-prompt system with exact reference fidelity. Generative video can be an optional future asset path, but requires a selected service/model, cost control, local asset ingestion and clip-level consistency checks. It has not been silently added here.

For Bengali speech alignment, do not install WhisperX and assume defaults will work. The [inspected alignment source](https://github.com/m-bain/whisperX/blob/main/whisperx/alignment.py) has language-specific models and does not list Bengali in its default maps. A suitable model and actual audio validation are needed. User timestamps remain the authority until that work is performed.
