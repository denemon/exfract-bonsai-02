from pathlib import Path
import bpy,bmesh,json,hashlib
from mathutils.bvhtree import BVHTree
R=Path(__file__).resolve().parents[1];rows=[]
for name in ['ancient-v01','ancient-v02']:
 p=R/'models'/(name+'.json');d=json.loads(p.read_text());basis=Path(d['basis_native']);assert hashlib.sha256(basis.read_bytes()).hexdigest()==d['basis_sha256'];bpy.ops.wm.open_mainfile(filepath=str(basis));core=bpy.data.objects['Continuous aged trunk and primary branches'];mesh=core.data
 def surface_fingerprint():return hashlib.sha256(json.dumps({'UV':[[list(v.uv)for v in layer.data]for layer in mesh.uv_layers],'color':[[list(v.color)for v in layer.data]for layer in mesh.color_attributes],'groups':[[[g.group,g.weight]for g in v.groups]for v in mesh.vertices]}).encode()).hexdigest()
 before=surface_fingerprint();original=[v.co.copy()for v in mesh.vertices];assert len(mesh.vertices)==len(d['control_positions'])
 for v,q in zip(mesh.vertices,d['control_positions']):v.co=q
 for i,value in d.get('authored_edge_creases',[]):mesh.attributes['crease_edge'].data[i].value=value
 mesh.update();bpy.context.view_layer.update();after=surface_fingerprint();assert before==after
 ev=core.evaluated_get(bpy.context.evaluated_depsgraph_get());m=ev.to_mesh();m.calc_loop_triangles();tri=[tuple(t.vertices)for t in m.loop_triangles];bm=bmesh.new();bm.from_mesh(m);volume=bm.calc_volume(signed=True);boundary=sum(e.is_boundary for e in bm.edges);nonmanifold=sum(not e.is_manifold for e in bm.edges);bm.free();tree=BVHTree.FromPolygons([v.co.copy()for v in m.vertices],tri,all_triangles=True,epsilon=1e-9);cross=sum(i<j and set(tri[i]).isdisjoint(tri[j])for i,j in tree.overlap(tree));adj=[set()for v in m.vertices]
 for e in m.edges:a,b=e.vertices;adj[a].add(b);adj[b].add(a)
 remaining=set(range(len(adj)));components=0
 while remaining:
  components+=1;todo=[remaining.pop()]
  while todo:
   i=todo.pop();new=adj[i]&remaining;remaining.difference_update(new);todo.extend(new)
 assert components==1 and boundary==nonmanifold==cross==0
 assert len(tri)==d['inspection']['evaluated_triangles']==18540 and abs(volume-d['inspection']['signed_volume'])<1e-7
 assert all((a-v.co).length==0 for a,v in zip(original,mesh.vertices)if a.z<=.415)
 row={'record':str(p.relative_to(R)),'record_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'basis_sha256':d['basis_sha256'],'restored_from_positions_and_authored_creases':True,'unchanged_UV_color_vertex_groups_fingerprint':before,'control_vertices':len(mesh.vertices),'subdivision_level':core.modifiers[0].levels,'evaluated_triangles':len(tri),'volume':volume,'volume_error':abs(volume-d['inspection']['signed_volume']),'components':components,'boundary_edges':boundary,'nonmanifold_edges':nonmanifold,'nonadjacent_intersections':cross,'native_modified':False,'aesthetic_gate':'not passed'};rows.append(row);ev.to_mesh_clear()
selected=R/'models/selected-editable.blend';assert selected.is_symlink();result={'passed':True,'purpose':'Non-adopted A/B can be restored from the immutable editable basis plus compact positions/creases. The selected editable native remains the protected original.','selected_native':str(selected.resolve()),'selected_sha256':hashlib.sha256(selected.read_bytes()).hexdigest(),'records':rows};(R/'qa/compact-restore.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
