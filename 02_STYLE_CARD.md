# Visual grammar — Turag reference

This is a reconstruction guide, not the original author's source specification. Observations come from the supplied 1280 × 720 video, all nine existing chronological video-2 contact sheets, full-size frames at 12 and 28 seconds, and character crops. Numerical geometry is an approximate drawing target. See `reference/analysis/` for the exhaustive decoded-frame audit.

## Recognizable identity

Flat editorial illustration on warm paper; unusually slender faceless people; heavy condensed Bengali type; cream, navy, grey, vermilion and electric blue; print-like halftone; a persistent fine publishing frame. Each scene illustrates a specific narrated mechanism. A sequence of centered headings is insufficient.

Most scenes leave a large quiet upper area. People and furniture share a low baseline. Diagrams and numeric evidence occupy the space above. Objects appear, transform and disappear while the environment remains continuous. Navy scenes concentrate in the night office, personal editing desk and empty-workstation argument. Countryside and garment sequences introduce green.

## Palette

These implementation tokens approximate the reference. Compression and texture change sampled pixels; they are not recovered original hex values.

| Role | Target | Use |
|---|---|---|
| Paper | `#E9E4D2` | Main background, signs, screens, light clothes |
| Ink / night | `#12141C` | Type, shadows, dark environments |
| Vermilion | `#FF3D17` | Guide shirt, sun, risk, emphasis, subtitle edge |
| Electric blue | `#2F3BFF` | AI, active screens, machine parts, automation |
| Slate light | `#A5A7B8` | Distant buildings, pale cast |
| Slate medium | `#6B6E85` | Clothing and furniture |
| Slate dark | `#3A3C4E` | Buildings, trousers, panels |
| Green | `#1F7A4D` | Agriculture, boards, signs, some clothing |
| Sand | `#CDBFA3` | Distant day skyline, paper variants |

Use one semantic accent per action. Blue does not color all secondary text. Vermilion does not border every prop. Human skin is abstract grey, not realistically shaded.

## Stage and composition

Design at 960 × 540 and scale uniformly to 1280 × 720 or 1920 × 1080. Draw chrome and subtitles after world/camera transforms.

| Region | Approximate design-space target |
|---|---|
| Corner registration marks | Centers near (23,23), (937,23), (23,517), (937,517) |
| Chapter tag | Begins near (55,55); tiny boxed number and short label |
| Top progress rule | 1–2 px high, vermilion, proportional to episode time |
| Main safe area | x 55–905, y 90–465 |
| Common floor baseline | y 430–465, depending on scene |
| Subtitles | Lower band around y 486–518, horizontally centered |
| Swatches | Four tiny squares near x 43–90, y 512 |
| Episode/scene counter | Small low-contrast mono at lower right |

The supplied detail frames show `EP.03`; the old toolkit's fixed `EP.01` was not a reliable transcription. Use current episode metadata.

Street depth: pale skyline → palms, mosque/tower and wires → back sidewalk walkers → road/traffic → foreground guide and tea stall. A simple comparison can use only a floor rule, two groups and a caption. Preserve intentional negative space.

## Material and marks

- Paper has soft uneven tone, sparse fibres and a weak vignette. Cache a seeded texture so it does not flicker.
- Halftone has geometric dots and a visible spacing/size gradient: lower sun edge, screen halo, field foreground or transition edge. Avoid a soft bloom on everything.
- Night offices use restrained navy layers, sparse cream windows and a faint patterned floor.
- Bodies and buildings use flat fills. Fine strokes belong to furniture, windows, props, diagrams and registration marks.
- Card shadows are short hard offsets; people have low flat oval shadows. Avoid bevels, photographic light, glossy 3D and rounded dashboard cards.
- Occasional color misregistration is deliberate, not applied to all text.

## Typography

Anek Bangla, Hind Siliguri and Space Mono were named by the prior toolkit; they are reconstruction choices, not verified original font identities. Use bundled local fonts. Heavy condensed Bengali is for hero lines; clear semibold Bengali for captions; tracked Latin mono for metadata.

| Role | Practical size at 960 × 540 |
|---|---|
| Opening headline | 54–84 px, one or two short lines |
| Large numeric evidence | 72–118 px; fit the actual digits |
| Diagram labels / local titles | 18–34 px |
| Subtitle | 18–20 px |
| Chapter label | 11–14 px |
| Mono metadata | 8–11 px; nonessential information only |

The old minimum of 70 px for every headline was too rigid. Measure after fonts load. Fit by shortening the on-screen summary or splitting it, not squeezing full narration into a title. Preserve Bengali grapheme clusters; never letter-space Bengali body text. Test চাকরি, প্রশ্ন, স্বাস্থ্য, প্রযুক্তি and সংখ্যা. Missing glyph boxes are a failed render.

Subtitles are exact script excerpts, normally a short white line inside a tightly fitted near-black rectangle with a thin vermilion left edge. Split long sentences into timed readable chunks. A two-line fallback is better than unreadably small type. Keep the bar within the safe frame and away from the key action.

## Emphasis and evidence

Observed devices: giant Bengali total in an ink box with red offset edge; red percentage; cream figure grid; newspaper headline; dashed ellipse; blue active cells; green check; empty outlined positions; faded removed people. Choose the device that explains the line.

Counts must remain truthful. Ten doctors means ten doctor figures. Label symbolic crowds illustrative if their count is not literal. Automating 40% of tasks does not mean eliminating all jobs. Supplied script claims are not independently verified research. Preserve wording, units and uncertainty; never invent source citations.

## Motion

Observed categories: horizontal camera travel; walking silhouettes; increasing counters; staggered cells; diagrams assembling; task colors turning blue; fading figures/empty positions; short focus push; blue/green wipes; halftone sweeps. Exact easing constants are not recoverable from these images; the following are reconstruction settings.

| Action | Suggested timing |
|---|---|
| Caption/card reveal | 0.25–0.45 s, cubic ease out |
| Concept assembly | 0.5–1.2 s, 0.04–0.10 s stagger |
| Focus settle | Scale 1.02–1.04 to 1.00 over 0.4–0.7 s |
| Graphic wipe | 0.35–0.65 s |
| Walking | About 1–1.5 cycles/s, opposing arm/leg phases |
| Reading hold | Long enough for the actual words, no perpetual bouncing |

A new subtitle does not require restarting the environment. Use sentence/action cues within a continuous scene. Do not crossfade every cut. Directly seeking time t must reproduce the frame reached by playing to t.

## Audio evidence

The supplied video2.mp4 has no audio stream. Its sound design cannot be recovered from that file. The supplied MP3 is the master clock. Quiet ticks, low stamps and brief noise whooshes are optional design choices, not observed sound evidence. Keep narration intelligible and inspect the final mix. Do not add a constant beat or loud chimes by default.

## Expanded source evidence

Read `09_REFERENCE_KNOWLEDGE.md` and the all-file folder audit for the latest evidence from all 341 supplied 1080p stills and 19,115 extracted 720p frames. Use the full-resolution images to match staging, supporting detail and negative space, not only the palette. Camera and object keyframes can reproduce the observed grammar of pans, close-ups and state changes.

## Source-video audio measurement

The original `video.mp4` includes audio. FFmpeg volumedetect measured mean level −17.7 dBFS and peak −1.3 dBFS for its combined audio track; see `reference/video1/audio-analysis.log`. This is a signal measurement, not LUFS, a separate narration measurement, or a perceptual classification of effects. `video2.mp4` contains no audio. Keep the supplied new narration as the timing master and check its actual level independently.
