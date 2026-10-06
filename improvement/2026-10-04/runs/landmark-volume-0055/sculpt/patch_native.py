from pathlib import Path
import bpy,bmesh,json,hashlib
from mathutils import Vector
from mathutils.bvhtree import BVHTree
R=Path('/Users/kazuki.tanaka/dev0/exfract-bonsai-02/improvement/2026-10-04/runs/landmark-volume-0055');version='landmark-v02'
assert not(R/'models'/f'{version}.glb').exists()
bpy.ops.wm.open_mainfile(filepath=str(R/'models/landmark-v01-editable.blend'));bpy.context.preferences.filepaths.save_version=0
o=bpy.data.objects['Continuous aged trunk and primary branches'];tw=bpy.data.objects['Terminal twig hierarchy'];old=o.data;record=json.loads((R/'sculpt/control-record.json').read_text());plan=json.loads((R/'design/landmarks.json').read_text());V=[v.co.copy()for v in old.vertices];F=[list(f.vertices)for f in old.polygons];roles=record['face_roles'][:];deleted=set();patches=[]
# Read exact existing native fields. Revisions add local mother-face strips and
# thick short necks. No whole-trunk radius or global relaxation is performed.
uvs=[[None]*len(V)for _ in old.uv_layers]
for j,layer in enumerate(old.uv_layers):
 for loop in old.loops:uvs[j][loop.vertex_index]=tuple(layer.data[loop.index].uv)
colors=[tuple(q.color)for q in old.color_attributes.active_color.data]
def add(p,source_ids,weights=None):
 k=len(V);V.append(Vector(p));weights=weights or [1/len(source_ids)]*len(source_ids)
 for field in uvs:field.append(tuple(sum(field[s][a]*w for s,w in zip(source_ids,weights))for a in range(2)))
 colors.append(tuple(sum(colors[s][a]*w for s,w in zip(source_ids,weights))for a in range(4)));return k

def bridge(a,b,role):
 assert len(a)==len(b)
 for j in range(len(a)):F.append([a[j],a[(j+1)%len(a)],b[(j+1)%len(b)],b[j]]);roles.append(role)

for branch in record['branches']:
 if branch['id'].startswith('root'):continue
 name=branch['id'];boundary=branch['mouth_vertex_ids'];firstSet=set(branch['control_vertex_ids'][:len(boundary)]);mouthSet=set(boundary);connection=[];mapping={}
 for ix,f in enumerate(F):
  if ix in deleted or len(f)!=4:continue
  if set(f)<=mouthSet|firstSet and set(f)&mouthSet and set(f)&firstSet:
   connection.append(ix)
   for a,b in zip(f,f[1:]+f[:1]):
    if a in mouthSet and b in firstSet:mapping[a]=b
    if b in mouthSet and a in firstSet:mapping[b]=a
 assert len(connection)==len(boundary)and set(mapping)==mouthSet
 first=[mapping[k]for k in boundary];deleted.update(connection);centre=sum((V[k]for k in boundary),Vector())/len(boundary);firstCentre=sum((V[k]for k in first),Vector())/len(first);normal=Vector(next(b['normal']for b in plan['branches']if b['id']==name)).normalized();neckDirection=(firstCentre-centre).normalized();inset=[];neck=[];mid=[]
 # Local restricted opening, front exposure80-100mm, longer posterior upper
 # collar. Mother perimeter remains fixed and gains a face strip, so it cannot
 # stretch directly into a triangular wing. The actual branch first section
 # remains intact; two added patches carry depth between body and that section.
 height={'first-left':.048,'right-crown':.05,'rear-ascending':.047,'upper-left':.042,'low-right':.043}[name]
 for a,b in zip(boundary,first):
  delta=V[a]-centre;q=centre+delta*.58;rear=V[a].y>centre.y;q.z=centre.z+max(-height,min(height+( .023 if rear and delta.z>0 else 0),delta.z*.6))
  inset.append(add(q,[a]+boundary,[.58]+[.42/len(boundary)]*len(boundary)))
 for a,b in zip(inset,first):
  q=V[a]+normal*.036;neck.append(add(q,[a,b],[.85,.15]))
 for a,b in zip(neck,first):
  # A short intermediate physical section avoids a broad membrane immediately
  # collapsing into a small cap. Its front/back locations are independently
  # inherited from the two actual native cross sections, not a common ellipse.
  q=V[a]*.48+V[b]*.52;mid.append(add(q,[a,b],[.48,.52]))
 bridge(boundary,inset,name+' mother-patch');bridge(inset,neck,name+' neck-depth');bridge(neck,mid,name+' collar');bridge(mid,first,name+' transition')
 # Native cap support at the retained terminal graft; prevents subdivision from
 # pulling the tip away from an unchanged leaf-attached tertiary root.
 lastSet=set(branch['control_vertex_ids'][-len(boundary):]);cap=[ix for ix,f in enumerate(F)if ix not in deleted and set(f)==lastSet];assert len(cap)==1;cap=cap[0];last=F[cap];deleted.add(cap);endCentre=sum((V[k]for k in last),Vector())/len(last);T=(endCentre-firstCentre).normalized();support=[];end=[]
 for k in last:
  support.append(add(V[k]+T*.006,[k]));end.append(add(endCentre+(V[k]-endCentre)*.78+T*.014,[k]))
 bridge(last,support,name+' terminal-support');bridge(support,end,name+' terminal-cap');F.append(end);roles.append(name+' terminal-cap')
 patches.append({'id':name,'native_mother_boundary':boundary,'restricted_opening':inset,'neck':neck,'intermediate_section':mid,'unchanged_first_section':first,'front_half_height_m':height,'terminal_support':support,'terminal_cap':end,'source_connecting_faces_removed':connection,'source_cap_removed':cap})
F=[f for ix,f in enumerate(F)if ix not in deleted];roles=[r for ix,r in enumerate(roles)if ix not in deleted];me=bpy.data.meshes.new('Native v01 local branch-mouth subdivision and depth');me.from_pydata(V,[],F);me.update();bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));
if bm.calc_volume(signed=True)<0:bmesh.ops.reverse_faces(bm,faces=list(bm.faces))
bm.to_mesh(me);bm.free()
for j,source in enumerate(old.uv_layers):
 layer=me.uv_layers.new(name=source.name)
 for loop in me.loops:layer.data[loop.index].uv=uvs[j][loop.vertex_index]
col=me.color_attributes.new(name=old.color_attributes.active_color.name,type='FLOAT_COLOR',domain='POINT');me.color_attributes.active_color=col
for k,c in enumerate(colors):col.data[k].color=c
for mat in old.materials:me.materials.append(mat)
crease=me.attributes.new('crease_edge','FLOAT','EDGE');oldCrease={frozenset(e.vertices):old.attributes['crease_edge'].data[e.index].value for e in old.edges}
for e in me.edges:crease.data[e.index].value=oldCrease.get(frozenset(e.vertices),0)
for f in me.polygons:f.use_smooth=True
o.data=me;o['authoring_version']=version;o['construction']='Direct native v01 branch-mouth face strips with restricted front opening, short depth and intermediate collar; all existing trunk and root controls unchanged';o['form_gate']='Unadopted until ordinary gray review';tw['authoring_version']=version
# Point groups rebuilt by inherited UV branch masks; original groups remain
# byte-identical on original vertices; new branch patch vertices assigned byid.
for patch in patches:
 group=o.vertex_groups.get(patch['id'])or o.vertex_groups.new(name=patch['id']);group.add(patch['restricted_opening']+patch['neck']+patch['intermediate_section']+patch['terminal_support']+patch['terminal_cap'],1,'REPLACE')
bpy.context.view_layer.update();ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get());surface=ev.to_mesh();surface.calc_loop_triangles();tris=[tuple(t.vertices)for t in surface.loop_triangles];bm=bmesh.new();bm.from_mesh(surface);volume=bm.calc_volume(signed=True);boundary=sum(e.is_boundary for e in bm.edges);nonmanifold=sum(not e.is_manifold for e in bm.edges);bm.free();tree=BVHTree.FromPolygons([v.co.copy()for v in surface.vertices],tris,all_triangles=True,epsilon=1e-9);pairs=[(a,b)for a,b in tree.overlap(tree)if a<b and set(tris[a]).isdisjoint(tris[b])];ins={'version':version,'control_vertices':len(me.vertices),'control_faces':len(me.polygons),'evaluated_vertices':len(surface.vertices),'triangles':len(tris),'volume':volume,'boundary_edges':boundary,'nonmanifold_edges':nonmanifold,'nonadjacent_intersections':len(pairs),'intersection_centres':[[list(sum((surface.vertices[v].co for v in tris[t]),Vector())/3)for t in pair]for pair in pairs[:40]],'root_actual_soil':record['evaluated_geometry']['root_actual_soil'],'original_control_positions_unchanged':all((me.vertices[j].co-old.vertices[j].co).length==0 for j in range(len(old.vertices))),'terminal_hierarchy_geometry_unchanged':True,'aesthetic_pass':False};(R/'qa/geometry-inspection-v02.json').write_text(json.dumps(ins,indent=2)+'\n');print(json.dumps(ins),flush=True);assert boundary==nonmanifold==len(pairs)==0 and volume>0 and ins['original_control_positions_unchanged']
record2={'source_native':str(R/'models/landmark-v01-editable.blend'),'source_native_sha256':hashlib.sha256((R/'models/landmark-v01-editable.blend').read_bytes()).hexdigest(),'local_patches':patches,'native_control_positions_sha256':hashlib.sha256(json.dumps([list(v.co)for v in me.vertices]).encode()).hexdigest(),'native_control_faces_sha256':hashlib.sha256(json.dumps([list(f.vertices)for f in me.polygons]).encode()).hexdigest(),'face_roles':roles,'evaluated_geometry':ins,'geometry_frozen_for_material':False};(R/'sculpt/control-record-v02.json').write_text(json.dumps(record2,indent=2)+'\n');ev.to_mesh_clear()
bpy.ops.wm.save_as_mainfile(filepath=str(R/'models'/f'{version}-editable.blend'),compress=True);bpy.ops.object.select_all(action='DESELECT');o.select_set(True);tw.select_set(True);bpy.ops.export_scene.gltf(filepath=str(R/'models'/f'{version}.glb'),export_format='GLB',use_selection=True,export_apply=True,export_extras=True,export_vertex_color='ACTIVE',export_draco_mesh_compression_enable=True,export_draco_mesh_compression_level=6,export_draco_position_quantization=15,export_draco_normal_quantization=11,export_draco_texcoord_quantization=13)
print(json.dumps({'native_bytes':(R/'models'/f'{version}-editable.blend').stat().st_size,'glb_bytes':(R/'models'/f'{version}.glb').stat().st_size}),flush=True)
