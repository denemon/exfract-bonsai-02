"""One connected quad cage; no old trunk, field, Boolean, grain or displacement."""
import bpy,bmesh,sys,argparse,json,math,shutil,hashlib
from pathlib import Path
from mathutils import Vector
p=argparse.ArgumentParser();p.add_argument('--version',required=True);p.add_argument('--controls');p.add_argument('--save-native',action='store_true');args=p.parse_args(sys.argv[sys.argv.index('--')+1:])
run=Path(__file__).resolve().parents[1];out=run/'models'/args.version;assert not out.with_suffix('.glb').exists();assert shutil.disk_usage(run).free>2*1024**3
soil=.393;N=16
controls={'method':'one closed quad cage with shared-vertex first fork','soil':soil,'sides':N,'subdivision':2,'sections':[
# z, centre x/y, width radius, depth radius, rotation in degrees
[-.09,.005,.035,.345,.272,-4],[.016,.015,.028,.304,.245,0],[.125,.050,.025,.254,.202,7],[.265,.083,.025,.225,.187,13],[.405,.020,.035,.221,.178,21],[.550,-.100,.055,.218,.179,27],[.685,-.155,.050,.207,.174,32],[.820,-.092,.033,.175,.167,38],[.955,.035,.018,.158,.157,42],[1.090,.137,.036,.140,.146,45],[1.210,.177,.057,.113,.123,48],[1.310,.191,.068,.097,.108,50],[1.352,.188,.069,.072,.078,51]],
'angular_profile':[1.05,1.0,.94,.90,.95,1.04,1.12,1.08,.98,.92,.94,1.02,1.10,1.08,.99,.97],
'root_lobes':[[-2.55,.19,.46],[-.78,.09,.61],[1.50,.13,.50]],
'branches':[{'name':'First left living branch','patch':{'rows':[5,7],'sectors':[6,10]},'sections':[[-.418,.020,.744,.113,.118],[-.586,-.005,.814,.090,.084],[-.754,-.018,.853,.066,.057],[-.890,-.030,.848,.048,.045],[-.958,-.026,.828,.029,.030],[-.985,-.024,.820,.021,.022]]}]}
if args.controls:controls=json.loads(Path(args.controls).read_text())
N=controls['sides'];soil=controls['soil'];verts=[];faces=[];rings=[];section_metrics=[]
def wrapped(a):return (a+math.pi)%(2*math.pi)-math.pi
for k,(z,cx,cy,rx,ry,turn) in enumerate(controls['sections']):
 ids=[];points=[];phi=math.radians(turn);root=max(0,1-max(z,0)/controls.get('root_falloff_height',.31))**controls.get('root_falloff_exponent',1.45)
 for j in range(N):
  theta=2*math.pi*j/N;profile=1+(controls['angular_profile'][j]-1)*(.60+.25*math.sin(z*2+.2));lobes=sum(amp*math.exp(-.5*(wrapped(theta-angle)/spread)**2) for angle,amp,spread in controls['root_lobes']);r=profile+root*lobes
  sx,sy=math.cos(theta),math.sin(theta)
  if 'section_shape' in controls:
   blend=controls.get('section_shape_strength',.8)*min(1,max(0,z/.28));px,py=controls['section_shape'][j];sx=sx*(1-blend)+px*blend;sy=sy*(1-blend)+py*blend
  x=rx*sx*r;y=ry*sy*r
  # Root crest heights vary, but all ring heights remain ordered. The lowest
  # perimeter is buried and no buttress is an exposed sharp-tipped tube.
  zz=z+soil+(0 if k==0 else (.016*root*math.cos(theta+.55) if 'root_height_amplitude' not in controls else root*(controls['root_height_amplitude']*lobes-controls.get('root_valley_lowering',0))))
  v=(cx+x*math.cos(phi)-y*math.sin(phi),cy+x*math.sin(phi)+y*math.cos(phi),zz)
  if str(k) in controls.get('section_overrides',{}):
   ox,oy,oz=controls['section_overrides'][str(k)][j];v=(ox,oy,oz+soil)
  ids.append(len(verts));verts.append(v);points.append(v)
 rings.append(ids);width=max(v[0] for v in points)-min(v[0] for v in points);depth=max(v[1] for v in points)-min(v[1] for v in points);section_metrics.append({'nominal_z_above_soil':z,'actual_z_range':[min(v[2] for v in points)-soil,max(v[2] for v in points)-soil],'frontal_width':width,'front_back_depth':depth,'depth_to_width':depth/width})
patches=[b['patch'] for b in controls['branches']]
for row in range(len(rings)-1):
 for j in range(N):
  if any(p['rows'][0]<=row<p['rows'][1] and p['sectors'][0]<=j<p['sectors'][1] for p in patches):continue
  faces.append((rings[row][j],rings[row][(j+1)%N],rings[row+1][(j+1)%N],rings[row+1][j]))
faces.append(tuple(reversed(rings[0])));faces.append(tuple(rings[-1]))
branch_boundaries=[]
for branch in controls['branches']:
 p=branch['patch'];r0,r1=p['rows'];j0,j1=p['sectors']
 loop=[rings[r0][j] for j in range(j0,j1)]+[rings[r][j1] for r in range(r0,r1)]+[rings[r1][j] for j in range(j1,j0,-1)]+[rings[r][j0] for r in range(r1,r0,-1)]
 base=sum((Vector(verts[i]) for i in loop),Vector())/len(loop)
 sections=branch['sections'];centres=[Vector((s[0],s[1],s[2]+soil)) for s in sections]
 axis=(centres[1]-base).normalized();u=Vector((0,1,0));u=(u-axis*u.dot(axis)).normalized();v=axis.cross(u).normalized()
 angles=[]
 for i in loop:
  q=Vector(verts[i])-base;angle=math.atan2(q.dot(v),q.dot(u))
  if angles:
   while angle<angles[-1]-.01:angle+=2*math.pi
  angles.append(angle)
 assert angles[-1]-angles[0]<2*math.pi,('Branch boundary folds',angles)
 relaxation=branch.get('angle_relaxation',0)
 if relaxation:
  start_angle=sum(angle-j*2*math.pi/len(loop) for j,angle in enumerate(angles))/len(loop)
  angles=[angle*(1-relaxation)+(start_angle+j*2*math.pi/len(loop))*relaxation for j,angle in enumerate(angles)]
 previous=loop;created=[]
 for k,(cx,cy,z,ru,rv) in enumerate(sections):
  center=centres[k];tangent=((centres[min(k+1,len(centres)-1)] if k<len(centres)-1 else center+(center-centres[k-1]))-(centres[k-1] if k else base)).normalized();u=Vector((0,1,0));u=(u-tangent*u.dot(tangent)).normalized();v=tangent.cross(u).normalized();current=[]
  for j,angle in enumerate(angles):
   # Unequal upper/underside shoulder radii are explicit cage controls. No
   # independent branch tube is intersected into the parent.
   under=1+.08*math.sin(angle) if k<2 else 1
   q=center+u*(math.cos(angle)*ru)+v*(math.sin(angle)*rv*under)
   current.append(len(verts));verts.append(tuple(q))
  for j in range(len(loop)):faces.append((previous[j],previous[(j+1)%len(loop)],current[(j+1)%len(loop)],current[j]))
  previous=current;created.append(current)
 faces.append(tuple(previous));branch_boundaries.append({'name':branch['name'],'shared_boundary_vertices':loop,'new_rings':created})
# The interior vertices of the removed branch patch have no incident faces.
# Compact them out; the shared perimeter remains exactly the same vertices.
used=sorted({i for face in faces for i in face});remap={old:new for new,old in enumerate(used)};verts=[verts[i] for i in used];faces=[tuple(remap[i] for i in face) for face in faces]
for branch in branch_boundaries:
 branch['shared_boundary_vertices']=[remap[i] for i in branch['shared_boundary_vertices']];branch['new_rings']=[[remap[i] for i in row] for row in branch['new_rings']]
# Assemble only the fixed support assets; no old wood or old controls are loaded.
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
base=run.parent/'volume-rebuild-1656/models/hero-v20.blend'
assert hashlib.sha256(base.read_bytes()).hexdigest()=='ca3eb2b5f1e55ba51671ecfafa20ff0d48076756f3dda7467da0e7e0bb6d5b08'
with bpy.data.libraries.load(str(base),link=False) as (source,target):target.objects=[n for n in source.objects if n.startswith(('Shallow unglazed pot','Low ceramic foot','Low split natural bedding stone','Continuous planted soil'))]
for ob in target.objects:
 if ob:bpy.context.collection.objects.link(ob)
mesh=bpy.data.meshes.new('Continuous anatomical control cage');mesh.from_pydata(verts,[],faces);mesh.update();bm=bmesh.new();bm.from_mesh(mesh);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(mesh);bm.free()
core=bpy.data.objects.new('Continuous aged trunk and primary branches',mesh);bpy.context.collection.objects.link(core);core['authoring_version']=args.version;core['construction']='single shared-vertex branched quad cage';core['no_texture_no_grain_no_old_trunk']=True
mat=bpy.data.materials.new('Neutral inspection wood');mat.use_nodes=True;bs=mat.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(.43,.43,.41,1);bs.inputs['Roughness'].default_value=1;mesh.materials.append(mat)
for f in mesh.polygons:f.use_smooth=True
sub=core.modifiers.new('Coarse cage interpolation','SUBSURF');sub.levels=controls['subdivision'];sub.render_levels=sub.levels
bpy.context.view_layer.objects.active=core;core.select_set(True)

def inspect(me):
 bm=bmesh.new();bm.from_mesh(me);bm.verts.ensure_lookup_table();seen=set();components=[]
 for start in bm.verts:
  if start.index in seen:continue
  stack=[start];seen.add(start.index);count=0
  while stack:
   cur=stack.pop();count+=1
   for edge in cur.link_edges:
    nxt=edge.other_vert(cur)
    if nxt.index not in seen:seen.add(nxt.index);stack.append(nxt)
  components.append(count)
 result={'vertices':len(bm.verts),'faces':len(bm.faces),'boundary_edges':sum(e.is_boundary for e in bm.edges),'nonmanifold_edges':sum(not e.is_manifold for e in bm.edges),'components':components,'signed_volume':bm.calc_volume(signed=True)};bm.free();assert result['boundary_edges']==0 and result['nonmanifold_edges']==0 and len(components)==1 and result['signed_volume']>0,result;return result
coarse=inspect(mesh);evaluated=core.evaluated_get(bpy.context.evaluated_depsgraph_get());fine=inspect(evaluated.to_mesh());evaluated.to_mesh_clear()
meta={'version':args.version,'controls':controls,'control_vertices':verts,'control_faces':faces,'branch_topology':branch_boundaries,'cross_sections':section_metrics,'control_inspection':coarse,'evaluated_inspection':fine,'support_reference':str(base),'wood_source':'new independent cage; no old wood geometry'}
out.with_suffix('.json').write_text(json.dumps(meta,indent=2)+'\n');out.with_suffix('.controls.json').write_text(json.dumps(controls,indent=2)+'\n')
if args.save_native:bpy.ops.wm.save_as_mainfile(filepath=str(out.with_suffix('.blend')),compress=True)
for ob in bpy.context.scene.objects:ob.select_set(ob.type=='MESH')
bpy.ops.export_scene.gltf(filepath=str(out.with_suffix('.glb')),export_format='GLB',use_selection=True,export_yup=True,export_normals=True,export_materials='EXPORT',export_apply=True,export_extras=True,export_draco_mesh_compression_enable=False)
shutil.copy2(out.with_suffix('.glb'),run/'site/public/models/hero.glb');print(json.dumps({'version':args.version,'control':coarse,'evaluated':fine,'cross_sections':section_metrics,'glb_bytes':out.with_suffix('.glb').stat().st_size}),flush=True)
