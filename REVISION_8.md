# Revision 8: autonomous director workflow

Revision 8 turns the toolkit handoff into a director workflow rather than a renderer-only workflow. The operating AI still supplies the intelligence; no local keyword script or canvas engine can understand arbitrary stories by itself.

New work must include an episode thesis, emotional and chapter arcs, cast/location bibles, visual motifs and density rhythm. Every cue records semantic meaning, at least two visual alternatives, the selected mechanism, composition, visible change, action peak, transition, reference rationale, continuity, on-screen copy provenance, factual-number provenance and start/peak/end review.

`tools/create_director_packet.py` creates the editable dossier and a whole-episode cue briefing. `tools/director_audit.py` rejects generic intent, incomplete decisions, unexplained references, missing continuity, unsupported on-screen copy/numbers and unreviewed cues. It also reports repeated arrangements, static characters and visual crutches. `tools/director_review.js` renders a three-frame board for every cue with the decision and critique beside the pictures.

`tools/finish_episode.py` now requires `directorStatus:"approved"`, runs the director audit, technical QA, variety review and start/peak/end review before encoding the full video. `--legacy-technical-check` exists only to inspect the old example and is forbidden for user deliverables.

The first-minute example contains 15 director-approved cue dossiers, 15 distinct mechanisms, copy/fact ledgers and 45 start/peak/end review images. The technical suite still includes the parser, renderer and articulated-action regressions from revision 7.

This workflow makes weak or unsupported decisions visible. It does not turn deterministic code into a language model, prove that an AI's written rationale is truthful, or guarantee pixel identity for an unseen scene. The operating AI must inspect the actual reference and rendered images, revise weak shots and report remaining differences honestly.
