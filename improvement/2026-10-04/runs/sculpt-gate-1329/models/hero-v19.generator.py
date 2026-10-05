"""A continuous, broad old-tree volume. Run inside Blender; original geometry only."""
import bpy, bmesh, math, random, json, argparse, sys, shutil, time
from pathlib import Path
from mathutils import Vector, Quaternion, noise, kdtree

args=argparse.ArgumentParser();args.add_argument('--out',required=True);args.add_argument('--version',default='v01');args.add_argument('--foliage',action='store_true')
opt=args.parse_args(sys.argv[sys.argv.index('--')+1:]);OUT=Path(opt.out);OUT.mkdir(parents=True,exist_ok=True)
started=time.monotonic()
def progress(text):print(f'{time.monotonic()-started:.1f}s {text}',flush=True)
random.seed(4101329)
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
SOIL=.393

def material(name,base,rough=.85):
 m=bpy.data.materials.new(name);m.use_nodes=True
 p=next((node for node in m.node_tree.nodes if node.type=='BSDF_PRINCIPLED'),None)
 if p is None:
  p=m.node_tree.nodes.new('ShaderNodeBsdfPrincipled');output=m.node_tree.nodes.new('ShaderNodeOutputMaterial');m.node_tree.links.new(p.outputs['BSDF'],output.inputs['Surface'])
 p.inputs['Base Color'].default_value=(*base,1);p.inputs['Roughness'].default_value=rough
 return m
WOOD=material('Sculpted wood shader',(0.27,.21,.15));LEAF=material('Scale foliage shader',(.10,.18,.055));POT=material('Unglazed ceramic shader',(.22,.12,.075));STONE=material('Natural bedding stone',(.22,.23,.20));SOILMAT=material('Moss and mineral soil',(.07,.085,.025))

def make(name,verts,faces,mat,smooth=True):
 me=bpy.data.meshes.new(name);me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(o);me.materials.append(mat)
 for p in me.polygons:p.use_smooth=smooth
 return o
def assign_flow(obj,values):
 layer=obj.data.uv_layers.new(name='Wood flow');layer.active_render=True
 for poly in obj.data.polygons:
  coords=[values[obj.data.loops[k].vertex_index] for k in poly.loop_indices];wrap=max(u for u,v in coords)-min(u for u,v in coords)>.5
  for loop,(u,v) in zip(poly.loop_indices,coords):layer.data[loop].uv=(u+1 if wrap and u<.5 else u,v)
def smooth(a,b,x):
 t=max(0,min(1,(x-a)/(b-a)));return t*t*(3-2*t)
def angle_delta(a,b):return (a-b+math.pi)%math.tau-math.pi
def cat(points,t):
 n=len(points)-1;i=min(n-1,int(t*n));u=t*n-i;a=points[max(0,i-1)];b=points[i];c=points[i+1];d=points[min(n,i+2)]
 return .5*(2*b+(-a+c)*u+(2*a-5*b+4*c-d)*u*u+(-a+3*b-3*c+d)*u*u*u)

# Z sections are sculpted cross-sections of a single body, not a swept living cord.
# Each row: height, centre X/Y, side-to-side and front-to-back half widths.
sections=[
 (-.070,.015,.01,.21,.17),(-.015,.015,.01,.235,.195),(.025,.020,.025,.26,.22),(.10,.035,.04,.28,.225),
 (.22,-.010,.065,.265,.23),(.34,-.065,.083,.25,.218),(.48,-.110,.095,.231,.207),
 (.61,-.104,.093,.211,.197),(.72,-.065,.084,.198,.180),(.83,-.004,.073,.180,.163),
 (.96,.082,.063,.161,.148),(1.08,.167,.056,.142,.132),(1.20,.251,.050,.115,.104),
 (1.32,.32,.055,.079,.074),(1.405,.34,.035,.045,.045),(1.45,.355,.04,.004,.005),
]
def section(z):
 k=0
 while k<len(sections)-2 and z>sections[k+1][0]:k+=1
 a=sections[k];b=sections[k+1];t=max(0,min(1,(z-a[0])/(b[0]-a[0])));h=b[0]-a[0]
 prev=sections[max(0,k-1)];nxt=sections[min(len(sections)-1,k+2)]
 return tuple((2*t**3-3*t*t+1)*a[j]+(t**3-2*t*t+t)*h*(b[j]-prev[j])/(b[0]-prev[0])+(-2*t**3+3*t*t)*b[j]+(t**3-t*t)*h*(nxt[j]-a[j])/(nxt[0]-a[0]) for j in range(1,5))
guides=[]
def add_guide(p,tangent,radius,arc,kind,seed):
 tangent=Vector(tangent).normalized();n=tangent.cross(Vector((0,1,0))).normalized()
 if n.length<.2:n=tangent.cross(Vector((1,0,0))).normalized()
 b=tangent.cross(n).normalized();guides.append((Vector(p),tangent,n,b,radius,arc,kind,seed))

channel_rng=random.Random(701)
channels=[(channel_rng.uniform(-math.pi,math.pi),channel_rng.uniform(.025,.09),channel_rng.uniform(.014,.075),channel_rng.uniform(.8,3.9),channel_rng.uniform(0,math.tau)) for _ in range(24)]
verts=[];faces=[];original_uv=[];main_arc=0;main_old=None;rings=265;sides=104
for j in range(rings+1):
 z=sections[0][0]+(sections[-1][0]-sections[0][0])*j/rings;cx,cy,rx,ry=section(z)
 centre=Vector((cx,cy,z))
 if main_old is not None:main_arc+=(centre-main_old).length
 main_old=centre
 dz=.002;pa=section(max(sections[0][0],z-dz));pb=section(min(sections[-1][0],z+dz));tangent=Vector((pb[0]-pa[0],pb[1]-pa[1],2*dz)).normalized();add_guide((cx,cy,z),tangent,(rx+ry)/2,z,0,.17)
 # Sections stand perpendicular to the tree's local growth direction. Horizontal
 # sections made the steep part of the first studies read as a thin extruded board.
 width_axis=Vector((0,1,0)).cross(tangent).normalized();depth_axis=tangent.cross(width_axis).normalized()
 for k in range(sides):
  a=k/sides*math.tau;root=0
  for ra,amp,width in [(0.10,.075,.20),(-.80,.09,.21),(-1.86,.095,.20),(-2.88,.075,.22),(2.22,.09,.22)]:
   root+=amp*math.exp(-(angle_delta(a,ra)/width)**2)*math.exp(-max(z,0)*15)
  # Unequal channels and swellings remove the regular fluting of the previous study.
  furrow=0
  scar_depth=.14+.12*math.exp(-((z-.72)/.42)**2)
  twist=.72*math.sin(z*2.8)-.70*z
  for centre,width,depth in [(-1.50+twist,.28+.035*math.sin(z*5),scar_depth),(-2.55+twist,.18,.14),(-.73+twist,.16,.12),(.80+twist,.20,.09)]:
   furrow+=depth*math.exp(-(angle_delta(a,centre)/width)**2)
  bulge=.095*math.sin(a*3+z*4)+.04*math.sin(a*5-z*2.3)
  bulge+=.10*math.exp(-((z-.57)/.18)**2)*math.exp(-(angle_delta(a,-2.0)/.45)**2)
  cambium_angle=-1.07+.62*math.sin(z*4.1+.2)
  bulge+=.038*math.exp(-(angle_delta(a,cambium_angle)/.34)**2)
  worn=.028*noise.noise_vector(Vector((math.cos(a)*7,math.sin(a)*7,z*2.2))).x
  for centre,width,depth,frequency,phase in channels:
   flow=centre+twist+.13*math.sin(z*frequency+phase)+.025*math.sin(z*9+phase)
   worn-=depth*math.exp(-(angle_delta(a,flow)/width)**2)*(.35+.65*(.5+.5*math.sin(z*frequency+phase)))
  factor=1+bulge-furrow*(.5+.5*smooth(.05,.30,z))+worn
  pos=Vector((cx,cy,z))+width_axis*math.cos(a)*(rx*factor+root)+depth_axis*math.sin(a)*(ry*factor+root*.72)
  pos+=tangent*(.007*math.sin(a*4+z*5)*smooth(.05,.2,z)*(1-smooth(1.3,1.45,z)))
  verts.append(tuple(pos))
  original_uv.append((k/sides,main_arc))
  if j<rings:faces.append((j*sides+k,j*sides+(k+1)%sides,(j+1)*sides+(k+1)%sides,(j+1)*sides+k))
faces.extend([tuple(range(sides-1,-1,-1)),tuple(rings*sides+k for k in range(sides))])
core=make('Continuous aged trunk and primary branches',verts,faces,WOOD);parts=[core]
assign_flow(core,original_uv)

# Primary supports are unequal, change depth, and emerge from the same connected wood mass.
branches=[
 ('left lower',[(-.21,.0,.69),(-.41,-.035,.675),(-.57,-.075,.70),(-.72,-.01,.655),(-.91,.025,.73),(-1.08,-.045,.725),(-1.31,.02,.84)],[.085,.064,.054,.040,.032,.020,.004],.19),
 ('left middle',[(-.08,.04,.95),(-.34,.09,1.075),(-.47,.035,1.035),(-.66,.12,1.13),(-.83,.155,1.12),(-1.00,.12,1.21)],[.073,.055,.041,.031,.018,.004],.31),
 ('crown right',[(.23,.065,1.16),(.47,.085,1.265),(.59,.015,1.19),(.77,-.035,1.265),(.90,.065,1.24),(1.055,.07,1.30)],[.075,.055,.043,.031,.018,.004],.42),
 ('upper left',[(.29,.04,1.29),(.11,-.035,1.38),(-.04,-.06,1.32),(-.22,-.02,1.405),(-.38,.04,1.395),(-.50,.06,1.45)],[.068,.047,.035,.026,.015,.003],.55),
 ('apex',[(.285,.07,1.26),(.405,.03,1.40),(.35,.07,1.50),(.48,.12,1.55),(.50,.14,1.62),(.63,.13,1.64)],[.067,.046,.034,.023,.014,.003],.64),
 ('subordinate low right',[(.15,-.035,.25),(.36,-.04,.39),(.48,.02,.34),(.65,.04,.385),(.76,-.005,.36),(.91,.07,.425)],[.069,.049,.037,.026,.016,.003],.74),
 ('rear left',[(-.12,.11,.88),(-.48,.33,1.02),(-.76,.40,1.09),(-1.03,.45,1.11)],[.070,.045,.028,.006],.83),
 ('rear apex',[(.24,.10,1.19),(.27,.31,1.39),(.20,.50,1.56),(.36,.60,1.61)],[.066,.044,.028,.006],.92),
 ('front crown',[(.28,.04,1.21),(.41,-.10,1.15),(.52,-.18,1.24),(.67,-.25,1.24),(.80,-.29,1.29)],[.057,.043,.030,.018,.004],.25),
 ('rear right',[(.29,.16,1.20),(.64,.30,1.23),(.93,.42,1.29),(1.1,.45,1.32)],[.066,.045,.025,.006],.48),
 ('upper bridge',[(.24,.08,1.26),(.10,-.015,1.43),(-.09,-.02,1.53),(-.13,.06,1.61)],[.052,.033,.018,.003],.38),
]
# Major branches grow from the interior of the authored trunk. When the trunk
# proportions change, their roots follow it instead of remaining on its skin.
for name,coords,radii,seed in branches:
 z=coords[0][2];cx,cy,rx,ry=section(z);coords[0]=(cx,cy,z);radii[0]=min((rx+ry)*.40,radii[0]*1.35)
def branch_mesh(name,coords,radii,steps=60,sides=24,kind=1,seed=.5):
 ps=[Vector(p) for p in coords];v=[];f=[];flow_uv=[];arc=0;old=None
 for j in range(steps+1):
  t=j/steps;p=cat(ps,t);d=(cat(ps,min(1,t+.002))-cat(ps,max(0,t-.002))).normalized();n=d.cross(Vector((0,0,1))).normalized()
  if n.length<.2:n=d.cross(Vector((0,1,0))).normalized()
  q=d.cross(n).normalized();rt=t*(len(radii)-1);k=min(len(radii)-2,int(rt));rad=radii[k]*(1-(rt-k))+radii[k+1]*(rt-k)
  if old is not None:arc+=(p-old).length
  old=p
  if kind>=0:add_guide(p,d,rad,arc+coords[0][2],kind,seed)
  for k in range(sides):
   a=k/sides*math.tau;r=rad*(1+.075*math.sin(a*3+t*5+seed*8)+.036*math.sin(a*7-t*4)+.021*math.sin(a*15+t*3))
   v.append(p+n*math.cos(a)*r+q*math.sin(a)*r*.91)
   flow_uv.append((k/sides,arc+coords[0][2]))
   if j<steps:f.append((j*sides+k,j*sides+(k+1)%sides,(j+1)*sides+(k+1)%sides,(j+1)*sides+k))
 f.extend([tuple(range(sides-1,-1,-1)),tuple(steps*sides+k for k in range(sides))])
 obj=make(name,v,f,WOOD);assign_flow(obj,flow_uv);return obj
for name,coords,radii,seed in branches:parts.append(branch_mesh(name,coords,radii,seed=seed))
for index,(coords,radii) in enumerate([
 ([(-.03,-.10,.105),(-.17,-.19,.043),(-.34,-.30,-.020)],[.080,.043,.006]),
 ([(.12,-.05,.115),(.29,-.16,.038),(.49,-.22,-.019)],[.088,.050,.006]),
 ([(-.12,.07,.13),(-.33,.18,.03),(-.50,.21,-.014)],[.085,.051,.006]),
 ([(.08,.12,.14),(.25,.30,.04),(.44,.34,-.015)],[.083,.051,.006])]):
 parts.append(branch_mesh('Grown root buttress',coords,radii,steps=36,kind=0,seed=.11+index*.17))
# A broken stub retains a short irregular torn point; it does not form an applied ribbon.
parts.append(branch_mesh('Old broken branch',[(-.23,-.075,.70),(-.43,-.13,.68),(-.58,-.13,.76)],[.084,.041,.004],steps=32,sides=20,kind=0,seed=.67))
parts.append(branch_mesh('Torn spur',[(-.43,-.13,.68),(-.51,-.17,.68),(-.57,-.16,.71)],[.028,.014,.001],steps=20,sides=16,kind=0,seed=.68))

bpy.ops.object.select_all(action='DESELECT')
for ob in parts:ob.select_set(True)
bpy.context.view_layer.objects.active=core;bpy.ops.object.join();core.data.remesh_voxel_size=.0045;core.data.use_remesh_preserve_attributes=True;progress('Remeshing continuous volume with authored surface coordinates');bpy.ops.object.voxel_remesh();progress(f'Remeshed: {len(core.data.vertices)} vertices; UV layers {[layer.name for layer in core.data.uv_layers]}')
modifier=core.modifiers.new('Continuous grown junctions','SMOOTH');modifier.factor=.32;modifier.iterations=2;bpy.ops.object.modifier_apply(modifier=modifier.name)
bm=bmesh.new();bm.from_mesh(core.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces))
if bm.calc_volume(signed=True)<0:bmesh.ops.reverse_faces(bm,faces=list(bm.faces))
bm.to_mesh(core.data);bm.free();core.data.update()

def cavity(name,location,scale):
 backup=core.data.copy();before=len(core.data.vertices)
 bpy.ops.mesh.primitive_uv_sphere_add(segments=40,ring_count=24,location=location);cut=bpy.context.object;cut.name=name
 for vertex in cut.data.vertices:
  v=vertex.co;v*=1+.19*noise.noise_vector(v*4.7).x;v.x+=.12*v.z*v.z
 cut.scale=scale;cut.rotation_euler=(0,.27,.13);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
 bpy.context.view_layer.objects.active=core;mod=core.modifiers.new(name,'BOOLEAN');mod.operation='DIFFERENCE';mod.solver='EXACT';mod.object=cut;bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(cut,do_unlink=True)
 if len(core.data.vertices)<before*.70:
  broken=core.data;core.data=backup;bpy.data.meshes.remove(broken);progress(f'{name}: rejected destructive boolean, retained continuous volume')
 else:bpy.data.meshes.remove(backup)
 progress(f'{name}: {len(core.data.vertices)} vertices')
cavity('Tapered weathered grain split',(-.035,-.158,.30),(.035,.095,.192))
progress('Cavities complete')
assert len(core.data.vertices)>100000,'Continuous trunk volume must survive cavity operations'
bm=bmesh.new();bm.from_mesh(core.data);bm.verts.ensure_lookup_table();seen=set();components=[]
for vertex in bm.verts:
 if vertex.index in seen:continue
 stack=[vertex];seen.add(vertex.index);component=[]
 while stack:
  current=stack.pop();component.append(current)
  for edge in current.link_edges:
   other=edge.other_vert(current)
   if other.index not in seen:seen.add(other.index);stack.append(other)
 components.append(component)
components.sort(key=len,reverse=True)
assert all(len(c)<64 for c in components[1:]),'A primary branch became disconnected from the trunk'
chips=[v for c in components[1:] for v in c]
if chips:bmesh.ops.delete(bm,geom=chips,context='VERTS')
bm.to_mesh(core.data);bm.free();core.data.update();progress(f'Continuous wood verified; removed {len(chips)} tiny remeshing fragment vertices')
assert 'Wood flow' in core.data.uv_layers,'Authored surface flow must survive volume fusion'
flow_layer=core.data.uv_layers['Wood flow'];surface_flow=[None]*len(core.data.vertices)
for loop in core.data.loops:surface_flow[loop.vertex_index]=tuple(flow_layer.data[loop.index].uv)

# Store UV flow and material masks on the SAME welded surface.
tree=kdtree.KDTree(len(guides))
for idx,g in enumerate(guides):tree.insert(g[0],idx)
tree.balance();uvs=[];masks=[]
normals=[vertex.normal.copy() for vertex in core.data.vertices]
for vertex,normal in zip(core.data.vertices,normals):
 p=vertex.co;nearest=tree.find_n(p,8);_,idx,dmin=nearest[0];centre,tangent,n,q,radius,arc,kind,seed=guides[idx];d=p-centre;theta=math.atan2(d.dot(q),d.dot(n));u0=theta/math.tau+.5
 weighted=[]
 for _,gi,distance in nearest:
  cc,tt,nn,qq,rr,aa,kk,ss=guides[gi];dd=p-cc;uu=math.atan2(dd.dot(qq),dd.dot(nn))/math.tau+.5;uu=u0+(uu-u0+.5)%1-.5;weight=math.exp(-((distance-dmin)/.032)**2)
  weighted.append((weight,uu,aa,ss,kk))
 total=sum(w[0] for w in weighted);u=sum(w[0]*w[1] for w in weighted)/total;arc=sum(w[0]*w[2] for w in weighted)/total;seed=sum(w[0]*w[3] for w in weighted)/total;branch_blend=sum(w[0]*(w[4]==1) for w in weighted)/total
 u,arc=surface_flow[vertex.index]
 z=p.z;front_theta=math.atan2(p.y-section(max(-.022,min(1.45,z)))[1],p.x-section(max(-.022,min(1.45,z)))[0])
 live_angle=-1.07+.62*math.sin(z*4.1+.2);width=.30+.105*math.sin(z*5+.4)
 living=1-smooth(width,width+.15,abs(angle_delta(front_theta,live_angle)))
 if branch_blend>0:
  cx,cy,rx,ry=section(max(-.022,min(1.45,z)));outside=math.hypot((p.x-cx)/max(rx,.04),(p.y-cy)/max(ry,.04));blend=smooth(1.0,2.2,outside)
  blend*=branch_blend;living=living*(1-blend)+(.76+.20*math.sin(theta+seed*7))*blend
 weather=.5+.25*noise.noise_vector(Vector((p.x*13,p.y*13,p.z*4))).x
 uvs.append((u,arc));masks.append((living,seed,weather,1))
 # Grain is subordinate to silhouette and large worn folds.
 vnoise=noise.noise_vector(Vector((p.x*27,p.y*27,p.z*4))).x
 fibre_noise=noise.noise_vector(Vector((math.cos(u*math.tau)*29,math.sin(u*math.tau)*29,arc*3.8))).x
 vertex.co+=normal*(vnoise*.0012+fibre_noise*.0025*(1-living*.55))
for poly in core.data.polygons:poly.use_smooth=True
# Keep the coordinates authored on the actual bark surface. The original
# cross-section and branch charts are transferred by the volume remesher.
for layer in list(core.data.uv_layers):
 if layer.name!='Wood flow':core.data.uv_layers.remove(layer)
core.data.uv_layers.active_index=0;core.data.uv_layers[0].active_render=True
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
f.append(tuple(range(80-1,-1,-1)));f.append(tuple((len(levels)-1)*80+k for k in range(80)));pot=make('Shallow unglazed pot',v,f,POT)
bev=pot.modifiers.new('Worn ceramic edges','BEVEL');bev.width=.002;bev.segments=2;bpy.context.view_layer.objects.active=pot;bpy.ops.object.modifier_apply(modifier=bev.name)
def cube(name,loc,scale,mat,bevel=0):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=name;o.dimensions=scale;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(mat)
 if bevel:
  be=o.modifiers.new('Worn edge','BEVEL');be.width=bevel;be.segments=3;bpy.ops.object.modifier_apply(modifier=be.name)
 for p in o.data.polygons:p.use_smooth=True
 return o
for x in [-.53,.53]:
 for y in [-.26,.26]:cube('Low ceramic foot',(x,y,.169),(.17,.13,.032),POT,.008)
exec((Path(__file__).parent/'support.py').read_text(),globals())
shutil.copy2(Path(__file__).parent/'support.py',OUT/f'hero-{opt.version}.support.py')

# Foliage is generated later from terminal branch fans, never from filled ellipsoids.
if opt.foliage:
 exec((Path(__file__).parent/'foliage.py').read_text(),globals())
 shutil.copy2(Path(__file__).parent/'foliage.py',OUT/f'hero-{opt.version}.foliage.py')

for obj in bpy.context.scene.objects:
 obj.select_set(obj.type=='MESH' or obj.name=='Branch led scale foliage')
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
bpy.ops.export_scene.gltf(filepath=str(glb),export_format='GLB',use_selection=True,export_yup=True,export_normals=True,export_materials='EXPORT',export_apply=True,export_vertex_color='ACTIVE',export_all_vertex_colors=True,export_gpu_instances=True,export_draco_mesh_compression_enable=True,export_draco_mesh_compression_level=6,export_draco_position_quantization=16,export_draco_normal_quantization=10,export_draco_texcoord_quantization=12)
shutil.copy2(__file__,OUT/f'hero-{opt.version}.generator.py')
meta={'version':opt.version,'source':'Original authored cross-section volume, fused primary branches, no applied living-cord mesh','axes':'Blender Z-up, front -Y, metres','soil_height':SOIL,'front_reference':'hybrid-1132/images/desktop-candidate01.png','hidden_geometry':'Back and occluded surfaces are inferred','main_sections':sections,'branches':branches,'vertices':sum(len(o.data.vertices) for o in bpy.context.scene.objects if o.type=='MESH'),'faces':sum(len(o.data.polygons) for o in bpy.context.scene.objects if o.type=='MESH'),'objects':[o.name for o in bpy.context.scene.objects],'foliage':opt.foliage,'glb_bytes':glb.stat().st_size}
meta.update(runtime_world_scale=.66,runtime_dimensions_note='Multiply authored lengths by 0.66 for the website; inspection reports use the original Blender coordinates')
(OUT/f'hero-{opt.version}.json').write_text(json.dumps(meta,indent=2));print(json.dumps({'saved':str(blend),'glb':str(glb),'vertices':meta['vertices'],'faces':meta['faces'],'bytes':meta['glb_bytes']}))
