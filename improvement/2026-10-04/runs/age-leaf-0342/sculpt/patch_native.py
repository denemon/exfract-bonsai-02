from pathlib import Path
import bpy,bmesh,json,math,hashlib
from mathutils import Vector
from mathutils.bvhtree import BVHTree
R=Path('/Users/kazuki.tanaka/dev0/exfract-bonsai-02/improvement/2026-10-04/runs/age-leaf-0342');O=R.parent/'landmark-volume-0055';version='age-v01';assert not(R/'models'/f'{version}.glb').exists()
bpy.ops.wm.open_mainfile(filepath=str(R.parent/'local-edges-0056/models/edge-v02-editable.blend'));soil=bpy.data.objects['Continuous planted soil'];bpy.context.view_layer.update();soilTree=BVHTree.FromPolygons([soil.matrix_world@v.co for v in soil.data.vertices],[list(f.vertices)for f in soil.data.polygons])
def soilH(x,y):
 hit,_,_,_=soilTree.ray_cast(Vector((x,y,2)),Vector((0,0,-1)));assert hit is not None;return hit.z
bpy.ops.wm.open_mainfile(filepath=str(R.parent/'root-flow-0206/models/root-v02-editable.blend'));bpy.context.preferences.filepaths.save_version=0;o=bpy.data.objects['Continuous aged trunk and primary branches'];me=o.data;oldV=[v.co.copy()for v in me.vertices];rec=json.loads((O/'sculpt/control-record.json').read_text());patch=json.loads((O/'sculpt/control-record-v02.json').read_text());plan=json.loads((O/'design/landmarks.json').read_text());changes=[]
# Unequal local growth ridge across the existing turn, shallow neighboring
# recesses and short asymmetric branch shoulders. No global radius change.
deltas={21:(-.005,-.005,0),22:(0,.012,0),31:(-.006,-.009,0),32:(.003,.020,0),41:(-.005,-.025,.004),42:(-.004,.012,0),49:(.006,-.033,.001),50:(0,.029,-.005),57:(.004,-.027,.004),58:(.003,.022,-.004),67:(-.005,-.027,.002),68:(0,.019,0),75:(.003,-.022,.003),76:(0,.011,0),83:(-.004,-.015,0),84:(0,.006,0),202:(-.006,-.007,-.003),203:(-.004,-.011,.009),206:(.002,.004,-.007),207:(-.004,-.006,-.004),209:(-.002,-.006,.006),212:(0,.005,-.006),302:(.005,-.006,-.004),303:(.008,-.002,-.007),305:(0,-.007,.004),306:(.004,-.004,-.004),307:(.005,0,-.005),309:(0,-.004,.003)}
for k,delta in deltas.items():
 q=me.vertices[k].co+Vector(delta);changes.append({'vertex':k,'old':list(me.vertices[k].co),'new':list(q),'reason':'Finite uneven growth ridge / adjacent recess or local unequal graft shoulder'});me.vertices[k].co=q
# The right root shoulder enters the soil earlier, with the buried cap and
# center load body retained. Do not thin all roots into a uniform skirt.
for k in [186,187,188,189]:
 q=me.vertices[k].co.copy();q.x-=.011;q.y+=.009;q.z-=.004 if k%2 else .001
 changes.append({'vertex':k,'old':list(me.vertices[k].co),'new':list(q),'reason':'Local right soil-line shoulder, buried cap retained'});me.vertices[k].co=q
me.update();bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free();V=[v.co.copy()for v in me.vertices]
crease=me.attributes.get('crease_edge');ridgePairs=[{32,41},{41,49},{49,57},{57,67},{67,75},{75,83}];creaseChanges=[]
for edge in me.edges:
 if set(edge.vertices)in ridgePairs:
  before=crease.data[edge.index].value;crease.data[edge.index].value=.22 if set(edge.vertices)!={75,83}else .13;creaseChanges.append({'edge':list(edge.vertices),'before':before,'after':crease.data[edge.index].value})
changedIDs={x['vertex']for x in changes};protectedControls=[k for k in range(len(V))if k not in changedIDs];assert all(V[k]==oldV[k]for k in protectedControls)
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
tw=bpy.data.objects['Terminal twig hierarchy'];tw['authoring_version']=version;o['authoring_version']=version;o['construction']='Native R25 retained; local main growth ridge, unequal graft shoulders, right soil-line; native terminal twigs and crown instances unchanged';o['form_gate']='Unadopted until ordinary neutral/night local root and UV checker review'
previous=json.loads((R.parent/'root-flow-0206/qa/geometry-inspection.json').read_text());twigchanges=[];protectedChecks=previous['protected_terminal_nodes']
rootchecks=[]
for br in rec['branches']:
 if not br['id'].startswith('root'):continue
 N=len(br['mouth_vertex_ids']);checks=[]
 for k in br['control_vertex_ids'][-N:]:
  q=V[k];h=soilH(q.x,q.y);checks.append({'position':list(q),'soil_z':h,'below_soil':h-q.z});assert h-q.z>.035
 rootchecks.append({'id':br['id'],'cap_burial':checks})
bpy.context.view_layer.update();ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get());surface=ev.to_mesh();surface.calc_loop_triangles();tris=[tuple(t.vertices)for t in surface.loop_triangles];bm=bmesh.new();bm.from_mesh(surface);volume=bm.calc_volume(signed=True);boundary=sum(e.is_boundary for e in bm.edges);nonmanifold=sum(not e.is_manifold for e in bm.edges);bm.free();tree=BVHTree.FromPolygons([v.co.copy()for v in surface.vertices],tris,all_triangles=True,epsilon=1e-9);pairs=[(a,b)for a,b in tree.overlap(tree)if a<b and set(tris[a]).isdisjoint(tris[b])];ins={'version':version,'control_vertices':len(me.vertices),'control_faces':len(me.polygons),'evaluated_vertices':len(surface.vertices),'triangles':len(tris),'volume':volume,'boundary_edges':boundary,'nonmanifold_edges':nonmanifold,'nonadjacent_intersections':len(pairs),'intersection_centres':[[list(sum((surface.vertices[v].co for v in tris[t]),Vector())/3)for t in pair]for pair in pairs[:20]],'root_soil':rootchecks,'protected_terminal_nodes':protectedChecks,'twig_changes':twigchanges,'all_unlisted_controls_unchanged':True,'geometry_only_not_aesthetic':True};(R/'qa/geometry-inspection.json').write_text(json.dumps(ins,indent=2)+'\n');print(json.dumps(ins),flush=True);assert boundary==nonmanifold==len(pairs)==0 and volume>0
sha=lambda x:hashlib.sha256(json.dumps(x).encode()).hexdigest();record={'version':version,'source_native_sha256':hashlib.sha256((R.parent/'root-flow-0206/models/root-v02-editable.blend').read_bytes()).hexdigest(),'local_control_changes':changes,'protected_control_count':len(protectedControls),'protected_control_positions_sha256':sha([list(V[k])for k in protectedControls]),'positions_sha256':sha([list(v.co)for v in me.vertices]),'faces_sha256':sha([list(f.vertices)for f in me.polygons]),'normals_sha256':sha([list(v.normal)for v in me.vertices]),'uv_sha256':{l.name:sha([list(d.uv)for d in l.data])for l in me.uv_layers},'color_sha256':sha([list(d.color)for d in me.color_attributes.active_color.data]),'geometry':ins,'uv_method':'Recomputed every point from main and owned branch growth fields; per-corner circular unwrap; periodic integerU separated from real-lengthV; main body does not borrow nearest horizontal root branchUV','geometry_frozen':False,'crease_changes':creaseChanges};(R/'sculpt/control-record.json').write_text(json.dumps(record,indent=2)+'\n');(R/'design/local-control-changes.json').write_text(json.dumps({'changes':changes,'all_unlisted_controls_unchanged':True,'crease_changes':creaseChanges,'terminal_changes':twigchanges},indent=2)+'\n');ev.to_mesh_clear()
bpy.ops.wm.save_as_mainfile(filepath=str(R/'models'/f'{version}-editable.blend'),compress=True);bpy.ops.object.select_all(action='DESELECT');o.select_set(True);tw.select_set(True);bpy.ops.export_scene.gltf(filepath=str(R/'models'/f'{version}.glb'),export_format='GLB',use_selection=True,export_apply=True,export_extras=True,export_vertex_color='ACTIVE',export_draco_mesh_compression_enable=True,export_draco_mesh_compression_level=6,export_draco_position_quantization=15,export_draco_normal_quantization=11,export_draco_texcoord_quantization=13)
print(json.dumps({'native_bytes':(R/'models'/f'{version}-editable.blend').stat().st_size,'glb_bytes':(R/'models'/f'{version}.glb').stat().st_size}),flush=True)
