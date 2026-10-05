from pathlib import Path
import bpy,json,bmesh
R=Path(__file__).resolve().parents[1]
record=json.loads((R/'sculpt/patch-v02-cage.json').read_text())
obj=next(o for o in bpy.data.objects if o.type=='MESH')
assert sum(o.type=='MESH' for o in bpy.data.objects)==1
points=[list(v.co)for v in obj.data.vertices]
position_error=max(abs(a-b)for p,q in zip(points,record['positions'])for a,b in zip(p,q))
faces=[list(p.vertices)for p in obj.data.polygons]
assert position_error==0 and faces==record['faces']
assert obj.modifiers[0].type=='SUBSURF' and obj.modifiers[0].levels==2
assert [g.name for g in obj.vertex_groups]==list(record['vertex_groups'])
for name,ids in record['vertex_groups'].items():
 group=obj.vertex_groups[name].index
 actual=[v.index for v in obj.data.vertices if any(g.group==group for g in v.groups)]
 assert actual==ids
for name,part in record['parts'].items():
 assert set(part['new_local_mouth']).issubset(record['vertex_groups'][name])
 assert part['sections'][0]==part['new_local_mouth']
me=obj.evaluated_get(bpy.context.evaluated_depsgraph_get()).to_mesh();me.calc_loop_triangles()
bm=bmesh.new();bm.from_mesh(me);volume=bm.calc_volume(signed=True);boundary=sum(e.is_boundary for e in bm.edges);nonmanifold=sum(not e.is_manifold for e in bm.edges);bm.free()
assert abs(volume-record['inspection']['volume'])<1e-12 and boundary==nonmanifold==0
result={'read_only_native':str(R/'models/patch-v02-editable.blend'),'native_meshes':1,'editable_control_vertices':len(points),'editable_control_faces':len(faces),'position_error':position_error,'faces_exact':faces==record['faces'],'subdivision_level':2,'vertex_groups':list(record['vertex_groups']),'shared_collar_ids_exact':True,'evaluated_triangles':len(me.loop_triangles),'volume':volume,'boundary_edges':boundary,'nonmanifold_edges':nonmanifold,'source_rewritten':False}
p=R/'qa/native-readback-v02.json';assert not p.exists();p.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result),flush=True)
