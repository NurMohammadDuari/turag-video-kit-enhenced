# Creating scenes not present in the reference

The toolkit supplies a visual grammar and drawing system, not a finite collection of screenshot backgrounds. Novel subjects should preserve palette, cast, proportions, material, staging, typography and motion. Pixel identity cannot be guaranteed for a reference scene that never existed.

## Begin with the mechanism

Write: “The viewer sees X change because Y.” Extract entities, action, comparison and conclusion. Preserve uncertainty: capability is different from actual layoffs; an illustrative example is different from measured research.

| Relationship | Construction |
|---|---|
| Many to fewer | Same grid/crowd before and after; removed positions faint or outlined |
| Work split into tasks | Outlined tiles; selected tasks turn blue |
| Input/process/output | Grounded components with dashed blue routes |
| Human/machine cost | Matched baseline and units, two labeled stacks |
| Hidden effect | Empty workstation or vacancy notice, restrained spotlight |
| Capacity/demand | Container or funnel with meaningful saturation |
| Broader access | Blue routes from one node to separated buildings/people |
| Skeptical claim | Person and cream claim card; response visibly changes one part |
| Routine work | Conveyor or task loop |
| Personal action | Guide at laptop, actionable checklist, return to street |

Choose by relationship rather than noun. A warehouse can inherit the factory floor. A new profession can inherit a room tableau. Do not use a generic card simply because the topic is new.

## Construction recipe

1. Select paper day, navy night, city street, office, field or minimal floor-rule diagram. Reuse the nearest baseline/margins/depth.
2. Use the established character rig. A new profession is a clothing/prop variant, not a new illustration style.
3. Draw the minimum identifying prop from rectangles, narrow paths and small labels. A server is a slate cabinet with blue slots; a pharmacy reuses the shopfront grammar.
4. Stage one dominant action: task changes color, queue grows, slot empties, route appears. If the action is unclear with text hidden, simplify.
5. Add only supplied evidence, unit/count or an illustrative label. Never manufacture a source.
6. Reveal near the relevant narrated phrase, perform the change, hold for reading, then exit. Subtitle lifetime is separate from environment lifetime.
7. Draw fixed chrome and caption outside camera transforms.
8. Compare midpoint and difficult transition against the closest observed shot. Fix composition, cast proportions and text scale first.

## Extension contract

For the primary composer workflow, register a named deterministic PROP in `engine/custom-props.js`, then arrange it inside that line's `shot.objects`; keep drawing outside the player. Full-scene legacy handlers in `engine/runtime.js` are reference examples, not the route for new script lines. Reuse palette, paper, characters, text helpers and easing. Content comes from the beat object rather than hard-coded episode claims. Preserve existing scene handlers.

The scene receives `TuragScenes.draw(ctx, absoluteSeconds, beat)` in 960 × 540 design coordinates. The beat has `scene`, `t0`, `t1` and optional `heading`, `label`, `value`, `values`, `items`, `mode`, `chapter`, `chapterTitle`. Read the runtime for the precise inputs each handler uses.

Document defaults, text limits, baseline and phases. A missing fact must remain absent; use a generic nonfactual prop rather than inventing a number. Add a fixture, render start/middle/end, register its ID and validate. An unknown scene ID should fail validation instead of silently becoming a generic slide.

## Example: logistics

Script idea: “One dispatcher can monitor several delivery routes with software.” This does not say a specific company cut staff.

- Family: adapt `ai_workflow`.
- Environment: paper office, desk left, route diagram right.
- Cast: existing grey seated worker; guide optional.
- Props: cream route cards, thin slate routes, flat vehicles, one blue system node.
- Action: routes connect to node; worker selects an exception. No disappearing employees unless the script says staffing falls.
- Overlay: short Bengali action label, no fabricated percentage.
- Motion: staggered route reveals, blue selected route, hold, familiar chrome/subtitles.

The shot should feel like another scene in the same series while explaining its own script.

## Completion

Check silhouette, palette, baseline, caption, typography and material against reference. Action reads at phone size; props stay attached; subtitles remain clear. Quantities match the script. Arbitrary seeks are deterministic. No missing handler/assets remain. Record deliberate differences rather than claiming exact replication.
