"""Edit the saved shared-vertex cage; broad growth surfaces, no fine grain."""
import bpy,bmesh,sys,json,math,argparse,hashlib,shutil
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
p=argparse.ArgumentParser();p.add_argument('--version',default='form-v01');p.add_argument('--controls');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);run=Path(__file__).resolve().parents[1];out=run/'models'/a.version;assert not out.with_suffix('.glb').exists();assert shutil.disk_usage(run).free>2*1024**3
basis=run.parent/'anatomy-2150';old=json.loads((basis/'models/cage-v06.json').read_text());c=old['controls'];soil=c['soil'];N=c['sides'];verts=[Vector(v) for v in old['control_vertices']];faces=[list(f) for f in old['control_faces']]
# Recover the original parent-ring indexing from the compact shared cage.
removed={r*N+j for b in c['branches'] for r in range(b['patch']['rows'][0]+1,b['patch']['rows'][1]) for j in range(b['patch']['sectors'][0]+1,b['patch']['sectors'][1])};originals=[i for i in range(N*len(c['sections'])) if i not in removed];mapping={old:i for i,old in enumerate(originals)};parent_rings=[[mapping.get(k*N+j) for j in range(N)] for k in range(len(c['sections']))]
control={'basis':'cage-v06 exact saved shared cage','main_centres':[[.005,.030],[.015,.022],[.043,.008],[.025,-.04],[.055,.004],[-.052,.080],[-.180,.102],[-.205,.11],[-.220,.065],[-.115,.02],[.032,-.03],[.092,-.078],[.115,-.09],[.143,-.038],[.105,-.044],[.10,.015],[.082,.073],[.143,.06],[.163,.045],[.265,.078],[.313,.09],[.302,.095]],'calibre':[[1,1],[1,1],[1,1],[.94,1.05],[1.12,.98],[1.07,1.09],[.93,1.04],[1.03,.96],[.93,1.10],[1.06,1.02],[.98,1.1],[1.08,.98],[1.04,.95],[.92,1.1],[1.05,.96],[1.03,1.12],[.87,1.03],[1.02,1.03],[1.12,.94],[1.0,1.05],[1.2,.9],[1.5,1.1]],'large_plane_strength':1,'branches':[
{'name':'First left living branch','sections':[[-.431,-.048,.718,.094,.073],[-.577,-.114,.714,.079,.052],[-.737,-.18,.797,.061,.045],[-.89,-.158,.819,.044,.032],[-.976,-.100,.803,.027,.025]]},
{'name':'Rear ascending primary','sections':[[-.18,.213,1.076,.068,.049],[-.35,.318,1.117,.052,.04],[-.514,.365,1.217,.039,.031],[-.727,.296,1.224,.021,.020],[-.793,.285,1.255,.014,.014]]},
{'name':'Right crown primary','sections':[[.317,-.018,1.125,.084,.065],[.503,-.11,1.119,.063,.049],[.649,-.105,1.214,.052,.033],[.787,-.018,1.214,.031,.030],[.918,.015,1.248,.023,.019],[.987,.002,1.249,.015,.018]]},
{'name':'Upper left primary','sections':[[-.1,-.032,1.448,.058,.053],[-.25,-.106,1.439,.051,.038],[-.4,-.156,1.521,.036,.031],[-.506,-.093,1.528,.021,.023],[-.566,-.068,1.559,.015,.014]]}],
'low_branch':{'name':'Subordinate low right','patch':{'rows':[3,5],'sectors':[14,16]},'angle_relaxation':.4,'sections':[[.337,-.016,.404,.068,.054],[.47,-.074,.411,.053,.046],[.58,-.036,.469,.045,.031],[.733,-.048,.455,.028,.025],[.855,-.075,.491,.018,.020]]}}
if a.controls:control=json.loads(Path(a.controls).read_text())
def delta(a,b):return (a-b+math.pi)%(2*math.pi)-math.pi
def gauss(a,b,w):return math.exp(-.5*(delta(a,b)/w)**2)
def smooth(a,b,v):t=max(0,min(1,(v-a)/(b-a)));return t*t*(3-2*t)
colours=[(0,.5,.5,1)]*len(verts)
for k,ring in enumerate(parent_rings):
 z,cx,cy,rx,ry,turn=c['sections'][k];original_height=z;nx,ny=control['main_centres'][k];wx,wy=control['calibre'][k]
 for j,idx in enumerate(ring):
  if idx is None:continue
  oldp=verts[idx].copy();q=oldp-Vector((cx,cy,original_height+soil));z=control.get('main_heights',[s[0] for s in c['sections']])[k];ang=math.atan2(q.y,q.x)
  if k>2:
   # Two unequal broad weathered planes and a rounded outer ridge. The
   # depression remains a fraction of an already solid elliptical section.
   front=-1.62-.58*math.exp(-((z-.64)/.23)**2)+.32*math.exp(-((z-1.24)/.18)**2)
   swell=.10*gauss(ang,front-.90,.40)*(1-smooth(1.35,1.72,z))
   plane=-.22*gauss(ang,front,.41)*smooth(.16,.34,z)*(1-smooth(1.42,1.72,z))
   shoulder=.09*gauss(ang,.15+z*.60,.55)*math.exp(-((z-.42)/.36)**2)
   shape=(1+(swell+plane+shoulder)*control['large_plane_strength'])*control.get('contour_profiles',{}).get(str(k),[1.]*N)[j]
   q.x*=wx*shape;q.y*=wy*shape
   q.z+=.009*math.sin(ang+z*3.1)*(1-smooth(1.5,1.73,z))
   verts[idx]=Vector((nx,ny,z+soil))+q
  # Live tissue follows the right flank, narrows at the inside bend, and
  # returns behind upper branches. It is an attribute of this same surface.
  life_angle=-.68-.69*math.exp(-((z-.60)/.23)**2)+.60*smooth(.98,1.56,z)
  life_width=.39-.10*math.exp(-((z-.73)/.27)**2)+.11*smooth(1.05,1.65,z)
  living=gauss(ang,life_angle,life_width)
  colours[idx]=(living,.5,.43+.1*math.cos(ang*1.3+z*4.1),1)

def fill_branch(record,sections,existing=None):
 loop=record['shared_boundary_vertices'];base=sum((verts[i] for i in loop),Vector())/len(loop);centres=[Vector((s[0],s[1],s[2]+soil)) for s in sections]
 axis=(centres[1]-base).normalized();u=Vector((0,1,0));u=(u-axis*u.dot(axis)).normalized();v=axis.cross(u).normalized();angles=[]
 for i in loop:
  q=verts[i]-base;ang=math.atan2(q.dot(v),q.dot(u))
  if angles and not control.get('uniform_branch_loops'):
   while ang<angles[-1]-.01:ang+=math.tau
  angles.append(ang)
 if control.get('uniform_branch_loops'):
  phase=math.atan2(sum(math.sin(ang-j*math.tau/len(loop)) for j,ang in enumerate(angles)),sum(math.cos(ang-j*math.tau/len(loop)) for j,ang in enumerate(angles)));angles=[phase+j*math.tau/len(loop) for j in range(len(loop))]
 else:assert angles[-1]-angles[0]<math.tau,(record['name'],angles)
 relax=record.get('angle_relaxation',.25);start_angle=sum(ang-j*math.tau/len(loop) for j,ang in enumerate(angles))/len(loop);angles=[ang*(1-relax)+(start_angle+j*math.tau/len(loop))*relax for j,ang in enumerate(angles)]
 previous=loop;new=[]
 for k,(cx,cy,z,ru,rv) in enumerate(sections):
  centre=centres[k];tangent=((centres[k+1] if k<len(centres)-1 else centre+(centre-centres[k-1]))-(centres[k-1] if k else base)).normalized();u=Vector((0,1,0));u=(u-tangent*u.dot(tangent)).normalized();v=tangent.cross(u).normalized();ring=[]
  for j,ang in enumerate(angles):
   rad=1-.13*gauss(ang,-1.6,.6)+.10*gauss(ang,.25+k*.12,.4)
   point=centre+u*(math.cos(ang)*ru*rad)+v*(math.sin(ang)*rv*rad)
   color=(.50+.47*smooth(-.65,.65,math.cos(ang-.3)),.5,.45+.08*math.sin(ang*2+k),1)
   if existing is not None:idx=existing[k][j];verts[idx]=point;colours[idx]=color
   else:idx=len(verts);verts.append(point);colours.append(color)
   ring.append(idx)
  if existing is None:
   for j in range(len(loop)):faces.append([previous[j],previous[(j+1)%len(loop)],ring[(j+1)%len(loop)],ring[j]])
  previous=ring;new.append(ring)
 if existing is None:faces.append(list(previous))
 return {'name':record['name'],'shared_boundary_vertices':loop,'new_rings':new,'sections':sections,'root':list(base-Vector((0,0,soil))),'angle_relaxation':relax}
branches=[]
for source,edit in zip(old['branch_topology'],control['branches']):
 assert source['name']==edit['name'];branches.append(fill_branch(source,edit['sections'],source['new_rings']))
if control.get('low_branch'):
 b=control['low_branch'];r0,r1=b['patch']['rows'];j0,j1=b['patch']['sectors'];at=lambda r,j:parent_rings[r][j%N]
 patch={frozenset((at(r,j),at(r,j+1),at(r+1,j+1),at(r+1,j))) for r in range(r0,r1) for j in range(j0,j1)};before=len(faces);faces=[f for f in faces if frozenset(f) not in patch];assert before-len(faces)==(r1-r0)*(j1-j0)
 loop=[at(r0,j) for j in range(j0,j1)]+[at(r,j1) for r in range(r0,r1)]+[at(r1,j) for j in range(j1,j0,-1)]+[at(r,j0) for r in range(r1,r0,-1)];assert None not in loop
 branches.append(fill_branch({'name':b['name'],'shared_boundary_vertices':loop,'angle_relaxation':b['angle_relaxation']},b['sections']))
used=sorted({i for f in faces for i in f});remap={i:n for n,i in enumerate(used)};verts=[verts[i] for i in used];colours=[colours[i] for i in used];faces=[[remap[i] for i in f] for f in faces]
for b in branches:b['shared_boundary_vertices']=[remap[i] for i in b['shared_boundary_vertices']];b['new_rings']=[[remap[i] for i in r] for r in b['new_rings']]
parent_rings=[[remap.get(i) for i in r] for r in parent_rings]
bpy.ops.wm.open_mainfile(filepath=str(basis/'models/best-coarse.blend'));core=bpy.data.objects['Continuous aged trunk and primary branches'];previous=core.data;me=bpy.data.meshes.new('Edited continuous large growth planes');me.from_pydata(verts,[],faces);me.update();bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free();core.data=me
core.vertex_groups.clear();root=core.vertex_groups.new(name='ROOT · retained continuous ground spread');root.add([i for i,v in enumerate(verts) if v.z<soil+.23],1,'REPLACE');branch_ids=set()
for b in branches:
 ids={i for ring in b['new_rings'] for i in ring};branch_ids.update(ids);group=core.vertex_groups.new(name='BRANCH · '+b['name']);group.add(sorted(ids|set(b['shared_boundary_vertices'])),1,'REPLACE')
group=core.vertex_groups.new(name='TRUNK · continuous major planes');group.add([i for i in range(len(verts)) if i not in branch_ids],1,'REPLACE')
for f in me.polygons:f.use_smooth=True
attr=me.color_attributes.new(name='Continuous growth masks',type='FLOAT_COLOR',domain='POINT');attr.data.foreach_set('color',[v for row in colours for v in row]);me.color_attributes.active_color=attr
uv=me.uv_layers.new(name='Coarse spatial coordinates')
for l in me.loops:p=me.vertices[l.vertex_index].co;uv.data[l.index].uv=(p.x,p.z)
mat=bpy.data.materials.new('Continuous wood growth');mat.use_nodes=True;mat.diffuse_color=(.43,.39,.31,1);bs=mat.node_tree.nodes.get('Principled BSDF');bs.inputs['Roughness'].default_value=.93;bs.inputs['Base Color'].default_value=(.43,.39,.31,1);me.materials.append(mat)
# Restore the support material names without changing any support geometry.
for ob in bpy.context.scene.objects:
 if ob.type!='MESH' or ob==core:continue
 name='Unglazed ceramic' if ob.name.startswith(('Shallow','Low ceramic')) else 'Planted soil' if ob.name.startswith('Continuous planted') else 'Bedding stone';m=bpy.data.materials.get(name) or bpy.data.materials.new(name);m.diffuse_color=(.18,.12,.08,1);ob.data.materials.clear();ob.data.materials.append(m)
core['authoring_version']=a.version;core['construction']='Edited cage-v06, shared root/trunk/branch vertices, continuous surface growth masks';core['no_fine_grain']=True
bpy.context.view_layer.update();ev=core.evaluated_get(bpy.context.evaluated_depsgraph_get());evaluated=ev.to_mesh();bm=bmesh.new();bm.from_mesh(evaluated);bm.verts.ensure_lookup_table();seen=set();components=[]
for v in bm.verts:
 if v.index in seen:continue
 stack=[v];seen.add(v.index);n=0
 while stack:
  q=stack.pop();n+=1
  for e in q.link_edges:
   nxt=e.other_vert(q)
   if nxt.index not in seen:seen.add(nxt.index);stack.append(nxt)
 components.append(n)
evaluated.calc_loop_triangles();tri=[tuple(t.vertices) for t in evaluated.loop_triangles];tree=BVHTree.FromPolygons([v.co for v in evaluated.vertices],tri,all_triangles=True,epsilon=1e-9);intersections=[(i,j) for i,j in tree.overlap(tree) if i<j and not set(tri[i]).intersection(tri[j])]
inspection={'control_vertices':len(verts),'control_faces':len(faces),'evaluated_vertices':len(evaluated.vertices),'triangles':len(tri),'volume':bm.calc_volume(signed=True),'components':components,'boundary_edges':sum(e.is_boundary for e in bm.edges),'nonmanifold_edges':sum(not e.is_manifold for e in bm.edges),'nonadjacent_intersections':len(intersections)};bm.free();ev.to_mesh_clear();assert inspection['boundary_edges']==0 and inspection['nonmanifold_edges']==0 and len(components)==1 and not intersections,inspection
meta={'version':a.version,'subdivision':2,'basis_native':str(basis/'models/best-coarse.blend'),'basis_sha256':hashlib.sha256((basis/'models/best-coarse.blend').read_bytes()).hexdigest(),'controls':control,'control_vertices':[list(v) for v in verts],'control_faces':faces,'colors':colours,'parent_rings':parent_rings,'branches':branches,'soil':soil,'inspection':inspection};out.with_suffix('.json').write_text(json.dumps(meta,indent=2)+'\n');out.with_suffix('.controls.json').write_text(json.dumps(control,indent=2)+'\n')
for ob in bpy.context.scene.objects:ob.select_set(ob.type=='MESH')
bpy.context.view_layer.objects.active=core;bpy.ops.export_scene.gltf(filepath=str(out.with_suffix('.glb')),export_format='GLB',use_selection=True,export_apply=True,export_yup=True,export_normals=True,export_materials='EXPORT',export_vertex_color='ACTIVE',export_extras=True,export_draco_mesh_compression_enable=False)
print(json.dumps({'version':a.version,'inspection':inspection,'glb_bytes':out.with_suffix('.glb').stat().st_size}),flush=True)
