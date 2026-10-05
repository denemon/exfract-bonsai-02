# Finished-image study

A static full-scene composition preview for the approved constrained-view hybrid approach. Deliberately motionless for image selection. Final parallax/local motion and their runtime checks have not yet been implemented.

Run `npm run dev` locally at http://127.0.0.1:5186/. Original ImageGen outputs are converted to WebP without visual edits. Landscape, portrait and especially tall portrait use separately generated compositions. No visible text appears in the scene.

`npm run build` builds the image-only study. With the local server running, `npm test` verifies the three selected viewport compositions in installed Chrome. The root 09:00 site and its production build remain untouched.
