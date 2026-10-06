from pathlib import Path
import bpy,bmesh,json,math,hashlib
from mathutils import Vector
from mathutils.bvhtree import BVHTree
R=Path('/Users/kazuki.tanaka/dev0/exfract-bonsai-02/improvement/2026-10-04/runs/root-flow-0206');O=R.parent/'landmark-volume-0055';version='root-v01';assert not(R/'models'/f'{version}.glb').exists()
bpy.ops.wm.open_mainfile(filepath=str(R.parent/'local-edges-0056/models/edge-v02-editable.blend'));soil=bpy.data.objects['Continuous planted soil'];bpy.context.view_layer.update();soilTree=BVHTree.FromPolygons([soil.matrix_world@v.co for v in soil.data.vertices],[list(f.vertices)for f in soil.data.polygons])
def soilH(x,y):
 hit,_,_,_=soilTree.ray_cast(Vector((x,y,2)),Vector((0,0,-1)));assert hit is not None;return hit.z
bpy.ops.wm.open_mainfile(filepath=str(O/'models/landmark-v02-editable.blend'));bpy.context.preferences.filepaths.save_version=0;o=bpy.data.objects['Continuous aged trunk and primary branches'];me=o.data;oldV=[v.co.copy()for v in me.vertices];rec=json.loads((O/'sculpt/control-record.json').read_text());patch=json.loads((O/'sculpt/control-record-v02.json').read_text());plan=json.loads((O/'design/landmarks.json').read_text());changes=[]
rootMoves={11:[-.15,-.185,.422],12:[-.05,-.094,.405],13:[.13,-.11,.398],21:[-.071,-.163,.566],22:[.045,-.108,.547],23:[.148,-.093,.520],31:[-.018,-.156,.717],32:[.065,-.158,.707],33:[.160,-.136,.691],17:[.067,.215,.424],26:[.155,.210,.552],27:[.027,.200,.558]}
for k,q in rootMoves.items():changes.append({'vertex':k,'old':list(me.vertices[k].co),'new':q,'reason':'Local asymmetric root seat and finite lateral anterior recess'});me.vertices[k].co=q
rootLeft=next(x for x in rec['branches']if x['id']=='root-left')
for k in rootLeft['control_vertex_ids'][:4]:
 q=me.vertices[k].co.copy()+Vector((.006,-.01,.032));changes.append({'vertex':k,'old':list(me.vertices[k].co),'new':list(q),'reason':'Left root emerges as a load mass before burying, cap unchanged'});me.vertices[k].co=q
left=next(x for x in patch['local_patches']if x['id']=='first-left');normal=Vector((-1,-.2,0)).normalized()
for field,d in [('restricted_opening',.016),('neck',.004)]:
 for k in left[field]:
  q=me.vertices[k].co+normal*d;changes.append({'vertex':k,'old':list(me.vertices[k].co),'new':list(q),'reason':'Convex local mother-face strip, no whole branch growth'});me.vertices[k].co=q
me.update();bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free();V=[v.co.copy()for v in me.vertices]
# End old front support rails locally, leave upper masses and all other creases.
crease=me.attributes.get('crease_edge')
for edge in me.edges:
 if sum(me.vertices[k].co.z for k in edge.vertices)/2<.79:crease.data[edge.index].value=.14 if set(edge.vertices)=={12,22}else .08 if set(edge.vertices)=={11,21}else 0
changedIDs={x['vertex']for x in changes};protected=[k for k in range(len(V))if k not in changedIDs];assert all(V[k]==oldV[k]for k in protected);assert all(V[k]==oldV[k]for k in range(40,114))
# Recompute every added/old point from the growth field. Do not interpolate
# the old wrapped0/1 UVs. Face-corner unwrap preserves a periodic U seam.
loops=[];offset=0
for source in plan['loops']:loops.append(list(range(offset,offset+len(source))));offset+=len(source)
main=[sum((V[k]for k in ids),Vector())/len(ids)for ids in loops];flows={'main':main};assignment={k:('main',0)for k in range(len(V))};branchSeed={}
for ix,br in enumerate(rec['branches']):
 N=len(br['mouth_vertex_ids']);path=[sum((V[k]for k in br['mouth_vertex_ids']),Vector())/N];pa=next((x for x in patch['local_patches']if x['id']==br['id']),None)
 if pa:
  for field,weight in [('restricted_opening',.16),('neck',.40),('intermediate_section',.76)]:
   ids=pa[field];path.append(sum((V[k]for k in ids),Vector())/len(ids))
   for k in ids:assignment[k]=(br['id'],weight)
 for j in range(0,len(br['control_vertex_ids']),N):
  ids=br['control_vertex_ids'][j:j+N];path.append(sum((V[k]for k in ids),Vector())/N)
  for k in ids:assignment[k]=(br['id'],.7 if br['id'].startswith('root')and j==0 else .93 if j==0 else 1)
 if pa:
  for field in ['terminal_support','terminal_cap']:
   ids=pa[field];path.append(sum((V[k]for k in ids),Vector())/len(ids))
   for k in ids:assignment[k]=(br['id'],1)
 flows[br['id']]=path;branchSeed[br['id']]=(.083*ix,.11*ix)
segments={}
for name,path in flows.items():
 arc=0;parts=[]
 for a,b in zip(path,path[1:]):
  d=b-a;L=d.length
  if L<1e-7:continue
  parts.append((a,d,L,arc));arc+=L
 segments[name]=parts

def field(q,name):
 options=[]
 for a,d,L,arc in segments[name]:
  t=max(0,min(1,(q-a).dot(d)/(L*L)));p=a+d*t;options.append(((q-p).length,p,d.normalized(),arc+L*t))
 distance,p,T,length=min(options,key=lambda x:x[0]);u=Vector((0,-1,0));u-=T*u.dot(T)
 if u.length<.1:u=Vector((1,0,0));u-=T*u.dot(T)
 u.normalize();b=T.cross(u);D=q-p;return(math.atan2(D.dot(b),D.dot(u))/math.tau+.5,length,distance)
fields=[]
for k,q in enumerate(V):
 a=field(q,'main');name,w=assignment[k];b=field(q,name);phase=branchSeed.get(name,(0,0));fields.append(((a[0],a[1]),(b[0]+phase[0],b[1]+phase[1]),(w,max(.08,min(1,b[2]/.22)))))
for j,layer in enumerate(me.uv_layers):
 for face in me.polygons:
  ids=list(face.vertices);values=[fields[k][j]for k in ids]
  if j<2:
   theta=[x[0]for x in values];mean=math.atan2(sum(math.sin(v*math.tau)for v in theta),sum(math.cos(v*math.tau)for v in theta))/math.tau
   values=[(u+round(mean-u),v)for u,v in values]
  for ix,value in zip(face.loop_indices,values):layer.data[ix].uv=value
sub=o.modifiers[0];sub.uv_smooth='PRESERVE_BOUNDARIES'
# Exact tertiary topology and all protected leaf-attached nodes are retained.
can=json.loads((R.parent/'integrated-form-2245/models/integrated-v03.canopy-topology.json').read_text());tv=[];tf=[];twigchanges=[];protectedChecks=[]
def tube(coords,rs,N=5):
 ids=[]
 for j,c in enumerate(coords):
  T=(coords[min(j+1,len(coords)-1)]-coords[max(j-1,0)]).normalized();u=T.cross(Vector((0,1,0)))
  if u.length<.1:u=T.cross(Vector((1,0,0)))
  u.normalize();b=T.cross(u);ring=[]
  for k in range(N):a=math.tau*k/N;ring.append(len(tv));tv.append(tuple(c+(u*math.cos(a)+b*math.sin(a))*rs[j]))
  if ids:
   for k in range(N):tf.append([ids[-1][k],ids[-1][(k+1)%N],ring[(k+1)%N],ring[k]])
  ids.append(ring)
 tf.extend([list(reversed(ids[0])),ids[-1]])
for region in can['regions']:
 source=[Vector(v)+Vector((0,0,.393))for v in region['nodes']];nodes=[v.copy()for v in source];parents=region['parents'];protected={a['node']for a in region['spray_attachments']};protected|={parents[a]for a in protected if parents[a]>=0};route=region['parent_route'];deltas={}
 if route=='left lower rear fork':
  for j in range(3):deltas[j]=Vector((-.005,-.041,-.025))*(1-j/3)
 if route=='rear crown fork':
  for j in range(3):deltas[j]=Vector((.033,.043,.021))*(1-j/3)
 if route=='subordinate low right':deltas={0:Vector((-.012,0,-.004)),1:Vector((-.003,0,.002))}
 for j,d in deltas.items():
  assert j not in protected;nodes[j]+=d;twigchanges.append({'route':route,'node':j,'source':list(source[j]),'new':list(nodes[j]),'no_direct_spray_or_parent':True})
 assert all(nodes[j]==source[j]for j in protected);protectedChecks.append({'route':route,'protected_nodes':len(protected),'unchanged':True});children=[[]for _ in nodes]
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
tw=bpy.data.objects['Terminal twig hierarchy'];tm=bpy.data.meshes.new('Local root graft reroute, exact terminal nodes');tm.from_pydata(tv,[],tf);tm.update()
for mat in tw.data.materials:tm.materials.append(mat)
for f in tm.polygons:f.use_smooth=len(f.vertices)==4
tw.data=tm;tw['authoring_version']=version;tw['fixed_terminal_sprays']=2800;o['authoring_version']=version;o['construction']='Stage24 masses preserved; local asymmetric root seat, left mother patch, hidden inner twig graft; fresh corner-unwrapped growth fields';o['form_gate']='Unadopted until gray and UV checker review'
rootchecks=[]
for br in rec['branches']:
 if not br['id'].startswith('root'):continue
 N=len(br['mouth_vertex_ids']);checks=[]
 for k in br['control_vertex_ids'][-N:]:
  q=V[k];h=soilH(q.x,q.y);checks.append({'position':list(q),'soil_z':h,'below_soil':h-q.z});assert h-q.z>.035
 rootchecks.append({'id':br['id'],'cap_burial':checks})
bpy.context.view_layer.update();ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get());surface=ev.to_mesh();surface.calc_loop_triangles();tris=[tuple(t.vertices)for t in surface.loop_triangles];bm=bmesh.new();bm.from_mesh(surface);volume=bm.calc_volume(signed=True);boundary=sum(e.is_boundary for e in bm.edges);nonmanifold=sum(not e.is_manifold for e in bm.edges);bm.free();tree=BVHTree.FromPolygons([v.co.copy()for v in surface.vertices],tris,all_triangles=True,epsilon=1e-9);pairs=[(a,b)for a,b in tree.overlap(tree)if a<b and set(tris[a]).isdisjoint(tris[b])];ins={'version':version,'control_vertices':len(me.vertices),'control_faces':len(me.polygons),'evaluated_vertices':len(surface.vertices),'triangles':len(tris),'volume':volume,'boundary_edges':boundary,'nonmanifold_edges':nonmanifold,'nonadjacent_intersections':len(pairs),'intersection_centres':[[list(sum((surface.vertices[v].co for v in tris[t]),Vector())/3)for t in pair]for pair in pairs[:20]],'root_soil':rootchecks,'protected_terminal_nodes':protectedChecks,'twig_changes':twigchanges,'major_main_controls40_to113_unchanged':True,'geometry_only_not_aesthetic':True};(R/'qa/geometry-inspection.json').write_text(json.dumps(ins,indent=2)+'\n');print(json.dumps(ins),flush=True);assert boundary==nonmanifold==len(pairs)==0 and volume>0
sha=lambda x:hashlib.sha256(json.dumps(x).encode()).hexdigest();record={'version':version,'source_native_sha256':hashlib.sha256((O/'models/landmark-v02-editable.blend').read_bytes()).hexdigest(),'local_control_changes':changes,'protected_control_count':len(protected),'protected_control_positions_sha256':sha([list(V[k])for k in protected]),'positions_sha256':sha([list(v.co)for v in me.vertices]),'faces_sha256':sha([list(f.vertices)for f in me.polygons]),'normals_sha256':sha([list(v.normal)for v in me.vertices]),'uv_sha256':{l.name:sha([list(d.uv)for d in l.data])for l in me.uv_layers},'color_sha256':sha([list(d.color)for d in me.color_attributes.active_color.data]),'geometry':ins,'uv_method':'Recomputed every point from main and owned branch growth fields; per-corner circular unwrap; periodic integerU separated from real-lengthV; main body does not borrow nearest horizontal root branchUV','geometry_frozen':False};(R/'sculpt/control-record.json').write_text(json.dumps(record,indent=2)+'\n');(R/'design/local-control-changes.json').write_text(json.dumps({'changes':changes,'main_indices40_113_protected':True,'terminal_changes':twigchanges},indent=2)+'\n');ev.to_mesh_clear()
bpy.ops.wm.save_as_mainfile(filepath=str(R/'models'/f'{version}-editable.blend'),compress=True);bpy.ops.object.select_all(action='DESELECT');o.select_set(True);tw.select_set(True);bpy.ops.export_scene.gltf(filepath=str(R/'models'/f'{version}.glb'),export_format='GLB',use_selection=True,export_apply=True,export_extras=True,export_vertex_color='ACTIVE',export_draco_mesh_compression_enable=True,export_draco_mesh_compression_level=6,export_draco_position_quantization=15,export_draco_normal_quantization=11,export_draco_texcoord_quantization=13)
print(json.dumps({'native_bytes':(R/'models'/f'{version}-editable.blend').stat().st_size,'glb_bytes':(R/'models'/f'{version}.glb').stat().st_size}),flush=True)
