"""Make an editor-friendly delivery copy and inspect the final source solid."""
import bpy,bmesh,json,argparse,sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--out',required=True);a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);out=Path(a.out)
if out.exists():raise FileExistsError(out)
bpy.ops.wm.open_mainfile(filepath=str(Path(a.source).resolve()))
library=bpy.data.collections.new('Runtime leaf detail library — hidden');bpy.context.scene.collection.children.link(library);library.hide_render=True
for ob in list(bpy.context.scene.objects):
 if ob.get('foliage_lod_template'):
  for collection in list(ob.users_collection):collection.objects.unlink(ob)
  library.objects.link(ob);ob.hide_render=True;ob.hide_set(True)
core=bpy.data.objects['Continuous aged trunk and primary branches'];bm=bmesh.new();bm.from_mesh(core.data)
inspection={'core_vertices':len(bm.verts),'core_faces':len(bm.faces),'boundary_edges':sum(e.is_boundary for e in bm.edges),'nonmanifold_edges':sum(not e.is_manifold for e in bm.edges),'signed_volume':bm.calc_volume(signed=True),'wood_alpha_min':min(x.color[3]for x in core.data.color_attributes.active_color.data),'runtime_templates_hidden':len(library.objects)};bm.free()
assert inspection['boundary_edges']==0 and inspection['nonmanifold_edges']==0 and inspection['signed_volume']>0
for ob in bpy.context.scene.objects:ob.select_set(False)
core.select_set(True);bpy.context.view_layer.objects.active=core
for screen in bpy.data.screens:
 for area in screen.areas:
  if area.type=='VIEW_3D':
   area.spaces.active.region_3d.view_location=(0,0,1.1);area.spaces.active.region_3d.view_distance=3.5
bpy.ops.wm.save_as_mainfile(filepath=str(out.resolve()),compress=True);out.with_suffix('.inspection.json').write_text(json.dumps(inspection,indent=2));print(json.dumps(inspection))
