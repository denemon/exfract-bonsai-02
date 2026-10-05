"""Restore a rejected geometry study for inspection; no output is written by default.
Blender --background --factory-startup --python restore_candidate.py -- --candidate a
Add --output /explicit/new/path.blend only when an editable native copy is required.
"""
import argparse, hashlib, json, shutil, sys
from pathlib import Path
import bpy, bmesh
import numpy as np

p=argparse.ArgumentParser();p.add_argument('--candidate',choices=['a','b'],required=True);p.add_argument('--output');args=p.parse_args(sys.argv[sys.argv.index('--')+1:])
run=Path(__file__).resolve().parents[1]
start=json.loads((run/'start.json').read_text())
base=Path(start['base_model']);assert hashlib.sha256(base.read_bytes()).hexdigest()==start['base_sha256'],'Protected source changed'
prefix=run/'models'/('local-'+args.candidate)
with np.load(prefix.with_suffix('.mesh.npz'),allow_pickle=False) as saved:
 positions=saved['positions'];faces=saved['faces']
assert positions.dtype==np.float32 and faces.dtype==np.int32
assert np.isfinite(positions).all() and faces.min()>=0 and faces.max()<len(positions)
meta=json.loads(prefix.with_suffix('.json').read_text());expected=meta['inspection']
bpy.ops.wm.open_mainfile(filepath=str(base))
core=bpy.data.objects['Continuous aged trunk and primary branches'];old=core.data
mesh=bpy.data.meshes.new('Restored compact rejected study');mesh.from_pydata(positions.tolist(),[],faces.tolist());mesh.update()
for material in old.materials:mesh.materials.append(material)
core.data=mesh;core.modifiers.clear();core['authoring_version']='local-'+args.candidate;core['decision']='Rejected clay geometry study; not a finished web model'
for face in mesh.polygons:face.use_smooth=True
bm=bmesh.new();bm.from_mesh(mesh)
report={'candidate':args.candidate,'vertices':len(bm.verts),'faces':len(bm.faces),'boundary_edges':sum(e.is_boundary for e in bm.edges),'nonmanifold_edges':sum(not e.is_manifold for e in bm.edges),'signed_volume':bm.calc_volume(signed=True),'saved_native':False}
bm.free()
for key in ['vertices','faces','boundary_edges','nonmanifold_edges']:assert report[key]==expected[key],(key,report,expected)
assert abs(report['signed_volume']-expected['signed_volume'])<1e-6
if args.output:
 dest=Path(args.output).expanduser().resolve();assert not dest.exists(),'Existing files are never overwritten';assert dest.suffix=='.blend';assert dest.parent.is_dir();assert shutil.disk_usage(dest.parent).free>2*1024**3
 bpy.ops.wm.save_as_mainfile(filepath=str(dest),compress=True);report['saved_native']=True;report['output']=str(dest)
print('RESTORE_CHECK '+json.dumps(report),flush=True)
