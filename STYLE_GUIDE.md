# Style Guide — Turag Visual Grammar

Flat editorial illustration on warm paper. Unusually slender faceless people. Heavy condensed Bengali type. Cream, navy, grey, vermilion, electric blue. Print-like halftone. Persistent fine publishing frame. Each scene illustrates a specific narrated mechanism.

This is a **reconstruction guide**, not the original author's source specification. Observations come from supplied reference frames. Numerical geometry is an approximate drawing target.

## Palette (`style-lock.json`)

| Role | Hex | Use |
|---|---|---|
| Paper | `#E9E4D2` | Main background, signs, screens, light clothes |
| Ink / night | `#12141C` | Type, shadows, dark environments |
| Vermilion | `#FF3D17` | Guide shirt, sun, risk, emphasis, subtitle edge |
| Electric blue | `#2F3BFF` | AI, active screens, machine parts, automation |
| Slate | `#4A4D63` | Furniture, trousers, panels |
| Green | `#216E50` | Agriculture, boards, signs, some clothing |

Use one semantic accent per action. Blue does not color all secondary text. Vermilion does not border every prop. Human skin is abstract grey, not realistically shaded.

## Composition (design space 960×540)

| Region | Target |
|---|---|
| Corner registration marks | Centers near (23,23), (937,23), (23,517), (937,517) |
| Chapter tag | Begins near (55,55); tiny boxed number + short label |
| Top progress rule | 1–2 px vermilion, proportional to episode time |
| Main safe area | x 54–906, y 85–465 |
| Common floor baseline | y 430–465 (default 455) |
| Subtitle band | y 485–518, horizontally centered |
| Swatches | Four tiny squares near x 43–90, y 512 |
| Scene counter | Small low-contrast mono at lower right |

Draw chrome and subtitles after world/camera transforms. Most scenes leave a large quiet upper area. People and furniture share a low baseline. Diagrams and numeric evidence occupy the space above.

## Material & Marks

- **Paper**: soft uneven tone, sparse fibres, weak vignette. Cache seeded texture (no flicker).
- **Halftone**: geometric dots, visible spacing/size gradient. Lower sun edge, screen halo, field or wipe edge. No soft bloom on everything.
- **Night offices**: restrained navy layers, sparse cream windows, faint patterned floor.
- **Fills**: flat fills for bodies and buildings. Fine strokes for furniture, windows, props, diagrams, registration marks.
- **Shadows**: short hard card offsets, low flat oval shadows for people. No bevels, photographic light, glossy 3D, rounded dashboard cards.
- **Misregistration**: occasional 2px color offset is deliberate, not applied to all text.

## Typography

Fonts: `Anek Bangla` (headline), `Hind Siliguri` (subtitle/captions), `Space Mono` (metadata). Bundled locally as data URLs.

| Role | Size (960×540) |
|---|---|
| Opening headline | 54–84 px, 1–2 short lines |
| Large numeric evidence | 72–118 px, fit actual digits |
| Diagram labels / local titles | 18–34 px |
| Subtitle | 18–20 px |
| Chapter label | 11–14 px |
| Mono metadata | 8–11 px, nonessential only |

- Heavy condensed Bengali for hero lines; clear semibold Bengali for captions; tracked Latin mono for metadata.
- Preserve Bengali grapheme clusters; never letter-space Bengali body text.
- Test: চাকরি, প্রশ্ন, স্বাস্থ্য, প্রযুক্তি, সংখ্যা. Missing glyph boxes = failed render.
- Subtitles: exact script excerpts, short white line in tightly fitted near-black rectangle with thin vermilion left edge. Split long sentences into timed chunks. Two-line fallback better than unreadably small type. Keep within safe frame, away from key action.

## Character Silhouettes

- Short narrow neck, sloped shoulders, long narrow tunic-like torso, tiny profile nose, asymmetric hair, jointed thin arms, long legs, small flat shoes.
- Small head (~0.10–0.13 of height), visible neck (0.025–0.045), shoulder width 0.15–0.19.
- Hair top to chin 0.10–0.13; hip to sole 0.46–0.54.
- Face blank — no detailed eyes, mouth, fingers, muscles, realistic shading.
- Guide: vermilion long top, charcoal trousers/shoes, dark grey face, swept hair, occasional blue visor/phone. Locked to variant 0.
- Shoes: low rounded rectangles aligned to ground, not circles.
- Limbs: jointed paths/capsules, continuity at elbow and knee.

## Poses

| Pose | Description |
|---|---|
| stand | Almost vertical weight, relaxed knees, arms down or one elbow bent |
| walk | Opposite legs form X at midstep, knees bend, arms counter-swing, feet contact floor |
| phone | Bent elbow, forearm toward small blue phone, head at screen, prop attached |
| point | Shoulder fixed, forearm aims at actual target, hand outside torso |
| raise | Diagonal arm above head, still joined at shoulder |
| sit/type | Thigh horizontal, shin vertical, shoe on floor, forearm reaches keyboard, slight lean |
| rest/hammock | Connected long body, head near hand — not rotated chair pose |
| field work | Hip hinge, bent knees, hand reaches rice |

## Motion

| Action | Timing |
|---|---|
| Caption/card reveal | 0.25–0.45 s, cubic ease out |
| Concept assembly | 0.5–1.2 s, 0.04–0.10 s stagger |
| Focus settle | Scale 1.02–1.04 → 1.00 over 0.4–0.7 s |
| Graphic wipe | 0.35–0.65 s |
| Walking | ~1–1.5 cycles/s, opposing arm/leg phases |
| Reading hold | Long enough for actual words, no perpetual bouncing |

Use motion selectively. Quiet holds should remain quiet. Offset recurring cycles with `phase` so crowds never move as one machine. Camera moves must follow a subject, reveal a relationship, or change scale — decorative drifting is rejected.

## Evidence Devices (choose per line)

- Giant Bengali total in ink box with red offset edge
- Red percentage
- Cream figure grid
- Newspaper headline
- Dashed ellipse
- Blue active cells
- Green check
- Empty outlined positions
- Faded removed people

Counts must remain truthful. Ten doctors means ten doctor figures. Label symbolic crowds illustrative if count is not literal.

## Backdrops

| Backdrop | Use |
|---|---|
| `paper` | Plain warm paper, neutral |
| `night` | Night pattern, navy tones |
| `city` | City skyline |
| `street` | Street with road, palms, skyline |
| `office` | Office grid with desks/windows |
| `field` | Green field with dots |

## What to Reject (`style-lock.json`)

- Generic card for every line
- Substituting an orb for every unseen noun
- Unmotivated floating props
- Photorealistic or glossy 3D additions
- Changing guide hair or clothing between lines
- Resetting an established place without narrative reason

## What to Preserve

- Cast identity
- Palette roles
- Slender character silhouettes
- Font hierarchy
- Publishing chrome
- Subtitle wording
- Script numbers and uncertainty

## Honesty

Pixel identity for scenes absent from reference cannot be verified or guaranteed. Compare actual result with supplied reference; do not describe a generic approximation as an exact clone. `style-lock.json` status: "Reference-informed reconstruction targets, not recovered original source parameters."
