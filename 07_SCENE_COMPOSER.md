# Script line → original composed shot

The AI reading this kit is the creative planner. It reads the supplied script, understands each line, and authors `shot` data. The renderer executes that data with the same shared art system. There is no hidden model API and no promise that a rule-based Python utility understands arbitrary stories. The included `compose_episode.py` only supplies editable starting suggestions; its output requires semantic review by the AI before final delivery.

Every narration cue must have its own beat with `scene: "compose"`, `cueIndex`, the exact `scriptLine`, `visualIntent` explaining the image, and `shot`. Short lines may reuse the previous environment and cast while changing their action, framing or prop state. They still own a separate shot. Do not route the line to one of the legacy full-scene renderers. Those are reference examples for visual construction.

The AI does the following autonomously for every line:

1. Identify literal nouns, actors, action, setting, quantities, negation and metaphor. Quote the relevant words in `visualIntent`.
2. Choose the backdrop and place objects with a clear reading order. Show the meaning rather than putting the entire narration on a card.
3. Reuse props when appropriate. Add a custom prop for a new noun. Preserve silhouette language, palette, grain, typography, scale, and character proportions.
4. Time entrances and action to that line's audio. Inspect the rendered start, middle and end. Correct collisions, text fitting and semantic mistakes.
5. Ensure every cue maps to exactly one shot, build the portable HTML, run QA, and render the complete video. Deliver the MP4 and editable scene graph.

## Declarative shot example

```json
{
  "id": "line-001", "t0": 0, "t1": 6,
  "scene": "compose", "cueIndex": 0,
  "scriptLine": "নতুন নিয়োগ না হলে চেয়ারটা খালিই থাকে।",
  "visualIntent": "নিয়োগ না হলে: an empty chair beside an unattended desk; a worker leaves the frame.",
  "chapter": 1, "chapterTitle": "চাকরি",
  "shot": {
    "backdrop": "office",
    "objects": [
      {"id":"vacancy", "type":"chair", "x":520, "y":455},
      {"id":"workstation", "type":"desk", "x":640, "y":455},
      {"id":"departing", "type":"person", "x":240, "y":455,
       "role":"extra", "pose":"walk", "variant":2,
       "motion":{"kind":"walk", "speed":-30}},
      {"id":"notice", "type":"label", "x":620, "y":210,
       "text":"নিয়োগ বন্ধ", "size":35, "enter":0.4}
    ],
    "links": []
  }
}
```

## API and layout

`engine/composer.js` registers `compose` with the shared renderer. `TuragComposer.register(name, drawFunction)` extends the prop vocabulary. Put reusable new functions in `engine/custom-props.js`; the builder bundles this file automatically. `TuragComposer.propNames()` lists available types. Unsupported props throw errors instead of silently producing a generic scene.

All coordinates use 960×540. Reserve y=485–518 for subtitle bars, and top-left for chapter chrome. Most objects use ground anchor y=455. A person of height 180 extends upward from its anchor. Draw with no external dependencies, faceless articulated figures and existing colors/fonts. Do not bake subtitles or chapter chrome into props.

Backdrops: `paper`, `night`, `city`, `street`, `office`, `field`. The backdrop establishes an environment; its objects and story are composed separately. Set `floor:false` or `floorY` if needed.

Objects require unique `id`, registered `type`, finite `x`,`y`. Optional `scale`, `rotation` in degrees, `z` painter order, `opacity`, `enter` and `exit` in seconds relative to beat start, `reveal` duration, `revealFrom` vertical reveal offset. Motion is `{kind:"walk",speed:18}` or `{kind:"float",speed:2,amplitude:4}`. For a more specific action, draw a custom prop from absolute time and the object's own data. Do not accumulate state.

Props: `person`, `desk`, `chair`, `calendar`, `phone`, `chat`, `atm`, `hospital`, `bed`, `paper_stack`, `orb`, `monitor`, `palm`, `building`, `shield`, `robot`, `label`, `card`, `number`, `bar`, `grid`, `box`, `vector`.

Person: `role` guide/extra/doctor, `pose` stand/walk/phone/point/raise/sit, `h`, `variant`, `dir`, optional `visor`. Calendar and chat: `text`, optional `label`. Labels: `size`,`color`,`align`,`maxWidth`. Card: `w`,`h`,`text`,`size`. Grid: `count`,`cols`,`active`,`color`. Bars: `w`,`h`,`color`,`text`. Desk/monitor: `ai`. Shield: `cracked`. Hospital/building: `label`. These are independent objects; combine as many as the story actually needs.

Links: `{from:"object-id",to:"other-id",fromDy:-60,toDy:-60,color:"#2F3BFF",width:2,dashed:true}`. They draw behind objects. Do not connect objects without a meaningful relationship.

## Unseen objects

Vector artwork now supports `{"kind":"path","d":"M0 0 C20 -50 60 -50 80 0 Z","fill":"#216E50","stroke":"#12141C","width":2}`. SVG path data permits curves and complex silhouettes without installing a new scene template. `fill:"none"` draws only the stroke. Each shape can have `translateX`, `translateY`, `rotation`, `scale`, `opacity`, `enter`, `exit` and numeric `keyframes`; these run in the parent object's local time. Split an unfamiliar object into independently moving parts. A hinged arm, spinning dial or bending leaf can therefore animate inside one reusable vector prop. SVG markup, scripts and external resources are not accepted as path data.

For recurring characters, put identity fields in the episode's `cast` map, e.g. `"cast":{"host":{"role":"guide","variant":0,"color":"#FF3D17","legColor":"#272A3A"}}`. A person with `"castId":"host"` inherits those fields. The builder rejects conflicting shot identity or identity changes in keyframes/action tracks. Stage position, height, action, facing and camera remain scene-specific. Use a distinct named costume identity for deliberate wardrobe changes.

Either register a new drawing function, using `TuragScenes.helpers` and the existing rig, or use `type:"vector"` with `shapes`. Supported shapes are `rect` (x,y,w,h), `ellipse` (x,y,rx,ry), `line` (x,y,x2,y2,width), `polygon` (points), `text` (x,y,text,size,maxWidth). Shapes accept `fill`, and where applicable `stroke`. Coordinates are local to the object's anchor. Use simple flat silhouettes, restrained halftone and the existing palette. The primitive vocabulary allows new props without adding a canned scene type.

An astronaut, sewing machine, combine harvester or cooking pot is not an excuse to substitute an orb. Draw its recognizable silhouette and relevant action. Inspect it next to source characters at equivalent scale. Keep it reusable by naming parameters for its content and state.

## Reproducible commands

```sh
python3 tools/prepare_episode.py --script script/new.md --audio audio/new.mp3 --output episodes/new.json
# AI authors/refines every shot in episodes/new.json, adds any custom props.
python3 tools/build_episode.py episodes/new.json --output engine/new.html
node tools/qa_episode.js engine/new.html output/new-qa
node tools/render_mp4.js engine/new.html audio/new.mp3 output/new.mp4 --workers 1
```

The shared look is enforceable through the drawing system and visual review. Pixel identity for scenes absent from the reference cannot be verified or guaranteed. Compare the actual result with the supplied reference; do not describe a generic approximation as an exact clone.

## Directed action and camera keyframes

Objects now accept `keyframes`, with local shot seconds in `at`. Numeric attributes interpolate with cubic easing. Example: `{"keyframes":[{"at":0,"x":180},{"at":2,"x":420},{"at":4,"x":420}]}`. The base object supplies unchanged attributes. This can animate x, y, scale, rotation, opacity or prop-specific numeric state such as bar height. Include an explicit first keyframe when the starting value matters.

`shot.camera` accepts `x`, `y`, `zoom` and optional `keyframes`. Example: `{"x":480,"y":270,"zoom":1,"keyframes":[{"at":0,"zoom":1},{"at":2,"x":600,"y":330,"zoom":1.35}]}`. The camera changes the illustrated world; chapter chrome and subtitles remain fixed. Keep the intended action inside the final crop.

The importer marks draft plans `planningStatus:"scaffold"`. Only an AI-reviewed plan marked `planningStatus:"authored"` builds. Follow `08_DIRECTOR_RULES.md`; the user should not have to edit that plan themselves.

## Expanded reference props

`tea_stall` (optional label), `rickshaw`, `window` (w,h,night), `fan`, `plant`, `television` (cells,cols,active,ai), `filing_cabinet`, `clipboard` (checked), and `conveyor` now draw supporting detail independently of any scene template. Set a ceiling fan's anchor near y=100–150; set ground furniture and vehicles near the common baseline. Size each prop in relation to the character. Do not use the isolated prop QA montage as a final scene composition.

## Held items and current engine fixes

Use `attachTo:"actor-id"`, `hand:"right"` (or `"left"`) on an independent prop to anchor it to that actor's actual reachable hand. The actor must be a root `person`. The prop's x/y are pixel offsets from the wrist, not world coordinates. Set a z above foreground furniture when the item is held above it. Parent visibility and opacity are inherited. The wrist accounts for actor height, facing, rotation, scale and gait; the prop's own rotation/scale remain independently controllable.

When supplying a separate crop bundle, cloth, file or phone, set `autoProps:false` on its person to suppress the carry action's default envelope or phone action's built-in handset. This changes the artwork only; wrist contact geometry remains the same. Desk and chair props accept `color` for readable thin furniture strokes in night scenes.

Numeric keyframes retain earlier values when later frames key a different property. Explicit zero scale/speed are supported. `instant:true` renders an object fully at its entry; use it for a background or held cut, so every shot does not start with an empty fade. Links remain hidden until both endpoints are visible. Current engine regressions are tested by `npm test`.
