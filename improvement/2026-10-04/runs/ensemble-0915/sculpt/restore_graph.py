"""Restore the exact rejected structural mesh for editing; save only on explicit --output.
Example Blender --background --python-exit-code 1 --python restore_graph.py --
 --record ../models/graph-v02.json --inspection ../qa/graph-v02-restore.json
The compact mesh and graph are retained without duplicate full native files.
"""
import bpy,bmesh,json,sys,argparse,hashlib
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--record',type=Path,required=True);p.add_argument('--inspection',type=Path,required=True);p.add_argument('--output',type=Path);a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);d=json.loads(a.record.read_text());bpy.ops.wm.read_factory_settings(use_empty=True)
me=bpy.data.meshes.new('Exact structural control mesh');me.from_pydata(d['control_positions'],[],d['control_faces']);me.update();o=bpy.data.objects.new(d['version']+' rejected structural study',me);bpy.context.collection.objects.link(o)
bm=bmesh.new();bm.from_mesh(me);volume=bm.calc_volume(signed=True);boundary=sum(e.is_boundary for e in bm.edges);nonmanifold=sum(not e.is_manifold for e in bm.edges);bm.free();me.calc_loop_triangles();expected=d['inspection'];r={'version':d['version'],'positions_faces_exact':[[list(v.co)for v in me.vertices],[list(f.vertices)for f in me.polygons]]==[d['control_positions'],d['control_faces']],'vertices':len(me.vertices),'faces':len(me.polygons),'triangles':len(me.loop_triangles),'volume':volume,'expected_volume':expected['signed_volume'],'volume_absolute_error':abs(volume-expected['signed_volume']),'boundary_edges':boundary,'nonmanifold_edges':nonmanifold,'record_sha256':hashlib.sha256(a.record.read_bytes()).hexdigest(),'native_saved':bool(a.output),'candidate_adopted':False};assert r['positions_faces_exact'] and boundary==nonmanifold==0 and r['volume_absolute_error']<1e-12
# Separate authored graph with real connectivity; visible in editor, not render.
controls=d['controls'];wire=bpy.data.meshes.new('Editable skeleton connectivity');wire.from_pydata([p[:3]for p in controls['points']],controls['edges'],[]);wire.update();w=bpy.data.objects.new('Authored graph controls',wire);bpy.context.collection.objects.link(w);w.hide_render=True;w.display_type='WIRE';w['controls_json']=json.dumps(controls)
o['rejected_candidate']=True;o['source_record']=str(a.record)
if a.output:
 assert not a.output.exists();bpy.ops.wm.save_as_mainfile(filepath=str(a.output))
assert not a.inspection.exists();a.inspection.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r),flush=True)
