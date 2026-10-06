from pathlib import Path
import bpy,bmesh,json,math,hashlib
from mathutils import Vector
from mathutils.bvhtree import BVHTree
R=Path('/Users/kazuki.tanaka/dev0/exfract-bonsai-02/improvement/2026-10-04/runs/grown-core-0554');version='grown-v02';source=R.parent/'root-flow-0206/models/root-v02-editable.blend';assert not(R/'models'/f'{version}.glb').exists();plan=json.loads((R/'design/sculpt-plan-v02.json').read_text())
bpy.ops.wm.open_mainfile(filepath=str(R.parent/'local-edges-0056/models/edge-v02-editable.blend'));soil=bpy.data.objects['Continuous planted soil'];bpy.context.view_layer.update();soilTree=BVHTree.FromPolygons([soil.matrix_world@v.co for v in soil.data.vertices],[list(f.vertices)for f in soil.data.polygons])
def soilH(x,y):
 p,_,_,_=soilTree.ray_cast(Vector((x,y,2)),Vector((0,0,-1)));return p.z
bpy.ops.wm.open_mainfile(filepath=str(source));bpy.context.preferences.filepaths.save_version=0;o=bpy.data.objects['Continuous aged trunk and primary branches'];tw=bpy.data.objects['Terminal twig hierarchy'];bpy.context.view_layer.objects.active=o
sha=lambda x:hashlib.sha256(json.dumps(x).encode()).hexdigest()
twigBefore={'position':sha([list(v.co)for v in tw.data.vertices]),'faces':sha([list(f.vertices)for f in tw.data.polygons])}
assert len(o.modifiers)==1 and o.modifiers[0].type=='SUBSURF' and o.modifiers[0].levels==2
bpy.ops.object.modifier_apply(modifier=o.modifiers[0].name);me=o.data;me.update();oldV=[v.co.copy()for v in me.vertices];oldFaces=[list(f.vertices)for f in me.polygons];oldUV={l.name:sha([list(d.uv)for d in l.data])for l in me.uv_layers};oldColor=sha([list(d.color)for d in me.color_attributes.active_color.data]);u=me.uv_layers[2];ownership=[[]for _ in me.vertices]
for f in me.polygons:
 for vi,li in zip(f.vertices,f.loop_indices):ownership[vi].append(u.data[li].uv.x)
def smooth(a,b,x):
 t=max(0,min(1,(x-a)/(b-a)));return t*t*(3-2*t)
masks=[smooth(.50,.56,q.z)*(1-smooth(1.64,1.69,q.z))*(1-smooth(.35,.72,max(ownership[k])))for k,q in enumerate(oldV)]
deltas=[Vector()for _ in me.vertices];records=[]
for tool in plan['coupled_native_sculpt_tools']:
 C=Vector(tool['centre']);A=Vector(tool['radii']);D=Vector(tool['maximum_delta']);weights=[]
 for k,q in enumerate(oldV):
  p=q-C;r=math.sqrt(sum((p[j]/A[j])**2 for j in range(3)));weights.append((1-r)**4*(1+4*r)*masks[k]if r<1 else 0)
 peak=max(weights);assert peak>1e-6,tool['name'];W=[w/peak for w in weights]
 for k,w in enumerate(W):deltas[k]+=D*w
 records.append({**tool,'actual_max_weight_before_normalization':peak,'vertices_in_stroke':sum(w>1e-8 for w in W)})
# One open short compression returns onto side/back; it replaces the two
# closed ellipsoid front tools rather than adding another decorative dent.
tool=plan['open_compression_stroke'];surfaceTree=BVHTree.FromPolygons(oldV,[list(f.vertices)for f in me.polygons]);anchors=[surfaceTree.find_nearest(Vector(p))[0]for p in tool['guide_anchors']];values=[Vector(d)for d in tool['deltas']];widths=tool['widths'];weights=[];strokeDelta=[]
for k,q in enumerate(oldV):
 options=[]
 for j,(a,b)in enumerate(zip(anchors,anchors[1:])):
  L=b-a;t=max(0,min(1,(q-a).dot(L)/L.length_squared));p=a+L*t;width=widths[j]*(1-t)+widths[j+1]*t;rho=(q-p).length/width;options.append((rho,j,t))
 rho,j,t=min(options);w=(1-rho)**4*(1+4*rho)*masks[k]if rho<1 else 0;weights.append(w);strokeDelta.append(values[j]*(1-t)+values[j+1]*t)
peak=max(weights);assert peak>1e-6
for k,w in enumerate(weights):deltas[k]+=strokeDelta[k]*(w/peak)
records.append({'name':'open-front-to-side-compression','projected_actual_anchors':[list(p)for p in anchors],'guide':tool,'vertices_in_stroke':sum(w>1e-8 for w in weights),'actual_max_weight_before_normalization':peak})
for k,v in enumerate(me.vertices):
 d=deltas[k]
 if d.length>.035:d*=.035/d.length
 v.co=oldV[k]+d
me.update();assert oldFaces==[list(f.vertices)for f in me.polygons];assert all(oldUV[l.name]==sha([list(d.uv)for d in l.data])for l in me.uv_layers);assert oldColor==sha([list(d.color)for d in me.color_attributes.active_color.data]);assert all(v.co==oldV[k]for k,v in enumerate(me.vertices)if masks[k]==0)
bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free();me.update();me.calc_loop_triangles();tris=[tuple(t.vertices)for t in me.loop_triangles];bm=bmesh.new();bm.from_mesh(me);volume=bm.calc_volume(signed=True);boundary=sum(e.is_boundary for e in bm.edges);nonmanifold=sum(not e.is_manifold for e in bm.edges);bm.free();tree=BVHTree.FromPolygons([v.co.copy()for v in me.vertices],tris,all_triangles=True,epsilon=1e-9);pairs=[(a,b)for a,b in tree.overlap(tree)if a<b and set(tris[a]).isdisjoint(tris[b])];assert boundary==nonmanifold==len(pairs)==0 and volume>0
protected=[k for k,m in enumerate(masks)if m==0];changed=[{'vertex':k,'old':list(q),'new':list(me.vertices[k].co),'delta':list(me.vertices[k].co-q)}for k,q in enumerate(oldV)if me.vertices[k].co!=q];root=[{'xyz':list(v.co),'soil_z':soilH(v.co.x,v.co.y)}for k,v in enumerate(me.vertices)if oldV[k].z<.40];assert all(me.vertices[k].co==q for k,q in enumerate(oldV)if q.z<=.50);assert twigBefore=={'position':sha([list(v.co)for v in tw.data.vertices]),'faces':sha([list(f.vertices)for f in tw.data.polygons])}
ins={'version':version,'native_surface_vertices':len(me.vertices),'native_surface_faces':len(me.polygons),'triangles':len(tris),'volume':volume,'boundary_edges':boundary,'nonmanifold_edges':nonmanifold,'nonadjacent_intersections':len(pairs),'actual_surface_below_z050_unchanged':True,'UV_color_index_unchanged_from_applied_R25':True,'protected_vertex_count':len(protected),'modified_vertex_count':len(changed),'max_actual_displacement':max((v.co-oldV[k]).length for k,v in enumerate(me.vertices)),'twig_unchanged':twigBefore,'geometry_frozen':False,'structure_only_not_aesthetic':True}
(R/'qa/geometry-inspection-v02.json').write_text(json.dumps(ins,indent=2)+'\n');(R/'sculpt/control-record-v02.json').write_text(json.dumps({'source_native':str(source),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'method':plan['stroke_method'],'coupled_strokes':records,'native_inspection':ins,'changes':changed,'protected_positions_sha256':sha([list(me.vertices[k].co)for k in protected]),'position_sha256':sha([list(v.co)for v in me.vertices]),'normal_sha256':sha([list(v.normal)for v in me.vertices]),'faces_sha256':sha(oldFaces),'UV_sha256':oldUV,'color_sha256':oldColor,'root_inspection':root,'geometry_frozen':False},separators=(',',':'))+'\n')
o['authoring_version']=version;tw['authoring_version']=version;o['construction']='ActualR25 applied closed surface directly sculpted as one coupled nonuniform grown core; unchangedroot load and terminal/crown';o['form_gate']='Beforematerial: wholegray night/neutral PC390320/limitedside mass/branchsupport gate'
bpy.ops.wm.save_as_mainfile(filepath=str(R/'models'/f'{version}-editable.blend'),compress=True);bpy.ops.object.select_all(action='DESELECT');o.select_set(True);tw.select_set(True);bpy.ops.export_scene.gltf(filepath=str(R/'models'/f'{version}.glb'),export_format='GLB',use_selection=True,export_apply=True,export_extras=True,export_vertex_color='ACTIVE',export_draco_mesh_compression_enable=True,export_draco_mesh_compression_level=6,export_draco_position_quantization=15,export_draco_normal_quantization=11,export_draco_texcoord_quantization=13)
print(json.dumps(ins),flush=True);print(json.dumps({'native_bytes':(R/'models'/f'{version}-editable.blend').stat().st_size,'glb_bytes':(R/'models'/f'{version}.glb').stat().st_size}),flush=True)
