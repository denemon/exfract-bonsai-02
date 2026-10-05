"""Closed irregular local surface patch graph; no whole-height contour loft."""
from pathlib import Path
import bpy,bmesh,math,json
from mathutils import Vector
from mathutils.bvhtree import BVHTree
R=Path(__file__).resolve().parents[1];version='patch-v02';assert not (R/'models'/f'{version}.glb').exists();bpy.ops.wm.read_factory_settings(use_empty=True)
plan=json.loads((R/'design/patch-plan-v02.json').read_text());cage=json.loads((R/'design/main-patch-cage-v02.json').read_text());V=cage['positions'];F=cage['all_faces'];removed=set(cage['removed_face_ids']);keys=cage['face_keys'];groups={};parts={}
for name,keyset in keys.items():groups[name]=set(i for faceid in keyset.values()for i in F[faceid])
def face_normal(face):
 tmp=bpy.data.meshes.new('temporary closed source for outward normal');tmp.from_pydata(V,[],[f for i,f in enumerate(F)if i not in removed]);tmp.update();bm=bmesh.new();bm.from_mesh(tmp);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces))
 if bm.calc_volume(signed=True)<0:bmesh.ops.reverse_faces(bm,faces=list(bm.faces))
 bm.normal_update();bm.verts.index_update();target=frozenset(face);normal=next(f.normal.copy()for f in bm.faces if frozenset(v.index for v in f.verts)==target);bm.free();bpy.data.meshes.remove(tmp);return normal

def mouth(faceid,scale):
 assert faceid not in removed;outer=F[faceid];normal=face_normal(outer);centre=sum((Vector(V[i])for i in outer),Vector())/4;removed.add(faceid);inner=[]
 for i in outer:inner.append(len(V));V.append(list(centre+(Vector(V[i])-centre)*scale))
 for k in range(4):F.append([outer[k],outer[(k+1)%4],inner[(k+1)%4],inner[k]])
 return outer,inner,centre,normal

def small_branch(name,faceid,scale,neck,route,radii):
 outer,initial,centre,n=mouth(faceid,scale);chain=[initial];neckids=[]
 for i in initial:neckids.append(len(V));V.append(list(centre+(Vector(V[i])-centre)*.86+n*neck))
 chain.append(neckids);route=[Vector(p)for p in route];route[0]=sum((Vector(V[i])for i in neckids),Vector())/4
 axis=(route[1]-route[0]).normalized();assert n.dot(axis)>.02,(name,list(n),list(axis));u=Vector(V[neckids[0]])-route[0];u-=axis*u.dot(axis);u.normalize();orientation=(Vector(V[neckids[1]])-Vector(V[neckids[0]])).cross(Vector(V[neckids[2]])-Vector(V[neckids[1]]));sign=1 if orientation.dot(axis)>0 else -1
 for j,p in enumerate(route):
  if j==0:continue
  nxt=p+(p-route[j-1])if j==len(route)-1 else route[j+1];t=(nxt-route[j-1]).normalized();u-=t*u.dot(t);u.normalize();b=t.cross(u).normalized();ids=[]
  for k in range(4):a=sign*k*math.pi/2;warp=[1.08,.83,1.13,.93][k];ids.append(len(V));V.append(list(p+u*(math.cos(a)*radii[j]*warp)+b*(math.sin(a)*radii[j]*.86*warp)))
  chain.append(ids)
 for a,b in zip(chain,chain[1:]):
  for k in range(4):F.append([a[k],a[(k+1)%4],b[(k+1)%4],b[k]])
 F.append(chain[-1]);groups[name]=set(outer+sum(chain,[]));parts[name]={'parent_face':outer,'new_local_mouth':initial,'sections':chain,'outward_normal':list(n),'route':[list(p)for p in route],'terminal_section':chain[-1]}

# No blind/oval wound in the second macro form; do not hide shape with a scar.
for index,root in enumerate(plan['root_stubs']):
 parent=keys['Unequal buried root seat']['side'+str(root['side'])];outer=F[parent];c=sum((Vector(V[i])for i in outer),Vector())/4;n=face_normal(outer);p=c+n*.05;tip=Vector(root['tip']);small_branch('Buried unequal root '+str(index),parent,root['inset'],.05,[list(p),list(tip)], [root['radius'],root['radius']*.62])
upper=plan['upper_branch'];small_branch('Separate posterior upper live branch',keys[upper['parent']][upper['face']],upper['inset'],upper['neck'],upper['route'],upper['radii'])
mesh=bpy.data.meshes.new('Finite rooted patches and physically terminated deadwood');mesh.from_pydata(V,[],[f for i,f in enumerate(F)if i not in removed]);mesh.update();obj=bpy.data.objects.new('Continuous aged trunk and primary branches',mesh);bpy.context.collection.objects.link(obj);bpy.context.view_layer.objects.active=obj;obj.select_set(True)
bm=bmesh.new();bm.from_mesh(mesh);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces))
if bm.calc_volume(signed=True)<0:bmesh.ops.reverse_faces(bm,faces=list(bm.faces))
bm.to_mesh(mesh);bm.free()
for name,ids in groups.items():obj.vertex_groups.new(name=name).add(sorted(ids),1,'REPLACE')
for p in mesh.polygons:p.use_smooth=True
# Different crease values only on local ending patches, never full-height rails.
crease=mesh.attributes.new('crease_edge','FLOAT','EDGE');lookup={tuple(sorted(e.vertices)):e.index for e in mesh.edges}
for name,weights in [('Oblique short shoulder',[.22,.42,.18,.28]),('Forward returned broad deadwood',[.08,.22,.46,.34])]:
 face=F[keys[name]['cap']]
 for k in range(4):
  e=lookup.get(tuple(sorted((face[k],face[(k+1)%4]))))
  if e is not None:crease.data[e].value=weights[k]
hinge=cage['finite_front_hinge']['edge'];ei=lookup.get(tuple(sorted(hinge)))
if ei is not None:crease.data[ei].value=.54
for edge,weight in [([24,19],.48),([16,24],.26)]:
 ei=lookup.get(tuple(sorted(edge)))
 if ei is not None:crease.data[ei].value=weight
for name in ['Growth direction','Branch growth direction','Branch blend and calibre']:mesh.uv_layers.new(name=name)
col=mesh.color_attributes.new(name='Unfinished structural role masks',type='FLOAT_COLOR',domain='POINT')
for c in col.data:c.color=(.6,.1,.3,1)
for loop in mesh.loops:
 p=mesh.vertices[loop.vertex_index].co
 for uv in mesh.uv_layers:uv.data[loop.index].uv=(p.x,p.z)if uv.name!='Branch blend and calibre'else(0,.4)
mat=bpy.data.materials.new('Continuous wood neutral structural review');mat.diffuse_color=(.34,.32,.29,1);mesh.materials.append(mat);mod=obj.modifiers.new('Local unequal patch interpolation','SUBSURF');mod.levels=2;mod.render_levels=2
obj['authoring_version']=version;obj['construction']=cage['method'];obj['editable_vertex_groups']=list(groups);obj['stage']='Core plus one upper branch, no leaf or bark finishing';obj['photo_origin_status']='Posterior depth, hidden branch origin and root stubs are authored inference'
bpy.context.view_layer.update();evaluated=obj.evaluated_get(bpy.context.evaluated_depsgraph_get());me=evaluated.to_mesh();me.calc_loop_triangles();tri=[tuple(t.vertices)for t in me.loop_triangles];bm=bmesh.new();bm.from_mesh(me);volume=bm.calc_volume(signed=True);boundary=sum(e.is_boundary for e in bm.edges);nonmanifold=sum(not e.is_manifold for e in bm.edges);areas=[f.calc_area()for f in bm.faces];bm.free();tree=BVHTree.FromPolygons([v.co.copy()for v in me.vertices],tri,all_triangles=True,epsilon=1e-8);pairs=[(i,j)for i,j in tree.overlap(tree)if i<j and set(tri[i]).isdisjoint(tri[j])];locations=[{'a':i,'b':j,'a_center':[sum(me.vertices[v].co[k]for v in tri[i])/3 for k in range(3)],'b_center':[sum(me.vertices[v].co[k]for v in tri[j])/3 for k in range(3)]}for i,j in pairs];(R/'qa/intersection-locations-v02.json').write_text(json.dumps(locations,indent=2)+'\n')
adj=[set()for _ in me.vertices]
for t in tri:
 for a,b in zip(t,t[1:]+t[:1]):adj[a].add(b);adj[b].add(a)
pending=set(range(len(adj)));components=[]
while pending:
 seed=pending.pop();stack=[seed];size=1
 while stack:
  for i in adj[stack.pop()]:
   if i in pending:pending.remove(i);stack.append(i);size+=1
 components.append(size)
inspection={'control_vertices':len(mesh.vertices),'control_faces':len(mesh.polygons),'evaluated_triangles':len(tri),'volume':volume,'boundary_edges':boundary,'nonmanifold_edges':nonmanifold,'nonadjacent_intersections':len(pairs),'connected_component_vertices':components,'minimum_face_area':min(areas),'genus_expected':0,'euler_characteristic':len(me.vertices)-len(me.edges)+len(me.polygons),'bounds':{'min':[min(v.co[k]for v in me.vertices)for k in range(3)],'max':[max(v.co[k]for v in me.vertices)for k in range(3)]}};evaluated.to_mesh_clear();(R/'qa/geometry-inspection-v02.json').write_text(json.dumps(inspection,indent=2)+'\n');print(json.dumps(inspection),flush=True)
assert boundary==nonmanifold==len(pairs)==0 and len(components)==1 and min(areas)>1e-12 and volume>0 and len(tri)<=18540,inspection
record={'version':version,'method':obj['construction'],'positions':[list(v.co)for v in mesh.vertices],'faces':[list(f.vertices)for f in mesh.polygons],'parts':parts,'vertex_groups':{n:sorted(ids)for n,ids in groups.items()},'inspection':inspection,'patch_graph':cage,'photo_plan':plan,'low_detail_only':True};(R/'sculpt/patch-v02-cage.json').write_text(json.dumps(record,indent=2)+'\n')
bpy.ops.wm.save_as_mainfile(filepath=str(R/'models/patch-v02-editable.blend'));bpy.ops.export_scene.gltf(filepath=str(R/'models/patch-v02.glb'),export_format='GLB',use_selection=True,export_apply=True,export_extras=True,export_vertex_color='ACTIVE',export_draco_mesh_compression_enable=True,export_draco_mesh_compression_level=6,export_draco_position_quantization=15,export_draco_normal_quantization=11,export_draco_texcoord_quantization=13)
print(json.dumps({'glb_bytes':(R/'models/patch-v02.glb').stat().st_size,'native_bytes':(R/'models/patch-v02-editable.blend').stat().st_size}),flush=True)
