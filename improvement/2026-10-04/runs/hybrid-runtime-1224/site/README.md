# Bonsai courtyard — constrained view candidate

A text-free blue-hour courtyard, built from five coherent generated compositions. The full image is the first and persistent visual layer. Fine-pointer desktop interaction adds a small perspective relief, with the far reference plane fixed and a maximum displacement of approximately 1.4 CSS pixels at 1440 × 900. There is no orbit control, zoom, idle camera movement, or touchscreen camera gesture.

This is an image-based hybrid, not a reconstructed bonsai mesh. Its shallow continuous relief is deliberately suitable only for minute motion. The independently generated views have minor surface-detail differences; they must not be exposed as a freely navigable 3D object.

## Run locally

Use the pinned dependencies in `package-lock.json` (`npm ci` in an independent checkout). Run `npm run dev` for local development, or `npm run build` followed by `npm run preview` for the production build. Both bind only to `127.0.0.1:5187`.

With the preview running, `npm test` uses the installed macOS Google Chrome through CDP. It checks eleven viewport compositions, limited pointer motion, idle stopping, reduced-motion changes, context loss/recovery and responsive source changes. Additional modes:

```sh
QA_DPR=2 QA_BASIC=1 QA_OUT=qa/retina npm test
QA_MODE=no-webgl QA_OUT=qa/no-webgl npm test
QA_MODE=blocked-js QA_OUT=qa/loading npm test
```

The test runner records screenshots, raw browser results, logs and timing evidence. These checks establish behavior; appearance is separately reviewed from the screenshots.

## Display behavior

- CSS selects tall portrait, portrait, square, standard landscape or wide landscape based on the viewport aspect ratio. PC1440×900, 390×844 and 320×932 keep the selected original compositions.
- Mobile/coarse pointers, reduced motion, data saving, JavaScript loading or disabled WebGL retain the full static image. The image does not depend on JavaScript or a canvas frame.
- The rendering module loads only after an eligible mouse movement. Shader preparation occurs while the finished still remains visible. No continuous animation loop runs when the pointer settles.
- Reduced motion disposes rendering resources. Context loss immediately exposes the still; restoration allows a fresh renderer on the next eligible interaction.
- No external image CDN, analytics, fonts or runtime API requests are used.

## Assets and evidence

The three selected source images and their generation records live in the protected sibling run `hybrid-1132/`. The additional panoramic and square PNG originals are in this run's `images/`. Served WebP files are format conversions of the generated images, without compositional edits. `REPORT.md`, `comparison.html`, `final/`, `final-retina/`, `final-no-webgl/` and `final-loading/` are the review evidence outside this source directory.

Physical Android/iOS, Safari, real mobile network conditions and 4K image quality have not been verified. Most original images are approximately 1.57 megapixels. The primary three image files are byte-identical to the selected image-study assets. Screenshots can differ slightly because of browser resampling/color output.

The protected 09:00 project source and build are not replaced by this candidate. Nothing is published remotely.
