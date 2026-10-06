from pathlib import Path
import bpy,bmesh,json,math,hashlib
from mathutils import Vector
from mathutils.bvhtree import BVHTree
R=Path(__file__).resolve().parents[1];p=json.loads((R/'design/landmarks.json').read_text());version=p['version'];basis=R.parent/'local-edges-0056/models/edge-v02-editable.blend';assert not(R/'models'/f'{version}.glb').exists()
bpy.ops.wm.open_mainfile(filepath=str(basis));soil=bpy.data.objects['Continuous planted soil'];bpy.context.view_layer.update();soilPoints=[soil.matrix_world@v.co for v in soil.data.vertices];print('SOIL_BOUNDS',[[min(q[k]for q in soilPoints),max(q[k]for q in soilPoints)]for k in range(3)],flush=True);soilTree=BVHTree.FromPolygons(soilPoints,[list(f.vertices)for f in soil.data.polygons]);
def soilH(x,y):
 hit,_,_,_=soilTree.ray_cast(Vector((x,y,2)),Vector((0,0,-1)));assert hit is not None,('soil ray miss',x,y);return hit.z
bpy.ops.wm.read_factory_settings(use_empty=True);bpy.context.preferences.filepaths.save_version=0
V=[];F=[];roles=[];loopids=[]
for loop in p['loops']:
 ids=list(range(len(V),len(V)+len(loop)));V.extend(loop);loopids.append(ids)
def bridge(a,b,role):
 i=j=0
 while i<len(a)or j<len(b):
  ai=(i+1)/len(a);bj=(j+1)/len(b)
  if abs(ai-bj)<1e-7:F.append([a[i%len(a)],a[(i+1)%len(a)],b[(j+1)%len(b)],b[j%len(b)]]);i+=1;j+=1
  elif ai<bj:F.append([a[i%len(a)],a[(i+1)%len(a)],b[j%len(b)]]);i+=1
  else:F.append([a[i%len(a)],b[(j+1)%len(b)],b[j%len(b)]]);j+=1
  roles.append(role)
for i in range(len(loopids)-1):bridge(loopids[i],loopids[i+1],'root-seat'if i<3 else'compression-turn'if i<7 else'upper-fold')
F.extend([list(reversed(loopids[0])),loopids[-1]]);roles.extend(['buried-cap','apex-cap'])
me=bpy.data.meshes.new('Independent front side rear landmark control surface');me.from_pydata(V,[],F);me.update();bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));
if bm.calc_volume(signed=True)<0:bmesh.ops.reverse_faces(bm,faces=list(bm.faces))
bm.to_mesh(me);bm.free();F=[list(f.vertices)for f in me.polygons];normals=[f.normal.copy()for f in me.polygons];deleted=set();branches=[];rootChecks=[]
for br in p['branches']:
 origin=Vector(br['origin']);direction=Vector(br['normal']).normalized();scores=[]
 for i,face in enumerate(F[:len(normals)]):
  if i in deleted or len(face)!=4:continue
  c=sum((Vector(V[k])for k in face),Vector())/len(face);n=normals[i];score=(c-origin).length_squared+.04*(1-n.dot(direction));scores.append((score,i))
 _,pick=min(scores);patch=[pick]
 if br['mouth_faces']==2:
  # Only one adjacent quad extending UP or BACK, avoid a symmetrical collar.
  edges={frozenset((a,b))for a,b in zip(F[pick],F[pick][1:]+F[pick][:1])};options=[]
  for _,j in scores:
   if j==pick:continue
   share=edges&{frozenset((a,b))for a,b in zip(F[j],F[j][1:]+F[j][:1])}
   if share:
    c=sum((Vector(V[k])for k in F[j]),Vector())/len(F[j]);options.append(((c-origin).length_squared-.025*(c.z-origin.z)-.015*(c.y-origin.y),j))
  assert options;br2=min(options)[1];patch.append(br2)
 edgeCount={};direct={}
 for j in patch:
  for a,b in zip(F[j],F[j][1:]+F[j][:1]):
   e=frozenset((a,b));edgeCount[e]=edgeCount.get(e,0)+1;direct[e]=(a,b)
 mapping={a:b for e,(a,b)in direct.items()if edgeCount[e]==1};boundary=[next(iter(mapping))]
 while mapping[boundary[-1]]!=boundary[0]:boundary.append(mapping[boundary[-1]])
 assert len(boundary)==len(mapping);deleted.update(patch);centre=sum((Vector(V[k])for k in boundary),Vector())/len(boundary);prev=boundary;path=[list(centre)];newids=[]
 for ix,row in enumerate(br['rings']):
  c=Vector(row[:3]);T=(c-Vector(path[-1])).normalized();u=Vector((0,-1,0));u-=T*u.dot(T)
  if u.length<.1:u=Vector((1,0,0));u-=T*u.dot(T)
  u.normalize();b=T.cross(u).normalized();a0=math.atan2((Vector(V[boundary[0]])-centre).dot(b),(Vector(V[boundary[0]])-centre).dot(u));ids=[]
  for k in range(len(boundary)):
   a=a0+math.tau*k/len(boundary);v=c+u*(math.cos(a)*row[4])+b*(math.sin(a)*row[3]);ids.append(len(V));V.append(list(v));newids.append(len(V)-1)
  # Choose section winding to agree with the attachment hole boundary.
  oldN=(Vector(V[prev[1]])-Vector(V[prev[0]])).cross(Vector(V[prev[2]])-Vector(V[prev[0]]));newN=(Vector(V[ids[1]])-Vector(V[ids[0]])).cross(Vector(V[ids[2]])-Vector(V[ids[0]]))
  if oldN.dot(newN)<0:ids=[ids[0]]+list(reversed(ids[1:]))
  bridge(prev,ids,br['id']);prev=ids;path.append(list(c))
 F.append(prev);roles.append(br['id']);branches.append({'id':br['id'],'mouth_faces':patch,'mouth_vertex_ids':boundary,'control_vertex_ids':newids,'centreline':path})
 if br['id'].startswith('root'):
  checks=[]
  for k in prev:
   q=V[k];h=soilH(q[0],q[1]);checks.append({'position':q,'soil_z':h,'below_soil':h-q[2]});assert h-q[2]>.035
  rootChecks.append({'id':br['id'],'cap_burial':checks})
F=[f for j,f in enumerate(F)if j not in deleted];roles=[r for j,r in enumerate(roles)if j not in deleted];me.clear_geometry();me.from_pydata(V,[],F);me.update();bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));
if bm.calc_volume(signed=True)<0:bmesh.ops.reverse_faces(bm,faces=list(bm.faces))
bm.to_mesh(me);bm.free();o=bpy.data.objects.new('Continuous aged trunk and primary branches',me);bpy.context.collection.objects.link(o);bpy.context.view_layer.objects.active=o;o.select_set(True)
# Local support at the finite lower recess rim/termination, not whole-height rails.
crease=me.attributes.new('crease_edge','FLOAT','EDGE')
for edge in me.edges:
 a,b=[Vector(V[k])for k in edge.vertices];front=a.y<-.07 and b.y<-.07;z=(a.z+b.z)/2
 if front and .42<z<.72:crease.data[edge.index].value=.22
 if .82<z<.875 and front:crease.data[edge.index].value=.28
for face in me.polygons:face.use_smooth=True
sub=o.modifiers.new('Local support surface subdivision','SUBSURF');sub.levels=2;sub.render_levels=2
# Independent provisional UV fields / roles for later frozen-form material tests.
main=[sum((Vector(q)for q in l),Vector())/len(l)for l in p['loops']];flows=[('main',main)]+[(b['id'],[Vector(q)for q in b['centreline']])for b in branches];segments=[]
for name,path in flows:
 arc=0
 for a,b in zip(path,path[1:]):
  d=b-a;L=d.length;segments.append((name,a,d,L,arc));arc+=L
field=[];groups={n:[]for n,_ in flows};col=me.color_attributes.new(name='Continuous wood role masks',type='FLOAT_COLOR',domain='POINT');me.color_attributes.active_color=col
for v in me.vertices:
 candidates=[]
 for name,a,d,L,arc in segments:
  t=max(0,min(1,(v.co-a).dot(d)/(L*L)));q=a+d*t;dist=(v.co-q).length;candidates.append((dist,name,q,d.normalized(),arc+L*t))
 near=min(candidates,key=lambda q:q[0]);m=min((q for q in candidates if q[1]=='main'),key=lambda q:q[0]);groups[near[1]].append(v.index)
 def uv(q):
  _,name,c,T,L=q;u=Vector((0,-1,0));u-=T*u.dot(T);u.normalize();b=T.cross(u);D=v.co-c;return(math.atan2(D.dot(b),D.dot(u))/math.tau+.5,L)
 blend=0 if near[1]=='main'else min(.95,max(0,(m[0]-near[0])/.09));field.append((uv(m),uv(near),(blend,.4)));col.data[v.index].color=(.5,max(0,min(1,(-v.co.y+.02)/.2)),.25,1)
for k,n in enumerate(['Growth flow','Branch flow','Branch transition']):
 layer=me.uv_layers.new(name=n)
 for loop in me.loops:layer.data[loop.index].uv=field[loop.vertex_index][k]
for n,ids in groups.items():
 if ids:o.vertex_groups.new(name=n).add(ids,1,'REPLACE')
mat=bpy.data.materials.new('wood neutral shape review');mat.diffuse_color=(.3,.29,.27,1);mat.roughness=1;me.materials.append(mat);o['authoring_version']=version;o['construction']=p['method'];o['form_gate']='Unadopted until ordinary gray review'
# Reconstruct exact leaf-attached tertiary nodes, reroute just inner rear-left
# graft before any spray attachment. Existing terminal positions remain fixed.
cp=R.parent/'integrated-form-2245/models/integrated-v03.canopy-topology.json';can=json.loads(cp.read_text());tv=[];tf=[];changed=[]
def tube(coords,rs,N=5):
 ids=[]
 for j,c in enumerate(coords):
  c=Vector(c);T=(Vector(coords[min(j+1,len(coords)-1)])-Vector(coords[max(j-1,0)])).normalized();u=T.cross(Vector((0,1,0)))
  if u.length<.1:u=T.cross(Vector((1,0,0)))
  u.normalize();b=T.cross(u);ring=[]
  for k in range(N):a=math.tau*k/N;ring.append(len(tv));tv.append(tuple(c+(u*math.cos(a)+b*math.sin(a))*rs[j]))
  if ids:
   for k in range(N):tf.append([ids[-1][k],ids[-1][(k+1)%N],ring[(k+1)%N],ring[k]])
  ids.append(ring)
 tf.extend([list(reversed(ids[0])),ids[-1]])
for region in can['regions']:
 nodes=[Vector(v)+Vector((0,0,.393))for v in region['nodes']];parents=region['parents'];protected={a['node']for a in region['spray_attachments']};protected|={parents[a]for a in protected if parents[a]>=0}
 if region['parent_route']=='left lower rear fork':
  delta=Vector((-.005,-.041,-.025))
  for j in range(3):
   assert j not in protected;nodes[j]+=delta*(1-j/3);changed.append({'region':region['parent_route'],'node':j,'position':list(nodes[j]),'no_spray_attachment':True})
 children=[[]for _ in nodes]
 for j,a in enumerate(parents):
  if a>=0:children[a].append(j)
 descendants=[0]*len(nodes)
 for j in reversed(range(len(nodes))):descendants[j]=sum(descendants[c]for c in children[j])if children[j]else 1
 radii=[min(.011,.00145*n**.48)for n in descendants]
 for start in [0]+[j for j,c in enumerate(children)if len(c)>1]:
  for child in children[start]:
   chain=[start,child]
   while len(children[chain[-1]])==1:chain.append(children[chain[-1]][0])
   tube([nodes[j]for j in chain],[radii[j]for j in chain])
tm=bpy.data.meshes.new('Rebuilt leaf-attached tertiary hierarchy');tm.from_pydata(tv,[],tf);tm.update();tw=bpy.data.objects.new('Terminal twig hierarchy',tm);bpy.context.collection.objects.link(tw);tmat=bpy.data.materials.new('twig dry gray review');tmat.diffuse_color=(.3,.29,.27,1);tm.materials.append(tmat)
for f in tm.polygons:f.use_smooth=len(f.vertices)==4
tw['authoring_version']=version;tw['fixed_terminal_sprays']=2800;tw['inner_route_changed']=len(changed)
# Inspect control and evaluated native body. No form judgment from topology.
ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get());surface=ev.to_mesh();surface.calc_loop_triangles();tris=[tuple(t.vertices)for t in surface.loop_triangles];bm=bmesh.new();bm.from_mesh(surface);volume=bm.calc_volume(signed=True);boundary=sum(e.is_boundary for e in bm.edges);nonmanifold=sum(not e.is_manifold for e in bm.edges);bm.free();tree=BVHTree.FromPolygons([v.co.copy()for v in surface.vertices],tris,all_triangles=True,epsilon=1e-9);pairs=[(a,b)for a,b in tree.overlap(tree)if a<b and set(tris[a]).isdisjoint(tris[b])];inspect={'version':version,'control_vertices':len(me.vertices),'control_faces':len(me.polygons),'evaluated_vertices':len(surface.vertices),'triangles':len(tris),'volume':volume,'boundary_edges':boundary,'nonmanifold_edges':nonmanifold,'nonadjacent_intersections':len(pairs),'intersection_examples':pairs[:12],'root_actual_soil':rootChecks,'twig_changed_nodes':changed,'twig_vertices':len(tv),'aesthetic_pass':False};(R/'qa/geometry-inspection.json').write_text(json.dumps(inspect,indent=2)+'\n');print(json.dumps(inspect),flush=True);assert boundary==nonmanifold==len(pairs)==0 and volume>0
record={'controls_sha256':hashlib.sha256((R/'design/landmarks.json').read_bytes()).hexdigest(),'native_control_positions_sha256':hashlib.sha256(json.dumps([list(v.co)for v in me.vertices]).encode()).hexdigest(),'native_control_faces_sha256':hashlib.sha256(json.dumps([list(f.vertices)for f in me.polygons]).encode()).hexdigest(),'branches':branches,'face_roles':roles,'vertex_groups':{k:len(v)for k,v in groups.items()},'evaluated_geometry':inspect,'editable_subdivision':2,'geometry_frozen_for_material':False};(R/'sculpt/control-record.json').write_text(json.dumps(record,indent=2)+'\n');ev.to_mesh_clear()
bpy.ops.wm.save_as_mainfile(filepath=str(R/'models'/f'{version}-editable.blend'),compress=True);o.select_set(True);tw.select_set(True);bpy.ops.export_scene.gltf(filepath=str(R/'models'/f'{version}.glb'),export_format='GLB',use_selection=True,export_apply=True,export_extras=True,export_vertex_color='ACTIVE',export_draco_mesh_compression_enable=True,export_draco_mesh_compression_level=6,export_draco_position_quantization=15,export_draco_normal_quantization=11,export_draco_texcoord_quantization=13)
print(json.dumps({'native_bytes':(R/'models'/f'{version}-editable.blend').stat().st_size,'glb_bytes':(R/'models'/f'{version}.glb').stat().st_size}),flush=True)
