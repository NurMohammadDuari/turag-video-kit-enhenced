# Give this toolkit to an AI

## What you give it

1. Extract the **whole toolkit ZIP**. Keep its folders together, especially `reference/`, `engine/`, `assets/` and `tools/`.
2. Open the extracted `turag-video-kit` folder in a coding AI that can read local files, view images, edit code and run terminal commands. This is the recommended way for a large toolkit. If you use a chat upload instead, the AI must be able to extract the ZIP and execute the renderer; attaching files to a text-only chat is insufficient.
3. Put your new timestamped script and matching narration in the folder, or attach both files to that AI. Give it their exact filenames. You do not need to describe scenes or choose templates.
4. Paste the prompt below. Replace the two input paths with your files.

## Copy this prompt

```text
Use this entire toolkit to make my COMPLETE animated video.

Script: script/my-script.md
Audio: audio/my-narration.mp3
Output name: my-video

Read AGENTS.md and REFERENCE_FIRST.md first, then 01_MASTER_PROMPT.md,
07_SCENE_COMPOSER.md, 08_DIRECTOR_RULES.md, 09_REFERENCE_KNOWLEDGE.md,
10_AUTONOMOUS_DIRECTOR.md, 11_ANIMATION_DIRECTOR.md and HOW_TO_USE.md.
Inspect the actual bundled reference images. They define the look I want.

Understand my whole script, including negation, numbers and cause and effect.
Author one original compose beat for every timestamped cue. Decide the setting,
characters, props, actions, diagrams, camera and transitions yourself. Create
missing artwork and actions when a scene is new; do not recycle fixed templates
or copy the example episode's content. Preserve consistent cast proportions,
colours, environments, Bengali typography and the reference animation grammar.
Use blue chapter cards where the script changes chapter.

Animate what the narration calls for: motivated hands and body movement, gaze,
anticipation, prop contact, weight, follow-through and secondary motion. Keep
held objects attached to the correct hands. Avoid repetitive idle movement.

Inspect every shot against suitable references and its script cue. Review
start/action-peak/end and five-phase animation boards, fix visible errors,
then record honest review notes. Do not mark a scaffold or an unseen shot
approved. Run the director audit and the guarded finish workflow with a fresh
review receipt. Render the entire audio duration, not a one-minute preview.

Deliver the full MP4, portable offline HTML, editable JSON, updated reusable
artwork, subtitles and brief usage notes. Verify the encoded video. State any
remaining visual differences or approximate timing honestly. Make routine
creative decisions autonomously; ask only for genuinely missing inputs.
```

## Your script format

Save as UTF-8 `.md` or provide `.srt`. Timestamps must match your narration:

```text
[00:00–00:04] প্রথম বাক্যের ভয়েসওভার।
[00:04–00:09] পরের বাক্যের ভয়েসওভার।
[00:09–00:14] এরপর যা বলা হবে।
```

Continue to the end of the audio. Use explicit chapter headings if you want specific chapter titles. Otherwise the AI infers chapter breaks. Short cues allow more precise scene changes; do not invent timecodes that disagree with the recording.

## What the toolkit does—and what the AI does

The toolkit supplies local reference evidence, a shared character rig, drawing tools, deterministic animation, rendering and validation. **The AI is the director:** it interprets each line, creates scenes and extends the artwork. This is not a standalone model that understands a script merely by running the importer. No external image-generation subscription is required for the bundled vector renderer.

The coding environment needs Python 3, Node 22.12+, Chrome/Chromium and FFmpeg/ffprobe; the AI runs `npm ci` for dependencies. Installation may require internet. Built players contain local artwork, fonts and audio and work offline. Compute or model usage costs depend on the AI environment you choose.

A prompt cannot guarantee identical quality from every AI. The actual references and visual review are essential. New scenes can follow the same visual language, but this reconstruction does not guarantee pixel-identical artwork or automatic word-perfect audio alignment.

## Where to find the result

For the prompt above: `output/my-video.mp4`, `engine/my-video.html`,
`episodes/my-video.json`, and `output/my-video-handoff/`.
Open the MP4 to watch or publish; open the HTML to preview and seek; keep the
whole folder to edit or make your next episode. For a revision, give the AI
the project plus the affected timestamps and ask it to repair, re-review and
render again. Do not reuse a previous review receipt after edits.

The supplied full-episode example is `episodes/ep02-full-directed.json`.
Its authoring script is specific to that episode; running it is not the way
to create a different story. Start new inputs with `tools/prepare_episode.py`
and follow `HOW_TO_USE.md` instead.
