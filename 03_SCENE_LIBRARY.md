# Scene library and observed shot grammar

The reference times below are visual anchor samples from the 6-second sheets, not exact cut boundaries. Use the frame index in `reference/analysis/` and the source video to locate precise transitions. The pasted transcript's chapter times can differ from picture changes by several seconds. Times are minutes:seconds unless otherwise stated.

The canvas is 960 × 540. `TuragScenes.draw(ctx, absoluteSeconds, beat)` draws the selected scene; the player owns fixed chrome and subtitles. Read `engine/runtime.js` for supported IDs/options. Do not assume this prose alone implements a shot.

## Observed episode structure

| Reference anchors | Scene family / runtime ID | Composition and action |
|---|---|---|
| 0:00–0:12 | `title_office` | Two staggered rows of seated staff, cream monitors, dark skyline through tall window mullions, exit sign. Title sits upper left. Envelopes and a leaving worker explain the offer. |
| 0:18–0:30 | `night_city` / `compare` | Despite the legacy ID, this section of the reference is a light skyline. Walking people carry boxes. Large numeric evidence stays upper left; two building-like comparison stacks arrive at right. |
| 0:36 | `street`, `shield` | Guide with phone on near sidewalk, shield above, tea stall at right, narrow walkers behind, skyline/palms/wires. |
| 0:42–0:48 | `profession_rooms` | Adjacent outlined/dashed rooms; hospital bed/doctor, classroom/teacher, garment work. Camera moves between environments instead of unrelated title cards. |
| 0:54–1:18 | `survey` | Navy AI lab rectangle on paper with three seated builders and blue orb. Clipboard then slider above; ordinary people form a group to the right. Comparison is population belief, not actual measured task replacement. |
| 1:30 | `shield` / phone variant | Seated person and oversized phone chat panel; skepticism is shown through interaction and emphasis mark. |
| 1:36–1:42 | `engine_garage` | Motor on table, tools and tyres, person; camera reveals road and incomplete vehicle analogy. |
| 1:48–1:54 | `ai_workflow` | Person left; blue orb, filing cabinet and computer at right, dashed links demonstrating data/access/checking. |
| 2:00 | `shopfronts` | Four grounded buildings with blue windows and hospital/bank/legal/call-center signs. |
| 2:06–2:18 | `street` / `hammock` adaptation | Guide before veiled hidden machinery, map transition, then relaxed office pose. Existing templates require adaptation for these exact motifs. |
| 2:24–2:30 | `task_tiles` | Guide at left, robot arm at right. One job card splits into eight task tiles such as email, report, calls and teaching. |
| 2:36–2:54 | `doctors` | Ten slender doctors, narrow vertical time bars above. Paperwork share moves out, empty positions remain, then remaining doctors treat patients. |
| 3:00–3:12 | `headcount` | Desk grid with active blue cells; camera can focus on one cell. Keep symbolic percentage separate from literal job elimination. |
| 3:18–3:42 | `rice_field` | Wide green textured field, huts, palms, red halftone sun, bent workers. Combine enters, fewer workers remain, labor card makes the count comparison explicit. |
| 3:48 | `title_office` light variant | Row of desks bridges field automation back to offices. |
| 3:54–4:24 | `night_desk`, `empty_chair` | Large navy room, person at desk, blue orb/code panel, city window, editing displays, clock. A missing editor becomes an empty workstation under a lamp. |
| 4:30–4:36 | `street` | Tea-stall conversation introduces the new-jobs counterargument. |
| 4:42–4:48 | `ledger` | Ruled table with red header. Team headcount at left and blue AI jobs at right; figures change in place. |
| 4:54 | `ledger` headline variant | Tilted newspaper panel states the relative-growth headline, with hard shadow. |
| 5:00 | `headcount` | Two groups on same baseline compare total people; red net result. Do not confuse growth rate with net headcount. |
| 5:12 | `profession_rooms` teacher variant | Teacher and a much larger student group explain expanded capacity. |
| 5:24–5:30 | `garment` | Seated sewing workers under ceiling fans; factory robot capability panel above. |
| 5:36–5:42 | `robot_cost` | Blue robot against human; large and small cost stacks. Tiny highlighted cells convey the very small cost-competitive share. |
| 5:48–6:00 | `robot_hand` | Articulated blue arm struggles with soft fabric; nearby person and table; later learning/observation panel. |
| 6:06–6:24 | `digital_copies` | Four outlined work rooms; blue AI node distributes to screens and task copies. Close view emphasizes inexpensive automation. |
| 6:30–6:42 | `government` | Cream office, fan/clock, tall grey cabinet, files tied with red string, clerk and assistant. Blue field covers paper tasks. |
| 6:48 | `government` notice variant | Recruitment notice and vacant desk; new hiring falls without a dramatic firing scene. |
| 6:54–7:06 | `queue`, `empty_chair` | Long applicants line to examination building; large number card; sparse red chairs communicate limited posts. |
| 7:12–7:24 | `compare` / accounting variant | First counterargument marker, spreadsheet desk, board contrasting clerks and accountants. |
| 7:30–7:36 | `queue`, `compare` | Clinic queue; Bangladesh medical-staff grid and comparison. |
| 7:42–7:48 | `village` | Four huts, family and phone; blue orb sends dashed arcs toward separated homes. |
| 7:54–8:06 | `demand_funnel` | Pipe and funnel for unmet demand; another container fills to saturation; people and task symbols explain the difference. |
| 8:12–8:18 | `compare` chart variant | Flat aggregate jobs line, magnifying glass, two people; “no clear evidence yet” is different from proof of no effect. |
| 8:24 | `podium` | Person at lectern with AI-labeled box and audience: a rhetorical packaging metaphor. |
| 8:30 | `ranking` | Dark chart panel with five ranked horizontal bars; AI highlighted fifth; guide beside chart. |
| 8:36–8:48 | `empty_chair`, `night_desk` | Spotlight on unfilled chair, then unused editing workstation; data arrives after events. |
| 8:54–9:06 | `bank_atm` | Blue-screen ATM beside human teller. Queue favors person, then a tall human cost stack changes the tradeoff. |
| 9:12–9:18 | `bank_atm` mobile variant | Phone/money thought bubble, then mobile banking shop and dashed path to home. |
| 9:24 | `chapter` | Full blue field, large striped Bengali chapter digits on red disc, cream/ink chapter title. |
| 9:30–9:36 | `conveyor` | Repeated task boxes pass through a large blue AI machine and emerge blue. |
| 9:42 | `hammock` | Guide reclines between two palms; relaxed posture carries the warning. |
| 9:48–10:06 | `laptop_tasks`, `checklist` | Guide at laptop; task tiles separate into blue automated group and red-outlined human group; calendar/checks mark recurring review. |
| 10:12–10:24 | `comments`, `street` | Return to the established tea-stall street. Comment entry panel types in; guide speaks to technically informed friend. |
| 10:30 onward | `end_card` | Navy background, opening question restated, small source list. Use only supplied sources. |

## Reusable layout rules

- Office: two staggered rows or a single explicit row, people at coherent furniture scale, monitor stem/keyboard/chair aligned. Use window mullions and cream windows for the night setting.
- Street: keep the same geographical arrangement across returns. Introduce motion with background walkers/traffic while the guide and tea stall anchor composition.
- Professional rooms: use thin dividers and consistent floor height; move camera/panels, not the subtitle overlay.
- Statistical panel: one clear quantity, one unit, one comparison baseline. Charts should use a shared scale. Numeric changes should be reflected by geometry when meaningful.
- Icon grid: decide whether each cell is a literal person or a representative unit. Count literal grids. If the grid is symbolic, say so.
- Process diagram: objects are recognizable props, linked by thin dashed blue routes. Use one dominant reading direction.
- Rural: low huts and bushes behind a continuous field; red sun and green halftone carry the environment. Human posture and machine action change the foreground.
- Empty-workstation argument: keep the furniture from the preceding occupied scene, remove the person and hold. This is clearer than an unrelated red warning slide.
- End card: preserve reading time and contrast. Avoid tiny invented bibliography text merely to imitate texture.

## Other observed video-1 families

The included first video also shows a living room with television tiles, split human/AI timing panels, a five-level pyramid, panel-stage speakers, a loop diagram, world/country map, shield/skills, and a hospital comparison table. These are additional design references. A matching runtime handler may need implementation before use; documentation of a scene is not evidence that code already supports it.

## Beat design

In the current workflow every timestamped narration cue owns one composed shot. Several consecutive shots may deliberately continue one environment and action. The legacy scene families below provide visual examples, not fixed template routing. For each beat record ID, time range, handler, chapter, short heading, relevant data and mode. Several successive beats can keep the same handler/environment with different data or phases. Do not reset all objects merely because narration wraps to another subtitle line.

Examples: a before/after count preserves positions; task automation changes selected tiles; a survey reveals the two groups before percentages; an empty-chair shot reuses the occupied room; return-to-street reuses the skyline/stall coordinates.

For new scenes, follow `05_NEW_SCENES.md`, add a registered handler, then validate representative frames. Never claim all 35 prose entries are exact reproductions: some are families combining several source shots, and the original animation source is unavailable.
