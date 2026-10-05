"""Flow-aligned wood refinement on the approved coarse volume, not a new loft."""
import bpy,bmesh,math,sys,argparse,json,random,shutil,time
import numpy as np
from pathlib import Path
from mathutils import Vector,kdtree,noise
from mathutils.bvhtree import BVHTree
p=argparse.ArgumentParser();p.add_argument('--base',required=True);p.add_argument('--out',required=True);p.add_argument('--version',required=True);p.add_argument('--foliage',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
base=Path(a.base);out=Path(a.out);out.mkdir(exist_ok=True,parents=True);prefix=out/('hero-'+a.version)
for suffix in ['.blend','.glb','.json']:
 if prefix.with_suffix(suffix).exists():raise FileExistsError('Choose a fresh version')
start=time.monotonic();meta=json.loads(base.with_suffix('.json').read_text());bpy.ops.wm.open_mainfile(filepath=str(base));SOIL=meta['soil_height']
core=bpy.data.objects['Continuous aged trunk and primary branches'];me=core.data
def progress(s):print(f'{time.monotonic()-start:.1f}s {s}',flush=True)
def smooth(a,b,x):
 t=max(0,min(1,(x-a)/(b-a)));return t*t*(3-2*t)
# Taubin pairs reduce grid-scale ridges while preserving the reviewed broad
# volume. This is smoothing on the existing solid, not replacement geometry.
edges=np.array([e.vertices[:] for e in me.edges],dtype=np.int32);left=edges[:,0];right=edges[:,1];count=np.bincount(np.concatenate([left,right]),minlength=len(me.vertices));positions=np.array([v.co[:] for v in me.vertices],dtype=np.float64)
for pair in range(4):
 for weight in [.5,-.53]:
  neighbours=np.stack([np.bincount(left,weights=positions[right,k],minlength=len(positions))+np.bincount(right,weights=positions[left,k],minlength=len(positions)) for k in range(3)],axis=1)/count[:,None]
  positions+=weight*(neighbours-positions)
me.vertices.foreach_set('co',positions.astype(np.float32).ravel());me.update();progress('Grid-scale smoothing: four volume-preserving Taubin pairs')
def root_mound(x,y):return .034*math.exp(-((x+.07)**2/.15+(y+.015)**2/.065))
soil=bpy.data.objects['Continuous planted soil']
for vertex in soil.data.vertices:vertex.co.z+=root_mound(vertex.co.x,vertex.co.y)
soil.data.update();meta['root_mound']={'height_author_units':.034,'centre':[-.07,-.015],'method':'continuous asymmetrical soil mound shared by soil mesh, moss and grit placement'}
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
 direction=Vector((0,0,0));total=0;living=0
 for record in records:
  weight=math.exp(-(record[0]-score)/.028);direction+=record[5]*weight;total+=weight
  name=meta['paths'][record[1]]['name'];local_living=0
  if record[1]==2:local_living=.97
  elif name in ['right anchoring root','rear root ridge','rear left surface root','front right surface root']:local_living=.82
  elif record[1] not in [0,1] and not any(x in name for x in ['root','buttress','torn','shoulder']):local_living=.50+.48*smooth(-.55,.30,math.sin(record[2]+.3))
  living+=weight*local_living
 living/=total
 direction.normalize()
 confidence=smooth(.005,.045,records[1][0]-score) if len(records)>1 else 1
 return theta,arc,radius,ri,living,direction,confidence

flow=[];colours=[];directions=[];rng=random.Random(170410)
normals=[v.normal.copy() for v in me.vertices]
for index,(vertex,normal) in enumerate(zip(me.vertices,normals)):
 point=vertex.co-Vector((0,0,SOIL));theta,arc,radius,ri,living,direction,confidence=map_point(point);u=theta/math.tau+.5;seed=(ri*.137+.21)%1
 # Several unequal widths of real relief follow local growth. The small relief
 # does not change the already reviewed root/trunk/branch mass arrangement.
 across=Vector((direction.z,0,-direction.x));across.normalize();depth=direction.cross(across).normalized()
 woodcoord=Vector((point.dot(across),point.dot(depth),point.dot(direction)))
 coarse=noise.noise_vector(Vector((woodcoord.x*85,woodcoord.y*85,woodcoord.z*5))).x
 fine=noise.noise_vector(Vector((woodcoord.x*210,woodcoord.y*210,woodcoord.z*14))).x
 worn=noise.noise_vector(point*19+Vector((.3,1.2,4.7))).x
 # Relief wavelengths stay above the source sampling interval. The previous
 # 21/63-frequency displacement was under-sampled and created a woven surface.
 fibre=noise.noise_vector(Vector((math.cos(theta)*4.5,math.sin(theta)*4.5,arc*2.5))).x
 fine_fibre=noise.noise_vector(Vector((math.cos(theta)*8,math.sin(theta)*8,arc*5.2))).x
 junction=noise.noise_vector(point*13+Vector((.7,2.4,1.3))).x
 displacement=((fibre*.0115+fine_fibre*.0027)*confidence+junction*.0035*(1-confidence)+worn*.0015)*(1-living*.82)*min(1,radius/.055)
 vertex.co+=normal*displacement
 weather=.5+.28*noise.noise_vector(point*7.3+Vector((1,0,3))).x
 flow.append((u,arc));colours.append((living,seed,weather,1));directions.append((direction.x,direction.z,-direction.y,confidence))
 if index%50000==0:progress(f'Wood relief and live-wood field {index}/{len(me.vertices)}')
# Geometry-based short-range ambient visibility. This is a material mask, not
# baked directional lighting: changing the key still changes all direct light.
me.update();bvh=BVHTree.FromPolygons([v.co for v in me.vertices],[p.vertices[:] for p in me.polygons],all_triangles=True)
ambient=[];hemisphere=[]
for k in range(12):
 z=math.sqrt((k+.5)/12);r=math.sqrt(1-z*z);phi=k*2.39996322973;hemisphere.append((r*math.cos(phi),r*math.sin(phi),z))
for index,vertex in enumerate(me.vertices):
 n=vertex.normal.normalized();right=n.cross(Vector((.371,.83,.419))).normalized();up=n.cross(right);origin=vertex.co+n*.0018;occluded=0
 for x,y,z in hemisphere:
  _,_,_,distance=bvh.ray_cast(origin,right*x+up*y+n*z,.16)
  if distance is not None:occluded+=(1-distance/.16)**1.4
 value=max(.32,1-occluded/len(hemisphere)*.9);ambient.append(value);colours[index]=(*colours[index][:3],value)
 if index%50000==0:progress(f'Geometric ambient visibility {index}/{len(me.vertices)}')
meta['ambient_visibility']={'method':'12 cosine-weighted rays per source vertex, 0.16 author-unit radius, wood only','min':min(ambient),'mean':sum(ambient)/len(ambient),'max':max(ambient),'stored':'COLOR_0 alpha; browser forces opacity to one and applies mask only to indirect illumination'}
for layer in list(me.uv_layers):me.uv_layers.remove(layer)
uv=me.uv_layers.new(name='Wood flow');uv.active_render=True
for face in me.polygons:
 coords=[flow[me.loops[k].vertex_index] for k in face.loop_indices];wrap=max(v[0] for v in coords)-min(v[0] for v in coords)>.5
 for loop,(u,v) in zip(face.loop_indices,coords):uv.data[loop].uv=(u+1 if wrap and u<.5 else u,v)
 face.use_smooth=True
uv1=me.uv_layers.new(name='Growth direction XY');uv2=me.uv_layers.new(name='Growth direction Z and chart confidence')
for loop in me.loops:
 x,y,z,confidence=directions[loop.vertex_index];uv1.data[loop.index].uv=(x,y);uv2.data[loop.index].uv=(z,confidence)
for attribute in list(me.color_attributes):me.color_attributes.remove(attribute)
col=me.color_attributes.new(name='Wood masks',type='FLOAT_COLOR',domain='POINT');col.data.foreach_set('color',[x for c in colours for x in c]);me.update()
bpy.context.view_layer.objects.active=core
core['authoring_version']=a.version;core['construction']='implicit volume with local growth-flow weathering; no applied living tube'
if a.foliage:
 exec((Path(__file__).parent/'canopy.py').read_text(),dict(globals()))
 shutil.copy2(Path(__file__).parent/'canopy.py',out/(prefix.name+'.canopy.py'))
meta['base_volume']=base.name;meta['version']=a.version;meta['refinement']={'type':'continuous spatial direction field, real surface relief and living mask on same solid','source_vertices':len(me.vertices),'guide_count':len(guides),'foliage':a.foliage,'seconds_before_export':time.monotonic()-start}
for ob in bpy.context.scene.objects:ob.select_set(ob.type=='MESH' or ob.name=='Branch led scale foliage' or ob.name.startswith('Canopy spatial group'))
bpy.context.view_layer.objects.active=core;bpy.ops.wm.save_as_mainfile(filepath=str(prefix.with_suffix('.blend')),compress=True)
mod=core.modifiers.new('Runtime wood budget','DECIMATE');mod.ratio=min(1,170000/len(me.polygons))
bpy.ops.export_scene.gltf(filepath=str(prefix.with_suffix('.glb')),export_format='GLB',use_selection=True,export_yup=True,export_normals=True,export_materials='EXPORT',export_apply=True,export_vertex_color='ACTIVE',export_all_vertex_colors=True,export_extras=True,export_gpu_instances=True,export_draco_mesh_compression_enable=True,export_draco_mesh_compression_level=6,export_draco_position_quantization=16,export_draco_normal_quantization=10,export_draco_texcoord_quantization=12)
meta['glb_bytes']=prefix.with_suffix('.glb').stat().st_size;meta['refinement']['seconds_total']=time.monotonic()-start;prefix.with_suffix('.json').write_text(json.dumps(meta,indent=2));shutil.copy2(__file__,out/(prefix.name+'.refine.py'));shutil.copy2(prefix.with_suffix('.glb'),out.parent/'site/public/models/hero.glb');progress(f'Saved {prefix.name}; {meta["glb_bytes"]} bytes')
