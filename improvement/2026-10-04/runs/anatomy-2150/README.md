# Selected editable coarse framework — cage-v06

This is a geometry study, not a completed garden release. The previous full runtime v23 remains unchanged.

- Open `models/best-coarse.blend`: 554 editable control vertices, 528 faces, unapplied Catmull–Clark level 2, named root/trunk/four branch groups, neutral material, inspection camera/lights. The saved file was reopened and checked. Its geometry is self-contained.
- `models/cage-v06.glb` is the selected plain inspection export. It is not equipped with the v23 wood-flow shader attributes, final canopy or matching no-WebGL stills. Do not copy it over the production hero.
- `models/cage-v01.json` through `cage-v06.json` retain exact control positions/faces and construction conditions. All six were reconstructed in Blender and checked against evaluated geometry/volume. Current-run intermediate GLB copies were removed only after this verification; previous stages were untouched.
- `sculpt/cage.py` can reproduce an authored control record; `sculpt/save_native.py` can restore a selected exact cage into a new native file. Later manual edits to the chosen native cage must be saved as a new version. Re-running procedural controls recreates this saved stage, not any future manual sculpt.
- `comparison.html` displays 14 unmodified representative screenshots in place. `validation.json` retains results of 33 original browser views and the final 6 rechecks, with a flag showing which provisional captures were retained. Additional intermediate PNGs were current-run scratch, not copied into archives.
- `site/` is a text-free clay inspection harness. It has no finished-scene fallback or mobile composition. Start locally with `npm run dev` from this folder when the port is free. Its final source was built in memory. The short-lived 5191 server was stopped on handoff.
- The capture helper requires `QA_PROFILE` pointing to the existing stage-three dedicated profile, holds an adjacent `.active` lock, and disables background Chrome updates. No new QA profile was created. Do not use it concurrently. No old profile is approved for deletion.

Read `REPORT.md`, `INDEPENDENT-FINAL-REVIEW.md` and `finish.json` before the next stage. No ZIP, publication, Git write, purchase or Library retry was made. Current v23 preview: http://127.0.0.1:5190/ on the Mac only.
