# Bonsai structural prototype — 2026-10-04

This isolated prototype preserves the 09:00 implementation in the parent project. It is a candidate for visual review, not an adopted production version. No visible text is rendered in the scene.

## Local use

With Node and the pinned dependencies installed, run `npm run dev -- --port 5184 --strictPort`. Build with `npm run build`, then run `npm run preview -- --port 5185 --strictPort`. All model, decoder and fallback assets are local; the application makes no remote requests.

## Original model

`public/models/bonsai-structural-study.glb` contains the original tree geometry, wood flow maps and foliage. Editable Blender files and the deterministic generators are in `../sculpt/`. The generator authors the root flare, noncoplanar trunk, irregular shari recess, unequal forks and branchlet/foliage hierarchy, then exports a Draco-compressed GLB with embedded WebP maps. No purchased or downloaded 3D asset is used.

The source reference is the user's attached bonsai photograph, visually inspected in the conversation. The current color direction is warm gray-brown deadwood and reddish living bark.

## Rendering and accessibility

Three.js WebGL2, ACES output, static shadows, restrained screen-space contact shading. Portrait cameras are authored separately. `prefers-reduced-motion` stops the animation loop. The completed candidate scene remains as a responsive static image while loading, if WebGL2 is unavailable, or during context loss.

## Third-party code

Three.js 0.185.1 is MIT licensed. The Draco decoder distributed with Three.js is Apache-2.0 licensed; its README, full license, WASM and JavaScript decoder are in `public/draco/`. The decoder is served locally.

## Review status

See `../REPORT.md` and `../comparison.html` for the actual visual decision, limitations, browser measurements and preservation checks. Test success does not establish the requested artistic quality.
