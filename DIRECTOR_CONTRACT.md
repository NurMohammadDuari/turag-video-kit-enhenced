# Director Contract — Autonomous Scene Direction

The user supplies only a timestamped script and narration audio. The AI director designs all shots autonomously. The code does not become intelligent by itself — the AI is the director.

## Director Loop (8 Steps)

1. **Episode design** — Write `episodeDesign`: thesis, emotional arc, chapter arc, recurring cast, recurring locations, visual motifs, density rhythm, chapter-card plan.

2. **Semantic analysis per cue** — Write `semanticAnalysis`: actors, action, setting, literal facts, relationship/change, tone, negation, uncertainty. Empty arrays acceptable only when the concept truly has none (explain in `notes`).

3. **Design decision** — Propose at least two materially different visual approaches in `designDecision.alternatives`. Write the selected mechanism, composition, visible change, action peak, camera purpose, transition, and why the chosen image explains the line better. This is a decision, not a list of prop names.

4. **Style references** — Select 1–2 real `styleRefs` (bundled full-size frames). Explain in `referenceUse` what is borrowed: staging, silhouette, density, material, motion, or editorial transition. Do not copy unrelated story content.

5. **Continuity** — Write `continuity` object with `cast`, `place`, `props`. Returning identities and locations retain established parameters.

6. **Copy ledger + fact basis** — Account for every on-screen phrase in `copyLedger` and every data-like number in `factBasis`. Mark basis as `script`, `derived`, `editorial`, or `decorative`. Relevant verbs must become visible actions. Held tools follow hands. Number comparisons share baseline and scale. Negation remains negation. Quotes visibly attributed.

7. **Review** — Run `tools/director_review.js`. Inspect start, action peak, end side by side. Record `review.start`, `review.middle`, `review.end`, `review.issues`, `review.fixes`, `review.approved`. "Looks good" is not an inspection record.

8. **Approve** — Review episode as sequence. Fix repeated arrangements, uniform density, arbitrary camera moves, missing chapter pages, cast drift, factual additions, weak transitions. Set `directorStatus: "approved"` only after `tools/director_audit.py` passes and rendered contact sheets inspected.

## Rejection Conditions

Reject a cue or episode when any is true:

- Generic intent could describe an unrelated sentence
- Only change from neighboring cue is text or a number
- Object floats without surface, hand, support, or diagram relationship
- Character present but does not perform narrated action
- Camera move has no reading or story purpose
- Reference named without explaining what evidence it supplies
- Displayed factual number, year, or claim not supplied or marked editorial/illustrative
- Every cue has same density, framing, or backdrop
- Chapter transition visible in reference grammar silently omitted
- Review records are boilerplate or claim inspection that did not happen

## Per-Line Decisions (`08_DIRECTOR_RULES.md`)

For every timestamped line:
- Write exact `scriptLine`, `cueIndex`, `visualIntent` (who does what, to which object, what visibly changes, what viewer understands)
- Preserve negation, causation, uncertainty
- Extract nouns, verbs, quantities, relationships
- A hiring freeze shows an unfilled workstation — not a firing the line didn't describe
- Select 1–2 `styleRefs` pointing to bundled full-size frames (nearest visual mechanism/environment, not same noun)
- Compose `shot.objects` from the script; most important action clear, on-screen text hidden
- Place props on surface or connect meaningfully in diagram
- Reuse environment across successive lines when continuity helps
- Establish → act → resolve → hold: object enters near narrated phrase, animates relevant state, leaves reading time
- Use absolute-time keyframes; no dependence on previous playback state
- Counter changes count, does not merely pulse; removed workers leave actual empty positions
- Geometry proportional to quantities when chart is literal

## Drafts Cannot Masquerade as Finished

- `planningStatus: "scaffold"` — initial noun matching only, builder rejects
- `planningStatus: "authored"` — AI assertion of completed planning after semantic review of every line
- Before authoring, check each line: literal subject represented, action represented, no unsupported added claim, correct quantities, neighboring continuity, readable silhouette, relevant references inspected
- Render start/middle/end for every shot; compare actual result with references
- Fix largest three differences in layout, character proportions, material, motion

## Animation Director (`11_ANIMATION_DIRECTOR.md`)

Per cue, write `animationPlan`:
- Primary action, character motivation, anticipation, contact, weight shift, action peak, follow-through, secondary motion, gaze target, camera motivation, intentional hold
- Action peak matches `designDecision.actionPeak` and review board's middle frame or `review.peakTime`

Acting sequence:
1. **Prepare**: eyes/head orient first, weight shifts, acting hand draws slightly away
2. **Act**: shoulder, elbow, wrist travel as connected chain; feet/seated hips support force
3. **Contact**: hand and prop meet at same coordinate; held props use character socket
4. **Settle**: hand overshoots slightly or body absorbs force, then holds long enough to read
5. **Recover**: actor returns toward rest or transitions into next cue without mechanical reset

Action profiles: typing, sew, phone, explain, raise, write, carry, examine, take, point, wave, handover, push, pull, lift, place, drink, read, listen, operate. Add new shared profile when verb needs different mechanics.

Hand silhouettes: relaxed, open, flat, grip, point. Prop sockets: rightHand, leftHand, head, torso, pelvis.

Object secondary motion: walk, float, bob, shake, pendulum, pulse, orbit. Entrance: slideLeft, slideRight, rise, scale. Exit: slideLeft, slideRight, drop, scale.

`shot.transitionIn`: motivated crossfade or directional wipe with duration. Chapter cards usually use hard editorial cut.

## Chapter Cards (`chapter_card` prop)

- Place at x=0, y=0 with `instant: true`, local `exit`
- Bengali `number`, `chapter`, `total`, `line1`, `line2`
- Delay following objects within that cue; retain exact script cue boundaries and uninterrupted narration
- Player suppresses ordinary chapter badge while prop visible
- Do not drop blue chapter page when replacing old scene layouts

## Reference Mechanisms (`director/REFERENCE_MECHANISMS.json`)

Decision vocabulary, not fixed templates. Mechanisms include:

| ID | Use When | Borrow | Avoid |
|---|---|---|---|
| grounded_environment_action | Person performs concrete task | slender cast, furniture scale, room detail, hand-tool contact | standing icon beside unrelated prop, floating tool, motionless hands |
| literal_quantity_grid | Narration states count/fraction/share | literal repeated figures, vermilion changed subset, shared baseline | decorative crowd, wrong denominator, percentage without visible whole |
| shared_scale_comparison | Two values directly compared | one baseline, consistent unit geometry, guide/bracket | unrelated scales, 3D chart styling, invented precision |
| claim_then_pressure | Person states belief tested by argument | cream claim card, distinct silhouettes, vermilion challenge mark | presenting belief as verified fact, identical speakers, full narration as text |
| process_transformation | Before/after workflow/automation | same spatial frame, objects transform in place, clear causal path | arbitrary cut between rooms, orb as universal cause, change shown only by label |

## Deliverables

- Complete MP4 with narration
- Editable episode JSON + timed cue/beat data
- Portable HTML preview (functioning audio + seeking)
- New reusable props in `engine/custom-props.js`
- Validation summary: passed, timing confidence, unsupported claims, stylistic limits

Do not stop at a plan or chapter demo. Reference controls desired aesthetic; exact pixel equivalence for unseen scenes cannot be established.

## Tools

- `tools/create_director_packet.py` — creates editable director fields + cue-by-cue briefing
- `tools/director_audit.py` — structural audit of director dossier
- `tools/director_review.js` — per-cue start/middle/end review recorder
- `tools/review_shot_variety.py` — flags repeated arrangements (structural warning only)
