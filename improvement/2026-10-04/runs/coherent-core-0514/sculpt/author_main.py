from pathlib import Path
import bpy,bmesh,json,math,hashlib
from mathutils import Vector
from mathutils.bvhtree import BVHTree
R=Path('/Users/kazuki.tanaka/dev0/exfract-bonsai-02/improvement/2026-10-04/runs/coherent-core-0514');O=R.parent/'landmark-volume-0055';version='core-v01';assert not(R/'models'/f'{version}.glb').exists()
bpy.ops.wm.open_mainfile(filepath=str(R.parent/'local-edges-0056/models/edge-v02-editable.blend'));soil=bpy.data.objects['Continuous planted soil'];bpy.context.view_layer.update();soilTree=BVHTree.FromPolygons([soil.matrix_world@v.co for v in soil.data.vertices],[list(f.vertices)for f in soil.data.polygons])
def soilH(x,y):
 hit,_,_,_=soilTree.ray_cast(Vector((x,y,2)),Vector((0,0,-1)));assert hit is not None;return hit.z
bpy.ops.wm.open_mainfile(filepath=str(R.parent/'root-flow-0206/models/root-v02-editable.blend'));bpy.context.preferences.filepaths.save_version=0;o=bpy.data.objects['Continuous aged trunk and primary branches'];me=o.data;oldV=[v.co.copy()for v in me.vertices];rec=json.loads((O/'sculpt/control-record.json').read_text());patch=json.loads((O/'sculpt/control-record-v02.json').read_text());plan=json.loads((O/'design/landmarks.json').read_text());changes=[]
proposal=json.loads((R/'design/main-plane-landmarks.json').read_text());oldFaces=[list(f.vertices)for f in me.polygons];oldTwig=bpy.data.objects['Terminal twig hierarchy'];twigBefore={'positions':hashlib.sha256(json.dumps([list(v.co)for v in oldTwig.data.vertices]).encode()).hexdigest(),'faces':hashlib.sha256(json.dumps([list(f.vertices)for f in oldTwig.data.polygons]).encode()).hexdigest()};offset=0;mainLoopIDs=[]
for loop in plan['loops']:mainLoopIDs.append(list(range(offset,offset+len(loop))));offset+=len(loop)
for number,row in proposal['main_loop_xyz'].items():
 ids=mainLoopIDs[int(number)];assert len(ids)==len(row)
 for k,q in zip(ids,row):changes.append({'vertex':k,'old':list(me.vertices[k].co),'new':q,'reason':'Independent main front-side-rear large face and unequal thickness landmark'});me.vertices[k].co=q
# Continue the SAME mother face into each existing branch opening; keep all
# old terminal sections and twig/leaf anchors. No second rounded arm object.
for pa in patch['local_patches']:
 boundary=pa['native_mother_boundary'];delta=[me.vertices[k].co-oldV[k]for k in boundary]
 for field,w in [('restricted_opening',.72),('neck',.35),('intermediate_section',.14)]:
  for k,d in zip(pa[field],delta):
   q=me.vertices[k].co+d*w;changes.append({'vertex':k,'old':list(me.vertices[k].co),'new':list(q),'reason':'Same structural mother-face delta fading into owned graft; terminal untouched'});me.vertices[k].co=q
# Two finite support points split one FRONT panel. Adjacent faces share the
# new vertices; no full constant-height support ring, surface overlay or gap.
me.update();bm=bmesh.new();bm.from_mesh(me);bm.verts.ensure_lookup_table();bm.edges.ensure_lookup_table();bm.faces.ensure_lookup_table();originalBM=[bm.verts[k]for k in range(len(oldV))];newPoints=[];panel=next(f for f in bm.faces if set(v.index for v in f.verts)=={41,42,49,50})
for p in proposal['finite_support_points']:
 bm.verts.ensure_lookup_table();bm.edges.ensure_lookup_table();e=next(e for e in bm.edges if set(v.index for v in e.verts)==set(p['edge']));_,v=bmesh.utils.edge_split(e,bm.verts[p['edge'][0]],p['fraction']);v.co=p['XYZ'];newPoints.append(v)
bmesh.utils.face_split(panel,newPoints[0],newPoints[1]);bm.verts.index_update();bm.edges.index_update();bm.faces.index_update();assert all(v.index==k for k,v in enumerate(originalBM));supportIDs=[v.index for v in newPoints];bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free()
for f in me.polygons:f.use_smooth=True
me.update();V=[v.co.copy()for v in me.vertices];assert supportIDs==[322,323];crease=me.attributes.get('crease_edge');creaseChanges=[]
finiteCreases={frozenset([23,33]):.26,frozenset([33,42]):.18,frozenset([41,322]):.16,frozenset([322,49]):.08,frozenset([322,323]):.34,frozenset([42,323]):.12,frozenset([323,50]):.07,frozenset([49,57]):.20,frozenset([57,67]):.10}
for e in me.edges:
 if all(k<114 or k in supportIDs for k in e.vertices)and sum(V[k].z for k in e.vertices)/2>.49:
  before=crease.data[e.index].value;crease.data[e.index].value=finiteCreases.get(frozenset(e.vertices),0)
  if before!=crease.data[e.index].value:creaseChanges.append({'vertices':list(e.vertices),'before':before,'after':crease.data[e.index].value})
changedIDs={x['vertex']for x in changes};protectedControls=[k for k in range(len(oldV))if k not in changedIDs];assert all(V[k]==oldV[k]for k in protectedControls);assert all(V[k]==oldV[k]for k in range(20));assert all(V[k]==oldV[k]for k in range(100,114))
assert twigBefore['positions']==hashlib.sha256(json.dumps([list(v.co)for v in oldTwig.data.vertices]).encode()).hexdigest()
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
# Native v01 tertiary graft hierarchy is copied without regeneration.
tw=bpy.data.objects['Terminal twig hierarchy'];tw['authoring_version']=version;o['authoring_version']=version;o['construction']='One hand-authored asymmetric main structural flow with finite diagonal front support; actualR25 soil load/rootcaps/whole terminaltwigs/crown retained';o['form_gate']='Unadopted until ordinary neutral/night local root and UV checker review'
previous=json.loads((R.parent/'root-flow-0206/qa/geometry-inspection.json').read_text());twigchanges=[];protectedChecks=previous['protected_terminal_nodes']
rootchecks=[]
for br in rec['branches']:
 if not br['id'].startswith('root'):continue
 N=len(br['mouth_vertex_ids']);checks=[]
 for k in br['control_vertex_ids'][-N:]:
  q=V[k];h=soilH(q.x,q.y);checks.append({'position':list(q),'soil_z':h,'below_soil':h-q.z});assert h-q.z>.035
 rootchecks.append({'id':br['id'],'cap_burial':checks})
bpy.context.view_layer.update();ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get());surface=ev.to_mesh();surface.calc_loop_triangles();tris=[tuple(t.vertices)for t in surface.loop_triangles];bm=bmesh.new();bm.from_mesh(surface);volume=bm.calc_volume(signed=True);boundary=sum(e.is_boundary for e in bm.edges);nonmanifold=sum(not e.is_manifold for e in bm.edges);bm.free();tree=BVHTree.FromPolygons([v.co.copy()for v in surface.vertices],tris,all_triangles=True,epsilon=1e-9);pairs=[(a,b)for a,b in tree.overlap(tree)if a<b and set(tris[a]).isdisjoint(tris[b])];ins={'version':version,'control_vertices':len(me.vertices),'control_faces':len(me.polygons),'evaluated_vertices':len(surface.vertices),'triangles':len(tris),'volume':volume,'boundary_edges':boundary,'nonmanifold_edges':nonmanifold,'nonadjacent_intersections':len(pairs),'intersection_centres':[[list(sum((surface.vertices[v].co for v in tris[t]),Vector())/3)for t in pair]for pair in pairs[:20]],'root_soil':rootchecks,'protected_terminal_nodes':protectedChecks,'twig_changes':twigchanges,'all_unlisted_controls_unchanged':True,'original_soil_support0_19_unchanged':True,'support_points':supportIDs,'geometry_only_not_aesthetic':True};(R/'qa/geometry-inspection.json').write_text(json.dumps(ins,indent=2)+'\n');print(json.dumps(ins),flush=True);assert boundary==nonmanifold==len(pairs)==0 and volume>0
sha=lambda x:hashlib.sha256(json.dumps(x).encode()).hexdigest();record={'version':version,'source_native_sha256':hashlib.sha256((R.parent/'root-flow-0206/models/root-v02-editable.blend').read_bytes()).hexdigest(),'local_control_changes':changes,'protected_control_count':len(protectedControls),'protected_control_positions_sha256':sha([list(V[k])for k in protectedControls]),'positions_sha256':sha([list(v.co)for v in me.vertices]),'faces_sha256':sha([list(f.vertices)for f in me.polygons]),'normals_sha256':sha([list(v.normal)for v in me.vertices]),'uv_sha256':{l.name:sha([list(d.uv)for d in l.data])for l in me.uv_layers},'color_sha256':sha([list(d.color)for d in me.color_attributes.active_color.data]),'geometry':ins,'uv_method':'Recomputed every point from main and owned branch growth fields; per-corner circular unwrap; periodic integerU separated from real-lengthV; main body does not borrow nearest horizontal root branchUV','geometry_frozen':False,'finite_support_points':supportIDs,'crease_changes':creaseChanges,'native_twig_before':twigBefore};(R/'sculpt/control-record.json').write_text(json.dumps(record,indent=2)+'\n');(R/'design/local-control-changes.json').write_text(json.dumps({'changes':changes,'soil0_19_and_upper100_113_protected':True,'finite_support_points':supportIDs,'crease_changes':creaseChanges,'terminal_changes':twigchanges},indent=2)+'\n');ev.to_mesh_clear()
bpy.ops.wm.save_as_mainfile(filepath=str(R/'models'/f'{version}-editable.blend'),compress=True);bpy.ops.object.select_all(action='DESELECT');o.select_set(True);tw.select_set(True);bpy.ops.export_scene.gltf(filepath=str(R/'models'/f'{version}.glb'),export_format='GLB',use_selection=True,export_apply=True,export_extras=True,export_vertex_color='ACTIVE',export_draco_mesh_compression_enable=True,export_draco_mesh_compression_level=6,export_draco_position_quantization=15,export_draco_normal_quantization=11,export_draco_texcoord_quantization=13)
print(json.dumps({'native_bytes':(R/'models'/f'{version}-editable.blend').stat().st_size,'glb_bytes':(R/'models'/f'{version}.glb').stat().st_size}),flush=True)
