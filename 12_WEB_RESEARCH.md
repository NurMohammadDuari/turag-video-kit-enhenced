# Research applied to this renderer

The local supplied videos remain the visual standard. These sources inform animation mechanics, not a replacement aesthetic.

- Disney Animation, https://disneyanimation.com/process/animation/ : timing, staging, anticipation, follow-through and secondary action help communicate character performance. Application: author the motivated sequence before adding motion; preserve reading holds.
- Blender manual, https://docs.blender.org/manual/en/2.92/animation/armatures/posing/bone_constraints/inverse_kinematics/introduction.html : IK treats connected bones as a chain subject to constraints. Application: retain the shared arm solver and use its reachable endpoint for attached objects. A named action is not proof that a hand reaches the scene's target.
- MDN, https://developer.mozilla.org/en-US/docs/Web/API/CanvasRenderingContext2D/transform : Canvas transformations multiply the current matrix. Application: socket calculations must match the actual drawing's transformation order; a different bob/rotation order introduces attachment drift.

Implementation finding: action tracks previously sampled the previous raw action when starting a new blend. If that previous action was itself still blending, the new transition jumped. The rig now evaluates the complete prior track at the transition boundary. Regression tests cover successive overlapping transitions. This is our implementation decision, not an algorithm claimed by the sources.

For unfamiliar script scenes, derive subject, action, target, setting, factual relationship and visual consequence from the cue. Reuse shared drawing grammar, add missing local assets, and verify meaning and physical contact against rendered frames. Internet examples do not certify scene semantics or reference fidelity.
