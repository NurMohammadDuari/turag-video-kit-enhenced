# Character specification

Primary evidence: `reference/characters/chars_v1.jpg`, `chars2.jpg`, and full-size scenes. `chars3.jpg` mostly shows field texture and subtitles, so it is not an anatomy reference. Reusable implementation: `engine/characters.js`. Review sheet: `engine/character-sheet.html`.

## Corrections to the earlier toolkit

These are not circles on sticks. Crops show a short narrow neck, sloped shoulders, long narrow tunic-like torso, tiny profile nose, asymmetric hair, jointed thin arms, long legs and small flat shoes. The old statement “no neck” was wrong. Not everyone wears a blue visor: some have a cream strip and many have none. Avoid detailed eyes, mouth, fingers, muscles or realistic facial shading.

The guide is a recurring vermilion accent, not compulsory in every scene. Office, medical and garment groups can consist entirely of supporting cast. Vary clothing and hair, without changing the underlying proportions.

## Standing proportions

H is hair-top to sole. These are approximate drawing targets from crops, not measurements of an original rig.

| Landmark / width | Fraction of H |
|---|---|
| Hair top to chin | 0.10–0.13 |
| Neck | 0.025–0.045 |
| Shoulder to hip / long shirt hem | 0.30–0.38 |
| Hip to sole | 0.46–0.54 |
| Shoulder width | 0.15–0.19 |
| Waist width | 0.10–0.14 |
| Head width | 0.08–0.11 |
| Upper arm / forearm thickness | 0.027–0.040 |
| Thigh / shin thickness | 0.040–0.060 |
| Shoe length | 0.10–0.15 |

These overlap: hair covers head, neck enters torso, legs start inside the shirt. Rounded trouser tops can visibly overlap the hem. Broad square shoulders and large circular heads immediately change the style.

## Shapes and drawing order

1. Flat low-opacity ground ellipse, roughly 0.25H wide and 0.025H tall.
2. Rear hair/head covering, far arm and far leg.
3. Torso with sloping shoulders, slight taper and subtly curved or angled hem.
4. Near leg/shoe, near arm and tiny hand.
5. Neck and narrow oval/profile head; asymmetric hair/cap and optional visor.
6. Held prop attached to the actual hand endpoint.

Hair is a dark swept cap or a longer shape behind the neck. Keep the face blank. Shoes are low rounded rectangles aligned to ground, not circles. Use jointed paths/capsules for limbs and maintain continuity at elbow and knee.

## Cast

| Variant | Construction |
|---|---|
| Guide | Vermilion long top, charcoal trousers/shoes, dark grey face, swept hair, occasional blue visor/phone |
| Office extra | Slate top/trousers with subtly different values; short hair, bun, long hair or cream cap |
| Cream panjabi | Long cream tunic, narrow dark legs, optional cream skull cap |
| Dress / kameez | Long slender skirt, slight flare, narrow red hem, visible shoes, long hair or head covering |
| Vendor / rural worker | Cream top, restrained red scarf/check marks, dark or green lower garment |
| Doctor | Cream coat-like torso, dark trousers, clipboard/tablet; prop/environment establish role |
| Garment worker | Grey/cream top, seated pose, hands toward sewing machine |

At crowd scale remove detail before enlarging the head. Tiny grid icons are symbolic marks and should not replace a foreground character.

## Poses

Every pose depends only on time and a stable character seed. Clothing must not randomize per frame.

- Stand: almost vertical weight, relaxed knees, arms down or one elbow bent; little bobbing.
- Walk: opposite legs form an X at midstep, knees bend slightly, arms counter-swing; feet contact the floor, face follows travel.
- Phone: bent elbow and forearm toward a small blue phone; head aims at the screen; prop stays attached.
- Point: shoulder fixed, forearm aims at the actual target; hand outside torso silhouette.
- Raise: diagonal arm above head, still joined at shoulder.
- Carry: forearms meet a cream box's edges while legs walk beneath it.
- Sit/type: thigh horizontal, shin vertical, shoe on floor; forearm reaches keyboard; slight forward lean.
- Rest/hammock: connected long body pose, head near hand; do not simply rotate a chair pose.
- Field work: hip hinge and bent knees, hand reaches rice; modest phase variation across people.

Mirror geometry with facing direction. Draw any readable prop text separately so lettering does not mirror.

## Furniture alignment

A seated person, chair and desk share one floor baseline. At standing scale H=150 design px, a useful seat height is 60–70 px and desk height 95–110 px. Fit visually: H is the body scale, not the sitting figure's literal height. The chair is narrow outlined furniture. The monitor has a dark bezel, cream/blue screen, small stem and flat foot. Check feet against floor, thighs against seat and hands against keyboard.

## Public API

```js
TuragCharacters.draw(ctx, {
  x: 240, y: 440, h: 165,
  role: 'guide',          // guide | extra | doctor | vendor
  pose: 'phone',          // stand | walk | phone | point | raise | sit
  t: 2.5, variant: 0, dir: 1,
  visor: true             // false or a color string also accepted
});
TuragCharacters.seated(ctx, options);
TuragCharacters.icon(ctx, x, y, h, color);
```

Optional color, legColor and alpha override appearance. Use actual current implementation for supported options. More elaborate carrying, lying or field poses can be composed in a scene or added to this shared rig; do not claim an unimplemented pose is exposed by the API.

## Review

Inspect foreground and crowd scale: standing, walking, sitting, phone, pointing, dress, cap, doctor and vendor. Compare silhouette first: head size, torso width, leg length, shoulder slope, attachment and shoe direction. Then inspect in the night office and street. The rig is reference-informed, not recovered source code or proof of pixel equivalence.

## Identity across a new script

The guide is locked to variant 0 in the shared rig even if an individual shot supplies a different hair variant. Keep a named episode cast and preserve recurring extras as well. The image-folder evidence shows tiny blue phones, bent elbows, feet on a common floor and seated hips aligned to narrow furniture. Compare those contact points at full size. See `reference/folder_audit/frames/fullsize/f_0010.jpg`, `f_0023.jpg`, `f_0082.jpg`, `f_0122.jpg`, and `f_0319.jpg`. These are visual anchors, not exact recovered geometry.
