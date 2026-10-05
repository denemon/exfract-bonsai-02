# Stage 2 — volume before surface

Started 2026-10-04 16:58 JST. Midpoint due 19:58 JST. Previous stage is preserved, rejected, and not promoted.

## Diagnosis from actual source and clay images

The front and +25° views of stage-one v27 were inspected with its generator, alongside the selected PC reference. The original attached bonsai image was also actually viewed earlier in this session. Hidden surfaces remain inferred.

- **Cross-section:** one elliptical section moving along a single centreline produces a broad, nearly uniform face. Longitudinal grooves divide that face into a corrugated sheet without changing its basic mass. The texture-free view still reads as a ribbon.
- **Torsion:** rotating groove angles changes surface lines, not the spatial relationship of different woody lobes. Front and rear growth masses need different paths and changing overlap.
- **Curvature and thickness:** previous tighter curves folded their inner offset. Clamping that offset made a clean surface but flattened the intended bend. A volume field has no offset surface that can fold through itself.
- **Branch joints:** a hard voxel union followed by small global smoothing preserved an abrupt shoulder at each branch. It was topologically connected, but did not look grown. Branch origins need broad, locally controlled blending into the supporting trunk mass.
- **Roots:** four similarly tapered fingers around the stump looked attached and repetitive. A dominant lateral buttress, front root flare and smaller rear supports need unequal depth, direction and soil contact.
- **Silhouette:** repeated branch zigzags and the single long blank trunk curve are too regular. Primary branches need individually authored bends, taper, depth and unequal weight before any terminal twigs are added.
- **Foliage (deferred):** repeated fine fans in v27 make thin feathery layers. The later canopy must develop compact, irregular groups from branches and twigs, with depth and intervening openings.

## Changed construction

This candidate does not reuse the former lofted trunk. It uses a signed volume field. A small set of authored, overlapping growth masses describes the root flare, a rear structural trunk, a distinct front deadwood mass, an integrated right growth mass, the upper fork and primary branches. Smooth distance unions blend each junction over a chosen physical width. A marching-cubes isosurface creates one solid skin; there are no independent applied bark cords and no ribbon offset operation.

Only the pot, planted substrate and bearing stone from v27 are reused as a fixed scale reference. They are read from the preserved file and copied into the new candidate. The initial pass has no leaves, grain, bark colour, cavities, architectural additions or surface displacement. Broad erosion will be introduced only where the positive masses call for it, and must remain convincing in clay.

The initial field is a 224³ rectangular sampling grid (approximately 14 × 7 × 9 mm in authoring units), extracted by the already installed Three.js marching-cubes implementation. Smoothing is limited to sampling artifacts. A coarse mesh budget of 150k triangles is a ceiling, not a target. The editable file retains named control paths and the extracted skin.

## Composition and gate

The fixed authoring soil height remains 0.393. The runtime world scale remains 0.66, making the pot approximately 1.06 m wide. The canopy will later spread roughly 1.7× pot width. Principal wood masses bend in depth as well as across the front view, with a thicker lower trunk, unequal rooted base, broad left branch shoulder and returning upper fork.

Compare v27 and the new coarse model using uniform clay, unchanged light and a shared camera envelope at 0°, -25°, +25° and +45°. Also inspect a trunk close view. The gate passes only if the trunk reads as a solid old tree in these views, roots grow into the soil, and primary branches emerge continuously. A watertight mesh, high polygon count or successful build does not pass this gate. If the first method still reads as a worm, pipe or ribbon, change the mass layout or field construction before adding detail.

After this gate: sculpt selective broad weathering and deadwood edges; define living wood on the same surface; then construct branch-led foliage with view-dependent detail if necessary. Stage-one PC GPU median was 17.45 ms, so geometry cannot grow without a measured budget. Background refinement remains blocked on the hero shape gate.

## Preserved constraints

No Git writes, publication, purchases, Library retry or old-project changes. All candidates remain in this run. GPT-6 Astra / max was requested; the execution tools do not expose runtime model identity, so it remains unverified. Midpoint and final reports will distinguish technical verification from aesthetic acceptance. Final deadline: 2026-10-10 23:00 JST.
