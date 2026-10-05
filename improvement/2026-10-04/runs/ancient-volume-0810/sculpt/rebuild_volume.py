"""Authored global control-volume change; shared topology and runtime budget preserved."""
from pathlib import Path
import bpy,bmesh,json,argparse,sys,math,hashlib
from mathutils import Vector
from mathutils.bvhtree import BVHTree
p=argparse.ArgumentParser();p.add_argument('--version',required=True);p.add_argument('--controls',type=Path,required=True);args=p.parse_args(sys.argv[sys.argv.index('--')+1:])
R=Path(__file__).resolve().parents[1];D=R.parent;start=json.loads((R/'start.json').read_text());basis=Path(start['protected_basis_native']);assert hashlib.sha256(basis.read_bytes()).hexdigest()==start['protected_basis_native_sha256'];record=D/'local-edges-0056/models/edge-v02.json';source=json.loads(record.read_text());guide=json.loads((D/'integrated-form-2245/models/form-v08.json').read_text());cfg=json.loads(args.controls.read_text());out=R/'models'/args.version;assert not out.with_suffix('.glb').exists() and not out.with_suffix('.json').exists();soil=.393
old=[Vector(v)for v in source['control_vertices']]
def smooth(a,b,v):t=max(0,min(1,(v-a)/(b-a)));return t*t*(3-2*t)
def interp(z,rows):
 if z<=rows[0][0]:return rows[0][1:]
 for a,b in zip(rows,rows[1:]):
  if z<=b[0]:
   t=(z-a[0])/(b[0]-a[0]);t=t*t*(3-2*t);return [a[i]+(b[i]-a[i])*t for i in range(1,len(a))]
 return rows[-1][1:]
def wrap(v):return (v+math.pi)%(2*math.pi)-math.pi
def bump(angle,centre,width):return math.exp(-.5*(wrap(angle-centre)/width)**2)
centres=[[z,*c]for z,c in zip(guide['controls']['main_heights'],guide['controls']['main_centres'])]
def main(v):
 z=v.z-soil;cx,cy=interp(z,centres);dx,dy,w,d,phase=interp(z,cfg['trunk_sections']);q=v-Vector((cx,cy,v.z));theta=math.atan2(q.y,q.x);fade=smooth(.025,.18,z)*(1-smooth(1.45,1.5572,z));
 # A wide erosion plane returns into one thick outer/back core. It is not
 # a thin independent ribbon or a row of narrow decorative grooves.
 cut=cfg['wide_plane_depth']*bump(theta,-1.42+phase,cfg.get('plane_width',.78))
 outer=cfg['outer_core_weight']*bump(theta,-2.60+phase,.66)
 depth_side=cfg['rear_core_weight']*bump(theta,1.00+phase,.85)
 rim=cfg.get('rim_weight',0)*bump(theta,-.64+phase,.29)
 shape=1+fade*(-cut+outer+depth_side+rim);q.x*=w*shape;q.y*=d*shape
 low=smooth(-.004,.10,z)*(1-smooth(.24,.48,z));root_shape=1+low*(cfg.get('root_left',.17)*bump(theta,-2.5,.40)+cfg.get('root_rear',.09)*bump(theta,.55,.49)-cfg.get('root_valley',.16)*bump(theta,-1.28,.48));q.x*=root_shape;q.y*=root_shape
 crest=low*(cfg.get('root_raise',.019)*bump(theta,-2.5,.4)-cfg.get('root_drop',.015)*bump(theta,-1.28,.48)+.009*bump(theta,.55,.49))
 if z<=.022:return v.copy()
 return Vector((cx+dx+q.x,cy+dy+q.y,v.z+crest))
branches=guide['branches'];groups=source['vertex_groups'];member={}
for j,b in enumerate(branches):
 for i,weight in groups['BRANCH · '+b['name']]:member.setdefault(i,[]).append(j)
def closest(v,path):
 lengths=[(b-a).length for a,b in zip(path,path[1:])];total=sum(lengths);best=None;before=0
 for i,(a,b,length)in enumerate(zip(path,path[1:],lengths)):
  delta=b-a;t=max(0,min(1,(v-a).dot(delta)/max(delta.length_squared,1e-9)));c=a+delta*t;distance=(v-c).length_squared
  if best is None or distance<best[0]:best=(distance,c,(before+t*length)/total,delta.normalized(),total)
  before+=length
 return best
paths=[]
for b in branches:paths.append([Vector((b['root'][0],b['root'][1],b['root'][2]+soil))]+[Vector((s[0],s[1],s[2]+soil))for s in b['sections']])
verts=[]
for i,v in enumerate(old):
 mv=main(v);options=member.get(i,[])
 if options:
  j=min(options,key=lambda j:closest(v,paths[j])[0]);distance,c,t,tangent,length=closest(v,paths[j]);b=branches[j];bc=cfg['branches'][b['name']];base=paths[j][0];offset=main(base)-base
  u=Vector((0,1,0));u=(u-tangent*u.dot(tangent)).normalized();n=tangent.cross(u).normalized();q=v-c;theta=math.atan2(q.dot(n),q.dot(u));strength=smooth(.03,.22,t)*(1-smooth(.72,.94,t));calibre=1+(bc['middle_calibre']-1)*strength
  radial=1+strength*(bc.get('upper_shoulder',.10)*bump(theta,-1.0,.65)-bc.get('underside_cut',.10)*bump(theta,1.85,.67))
  lateral=u*(q.dot(u)*calibre*radial)+n*(q.dot(n)*calibre*radial);along=tangent*q.dot(tangent)
  bend=Vector(bc['bend'])*math.sin(math.pi*t)*strength
  # The shoulder displacement dies out toward the fixed shoot attachment.
  bv=c+offset*(1-smooth(.14,.76,t))+bend+lateral+along
  mix=smooth(.02,.30,t);mv=mv.lerp(bv,mix)
 verts.append(mv)
# Lowest support controls and all distal branch joins stay fixed.
locked=[]
for i,v in enumerate(old):
 fixed=v.z<=soil+.022
 for j in member.get(i,[]):
  if closest(v,paths[j])[2]>.94:fixed=True
 if fixed:verts[i]=v.copy();locked.append(i)
bpy.ops.wm.open_mainfile(filepath=str(basis));core=bpy.data.objects['Continuous aged trunk and primary branches'];mesh=core.data;assert len(mesh.vertices)==len(verts)
for v,q in zip(mesh.vertices,verts):v.co=q
mesh.update()
# Creased long borders belong to the broad eroded face, not surface noise.
# The rear load-bearing cross-section stays rounded and thick.
added_creases=[]
if cfg.get('structural_crease',0):
 attr=mesh.attributes.get('crease_edge') or mesh.attributes.new('crease_edge','FLOAT','EDGE')
 for e in mesh.edges:
  a,b=[old[i] for i in e.vertices];z=(a.z+b.z)*.5-soil
  if not .10<z<1.40 or abs(a.z-b.z)<.028:continue
  cx,cy=interp(z,centres);phase=interp(z,cfg['trunk_sections'])[-1];v=(a+b)*.5;theta=math.atan2(v.y-cy,v.x-cx)
  if min(abs(wrap(theta-(-1.42+phase-cfg['plane_width']))),abs(wrap(theta-(-1.42+phase+cfg['plane_width']))))<.20:
   value=cfg['structural_crease']*smooth(.10,.25,z)*(1-smooth(1.15,1.40,z));attr.data[e.index].value=max(attr.data[e.index].value,value);added_creases.append([e.index,attr.data[e.index].value])
core['authoring_version']=args.version;core['construction']='Global authored volume: unequal front/back centre shifts, wide erosion plane returning into thick core, shorter asymmetric branch shoulder and unequal root support';core['source_basis_sha256']=start['protected_basis_native_sha256'];core['controls_source']=str(args.controls)
bpy.context.view_layer.update();ev=core.evaluated_get(bpy.context.evaluated_depsgraph_get());me=ev.to_mesh();me.calc_loop_triangles();tri=[tuple(t.vertices)for t in me.loop_triangles];bm=bmesh.new();bm.from_mesh(me);volume=bm.calc_volume(signed=True);boundary=sum(e.is_boundary for e in bm.edges);nonmanifold=sum(not e.is_manifold for e in bm.edges);bm.free();tree=BVHTree.FromPolygons([v.co.copy()for v in me.vertices],tri,all_triangles=True,epsilon=1e-9);cross=sum(i<j and set(tri[i]).isdisjoint(tri[j]) for i,j in tree.overlap(tree));sections=[]
for z in [.12,.29,.49,.70,.89,1.07,1.26]:
 plane=z+soil;points=[]
 for t in me.loop_triangles:
  poly=[me.vertices[i].co for i in t.vertices]
  for a,b in zip(poly,poly[1:]+poly[:1]):
   if (a.z-plane)*(b.z-plane)<0:points.append(a+(b-a)*((plane-a.z)/(b.z-a.z)))
 if points:
  cx,cy=interp(z,centres);near=[q for q in points if abs(q.x-cx)<.42 and abs(q.y-cy)<.42];width=max(q.x for q in near)-min(q.x for q in near);depth=max(q.y for q in near)-min(q.y for q in near);sections.append({'z_above_soil':z,'width':width,'depth':depth,'depth_width_ratio':depth/width})
inspection={'control_vertices':len(verts),'evaluated_triangles':len(tri),'signed_volume':volume,'volume_vs_basis':volume/source['inspection']['volume'],'boundary_edges':boundary,'nonmanifold_edges':nonmanifold,'nonadjacent_intersections':cross,'locked_control_count':len(locked),'locked_control_max_error':max((verts[i]-old[i]).length for i in locked),'max_move':max((a-b).length for a,b in zip(verts,old)),'cross_sections':sections};ev.to_mesh_clear();assert boundary==nonmanifold==cross==0,inspection;assert len(tri)<=18540 and volume>0;assert all(s['depth_width_ratio']>.48 for s in sections),inspection
meta={'version':args.version,'basis_native':str(basis),'basis_sha256':start['protected_basis_native_sha256'],'basis_controls':str(record),'basis_controls_sha256':hashlib.sha256(record.read_bytes()).hexdigest(),'controls':cfg,'control_positions':[list(v)for v in verts],'inspection':inspection,'unchanged':'Topology,UVs,color attributes,creases,pot/soil/stone/foliage; root contact ends and distal branch attachments','native_saved':False,'authored_edge_creases':added_creases};out.with_suffix('.json').write_text(json.dumps(meta,indent=2)+'\n')
# Geometry-only runtime material placeholder: browser shader supplies final PBR.
mat=bpy.data.materials.new('Continuous wood runtime placeholder');mat.diffuse_color=(.34,.29,.21,1);mesh.materials.clear();mesh.materials.append(mat)
for o in bpy.context.scene.objects:o.select_set(o==core)
bpy.context.view_layer.objects.active=core;bpy.ops.export_scene.gltf(filepath=str(out.with_suffix('.glb')),export_format='GLB',use_selection=True,export_apply=True,export_extras=True,export_vertex_color='ACTIVE',export_draco_mesh_compression_enable=True,export_draco_mesh_compression_level=6,export_draco_position_quantization=15,export_draco_normal_quantization=11,export_draco_texcoord_quantization=13)
assert out.with_suffix('.glb').stat().st_size<=150000
print(json.dumps({'version':args.version,'inspection':inspection,'glb_bytes':out.with_suffix('.glb').stat().st_size}),flush=True)
