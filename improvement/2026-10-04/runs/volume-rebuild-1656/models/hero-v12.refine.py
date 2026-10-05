"""Flow-aligned wood refinement on the approved coarse volume, not a new loft."""
import bpy,bmesh,math,sys,argparse,json,random,shutil,time
from pathlib import Path
from mathutils import Vector,kdtree,noise
p=argparse.ArgumentParser();p.add_argument('--base',required=True);p.add_argument('--out',required=True);p.add_argument('--version',required=True);p.add_argument('--foliage',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
base=Path(a.base);out=Path(a.out);out.mkdir(exist_ok=True,parents=True);prefix=out/('hero-'+a.version)
for suffix in ['.blend','.glb','.json']:
 if prefix.with_suffix(suffix).exists():raise FileExistsError('Choose a fresh version')
start=time.monotonic();meta=json.loads(base.with_suffix('.json').read_text());bpy.ops.wm.open_mainfile(filepath=str(base));SOIL=meta['soil_height']
core=bpy.data.objects['Continuous aged trunk and primary branches'];me=core.data
def progress(s):print(f'{time.monotonic()-start:.1f}s {s}',flush=True)
def smooth(a,b,x):
 t=max(0,min(1,(x-a)/(b-a)));return t*t*(3-2*t)
guides=[];trees=[];route_guides=[]
for ri,route in enumerate(meta['paths']):
 samples=route['sampled'];tree=kdtree.KDTree(len(samples));gs=[];arc=0
 for i,row in enumerate(samples):
  point=Vector(row[:3]);before=Vector(samples[max(i-1,0)][:3]);after=Vector(samples[min(i+1,len(samples)-1)][:3]);tangent=(after-before).normalized();width=Vector((tangent.z,0,-tangent.x))
  if width.length<.01:width=tangent.cross(Vector((0,0,1)))
  width.normalize();depth=tangent.cross(width).normalized()
  if i:arc+=(point-Vector(samples[i-1][:3])).length
  guide=(point,tangent,width,depth,row[3],arc,ri);gs.append(guide);guides.append(guide);tree.insert(point,i)
 tree.balance();trees.append(tree);route_guides.append(gs)
global_tree=kdtree.KDTree(len(guides))
for i,g in enumerate(guides):global_tree.insert(g[0],i)
global_tree.balance();progress(f'{len(guides)} continuous growth guides')
WOOD=core.active_material
def map_point(point):
 candidates={guides[i][-1] for _,i,_ in global_tree.find_n(point,8)}
 if point.z<1.30 and abs(point.x)<.72:candidates.update([0,1,2])
 if point.z<.25:candidates.update(i for i,r in enumerate(meta['paths']) if 'root' in r['name'] or 'buttress' in r['name'])
 records=[]
 for ri in candidates:
  _,gi,_=trees[ri].find(point);g=route_guides[ri][gi];centre,tangent,width,depth,radius,arc,_=g;delta=point-centre
  x=delta.dot(width);y=delta.dot(depth)/meta['paths'][ri]['depth'];z=delta.dot(tangent)
  score=math.sqrt(x*x+y*y+z*z)-radius
  records.append((score,ri,math.atan2(y,x),arc+z,radius,tangent))
 records.sort(key=lambda r:r[0]);score,ri,theta,arc,radius,_=records[0]
 name=meta['paths'][ri]['name'];living=0.0
 if ri==2:living=.97
 elif ri not in [0,1] and not any(x in name for x in ['root','buttress','torn','shoulder']):
  living=.50+.48*smooth(-.55,.30,math.sin(theta+.3))
 # The red-brown growth mass is a mask on this same skin, never an applied tube.
 for other_score,other_ri,*_ in records[1:]:
  if other_ri==2:living=max(living,.84*(1-smooth(.002,.042,other_score-score)))
 direction=Vector((0,0,0));total=0
 for record in records:
  weight=math.exp(-(record[0]-score)/.028);direction+=record[5]*weight;total+=weight
 direction.normalize()
 return theta,arc,radius,ri,living,direction

flow=[];colours=[];directions=[];rng=random.Random(170410)
normals=[v.normal.copy() for v in me.vertices]
for index,(vertex,normal) in enumerate(zip(me.vertices,normals)):
 point=vertex.co-Vector((0,0,SOIL));theta,arc,radius,ri,living,direction=map_point(point);u=theta/math.tau+.5;seed=(ri*.137+.21)%1
 # Several unequal widths of real relief follow local growth. The small relief
 # does not change the already reviewed root/trunk/branch mass arrangement.
 across=Vector((direction.z,0,-direction.x));across.normalize();depth=direction.cross(across).normalized()
 woodcoord=Vector((point.dot(across),point.dot(depth),point.dot(direction)))
 coarse=noise.noise_vector(Vector((woodcoord.x*85,woodcoord.y*85,woodcoord.z*5))).x
 fine=noise.noise_vector(Vector((woodcoord.x*210,woodcoord.y*210,woodcoord.z*14))).x
 worn=noise.noise_vector(point*19+Vector((.3,1.2,4.7))).x
 displacement=(coarse*.0045+fine*.0017+worn*.0018)*(1-living*.66)*min(1,radius/.055)
 vertex.co+=normal*displacement
 weather=.5+.28*noise.noise_vector(point*7.3+Vector((1,0,3))).x
 flow.append((u,arc));colours.append((living,seed,weather,1));directions.append((direction.x,direction.z,-direction.y,radius))
 if index%50000==0:progress(f'Wood relief and live-wood field {index}/{len(me.vertices)}')
for layer in list(me.uv_layers):me.uv_layers.remove(layer)
uv=me.uv_layers.new(name='Wood flow');uv.active_render=True
for face in me.polygons:
 coords=[flow[me.loops[k].vertex_index] for k in face.loop_indices];wrap=max(v[0] for v in coords)-min(v[0] for v in coords)>.5
 for loop,(u,v) in zip(face.loop_indices,coords):uv.data[loop].uv=(u+1 if wrap and u<.5 else u,v)
 face.use_smooth=True
uv1=me.uv_layers.new(name='Growth direction XY');uv2=me.uv_layers.new(name='Growth direction Z and radius')
for loop in me.loops:
 x,y,z,radius=directions[loop.vertex_index];uv1.data[loop.index].uv=(x,y);uv2.data[loop.index].uv=(z,radius)
for attribute in list(me.color_attributes):me.color_attributes.remove(attribute)
col=me.color_attributes.new(name='Wood masks',type='FLOAT_COLOR',domain='POINT');col.data.foreach_set('color',[x for c in colours for x in c]);me.update()
bpy.context.view_layer.objects.active=core
core['authoring_version']=a.version;core['construction']='implicit volume with local growth-flow weathering; no applied living tube'
if a.foliage:
 exec((Path(__file__).parent/'canopy.py').read_text(),globals())
 shutil.copy2(Path(__file__).parent/'canopy.py',out/(prefix.name+'.canopy.py'))
meta['base_volume']=base.name;meta['version']=a.version;meta['refinement']={'type':'continuous spatial direction field, real surface relief and living mask on same solid','source_vertices':len(me.vertices),'guide_count':len(guides),'foliage':a.foliage,'seconds_before_export':time.monotonic()-start}
for ob in bpy.context.scene.objects:ob.select_set(ob.type=='MESH' or ob.name=='Branch led scale foliage')
bpy.context.view_layer.objects.active=core;bpy.ops.wm.save_as_mainfile(filepath=str(prefix.with_suffix('.blend')),compress=True)
mod=core.modifiers.new('Runtime wood budget','DECIMATE');mod.ratio=min(1,170000/len(me.polygons))
bpy.ops.export_scene.gltf(filepath=str(prefix.with_suffix('.glb')),export_format='GLB',use_selection=True,export_yup=True,export_normals=True,export_materials='EXPORT',export_apply=True,export_vertex_color='ACTIVE',export_all_vertex_colors=True,export_extras=True,export_gpu_instances=True,export_draco_mesh_compression_enable=True,export_draco_mesh_compression_level=6,export_draco_position_quantization=16,export_draco_normal_quantization=10,export_draco_texcoord_quantization=12)
meta['glb_bytes']=prefix.with_suffix('.glb').stat().st_size;meta['refinement']['seconds_total']=time.monotonic()-start;prefix.with_suffix('.json').write_text(json.dumps(meta,indent=2));shutil.copy2(__file__,out/(prefix.name+'.refine.py'));shutil.copy2(prefix.with_suffix('.glb'),out.parent/'site/public/models/hero.glb');progress(f'Saved {prefix.name}; {meta["glb_bytes"]} bytes')
