"""A broad open weathered face in the existing shared solid; no new density."""
import bpy,bmesh,json,math,sys,argparse,hashlib,shutil,time
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree

p=argparse.ArgumentParser();p.add_argument('--version',default='wood-v01');p.add_argument('--design');a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
RUN=Path(__file__).resolve().parents[1];BASIS=RUN.parent/'integrated-form-2245';dest=RUN/'models'/a.version
assert not dest.with_suffix('.glb').exists();assert shutil.disk_usage(RUN).free>2*1024**3
source=json.loads((BASIS/'models/form-v08.json').read_text());soil=source['soil']
original=json.loads((RUN.parent/'anatomy-2150/models/cage-v06.json').read_text())['controls']['sections']
heights=source['controls']['main_heights'];centres=source['controls']['main_centres'];calibre=source['controls']['calibre']
design={
 'face':[[.005,-.77,.52,.68],[.10,-.70,.49,.66],[.26,-.79,.44,.64],[.41,-.72,.28,.67],[.55,-.61,.43,.73],[.64,-.30,.64,.83],[.72,.02,.70,.93]],
 'max_removal':.041,'shoulder_depth':.046,'shoulder_width':.32,'shoulder_heights':[.04,.17,.39,.61],
 'face_tilt':.065,'crease':.26,
 'knuckles':[{'branch':0,'t':.20,'width':.20,'swell':.16},{'branch':2,'t':.18,'width':.16,'swell':.12}]
}
if a.design:design=json.loads(Path(a.design).read_text())
def smooth(a,b,x):t=max(0,min(1,(x-a)/(b-a)));return t*t*(3-2*t)
def window(z,knots):a,b,c,d=knots;return smooth(a,b,z)*(1-smooth(c,d,z))
def guide(z):
 k=next((i for i in range(len(heights)-1) if heights[i+1]>=z),len(heights)-2)
 t=max(0,min(1,(z-heights[k])/(heights[k+1]-heights[k])))
 c=Vector((*centres[k],z+soil)).lerp(Vector((*centres[k+1],z+soil)),t)
 rx=original[k][3]*calibre[k][0]*(1-t)+original[k+1][3]*calibre[k+1][0]*t
 ry=original[k][4]*calibre[k][1]*(1-t)+original[k+1][4]*calibre[k+1][1]*t
 return c,rx,ry
def face_section(z):
 rows=design['face'];k=next((i for i in range(len(rows)-1) if rows[i+1][0]>=z),len(rows)-2)
 t=max(0,min(1,(z-rows[k][0])/(rows[k+1][0]-rows[k][0])));t=t*t*(3-2*t)
 return [rows[k][j]*(1-t)+rows[k+1][j]*t for j in range(1,4)]

bpy.ops.wm.open_mainfile(filepath=str(BASIS/'models/integrated-v03.blend'))
core=bpy.data.objects['Continuous aged trunk and primary branches'];mesh=core.data
assert len(mesh.vertices)==2314 and core.modifiers[0].levels==1
old_positions=[v.co.copy() for v in mesh.vertices];weather=[];shoulder=[]
for v in mesh.vertices:
 z=v.co.z-soil;c,rx,ry=guide(z);q=v.co-c;s=q.x/max(rx,.02);front=-q.y/max(ry,.02)
 left,right,depth=face_section(z)
 # The front plane opens into the root at the bottom and dissolves before
 # the branch shoulder. Only its left edge has a broad, substantial bank.
 territory=1-smooth(1.0,1.48,abs(s));front_weight=smooth(.05,.54,front)
 inside=smooth(left-.14,left+.14,s)*(1-smooth(right-.18,right+.48,s))
 ends=smooth(-.035,.055,z)*(1-smooth(.55,.73,z))
 face=inside*ends*front_weight*territory
 target_y=c.y-ry*depth+(s-left)*design['face_tilt']*ry
 removal=min(design['max_removal'],max(0,target_y-v.co.y))*face
 v.co.y+=removal
 # Convex support on only one flank; broad and bounded, not a detached lip.
 bank=math.exp(-.5*((s-(left-.14))/design['shoulder_width'])**2)*window(z,design['shoulder_heights'])*front_weight*territory
 v.co.y-=design['shoulder_depth']*bank
 v.co.x-=.018*bank
 # A small change of normal through the broad face keeps it from a single
 # mathematically flat panel; this is not a central hollow.
 v.co.y-=.009*face*math.exp(-((z-.34)/.16)**2)*smooth(-.1,.5,s)
 weather.append(face);shoulder.append(bank)

# Real branch routes also define the bark coordinates. Endpoints remain fixed,
# so the inherited twig attachments remain inside the branches.
paths=[]
main_points=[Vector((c[0],c[1],h+soil)) for c,h in zip(centres,heights)]
main_radii=[(o[3]*k[0]+o[4]*k[1])*.5 for o,k in zip(original,calibre)]
paths.append({'name':'main trunk','points':main_points,'radii':main_radii,'offset':0})
for b in source['branches']:
 pts=[Vector((v[0],v[1],v[2]+soil)) for v in [b['root']]+b['sections']]
 radii=[max(.065,sum(b['sections'][0][3:])*.6)]+[sum(v[3:])*.5 for v in b['sections']]
 paths.append({'name':b['name'],'points':pts,'radii':radii,'offset':b['root'][2]+.09})
for path in paths:
 total=[0.]
 for p0,p1 in zip(path['points'],path['points'][1:]):total.append(total[-1]+(p1-p0).length)
 path['lengths']=total
def nearest(point,path):
 best=None
 for i,(p0,p1) in enumerate(zip(path['points'],path['points'][1:])):
  edge=p1-p0;t=max(0,min(1,(point-p0).dot(edge)/edge.length_squared));c=p0+edge*t;q=point-c;distance=q.length
  if best is None or distance<best[0]:best=(distance,c,edge.normalized(),path['radii'][i]*(1-t)+path['radii'][i+1]*t,path['lengths'][i]+edge.length*t,i,t)
 return best
for knuckle in design['knuckles']:
 path=paths[knuckle['branch']+1]
 for v in mesh.vertices:
  d,c,tangent,radius,length,i,t=nearest(v.co,path);u=length/path['lengths'][-1]
  if d<radius*1.6 and u>.07 and u<.58:
   strength=knuckle['swell']*math.exp(-((u-knuckle['t'])/knuckle['width'])**2)*smooth(.07,.13,u)*(1-smooth(.4,.58,u))
   radial=v.co-c;radial-=tangent*radial.dot(tangent)
   v.co+=radial*strength

mesh.update()
# Same surface attributes; no red stripe or independent bark object.
color=mesh.color_attributes.get('Continuous growth masks')
for i,v in enumerate(mesh.vertices):color.data[i].color=(.78-.52*weather[i],weather[i],.48+.11*math.sin(v.co.z*3.1+v.co.x*2.8),1)
mesh.color_attributes.active_color=color
# A short partially sharp edge on the heavy bank, never a closed wound rim.
crease=mesh.attributes.get('crease_edge') or mesh.attributes.new('crease_edge','FLOAT','EDGE')
for e in mesh.edges:
 p0,p1=[mesh.vertices[i].co for i in e.vertices];mid=(p0+p1)*.5;z=mid.z-soil;c,rx,ry=guide(z);s=(mid.x-c.x)/rx;left,_,_=face_section(z)
 value=design['crease']*window(z,[.09,.17,.40,.55])*math.exp(-((s-left)/.20)**2)*smooth(.24,.58,-(mid.y-c.y)/ry)
 crease.data[e.index].value=value
for layer in list(mesh.uv_layers):mesh.uv_layers.remove(layer)
flow=mesh.uv_layers.new(name='Growth distance and circumference');metric=mesh.uv_layers.new(name='Growth calibre')
def path_for(point):
 candidates=[nearest(point,path) for path in paths]
 scores=[d/max(r,.018) for d,c,t,r,length,i,u in candidates]
 for j,value in enumerate(candidates[1:],1):
  # Keep the merged collar on the main trunk mapping until the branch has
  # enough independent length. Texture seams remain in a small saddle.
  length=value[4];scores[j]+=1.4*(1-smooth(.02,.11,length))
 return min(range(len(scores)),key=lambda j:scores[j])
for face in mesh.polygons:
 centre=sum((mesh.vertices[i].co for i in face.vertices),Vector())/len(face.vertices);path=paths[path_for(centre)];values=[]
 for li in face.loop_indices:
  point=mesh.vertices[mesh.loops[li].vertex_index].co;d,c,t,r,length,i,u=nearest(point,path)
  cross=Vector((0,1,0));cross=(cross-t*cross.dot(t)).normalized();side=t.cross(cross).normalized();q=point-c
  phase=math.atan2(q.dot(side),q.dot(cross))/math.tau
  values.append([li,phase,length+path['offset'],r])
 base=values[0][1]
 for li,phase,length,r in values:
  phase-=round(phase-base);flow.data[li].uv=(phase,length);metric.data[li].uv=(r,0.)
for f in mesh.polygons:f.use_smooth=True

material=bpy.data.materials.new('Continuous grey brown wood');material.use_nodes=True
material.diffuse_color=(.16,.115,.077,1);bs=material.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(.16,.115,.077,1);bs.inputs['Roughness'].default_value=.94
mesh.materials.clear();mesh.materials.append(material)
core['authoring_version']=a.version;core['construction']='One continuous existing solid; open broad weathered face and single substantial shoulder; growth-directed bark coordinates'
core['normal_scene_color']='Natural grey-brown and brown; no white';core['source_native']=str(BASIS/'models/integrated-v03.blend')
core['status']='Surface candidate; requires independent clay and whole-scene review'

bpy.context.view_layer.update();ev=core.evaluated_get(bpy.context.evaluated_depsgraph_get());evaluated=ev.to_mesh();evaluated.calc_loop_triangles()
positions=[v.co.copy() for v in evaluated.vertices];triangles=[tuple(t.vertices) for t in evaluated.loop_triangles]
tree=BVHTree.FromPolygons(positions,triangles,all_triangles=True,epsilon=1e-9);intersections=sum(i<j and set(triangles[i]).isdisjoint(triangles[j]) for i,j in tree.overlap(tree))
bm=bmesh.new();bm.from_mesh(evaluated);volume=bm.calc_volume(signed=True)
inspection={'control_vertices':len(mesh.vertices),'control_faces':len(mesh.polygons),'evaluated_vertices':len(positions),'evaluated_triangles':len(triangles),'volume':volume,'retained_volume_fraction':volume/source['inspection']['volume'],'boundary_edges':sum(e.is_boundary for e in bm.edges),'nonmanifold_edges':sum(not e.is_manifold for e in bm.edges),'nonadjacent_intersections':intersections,'max_edit':max((v.co-p).length for v,p in zip(mesh.vertices,old_positions)),'changed_controls':sum((v.co-p).length>1e-6 for v,p in zip(mesh.vertices,old_positions)),'subdivision':1}
assert not intersections and not inspection['boundary_edges'] and not inspection['nonmanifold_edges'] and .94<inspection['retained_volume_fraction']<1.08,inspection
bm.free();ev.to_mesh_clear()
record={'version':a.version,'basis_native':str(BASIS/'models/integrated-v03.blend'),'basis_sha256':hashlib.sha256((BASIS/'models/integrated-v03.blend').read_bytes()).hexdigest(),'design':design,'control_vertices':[list(v.co) for v in mesh.vertices],'control_faces':[list(f.vertices) for f in mesh.polygons],'colors':[list(c.color) for c in color.data],'flow_uv':[list(v.uv) for v in flow.data],'metric_uv':[list(v.uv) for v in metric.data],'edge_creases':[v.value for v in crease.data],'weather_masks':weather,'shoulder_masks':shoulder,'inspection':inspection}
dest.with_suffix('.json').write_text(json.dumps(record,indent=2)+'\n')
for obj in bpy.context.scene.objects:
 if obj.get('foliage_lod_template'):obj.hide_set(False);obj.hide_render=False
 obj.select_set(obj.type=='MESH' or obj.name=='Branch led scale foliage' or obj.name.startswith('Canopy spatial group'))
bpy.context.view_layer.objects.active=core
bpy.ops.export_scene.gltf(filepath=str(dest.with_suffix('.glb')),export_format='GLB',use_selection=True,export_apply=True,export_yup=True,export_normals=True,export_materials='EXPORT',export_vertex_color='ACTIVE',export_all_vertex_colors=True,export_extras=True,export_gpu_instances=True,export_draco_mesh_compression_enable=True,export_draco_mesh_compression_level=6,export_draco_position_quantization=16,export_draco_normal_quantization=10,export_draco_texcoord_quantization=14)
print(json.dumps({'version':a.version,'inspection':inspection,'glb_bytes':dest.with_suffix('.glb').stat().st_size}),flush=True)
