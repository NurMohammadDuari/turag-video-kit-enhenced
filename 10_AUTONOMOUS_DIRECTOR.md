# Autonomous director contract

This toolkit is operated by an AI with image inspection, file editing and code execution. The code does not become intelligent by itself. The AI is the director; this contract makes its reasoning and review concrete enough to inspect and reject when weak.

The user supplies only a timestamped script and matching narration audio. The director must understand the full argument before drawing individual cues. It decides the visual idea, setting, cast, props, action, camera, transition and timing. It may create new deterministic vector props and shared character actions. It must preserve the supplied reference style and never ask the user to design the shots.

## Director loop

1. Read the complete script and write an `episodeDesign` containing the thesis, emotional arc, chapter arc, recurring cast, recurring locations, visual motifs, density rhythm and chapter-card plan.
2. For every cue, write `semanticAnalysis`: actors, action, setting, literal facts, relationship or change, tone, negation and uncertainty. Empty arrays are acceptable only when the concept truly has none; explain that in `notes`.
3. Propose at least two materially different visual approaches. Record them in `designDecision.alternatives`, then write the selected mechanism, composition, visible change, action peak, camera purpose, transition and why the chosen image explains the line better. This is a decision, not a list of prop names.
4. Select one or two real `styleRefs`. Explain in `referenceUse` what is borrowed: staging, silhouette, density, material, motion or editorial transition. Do not copy unrelated story content.

Use `director/REFERENCE_MECHANISMS.json` as a decision vocabulary. It maps story relationships to evidence and failure modes. It is not a router and must not replace reading the actual images.
5. Write `continuity` as an object with `cast`, `place` and `props`. Returning identities and locations retain their established parameters.
6. Account for every on-screen phrase in `copyLedger` and every data-like number in `factBasis`. Mark the basis as `script`, `derived`, `editorial` or `decorative` and explain it. Then build the shot. Relevant verbs must become visible actions. Held tools follow hands. A number comparison shares a baseline and scale. Negation must remain negation. A quote is visibly attributed as a belief or claim.
7. Run `tools/director_review.js` and inspect the start, action peak and end side by side. Record `review.start`, `review.middle`, `review.end`, `review.issues`, `review.fixes` and `review.approved`. “Looks good” is not an inspection record.
8. Review the episode as a sequence. Fix repeated arrangements, uniform density, arbitrary camera moves, missing chapter pages, cast drift, factual additions and weak transitions. Set `directorStatus:"approved"` only after `tools/director_audit.py` passes and the rendered contact sheets have been inspected.

## What a real design decision contains

For “the chair stays empty because nobody was hired,” a valid decision states that a worker exits, the chair remains centered under a quiet pool of light, and the camera holds after the departure so absence becomes the subject. “Office, chair, person” is inventory, not direction.

For an unseen subject, choose a compatible visual mechanism from the reference evidence. A delivery-dispatch line can borrow the grounded office scale, dashed-route grammar and street vehicle silhouettes, while drawing a dispatcher, route board and delivery vehicle specific to that meaning.

## Rejection conditions

Reject a cue or episode when any of these are true:

- generic intent could describe an unrelated sentence;
- the only change from a neighboring cue is text or a number;
- an object floats without a surface, hand, support or diagram relationship;
- a character is present but does not perform the narrated action;
- a camera move has no reading or story purpose;
- a reference is named without explaining what evidence it supplies;
- a displayed factual number, year or claim was not supplied or explicitly marked editorial/illustrative;
- every cue has the same density, framing or backdrop;
- a chapter transition visible in the reference grammar is silently omitted;
- review records are boilerplate or claim inspection that did not happen.

`tools/create_director_packet.py` creates the editable director fields and a cue-by-cue briefing. `tools/director_audit.py` checks structure and common failure patterns. These tools cannot understand the story or judge visual beauty; the operating AI must do that work and inspect the images.
