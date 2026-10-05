"""Restore the selected changed topology in a new native file, then reopen it.

The protected basis is read only. Packed source images and all other objects
are retained. The browser shader remains the final color reference.
"""
import bpy,bmesh,json,sys,argparse,hashlib
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree

p=argparse.ArgumentParser();p.add_argument('--version',required=True)
args=p.parse_args(sys.argv[sys.argv.index('--')+1:])
RUN=Path(__file__).resolve().parents[1]
record=RUN/'models'/f'{args.version}.json';d=json.loads(record.read_text())
basis=Path(d['basis_native']);sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(basis)==d['basis_sha256']
destination=RUN/'models'/f'{args.version}-editable.blend';assert not destination.exists()
bpy.ops.wm.open_mainfile(filepath=str(basis))
core=bpy.data.objects['Continuous aged trunk and primary branches']
materials=list(core.data.materials)
mesh=bpy.data.meshes.new('Local shoulder and broad front editable control net')
mesh.from_pydata(d['control_vertices'],[],d['control_faces']);mesh.update();core.data=mesh
for f in mesh.polygons:f.use_smooth=True
color=mesh.color_attributes.new(name='Continuous growth masks',type='FLOAT_COLOR',domain='POINT')
color.data.foreach_set('color',[v for row in d['colors'] for v in row]);mesh.color_attributes.active_color=color
keys=[('Main growth surface','flow_uv'),('Branch growth surface','branch_uv'),('Collar transition and calibre','metric_uv')]
for name,key in keys:
    layer=mesh.uv_layers.new(name=name)
    assert len(layer.data)==len(d[key])
    for loop,value in zip(layer.data,d[key]):loop.uv=value
crease=mesh.attributes.new('crease_edge','FLOAT','EDGE');assert len(crease.data)==len(d['edge_creases'])
for edge,value in zip(crease.data,d['edge_creases']):edge.value=value
core.vertex_groups.clear()
for name,weights in d['vertex_groups'].items():
    g=core.vertex_groups.new(name=name)
    for index,weight in weights:g.add([index],weight,'REPLACE')
for material in materials:mesh.materials.append(material)
assert len(materials)==1 and 'packed editing preview' in materials[0].name
assert core.modifiers[0].type=='SUBSURF' and core.modifiers[0].levels==1
core['authoring_version']=args.version;core['source_control_record']=str(record)
core['source_native']=str(basis)
core['construction']='56 authored control moves, five added shoulder rail points and six split cells; fixed perimeter, rear, root tips and branch attachments'
core['normal_scene_color']='Natural grey-brown and brown; no white/silver region'
core['status']='Stage 7 root attachment repair only; old wood major form and whole garden remain unfinished'
for ob in bpy.context.scene.objects:
    if ob.get('foliage_lod_template'):ob.hide_render=True;ob.hide_set(True)
    ob.select_set(ob==core)
bpy.context.view_layer.objects.active=core
bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=str(destination),compress=True)
bpy.ops.wm.open_mainfile(filepath=str(destination))
core=bpy.data.objects['Continuous aged trunk and primary branches'];mesh=core.data
position_error=max((v.co-Vector(p)).length for v,p in zip(mesh.vertices,d['control_vertices']))
uv_errors={name:max((v.uv-Vector(q)).length for v,q in zip(mesh.uv_layers[name].data,d[key])) for name,key in keys}
assert position_error==0 and max(uv_errors.values())==0
assert [list(f.vertices) for f in mesh.polygons]==d['control_faces']
assert [v.value for v in mesh.attributes['crease_edge'].data]==d['edge_creases']
restored_groups={g.name:[[v.index,x.weight] for v in mesh.vertices for x in v.groups if x.group==g.index] for g in core.vertex_groups}
assert restored_groups==d['vertex_groups']
ev=core.evaluated_get(bpy.context.evaluated_depsgraph_get());surface=ev.to_mesh();surface.calc_loop_triangles()
bm=bmesh.new();bm.from_mesh(surface);volume=bm.calc_volume(signed=True)
boundary=sum(e.is_boundary for e in bm.edges);nonmanifold=sum(not e.is_manifold for e in bm.edges)
tri=[tuple(t.vertices) for t in surface.loop_triangles]
tree=BVHTree.FromPolygons([v.co.copy() for v in surface.vertices],tri,all_triangles=True,epsilon=1e-9)
intersections=sum(i<j and set(tri[i]).isdisjoint(tri[j]) for i,j in tree.overlap(tree))
assert abs(volume-d['inspection']['volume'])<1e-7 and boundary==nonmanifold==intersections==0
packed=[{'name':im.name,'bytes':im.packed_file.size} for im in bpy.data.images if im.packed_file]
hidden=sum(bool(o.get('foliage_lod_template') and o.hide_render and o.hide_get()) for o in bpy.context.scene.objects)
assert len(packed)==4 and hidden==12 and sha(basis)==d['basis_sha256']
result={'version':args.version,'native_file':str(destination),'native_sha256':sha(destination),'native_bytes':destination.stat().st_size,'protected_basis_sha256_after':sha(basis),'reopened':True,'control_vertices':len(mesh.vertices),'control_faces':len(mesh.polygons),'unapplied_subdivision':core.modifiers[0].levels,'evaluated_vertices':len(surface.vertices),'evaluated_triangles':len(tri),'max_position_error':position_error,'max_uv_errors':uv_errors,'vertex_groups_exact':True,'vertex_groups':list(restored_groups),'volume':volume,'boundary_edges':boundary,'nonmanifold_edges':nonmanifold,'nonadjacent_intersections':intersections,'packed_images':packed,'hidden_lod_templates':hidden,'browser_is_final_rendering_reference':True,'native_preview_limitations':'Packed editing preview retains both UV flows. Exact color clamp/desaturation/relief are in site/src/materials.js.'}
(RUN/'qa/native-roundtrip.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False),flush=True);bm.free();ev.to_mesh_clear()
