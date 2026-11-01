# Instructions for an AI using this toolkit

Read `REFERENCE_FIRST.md` first. The actual supplied videos and images define the visual target. The AI invents scene content from the timestamped script and audio, and extends or corrects the renderer to match those references. Existing templates, style-token guesses and the example reconstruction must not limit new scenes or preserve visual mismatches.

Read 01_MASTER_PROMPT.md and 07_SCENE_COMPOSER.md first. The user provides a timestamped script and audio. Infer the topic and make the complete video autonomously. Do not request scene descriptions, a template choice or chapter-by-chapter approval unless the user asks for that workflow.

For every script cue author exactly one `scene:"compose"` beat with matching `cueIndex`, exact `scriptLine`, a specific `visualIntent` and original `shot.objects`. Analyze meaning, negation and numerical relationships. Generic keyword suggestions are only scaffolding. Do not present them as semantic understanding.

Reuse the shared rig and drawing grammar. Add unseen props through engine/custom-props.js or declarative vector shapes, and compose them with backgrounds and people. Keep all data and assets local. Follow the timestamped narration, inspect every shot, validate coverage and deterministic seeking, then render the full MP4. Deliver the editable manifest and portable HTML too. Report material stylistic/timing limits honestly; do not call a reference mux a newly generated video.

Read `08_DIRECTOR_RULES.md`, `09_REFERENCE_KNOWLEDGE.md`, `style-lock.json` and the image-folder audit. The AI makes scene decisions; the user supplies only timestamped script and audio. Analyze every line semantically, pick bundled style evidence, maintain recurring cast/place identity, add new props and action/camera keyframes. Draft keyword suggestions must be reviewed and replaced as needed before setting `planningStatus:"authored"`. The builder rejects unreviewed scaffolds.

Read `10_AUTONOMOUS_DIRECTOR.md`. New deliverables require a completed director dossier and `directorStatus:"approved"`. Run `tools/director_audit.py`; do not bypass it with the legacy technical-check flag for user work.

Read `11_ANIMATION_DIRECTOR.md`. Every cue needs a motivated animation plan with anticipation, contact, weight shift, action peak, follow-through, gaze, secondary motion and camera motivation. Add shared actions when the existing rig cannot express the verb.
