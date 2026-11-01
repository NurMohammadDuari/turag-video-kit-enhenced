# The AI decides; the supplied references control the look

The user's only creative inputs are a timestamped script and its narration audio. The AI must design the shots. Do not ask the user to select templates, name props, write a storyboard or provide JSON. Make those decisions autonomously from the script, this evidence library and the shared drawing rules.

Read `style-lock.json`, `09_REFERENCE_KNOWLEDGE.md`, `04_CHARACTER_SPEC.md` and `07_SCENE_COMPOSER.md`. Inspect the actual reference images. A list of colors is insufficient preparation.

## Decisions for every timestamped line

Write an exact `scriptLine`, its `cueIndex`, and a `visualIntent` that answers: who does what, to which object, what visibly changes, and what the viewer should understand. Preserve negation, causation and uncertainty. Extract all relevant nouns, verbs, quantities and relationships. A line mentioning a hiring freeze should visibly show an unfilled workstation, rather than a firing that the line did not describe.

Select one or two `styleRefs` pointing to bundled full-size frames. Choose the nearest visual mechanism and environment, not merely the same noun. For a genuinely new subject, borrow the staging and silhouette grammar while drawing its own recognizable objects. Use `reference/folder_audit/frames/fullsize/` and `reference/analysis/scene_stills/`.

Compose `shot.objects` from the script. Keep the most important action clear with on-screen text hidden. Place props on a surface or connect them meaningfully in an intentional diagram. Do not leave random large objects floating beside the guide. Reuse a real environment across successive lines when it helps continuity. A separate shot per line does not require a new location per line.

Establish, act, resolve, hold. Let an object enter near the narrated phrase, animate its relevant state, and leave enough reading time. Use absolute-time keyframes; do not rely on previous playback state. A counter changes a count; it should not merely pulse. Removed workers must leave actual empty positions. Keep geometry proportional to quantities when the chart is literal.

Keep a `cast` at episode level and a `continuity` note per shot. The guide keeps the same hair, face silhouette, shirt, trousers and scale relationship. Extras may vary; a recurring extra keeps its identity. Props that return retain silhouette, palette and parameters. Street landmarks and furniture keep their spatial relationships.

For an unknown prop, add a deterministic drawing function to `engine/custom-props.js`, or compose `vector.shapes`. Test it against a foreground character, crowd scale and the nearest reference setting. Do not change the style because the subject is new. A simple accurate silhouette beats an unrelated generic icon.

## Drafts cannot masquerade as finished decisions

The importer marks a new episode `planningStatus: "scaffold"`. Its noun matching supplies initial suggestions only. The builder rejects composed scaffolds. The AI must analyze every line, replace unsuitable shots, add missing props, inspect references, and then set `planningStatus: "authored"`. This flag records the AI's assertion of completed planning; it is not an automatic semantic or style certificate.

Before that change, check each line: literal subject represented; intended action represented; no unsupported added claim; correct quantities; neighboring continuity; readable silhouette; relevant reference images inspected. Then render start/middle/end for every shot and compare the actual result with the references. Fix the largest three differences in layout, character proportions, material and motion. Continue until the complete episode passes the checks in `06_QA.md`.

Deliver the complete MP4, editable manifest, portable HTML, newly drawn props and a short honest validation report. Do not stop at a plan or chapter demo. The reference controls the desired aesthetic; exact pixel equivalence for a scene that never existed cannot be established.

## Avoid the rejected sample's repetition

Do not duplicate a whole object arrangement and change only its heading, statistic or camera crop to imply a newly authored scene. For each cue, record the physical action or visual relationship that changes. Reuse a setting only when continuity helps that line; otherwise compose an appropriate new setting and draw the missing objects. A list of distinct IDs or fifteen copies of one layout does not establish scene variety.

Use `tools/review_shot_variety.py episodes/current.json` to flag repeated arrangements for human/AI inspection. Its result is a structural warning, not semantic understanding. Compare the actual rendered shots. `episodes/ep02-first-minute-revised.json` illustrates separate offer, exchange, aggregate, archive, comparison, street, ward, classroom, sewing and lab compositions.

Animate actors' joints with `action`, `actionTime`, `phase`, `rightHandFrames` and `leftHandFrames`. Keyframe hand targets in normalized character coordinates; inspect that the elbows remain connected and the hand actually touches its tool. Character actions include typing, phone, explain, raise, write, carry, take, sew and examine. New actions belong in the shared rig. A camera zoom, floating object or entire-person bob does not count as hand animation. Held props must follow the actual hand; sewing needs cloth feed and a moving needle as well as hands. Inspect action onset, peak and resolution.

## Preserve editorial identity as well as illustration style

Inspect chapter/title cards and transitions in the source. Do not drop the blue chapter page when replacing old scene layouts. `chapter_card` is a reusable full-frame prop: place it at x=0,y=0 with `instant:true`, a local `exit`, Bengali `number`, `chapter`, `total`, `line1` and `line2`. Delay the following objects within that cue; retain exact script cue boundaries and uninterrupted narration. The player suppresses its ordinary chapter badge while this prop is visible. For excerpts, `progressDuration` can retain the original full-episode progress scale. For new full videos omit it and use the new video's actual duration. Do not infer explicit calendar years from “this year” unless the supplied script or verified input context establishes the intended year.
