# Props Reference — Turag Video Kit

All props are registered drawing functions in `engine/composer.js` (built-in) and `engine/custom-props.js` (AI-authored). Coordinates are local to each object's anchor (0,0 = ground/floor contact point). Design space: 960×540.

## Built-in Props (`composer.js`)

Registered via `TuragComposer.register(name, drawFn)`. List with `TuragComposer.propNames()`.

### People & Characters

| Prop | Purpose | Key Options |
|---|---|---|
| `person` | Articulated faceless character | `role`, `pose`, `variant`, `dir`, `visor`, `color`, `legColor`, `h`, `action`, `actions`, `attachTo`, `hand`, `socket` |
| `icon` | Tiny symbolic crowd figure | `color` |

Poses: `stand`, `walk`, `phone`, `point`, `raise`, `sit`, `type`, `sew`, `examine`, `take`, `wave`, `handover`, `push`, `pull`, `lift`, `place`, `drink`, `read`, `listen`, `operate`.

Roles: `guide` (recurring, vermilion accent), `extra`, `doctor`, `vendor`.

### Furniture & Environment

| Prop | Purpose | Key Options |
|---|---|---|
| `desk` | Work desk with monitor + seated person | `scale`, `color`, `ai`, `empty`, `monitor` |
| `chair` | Narrow outlined chair | `color` |
| `bed` | Simple bed frame | `w` |
| `monitor` | Computer monitor | `w`, `ai` |
| `building` | Building with windows + label | `w`, `h`, `label`, `blue` |
| `palm` | Animated palm tree | `h` |
| `skyline` | City silhouette | `y`, `col`, `nightMode` |

### UI & Information

| Prop | Purpose | Key Options |
|---|---|---|
| `label` | Text label | `text`, `size`, `color`, `align`, `maxWidth` |
| `card` | Panel card with wrapped text | `w`, `h`, `text`, `size`, `color` |
| `number` | Large hero numeric evidence | `text`, `label`, `w`, `size` |
| `bar` | Vertical bar | `w`, `h`, `color`, `text` |
| `grid` | Activating figure grid | `count`, `cols`, `active`, `color` |
| `box` | Simple box | `color`, `text` |
| `orb` | Animated blue orb | `r` |

### Specialized

| Prop | Purpose | Key Options |
|---|---|---|
| `calendar` | Calendar with date | `text`, `label` |
| `phone` | Phone device | `text`, `ai` |
| `chat` | Chat bubble panel | `text` |
| `atm` | ATM machine | `label` |
| `hospital` | Hospital building | `label`, `text` |
| `paper_stack` | Stack of papers | `count`, `w` |
| `shield` | Shield, optional crack | `cracked` |
| `robot` | Robot figure | — |

## Custom Props (`custom-props.js`)

~50 AI-authored props, bundled automatically. Full list:

| Prop | Purpose |
|---|---|
| `custom_machine` | AI machine with active/inactive cells |
| `asset_bubble` | Expanding red value bubble |
| `direction_arrow` | Bidirectional arrow |
| `cross_mark` | Animated red X mark |
| `survey_scale` | 0–100% slider with moving red indicator |
| `percent_column` | Filling percentage bar |
| `chat_screen` | AI chat interface with message states |
| `road_sign` | Green directional road sign |
| `workflow_strip` | 3-stage workflow panel (data → run → verify) |
| `stage_curtain` | Opening/closing stage curtain |
| `scaffold` | Construction scaffolding with orb |
| `task_bundle` | Task blocks splitting apart |
| `timebar` | Vertical animated time bar |
| `patient` | Medical patient icon |
| `task_matrix` | Grid of tasks activating over time |
| `rice_patch` | Rice field with cut-line animation |
| `rice_bundles` | Three rice bundles |
| `combine_live` | Combine harvester with rotating parts |
| `editing_timeline` | Video editing timeline with playhead |
| `code_panel` | Code editor panel with typing lines |
| `spotlight` | Spotlight beam polygon |
| `ledger` | Two-column accounting ledger |
| `newspaper` | Newspaper front page with headline |
| `four_cells` | 4-cell activation counter |
| `cloth_gripper` | Sewing machine cloth feed mechanism |
| `copy_network` | Copy distribution network |
| `recruitment_notice` | Hiring notice, optional closed state |
| `demand_flow` | Demand flow diagram |
| `history_ledger` | History vs accountant comparison |
| `village_hut` | Rural hut with roof |
| `health_route` | Healthcare route with dashed paths |
| `bounded_requests` | Request grid with active subset |
| `magnifier` | Magnifying glass |
| `podium` | Speaker podium |
| `attribution_folder` | Attribution folder with AI overlay |
| `rank_list` | Ranked list (AI at position 4) |
| `partial_picture` | Partial picture reveal |
| `late_report_wave` | Late data wave animation |
| `mobile_shop` | Mobile money shop front |
| `speed_bump` | Speed bump graphic |
| `audit_tasks` | Task audit with AI/human split |

## Vector Shapes API

For unseen props, use `type: "vector"` with `shapes` array. No SVG markup, scripts, or external resources — SVG path data only.

```json
{
  "id": "custom-obj",
  "type": "vector",
  "x": 400, "y": 455,
  "shapes": [
    {
      "kind": "path",
      "d": "M0 0 C20 -50 60 -50 80 0 Z",
      "fill": "#216E50",
      "stroke": "#12141C",
      "width": 2,
      "enter": 0,
      "exit": 4,
      "opacity": 1,
      "scale": 1,
      "rotation": 0,
      "translateX": 0,
      "translateY": 0,
      "keyframes": [ { "at": 0, "scale": 0 }, { "at": 1, "scale": 1 } ]
    },
    {
      "kind": "rect",
      "x": -10, "y": -10, "w": 20, "h": 20,
      "fill": "#FF3D17"
    },
    {
      "kind": "ellipse",
      "x": 0, "y": 0, "rx": 15, "ry": 10,
      "fill": "#2F3BFF"
    },
    {
      "kind": "line",
      "x": 0, "y": 0, "x2": 40, "y2": 0,
      "stroke": "#12141C", "width": 2
    },
    {
      "kind": "polygon",
      "points": [[0,0],[20,-40],[40,0]],
      "fill": "#216E50",
      "stroke": "#12141C"
    },
    {
      "kind": "text",
      "x": 0, "y": 0, "text": "এআই", "size": 24,
      "fill": "#12141C", "align": "center", "maxWidth": 200
    }
  ]
}
```

### Shape Fields

| Field | Applies to | Description |
|---|---|---|
| `kind` | all | `path`, `rect`, `ellipse`, `line`, `polygon`, `text` |
| `fill` | all | Fill color |
| `stroke` | path, rect, line, polygon | Stroke color |
| `width` | path, line, polygon | Stroke width |
| `d` | path | SVG path data string |
| `x, y` | rect, ellipse, line, polygon, text | Position |
| `w, h` | rect | Width, height |
| `rx, ry` | ellipse | Radii |
| `x2, y2` | line | End point |
| `points` | polygon | Array of [x,y] points |
| `text` | text | Text string |
| `size` | text | Font size |
| `maxWidth` | text | Max width for auto-shrink |
| `align` | text | Text alignment |
| `fillRule` | path | `nonzero` (default) |

### Shape Animation Options

| Field | Description |
|---|---|
| `enter` | Seconds relative to beat start when shape appears |
| `exit` | Seconds when shape disappears |
| `opacity` | 0–1 opacity |
| `scale` | Scale factor (>=0) |
| `rotation` | Rotation in degrees |
| `translateX, translateY` | Local translation |
| `keyframes` | `[{at, <prop>}, ...]` for numeric interpolation |

## Prop Rules

1. **Unique IDs** — every object in a shot needs a unique `id`.
2. **Registered types** — unknown prop types throw errors; register first or use `vector`.
3. **Finite coordinates** — `x` and `y` must be finite numbers.
4. **No floating props** — objects must sit on a surface, be held, or connect in a diagram.
5. **Held props** — use `attachTo: "person-id"`, `hand: "right"\|"left"`, optional `socket`.
6. **Deterministic** — all drawing from absolute time and stable data only.
7. **One semantic accent per action** — don't color everything blue or vermilion.
8. **Reuse silhouettes** — a simple accurate silhouette beats an unrelated generic icon.
9. **No orbs for unseen nouns** — draw the actual recognizable object.

## Adding a New Prop

1. Choose built-in prop if suitable, else register in `engine/custom-props.js`:
```js
R('my_prop', (c, t, o) => {
  const H = TuragScenes.helpers, P = TuragScenes.palette;
  H.rect(c, -30, -60, 60, 60, P.paper, P.ink);
  // deterministic drawing from local time t and object o
});
```
2. Test against a foreground character at crowd scale.
3. Validate in `composer.js` — registration throws on invalid args.
4. Document the prop's options and purpose.
