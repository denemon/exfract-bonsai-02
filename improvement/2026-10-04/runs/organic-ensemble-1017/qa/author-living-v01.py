from pathlib import Path
import bpy,bmesh,json,math,hashlib
from mathutils import Vector
from mathutils.bvhtree import BVHTree
R=Path('/Users/kazuki.tanaka/dev0/exfract-bonsai-02/improvement/2026-10-04/runs/organic-ensemble-1017');version='living-v01';source=R.parent/'aged-ensemble-0831/models/aged-v01-editable.blend';assert not(R/'models'/f'{version}.glb').exists()
bpy.ops.wm.open_mainfile(filepath=str(source));bpy.context.preferences.filepaths.save_version=0;o=bpy.data.objects['Continuous aged trunk and primary branches'];tw=bpy.data.objects['Terminal twig hierarchy'];m=o.data;m.update();assert not o.modifiers
sha=lambda x:hashlib.sha256(json.dumps(x).encode()).hexdigest();old=[v.co.copy()for v in m.vertices];faces=[list(f.vertices)for f in m.polygons];uv={l.name:sha([list(d.uv)for d in l.data])for l in m.uv_layers};color=sha([list(d.color)for d in m.color_attributes.active_color.data]);twig={'position':sha([list(v.co)for v in tw.data.vertices]),'faces':sha([list(f.vertices)for f in tw.data.polygons])}
owners=[[]for _ in m.vertices]
for f in m.polygons:
 for vi,li in zip(f.vertices,f.loop_indices):owners[vi].append(m.uv_layers[2].data[li].uv.x)
views=[Vector(v).normalized()for v in [[0,-1,.176],[-.643,-.765,.105],[-.493,-.847,.095],[.422,-.906,.15],[-.422,-.906,.15]]]
def smooth(a,b,x):
 t=max(0,min(1,(x-a)/(b-a)));return t*t*(3-2*t)
normal=[v.normal.copy()for v in m.vertices];mask=[]
for k,q in enumerate(old):
 envelope=smooth(.50,.56,q.z)*(1-smooth(1.68,1.72,q.z))*(1-smooth(.70,.88,max(owners[k])))
 # Local surface changes stay away from the tangent silhouette for all five
 # protected views. This is a geometry constraint, not an aesthetic pass.
 contour=min(abs(normal[k].dot(v))for v in views);mask.append(envelope*smooth(.06,.28,contour))
tools=[{'name': 'rising-main-bearing-volume', 'anchors': [[0.04, -0.14, 0.63], [0.015, -0.16, 0.83], [-0.08, -0.13, 1.04], [-0.17, -0.065, 1.225], [-0.06, -0.085, 1.413]], 'widths': [0.095, 0.158, 0.182, 0.176, 0.108], 'deltas': [[0, 0, 0], [0.012, -0.032, 0.005], [0.018, -0.06, 0.008], [-0.012, -0.048, 0.012], [0, -0.004, 0]]}, {'name': 'inner-turn-open-compression-plane', 'anchors': [[0.14, -0.075, 0.73], [0.11, -0.065, 0.88], [-0.015, -0.055, 1.07], [-0.145, -0.012, 1.265]], 'widths': [0.086, 0.12, 0.148, 0.1], 'deltas': [[0, 0, 0], [-0.009, 0.022, 0.004], [0.012, 0.026, -0.01], [0, 0, 0]]}, {'name': 'side-return-growth-thickness', 'anchors': [[0.055, 0.08, 0.72], [0.07, 0.09, 0.93], [-0.13, 0.07, 1.24], [-0.11, 0.08, 1.38]], 'widths': [0.09, 0.158, 0.16, 0.105], 'deltas': [[0, 0, 0], [0.009, 0.025, 0.002], [-0.015, 0.041, 0.009], [0, 0, 0]]}, {'name': 'mother-fork-load-bearing-shoulder', 'anchors': [[-0.13, -0.09, 1.3], [-0.055, -0.094, 1.41], [0.08, -0.074, 1.483], [0.19, -0.047, 1.526], [0.31, -0.015, 1.57]], 'widths': [0.098, 0.135, 0.108, 0.068, 0.042], 'deltas': [[0, 0, 0], [-0.01, -0.025, 0.008], [0.008, -0.026, 0.016], [0.004, -0.012, 0.009], [0, 0, 0]]}, {'name': 'branch-under-return-with-open-exit', 'anchors': [[0.011, -0.067, 1.425], [0.12, -0.072, 1.478], [0.24, -0.05, 1.514]], 'widths': [0.083, 0.064, 0.04], 'deltas': [[0, 0, 0], [0.002, 0.006, -0.007], [0, 0, 0]]}, {'name': 'upper-stem-irregular-bearing-plane', 'anchors': [[-0.03, -0.055, 1.46], [0.085, -0.03, 1.55], [0.155, -0.006, 1.66]], 'widths': [0.078, 0.099, 0.06], 'deltas': [[0, 0, 0], [-0.01, -0.025, 0.008], [0, 0, 0]]}]
tree=BVHTree.FromPolygons(old,faces);deltas=[Vector()for _ in old];records=[]
for tool in tools:
 anchors=[tree.find_nearest(Vector(p))[0]for p in tool['anchors']];values=[Vector(v)for v in tool['deltas']];weights=[];directions=[]
 for k,q in enumerate(old):
  options=[]
  for j,(a,b)in enumerate(zip(anchors,anchors[1:])):
   L=b-a;t=max(0,min(1,(q-a).dot(L)/L.length_squared));p=a+L*t;w=tool['widths'][j]*(1-t)+tool['widths'][j+1]*t;options.append(((q-p).length/w,j,t))
  rho,j,t=min(options);weight=(1-rho)**4*(1+4*rho)*mask[k]if rho<1 else 0;weights.append(weight);directions.append(values[j]*(1-t)+values[j+1]*t)
 peak=max(weights);assert peak>1e-6,tool['name']
 for k,w in enumerate(weights):deltas[k]+=directions[k]*(w/peak)
 records.append({**tool,'projected_surface_anchors':[list(a)for a in anchors],'vertices_affected':sum(w>1e-8 for w in weights),'mask_peak_before_normalization':peak})
for k,v in enumerate(m.vertices):
 d=deltas[k]
 if d.length>.072:d*=.072/d.length
 v.co=old[k]+d
m.update();assert faces==[list(f.vertices)for f in m.polygons];assert uv=={l.name:sha([list(d.uv)for d in l.data])for l in m.uv_layers};assert color==sha([list(d.color)for d in m.color_attributes.active_color.data]);assert all(list(v.co)==list(old[k])for k,v in enumerate(m.vertices)if mask[k]==0)
assert twig=={'position':sha([list(v.co)for v in tw.data.vertices]),'faces':sha([list(f.vertices)for f in tw.data.polygons])};assert all(list(v.co)==list(old[k])for k,v in enumerate(m.vertices)if old[k].z<=.50 or old[k].z>=1.72)
m.calc_loop_triangles();tris=[tuple(t.vertices)for t in m.loop_triangles];bm=bmesh.new();bm.from_mesh(m);volume=bm.calc_volume(signed=True);boundary=sum(e.is_boundary for e in bm.edges);nonmanifold=sum(not e.is_manifold for e in bm.edges);bm.free();tree=BVHTree.FromPolygons([v.co.copy()for v in m.vertices],tris,all_triangles=True,epsilon=1e-9);pairs=[(a,b)for a,b in tree.overlap(tree)if a<b and set(tris[a]).isdisjoint(tris[b])];assert boundary==nonmanifold==len(pairs)==0 and volume>0
changed=[{'vertex':k,'old':list(q),'new':list(m.vertices[k].co),'delta':list(m.vertices[k].co-q)}for k,q in enumerate(old)if list(m.vertices[k].co)!=list(q)];protected=[k for k,x in enumerate(mask)if x==0]
inspection={'stage':34,'version':version,'native_vertices':len(m.vertices),'native_faces':len(m.polygons),'triangles':len(tris),'volume':volume,'boundary':boundary,'nonmanifold':nonmanifold,'nonadjacent_intersections':len(pairs),'changed_vertices_exact':len(changed),'protected_vertices':len(protected),'maximum_native_displacement_m':max((v.co-old[k]).length for k,v in enumerate(m.vertices)),'root_upper_terminal_UV_color_face_exact':True,'five_view_soft_tangent_guard':True,'not_aesthetic_pass':True,'form_frozen':False}
rec={'source':str(source),'source_SHA256':hashlib.sha256(source.read_bytes()).hexdigest(),'world_scale':.66,'method':'Six coupled C2 finite large/middle volume strokes: uneven ascending front/back bearing planes, inner-turn compression opening along growth and a thick load-bearing fork shoulder. Direct closed surface authoring; no surface noise or ring dents.','strokes':records,'protected_positions_sha256':sha([list(m.vertices[k].co)for k in protected]),'protected_vertex_ids':protected,'changes':changed,'position_sha256':sha([list(v.co)for v in m.vertices]),'normal_sha256':sha([list(v.normal)for v in m.vertices]),'faces_sha256':sha(faces),'UV_sha256':uv,'color_sha256':color,'twig_unchanged':twig,'native_inspection':inspection}
for path,data in [(R/'sculpt/control-record-v01.json',rec),(R/'qa/geometry-inspection-v01.json',inspection)]:
 with path.open('x')as f:json.dump(data,f,separators=(',',':'))
o['authoring_version']=version;tw['authoring_version']=version;o['construction']='R32 root and terminal domains retained; major/middle bearing volume and supported fork shoulder directly authored into closed native surface';o['form_gate']='Unadopted until independent clay and whole garden review'
bpy.ops.wm.save_as_mainfile(filepath=str(R/'models'/f'{version}-editable.blend'),compress=True);bpy.ops.object.select_all(action='DESELECT');o.select_set(True);tw.select_set(True);bpy.ops.export_scene.gltf(filepath=str(R/'models'/f'{version}.glb'),export_format='GLB',use_selection=True,export_apply=True,export_extras=True,export_vertex_color='ACTIVE',export_draco_mesh_compression_enable=True,export_draco_mesh_compression_level=6,export_draco_position_quantization=15,export_draco_normal_quantization=11,export_draco_texcoord_quantization=13)
print(json.dumps(inspection),flush=True)
