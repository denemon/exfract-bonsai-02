# Rejected local structure studies

Both A and B failed the visual gate. The retained runtime candidate remains the previous stage's v23. This directory is a diagnostic study, not a finished garden release.

- `comparison.html` reuses saved images without copying previous evidence.
- `models/local-{a,b}.mesh.npz` stores the full changed wood surface as compressed float32 positions/int32 faces. The pot, soil and support are referenced from the immutable v20 Blender base recorded in `start.json`.
- `models/local-{a,b}.glb` is a coarse clay inspection export. It does not carry v23's final wood flow attributes or foliage.
- `sculpt/restore_candidate.py` restores either compact mesh into the protected base in memory. Both variants were actually restored and checked in Blender. No native duplicates were saved. Optional `--output` must name a new `.blend` file; existing files are refused. Current operations and metadata remain the editable source for changes.
- `site/` is the clay browser harness. Public textures, decoder and stills are read-only symlinks to the previous stage. Its inherited v23 fallback does not represent A/B. Do not use this harness as a finished no-WebGL release or promote its model by copying it into the previous production site.
- `sculpt/build_check.mjs` validates the diagnostic source with Vite in memory (`write:false`, `copyPublicDir:false`). The unchanged v23 production build and its 44 checks remain in the previous stage.
- `qa/browser-profile` is one reusable dedicated profile, retained after two Chrome runs. Never share it concurrently. `site/scripts/capture.mjs` takes `QA_PROFILE`; its adjacent `.active` directory provides exclusion. The 55 older profiles are untouched and are not approved for deletion.

Restoration, without saving another model:

```sh
/Applications/Blender.app/Contents/MacOS/Blender --background --factory-startup --python-exit-code 1 --python sculpt/restore_candidate.py -- --candidate a
```

The previous v23 preview is Mac-local at http://127.0.0.1:5190/. The short-lived 5191 study server is stopped on handoff. No ZIP/archive, publication, Git write, purchase or Library retry was made in this stage.
