# Revision 9 — animator-grade motion pass

Revision 9 turns character motion from a handful of pose changes into a reusable acting layer. The shared rig now has explicit hand silhouettes, body lean, breathing, head/torso/pelvis sockets, alternating foot lift, dress/panjabi gait, and twenty-one named actions. Props remain attached through scale, rotation and movement.

The composer adds deterministic walk, float, bob, shake, pendulum, pulse and orbit motion; entrance/exit choreography; and wipe/crossfade shot transitions. Reusable interactive props include a hinged door, live drawer, hand tools, cup, wheeled cart, flexible sheet and control panel. They are primitives for new script-specific scenes, not templates.

Every authored cue must now include an `animationPlan` describing motivation, anticipation, contact, weight shift, action peak, follow-through, secondary motion, gaze and camera motivation. `tools/animation_review.js` renders five phases of every cue and reports a coarse pixel-motion diagnostic. The AI must inspect those pictures; a numerical delta cannot certify good acting.

This remains a deterministic stylized 2D rig, not physics simulation, motion capture or automatic semantic intelligence. The AI operating the toolkit is responsible for interpreting each line and authoring the shot.
