# Bonsai volume study / stage 2

This is a local, text-free, real Three.js scene and editable Blender sculpture. It is a **work-in-progress candidate, not an accepted premium garden**. Read `REPORT.md` and open `comparison.html` first. Protected root 09best and the initial archive were not replaced.

## Run the saved site

The current production preview on this Mac is `http://127.0.0.1:5190/`. This URL is local to the Mac.

From `site/`, the existing workspace dependencies resolve from the project root. In an independent copy, install the exact dependencies from `package-lock.json` with `npm ci`, then run:

```
npm run build
npm run preview -- --port 5190
```

The site has no visible text or UI controls. Drag gently to inspect; wheel or two-finger pinch approaches the tree; double-click resets. Reduced-motion preference suppresses these camera gestures. The camera otherwise stays still and the renderer has no continuous animation loop. Loading starts with a small embedded render, then the full-resolution still, then actual 3D. WebGL loss/unavailability retains the same candidate still.

## Edit and reproduce the model

- `models/hero-v23-editable.blend`: native full-resolution model, named growth control paths, closed primary wood surface, linked shoot prototypes, individually placed instances. Runtime-only low-detail templates are hidden in a separate collection.
- `models/hero-v23.glb`: 2,834,228-byte compressed runtime shape, flow coordinates, material masks and instancing.
- `models/hero-v20.blend`: coarse volume before fine relief, canopy and substrate detail.
- `models/hero-v23.canopy-topology.json`: twig parents, positions, foliage attachments and prototype construction counts.
- `sculpt/`: authored field, extraction, assembly, relief, canopy, leaf and substrate source.

Blender 5.2.1 LTS, Python 3.12 + NumPy, Node 24.9, Three 0.185.1 and Vite 8.2.2 were used. The Python entry points reject an already existing version. Always choose a fresh version and work in a new run when continuing.

To refine the included coarse volume, from this run directory:

```
/Applications/Blender.app/Contents/MacOS/Blender --background --factory-startup --python-exit-code 1 --python sculpt/refine.py -- --base models/hero-v20.blend --out models --version v24 --foliage
```

This generates and installs the new GLB into this run's `site/public/models/hero.glb`. It does not modify the protected root site. The `sculpt/build.py vNN --support models/hero-v20.blend` entry point can rebuild a fresh coarse field using the included pot/support. Its support argument was made portable after the saved v20 generation; that new command has not been used to claim another tested model. `models/hero-v20.field.f32.gz` and `.triangles.f32.gz` retain the exact sampled arrays; `.archive.json` records their uncompressed SHA256.

Native Blender previews and bare GLB material previews **do not reproduce the custom browser wood shader**. `COLOR_0` is mask data: R living wood, G/B variation, A ambient visibility. UV layers encode growth flow and direction. The browser enforces opacity 1 and uses A only for indirect light. Keep `site/src/materials.js`, the authored wood data texture and `foliage-lod.js` with the asset. No generated reference photo is used to impersonate 3D.

## Verification

`qa/final-production/` contains the final functional report and PC/390/320/tall/retina, inspection and fallback screenshots. `qa/final-gpu/` contains actual WebGL GPU timer measurements on the Mac. These are not physical-phone tests. `qa/final-comparison/` contains neutral-clay and material comparisons. `qa/final-still-source/` contains the six unedited WebGL screenshots used for fallback assets.

From `site/`:

```
QA_URL=http://127.0.0.1:5190/ QA_OUT=../qa/new-verification node scripts/verify.mjs
```

The verifier intentionally checks the saved v23 and its six crowns / 72 foliage instance groups. Update the expected candidate only when changing the model and saving a new run. The capture script also supports `QA_EXPECT_VERSION=v23`; never label images from a failed export as a new model.

The background remains a scaffold. Appearance acceptance, Safari, real phones and sustained thermal performance are pending. Library transfer was blocked by the previously reported official helper TLS failure; no upload ID exists and no retry was made here. Push, PR, merge, publication and purchases were not performed.
