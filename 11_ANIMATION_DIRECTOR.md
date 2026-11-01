# Animation director contract

Movement must explain the narration. Do not animate everything continuously and do not accept whole-body bobbing as acting.

For each cue, write `animationPlan` with the primary action, character motivation, anticipation, contact, weight shift, action peak, follow-through, secondary motion, gaze target, camera motivation and any intentional hold. The action peak should match `designDecision.actionPeak` and the review board's middle frame or an explicit `review.peakTime`.

## Acting sequence

1. **Prepare:** eyes/head orient first, weight shifts, the acting hand draws slightly away from the target.
2. **Act:** shoulder, elbow and wrist travel as a connected chain. Feet or seated hips support the force.
3. **Contact:** hand and prop meet at the same coordinate. Held props use a character socket instead of independent approximate keyframes.
4. **Settle:** the hand overshoots slightly or the body absorbs force, then holds long enough to read.
5. **Recover:** the actor returns toward rest or transitions into the next cue without a mechanical reset.

Use the shared action profiles: `typing`, `sew`, `phone`, `explain`, `raise`, `write`, `carry`, `examine`, `take`, `point`, `wave`, `handover`, `push`, `pull`, `lift`, `place`, `drink`, `read`, `listen` and `operate`. Add a new shared profile when a verb needs different mechanics. Do not misuse the nearest profile for an unrelated action.

Hands support `relaxed`, `open`, `flat`, `grip` and `point` silhouettes. Props can attach to `rightHand`, `leftHand`, `head`, `torso` or `pelvis`. The socket includes body lean, breathing, facing, scale, rotation, gait and seated posture.

Object secondary motion supports `walk`, `float`, `bob`, `shake`, `pendulum`, `pulse` and `orbit`. Entrance styles support `slideLeft`, `slideRight`, `rise` and `scale`; exit styles support `slideLeft`, `slideRight`, `drop` and `scale`. Use them only when the physical or editorial logic calls for them.

`shot.transitionIn` supports a motivated `crossfade` or directional `wipe` with a duration. Chapter cards usually use a hard editorial cut. Camera movement must follow a subject, reveal a relationship or change scale; decorative drifting is rejected.

Inspect feet for sliding, hips for unsupported leaning, elbows for disconnection, hands for tool contact, held props for lag, cloth/paper for response, and secondary objects for synchronized looping. Offset recurring cycles with `phase` so a crowd or office never moves as one machine.

## Scene repair loop

### Sequenced acting

A person accepts `actions:[{at:0,action:"take",blend:.2},{at:1.5,action:"read",blend:.3},{at:3.5,action:"point",blend:.25}]`. Times are seconds relative to the actor's entrance. Every entry starts its own action clock; wrists, lean, head motion and gaze blend from the previous action. The same track drives sockets and drawing. Tracks must be ordered, use unique nonnegative times and supported actions. Use explicit hand keyframes for contact that a generic action cannot reach. Preview the action boundary and prop transition; action names alone do not establish physical contact.

For each cue, answer these questions against the rendered pictures, not just the manifest:

1. What exactly does the narration assert, deny, compare or question? Does the scene preserve that relationship?
2. What visible change communicates that meaning? Identify the actor, target, contact and consequence. An evidence hold may be deliberate; record its reason.
3. Does the chosen reference support the character proportions, density, type, material and staging? Record concrete differences and fix the largest first.
4. Are the action phases readable at the cue's actual duration? Compare onset, anticipation, peak, settle and end; inspect extra frames around hand contact.
5. Are hands, props, furniture and feet physically aligned? Does a returning person or place preserve identity?
6. Does the scene add an unsupported fact, contradict negation, distort a ratio, repeat an unrelated layout or hide essential text?

When any answer fails, edit the shared rig, prop or shot, regenerate both review boards and inspect again. Keep unresolved issues visible in the delivery. Do not mark a review approved merely because its fields are populated or a test passed. The toolkit cannot perform semantic or aesthetic judgment without the AI operating it.

Use motion selectively. Quiet reading holds and restrained typing should remain quiet. A low pixel delta is a prompt to inspect the shot; it is not a reason to add arbitrary shaking, camera drift or unrelated movement.
