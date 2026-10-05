"""A continuous, broad old-tree volume. Run inside Blender; original geometry only."""
import bpy, math, random, json, argparse, sys, shutil, time
from pathlib import Path
from mathutils import Vector, noise, kdtree

args=argparse.ArgumentParser();args.add_argument('--out',required=True);args.add_argument('--version',default='v01');args.add_argument('--foliage',action='store_true')
opt=args.parse_args(sys.argv[sys.argv.index('--')+1:]);OUT=Path(opt.out);OUT.mkdir(parents=True,exist_ok=True)
started=time.monotonic()
def progress(text):print(f'{time.monotonic()-started:.1f}s {text}',flush=True)
random.seed(4101329)
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
SOIL=.393

def material(name,base,rough=.85):
 m=bpy.data.materials.new(name);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*base,1);p.inputs['Roughness'].default_value=rough
 return m
WOOD=material('Sculpted wood shader',(0.27,.21,.15));LEAF=material('Scale foliage shader',(.10,.18,.055));POT=material('Unglazed ceramic shader',(.22,.12,.075));STONE=material('Natural bedding stone',(.22,.23,.20));SOILMAT=material('Moss and mineral soil',(.07,.085,.025))

def make(name,verts,faces,mat,smooth=True):
 me=bpy.data.meshes.new(name);me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(o);me.materials.append(mat)
 for p in me.polygons:p.use_smooth=smooth
 return o
def smooth(a,b,x):
 t=max(0,min(1,(x-a)/(b-a)));return t*t*(3-2*t)
def angle_delta(a,b):return (a-b+math.pi)%math.tau-math.pi
def cat(points,t):
 n=len(points)-1;i=min(n-1,int(t*n));u=t*n-i;a=points[max(0,i-1)];b=points[i];c=points[i+1];d=points[min(n,i+2)]
 return .5*(2*b+(-a+c)*u+(2*a-5*b+4*c-d)*u*u+(-a+3*b-3*c+d)*u*u*u)

# Z sections are sculpted cross-sections of a single body, not a swept living cord.
# Each row: height, centre X/Y, side-to-side and front-to-back half widths.
sections=[
 (-.022,.015,.01,.22,.18),(.025,.012,.025,.245,.20),(.10,.035,.04,.248,.205),
 (.22,.055,.06,.235,.18),(.34,-.015,.075,.235,.17),(.48,-.15,.075,.225,.175),
 (.61,-.25,.035,.225,.16),(.72,-.245,-.012,.23,.155),(.83,-.12,-.035,.205,.145),
 (.96,.07,-.015,.165,.135),(1.08,.205,.045,.14,.12),(1.20,.28,.075,.112,.105),
 (1.32,.32,.055,.079,.074),(1.405,.34,.035,.045,.045),(1.45,.355,.04,.004,.005),
]
def section(z):
 k=0
 while k<len(sections)-2 and z>sections[k+1][0]:k+=1
 a=sections[k];b=sections[k+1];t=(z-a[0])/(b[0]-a[0]);t=max(0,min(1,t));t=t*t*(3-2*t)
 return tuple(a[j]*(1-t)+b[j]*t for j in range(1,5))
guides=[]
def add_guide(p,tangent,radius,arc,kind,seed):
 tangent=Vector(tangent).normalized();n=tangent.cross(Vector((0,1,0))).normalized()
 if n.length<.2:n=tangent.cross(Vector((1,0,0))).normalized()
 b=tangent.cross(n).normalized();guides.append((Vector(p),tangent,n,b,radius,arc,kind,seed))

verts=[];faces=[];rings=235;sides=80
for j in range(rings+1):
 z=sections[0][0]+(sections[-1][0]-sections[0][0])*j/rings;cx,cy,rx,ry=section(z)
 dz=.002;pa=section(max(sections[0][0],z-dz));pb=section(min(sections[-1][0],z+dz));add_guide((cx,cy,z),(pb[0]-pa[0],pb[1]-pa[1],2*dz),(rx+ry)/2,z,0,.17)
 for k in range(sides):
  a=k/sides*math.tau;root=0
  for ra,amp,width in [(0.10,.075,.20),(-.80,.09,.21),(-1.86,.095,.20),(-2.88,.075,.22),(2.22,.09,.22)]:
   root+=amp*math.exp(-(angle_delta(a,ra)/width)**2)*math.exp(-max(z,0)*15)
  # Unequal channels and swellings remove the regular fluting of the previous study.
  furrow=0
  for centre,width,depth in [(-1.7+.33*math.sin(z*4),.17,.20),(-2.55+.27*math.sin(z*3+1),.12,.16),(-.73+.20*math.sin(z*5+.4),.13,.14),(.80+.23*math.sin(z*4.1),.15,.13)]:
   furrow+=depth*math.exp(-(angle_delta(a,centre)/width)**2)
  bulge=.055*math.sin(a*3+z*4)+.04*math.sin(a*5-z*2.3)
  bulge+=.10*math.exp(-((z-.57)/.18)**2)*math.exp(-(angle_delta(a,-2.0)/.45)**2)
  factor=1+bulge-furrow*(.5+.5*smooth(.05,.30,z))
  x=cx+math.cos(a)*(rx*factor+root);y=cy+math.sin(a)*(ry*factor+root*.72)
  zz=z+.007*math.sin(a*4+z*5)*smooth(.05,.2,z)*(1-smooth(1.3,1.45,z))
  verts.append((x,y,zz))
  if j<rings:faces.append((j*sides+k,j*sides+(k+1)%sides,(j+1)*sides+(k+1)%sides,(j+1)*sides+k))
faces.extend([tuple(range(sides-1,-1,-1)),tuple(rings*sides+k for k in range(sides))])
core=make('Continuous aged trunk and primary branches',verts,faces,WOOD);parts=[core]

# Primary supports are unequal, change depth, and emerge from the same connected wood mass.
branches=[
 ('left lower',[(-.21,.0,.69),(-.43,-.035,.71),(-.72,-.01,.76),(-1.04,-.045,.84),(-1.34,.02,.92)],[.085,.060,.044,.023,.005],.19),
 ('left middle',[(-.08,.04,.95),(-.36,.09,1.065),(-.65,.14,1.16),(-.99,.12,1.22)],[.070,.046,.026,.005],.31),
 ('crown right',[(.23,.065,1.16),(.53,.085,1.265),(.80,.015,1.29),(1.055,.07,1.31)],[.075,.050,.030,.005],.42),
 ('upper left',[(.29,.04,1.29),(.065,-.035,1.38),(-.22,-.02,1.42),(-.50,.06,1.47)],[.076,.052,.033,.008],.55),
 ('apex',[(.285,.07,1.26),(.41,.03,1.43),(.44,.09,1.56),(.62,.13,1.60)],[.074,.043,.024,.006],.64),
 ('subordinate low right',[(.15,-.035,.25),(.40,-.04,.40),(.66,-.015,.365),(.91,.07,.435)],[.085,.054,.03,.006],.74),
 ('rear left',[(-.12,.11,.88),(-.48,.33,1.02),(-.76,.40,1.09),(-1.03,.45,1.11)],[.070,.045,.028,.006],.83),
 ('rear apex',[(.24,.10,1.19),(.27,.31,1.39),(.20,.50,1.56),(.36,.60,1.61)],[.066,.044,.028,.006],.92),
 ('front crown',[(.23,-.055,1.16),(.46,-.24,1.27),(.64,-.35,1.365),(.82,-.38,1.39)],[.071,.043,.026,.007],.25),
 ('rear right',[(.29,.16,1.20),(.64,.30,1.23),(.93,.42,1.29),(1.1,.45,1.32)],[.066,.045,.025,.006],.48),
]
def branch_mesh(name,coords,radii,steps=60,sides=24,kind=1,seed=.5):
 ps=[Vector(p) for p in coords];v=[];f=[];arc=0;old=None
 for j in range(steps+1):
  t=j/steps;p=cat(ps,t);d=(cat(ps,min(1,t+.002))-cat(ps,max(0,t-.002))).normalized();n=d.cross(Vector((0,0,1))).normalized()
  if n.length<.2:n=d.cross(Vector((0,1,0))).normalized()
  q=d.cross(n).normalized();rt=t*(len(radii)-1);k=min(len(radii)-2,int(rt));rad=radii[k]*(1-(rt-k))+radii[k+1]*(rt-k)
  if old is not None:arc+=(p-old).length
  old=p
  if kind>=0:add_guide(p,d,rad,arc+coords[0][2],kind,seed)
  for k in range(sides):
   a=k/sides*math.tau;r=rad*(1+.048*math.sin(a*3+t*5+seed*8)+.025*math.sin(a*7-t*4))
   v.append(p+n*math.cos(a)*r+q*math.sin(a)*r*.91)
   if j<steps:f.append((j*sides+k,j*sides+(k+1)%sides,(j+1)*sides+(k+1)%sides,(j+1)*sides+k))
 f.extend([tuple(range(sides-1,-1,-1)),tuple(steps*sides+k for k in range(sides))])
 return make(name,v,f,WOOD)
for name,coords,radii,seed in branches:parts.append(branch_mesh(name,coords,radii,seed=seed))
for index,(coords,radii) in enumerate([
 ([(-.03,-.10,.14),(-.23,-.25,.055),(-.43,-.31,-.014)],[.105,.063,.009]),
 ([(.12,-.05,.135),(.30,-.22,.045),(.51,-.20,-.012)],[.10,.060,.007]),
 ([(-.12,.07,.13),(-.33,.18,.03),(-.50,.21,-.014)],[.085,.051,.006]),
 ([(.08,.12,.14),(.25,.30,.04),(.44,.34,-.015)],[.083,.051,.006])]):
 parts.append(branch_mesh('Grown root buttress',coords,radii,steps=36,kind=0,seed=.11+index*.17))
# A broken stub retains a short irregular torn point; it does not form an applied ribbon.
parts.append(branch_mesh('Old broken branch',[(-.23,-.075,.70),(-.52,-.13,.74),(-.65,-.10,.82)],[.09,.047,.0015],steps=32,sides=16,kind=0,seed=.67))

bpy.ops.object.select_all(action='DESELECT')
for ob in parts:ob.select_set(True)
bpy.context.view_layer.objects.active=core;bpy.ops.object.join();core.data.remesh_voxel_size=.0045;progress('Remeshing continuous volume');bpy.ops.object.voxel_remesh();progress(f'Remeshed: {len(core.data.vertices)} vertices')
modifier=core.modifiers.new('Continuous grown junctions','SMOOTH');modifier.factor=.35;modifier.iterations=2;bpy.ops.object.modifier_apply(modifier=modifier.name)

def cavity(name,location,scale):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=40,ring_count=24,location=location);cut=bpy.context.object;cut.name=name
 for vertex in cut.data.vertices:
  v=vertex.co;v*=1+.085*noise.noise_vector(v*3.7).x
 cut.scale=scale;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
 bpy.context.view_layer.objects.active=core;mod=core.modifiers.new(name,'BOOLEAN');mod.operation='DIFFERENCE';mod.solver='EXACT';mod.object=cut;bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(cut,do_unlink=True)
cavity('Open weathered hollow',(-.14,-.13,.48),(.071,.085,.14))
cavity('Upper shallow scar',(.20,-.11,1.055),(.048,.065,.09))
progress('Cavities complete')

# Store UV flow and material masks on the SAME welded surface.
tree=kdtree.KDTree(len(guides))
for idx,g in enumerate(guides):tree.insert(g[0],idx)
tree.balance();uvs=[];masks=[]
normals=[vertex.normal.copy() for vertex in core.data.vertices]
for vertex,normal in zip(core.data.vertices,normals):
 p=vertex.co;_,idx,_=tree.find(p);centre,tangent,n,q,radius,arc,kind,seed=guides[idx];d=p-centre;theta=math.atan2(d.dot(q),d.dot(n));u=theta/math.tau+.5
 z=p.z;front_theta=math.atan2(p.y-section(max(-.022,min(1.45,z)))[1],p.x-section(max(-.022,min(1.45,z)))[0])
 live_angle=-.31+.46*math.sin(z*3.8+.3);width=.31+.10*math.sin(z*5)
 living=1-smooth(width,width+.15,abs(angle_delta(front_theta,live_angle)))
 if kind==1:
  cx,cy,rx,ry=section(max(-.022,min(1.45,z)));outside=math.hypot((p.x-cx)/max(rx,.04),(p.y-cy)/max(ry,.04));blend=smooth(1.0,2.2,outside)
  living=living*(1-blend)+(.76+.20*math.sin(theta+seed*7))*blend
 weather=.5+.25*noise.noise_vector(Vector((p.x*13,p.y*13,p.z*4))).x
 uvs.append((u,arc));masks.append((living,seed,weather,1))
 # Grain is subordinate to silhouette and large worn folds.
 vnoise=noise.noise_vector(Vector((p.x*27,p.y*27,p.z*4))).x
 vertex.co+=normal*(vnoise*.0012)
for poly in core.data.polygons:poly.use_smooth=True
uv=core.data.uv_layers.new(name='Wood flow')
for poly in core.data.polygons:
 values=[uvs[core.data.loops[k].vertex_index] for k in poly.loop_indices];wrap=max(x[0] for x in values)-min(x[0] for x in values)>.5
 for li,(u,v) in zip(poly.loop_indices,values):uv.data[li].uv=(u+1 if wrap and u<.5 else u,v)
at=core.data.color_attributes.new(name='Wood masks',type='FLOAT_COLOR',domain='POINT');at.data.foreach_set('color',[v for c in masks for v in c]);core.location.z=SOIL
progress('Surface flow and masks complete')

# A genuinely shallow ceramic vessel with its lip, inner wall, bottom and feet.
def rounded_ring(rx,ry,corner,z,count=80):
 result=[];quarter=count//4
 for j in range(4):
  cx=(rx-corner)*(1 if j in [0,3] else -1);cy=(ry-corner)*(1 if j in [0,1] else -1)
  for k in range(quarter):
   a=(j*math.pi/2+k/(quarter-1)*math.pi/2)
   result.append((cx+corner*math.cos(a),cy+corner*math.sin(a),z))
 return result
levels=[(.681,.353,.068,.184),(.696,.368,.070,.204),(.785,.417,.080,.386),(.802,.430,.086,.403),(.799,.427,.082,.414),(.779,.405,.074,.413),(.763,.390,.073,.385),(.678,.340,.067,.211)]
v=[];f=[]
for j,(rx,ry,c,z) in enumerate(levels):
 for x,y,z in rounded_ring(rx,ry,c,z):
  v.append((x,y,z+.0007*math.sin(x*20+y*17)))
 for k in range(80):
  if j<len(levels)-1:f.append((j*80+k,j*80+(k+1)%80,(j+1)*80+(k+1)%80,(j+1)*80+k))
f.append(tuple(range(80-1,-1,-1)));pot=make('Shallow unglazed pot',v,f,POT)
bev=pot.modifiers.new('Worn ceramic edges','BEVEL');bev.width=.002;bev.segments=2;bpy.context.view_layer.objects.active=pot;bpy.ops.object.modifier_apply(modifier=bev.name)
def cube(name,loc,scale,mat,bevel=0):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=name;o.dimensions=scale;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(mat)
 if bevel:
  be=o.modifiers.new('Worn edge','BEVEL');be.width=bevel;be.segments=3;bpy.ops.object.modifier_apply(modifier=be.name)
 for p in o.data.polygons:p.use_smooth=True
 return o
for x in [-.53,.53]:
 for y in [-.26,.26]:cube('Low ceramic foot',(x,y,.169),(.17,.13,.032),POT,.008)
stone=cube('Low natural bedding stone',(-.015,.015,.064),(2.06,1.26,.194),STONE,.048)
bpy.context.view_layer.objects.active=stone;mod=stone.modifiers.new('Stone surface','SUBSURF');mod.subdivision_type='SIMPLE';mod.levels=3;bpy.ops.object.modifier_apply(modifier=mod.name)
stone_normals=[vv.normal.copy() for vv in stone.data.vertices]
for vv,normal in zip(stone.data.vertices,stone_normals):
 p=vv.co;edge=max(abs(p.x)/1.03,abs(p.y)/.63);f=noise.noise_vector(Vector((p.x*4.4,p.y*4.4,p.z*13))).x
 vv.co+=normal*(.015*f*max(.25,edge));vv.co.z+=.004*math.sin(p.x*13+p.y*7)*max(0,edge-.60)
stone.data.update()

sv=[];sf=[];rings=18;sides=80
for j in range(rings+1):
 factor=j/rings
 for x,y,z in rounded_ring(.755*factor,.381*factor,.074*factor,SOIL):
  sv.append((x,y,z+.018*math.exp(-(x*x+y*y)*9)+.003*noise.noise_vector(Vector((x*25,y*25,1))).x))
 for k in range(sides):
  if j<rings:sf.append((j*sides+k,(j+1)*sides+k,(j+1)*sides+(k+1)%sides,j*sides+(k+1)%sides))
make('Continuous planted soil',sv,sf,SOILMAT)

# Foliage is generated later from terminal branch fans, never from filled ellipsoids.
if opt.foliage:
 exec((Path(__file__).parent/'foliage.py').read_text(),globals())
 shutil.copy2(Path(__file__).parent/'foliage.py',OUT/f'hero-{opt.version}.foliage.py')

for obj in bpy.context.scene.objects:
 obj.select_set(obj.type=='MESH')
 if obj.type=='MESH' and obj.active_material in [STONE,POT,SOILMAT]:
  if not obj.data.uv_layers:
   layer=obj.data.uv_layers.new(name='Surface UV')
   for poly in obj.data.polygons:
    for loop in poly.loop_indices:
     p=obj.data.vertices[obj.data.loops[loop].vertex_index].co;layer.data[loop].uv=(p.x,p.y+p.z)
bpy.context.scene.render.engine='CYCLES';bpy.context.scene.cycles.samples=24
blend=OUT/f'hero-{opt.version}.blend';glb=OUT/f'hero-{opt.version}.glb'
bpy.ops.wm.save_as_mainfile(filepath=str(blend))
progress('Saved Blender file; exporting GLB')
decimate=core.modifiers.new('Runtime surface reduction','DECIMATE');decimate.ratio=.45
bpy.ops.export_scene.gltf(filepath=str(glb),export_format='GLB',use_selection=True,export_yup=True,export_normals=True,export_materials='EXPORT',export_apply=True,export_vertex_color='ACTIVE',export_all_vertex_colors=True,export_draco_mesh_compression_enable=True,export_draco_mesh_compression_level=6,export_draco_position_quantization=16,export_draco_normal_quantization=10,export_draco_texcoord_quantization=12)
shutil.copy2(__file__,OUT/f'hero-{opt.version}.generator.py')
meta={'version':opt.version,'source':'Original authored cross-section volume, fused primary branches, no applied living-cord mesh','axes':'Blender Z-up, front -Y, metres','soil_height':SOIL,'front_reference':'hybrid-1132/images/desktop-candidate01.png','hidden_geometry':'Back and occluded surfaces are inferred','main_sections':sections,'branches':branches,'vertices':sum(len(o.data.vertices) for o in bpy.context.scene.objects if o.type=='MESH'),'faces':sum(len(o.data.polygons) for o in bpy.context.scene.objects if o.type=='MESH'),'objects':[o.name for o in bpy.context.scene.objects],'foliage':opt.foliage,'glb_bytes':glb.stat().st_size}
(OUT/f'hero-{opt.version}.json').write_text(json.dumps(meta,indent=2));print(json.dumps({'saved':str(blend),'glb':str(glb),'vertices':meta['vertices'],'faces':meta['faces'],'bytes':meta['glb_bytes']}))
