import bpy,json
from pathlib import Path
r=Path('/Users/kazuki.tanaka/dev0/exfract-bonsai-02/improvement/2026-10-04/runs/hero-rebuild-1016')
bpy.ops.wm.open_mainfile(filepath=str(r/'sculpt/bonsai-structural-study.blend'))
bpy.ops.export_scene.gltf(filepath=str(r/'prototype/public/models/bonsai-structural-study.glb'),export_format='GLB',use_selection=True,export_yup=True,export_normals=True,export_materials='EXPORT')
meta={'vertices':sum(len(o.data.vertices) for o in bpy.context.scene.objects if o.type=='MESH'),'polygons':sum(len(o.data.polygons) for o in bpy.context.scene.objects if o.type=='MESH'),'objects':[o.name for o in bpy.context.scene.objects],'seed':8196,'source':'Original generated geometry; no downloaded assets'}
(r/'sculpt/asset-metadata.json').write_text(json.dumps(meta,indent=2));print(json.dumps(meta))
