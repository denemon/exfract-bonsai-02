"""Restore one selected compact control record into the protected native basis in memory.

Writes a new native file only, packs the CC0 bark maps, reopens and validates it.
The browser material remains the authoritative final rendering implementation.
"""
import bpy, bmesh, json, sys, hashlib, argparse
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree

parser=argparse.ArgumentParser()
parser.add_argument('--version',required=True)
args=parser.parse_args(sys.argv[sys.argv.index('--')+1:])
RUN=Path(__file__).resolve().parents[1]
record=RUN/'models'/f'{args.version}.json'
meta=json.loads(record.read_text())
basis=Path(meta['basis_native'])
assert hashlib.sha256(basis.read_bytes()).hexdigest()==meta['basis_sha256']
destination=RUN/'models'/f'{args.version}-editable.blend'
assert not destination.exists()
bpy.ops.wm.open_mainfile(filepath=str(basis))
core=bpy.data.objects['Continuous aged trunk and primary branches']
mesh=core.data
assert len(mesh.vertices)==len(meta['control_vertices'])
assert [list(f.vertices) for f in mesh.polygons]==meta['control_faces']
for vertex,position in zip(mesh.vertices,meta['control_vertices']):vertex.co=position
for color,value in zip(mesh.color_attributes.active_color.data,meta['colors']):color.color=value
for layer in list(mesh.uv_layers):mesh.uv_layers.remove(layer)
for name,key in [('Main growth surface','flow_uv'),('Branch growth surface','branch_uv'),('Collar transition and calibre','metric_uv')]:
    layer=mesh.uv_layers.new(name=name)
    for loop,value in zip(layer.data,meta[key]):loop.uv=value
crease=mesh.attributes.get('crease_edge') or mesh.attributes.new('crease_edge','FLOAT','EDGE')
for edge,value in zip(crease.data,meta['edge_creases']):edge.value=value
mesh.update()
assert core.modifiers[0].type=='SUBSURF' and core.modifiers[0].levels==1
core['authoring_version']=args.version
core['source_control_record']=str(record)
core['source_native']=str(basis)
core['construction']='Single connected solid cage; front growth plane and two branch shoulders; dual growth UV surfaces'
core['normal_scene_color']='Natural grey-brown and brown; no white/silver region'
core['status']='Selected stage 6 study; see REPORT.md for geometry and full-garden limitations'
core['bark_source']='Poly Haven Chinese Cedar Bark / Charlotte Baglioni / CC0-1.0'
for name,key in [('SURFACE · broad front plane','weather_masks'),('SURFACE · heavy root shoulder','shoulder_masks')]:
    old=core.vertex_groups.get(name)
    if old:core.vertex_groups.remove(old)
    group=core.vertex_groups.new(name=name)
    for i,weight in enumerate(meta[key]):
        if weight>0.0001:group.add([i],weight,'REPLACE')

# Self-contained native editing preview. Use both growth coordinates and pack
# all source maps, while retaining the exact browser shader alongside the native.
material=bpy.data.materials.new('Grey brown cedar — packed editing preview')
material.use_nodes=True;material.diffuse_color=(.16,.115,.077,1)
nodes=material.node_tree.nodes;links=material.node_tree.links
bs=nodes.get('Principled BSDF');bs.inputs['Roughness'].default_value=.94
maps={}
for name in ['color','normal','height','roughness']:
    im=bpy.data.images.load(str(RUN/'site/public/bark'/f'{name}.jpg'),check_existing=False)
    im.colorspace_settings.name='sRGB' if name=='color' else 'Non-Color'
    im.pack();maps[name]=im
metric=nodes.new('ShaderNodeUVMap');metric.uv_map='Collar transition and calibre'
separate=nodes.new('ShaderNodeSeparateXYZ');links.new(metric.outputs['UV'],separate.inputs[0])
colors=[];normals=[];roughs=[]
for index,uvname in enumerate(['Main growth surface','Branch growth surface']):
    uv=nodes.new('ShaderNodeUVMap');uv.uv_map=uvname
    scale=nodes.new('ShaderNodeVectorMath');scale.operation='SCALE';scale.inputs['Scale'].default_value=1/.72
    links.new(uv.outputs['UV'],scale.inputs[0])
    offset=nodes.new('ShaderNodeVectorMath');offset.operation='ADD';offset.inputs[1].default_value=(.07 if index==0 else .38,.11,0)
    links.new(scale.outputs[0],offset.inputs[0])
    textures={}
    for name in maps:
        tex=nodes.new('ShaderNodeTexImage');tex.image=maps[name];tex.extension='REPEAT';tex.label=name+' / '+uvname
        links.new(offset.outputs[0],tex.inputs['Vector']);textures[name]=tex
    normal=nodes.new('ShaderNodeNormalMap');normal.uv_map=uvname;normal.inputs['Strength'].default_value=.44
    links.new(textures['normal'].outputs['Color'],normal.inputs['Color'])
    colors.append(textures['color'].outputs['Color']);normals.append(normal.outputs['Normal']);roughs.append(textures['roughness'].outputs['Color'])
def blend(a,b):
    node=nodes.new('ShaderNodeMixRGB');links.new(separate.outputs['X'],node.inputs[0]);links.new(a,node.inputs[1]);links.new(b,node.inputs[2]);return node.outputs[0]
links.new(blend(colors[0],colors[1]),bs.inputs['Base Color'])
links.new(blend(normals[0],normals[1]),bs.inputs['Normal'])
rough=nodes.new('ShaderNodeMath');rough.operation='MULTIPLY_ADD';rough.inputs[1].default_value=.13;rough.inputs[2].default_value=.86
links.new(blend(roughs[0],roughs[1]),rough.inputs[0]);links.new(rough.outputs[0],bs.inputs['Roughness'])
mesh.materials.clear();mesh.materials.append(material)
for ob in bpy.context.scene.objects:
    if ob.get('foliage_lod_template'):ob.hide_render=True;ob.hide_set(True)
    ob.select_set(ob==core)
bpy.context.view_layer.objects.active=core
bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=str(destination),compress=True)
bpy.ops.wm.open_mainfile(filepath=str(destination))
core=bpy.data.objects['Continuous aged trunk and primary branches'];mesh=core.data
error=max((v.co-Vector(p)).length for v,p in zip(mesh.vertices,meta['control_vertices']))
assert error<1e-7
assert [list(f.vertices) for f in mesh.polygons]==meta['control_faces']
uv_error={}
for name,key in [('Main growth surface','flow_uv'),('Branch growth surface','branch_uv'),('Collar transition and calibre','metric_uv')]:
    uv_error[name]=max((p.uv-Vector(q)).length for p,q in zip(mesh.uv_layers[name].data,meta[key]))
assert max(uv_error.values())<1e-7
evaluated=core.evaluated_get(bpy.context.evaluated_depsgraph_get());surface=evaluated.to_mesh();surface.calc_loop_triangles()
bm=bmesh.new();bm.from_mesh(surface);volume=bm.calc_volume(signed=True)
boundary=sum(e.is_boundary for e in bm.edges);nonmanifold=sum(not e.is_manifold for e in bm.edges)
triangles=[tuple(t.vertices) for t in surface.loop_triangles]
tree=BVHTree.FromPolygons([v.co.copy() for v in surface.vertices],triangles,all_triangles=True,epsilon=1e-9)
intersections=sum(i<j and set(triangles[i]).isdisjoint(triangles[j]) for i,j in tree.overlap(tree))
assert abs(volume-meta['inspection']['volume'])<1e-7 and boundary==nonmanifold==intersections==0
hidden=sum(bool(o.get('foliage_lod_template') and o.hide_render and o.hide_get()) for o in bpy.context.scene.objects)
assert hidden==12
packed=[{'name':im.name,'bytes':im.packed_file.size} for im in bpy.data.images if im.packed_file]
assert len(packed)==4
result={'version':args.version,'native_file':str(destination),'native_bytes':destination.stat().st_size,'native_sha256':hashlib.sha256(destination.read_bytes()).hexdigest(),'protected_basis_sha256_after':hashlib.sha256(basis.read_bytes()).hexdigest(),'reopened':True,'control_vertices':len(mesh.vertices),'control_faces':len(mesh.polygons),'unapplied_subdivision':core.modifiers[0].levels,'evaluated_vertices':len(surface.vertices),'evaluated_triangles':len(triangles),'max_position_error':error,'max_uv_errors':uv_error,'volume':volume,'boundary_edges':boundary,'nonmanifold_edges':nonmanifold,'nonadjacent_intersections':intersections,'hidden_lod_templates':hidden,'packed_images':packed,'vertex_groups':[g.name for g in core.vertex_groups],'browser_is_final_rendering_reference':True,'native_preview_limitations':'Native material retains both UV flows and packed images. Custom shader desaturation, clamping and vertex-conditioned relief are implemented in site/src/materials.js rather than reproduced exactly by the preview node graph.'}
assert result['protected_basis_sha256_after']==meta['basis_sha256']
(RUN/'qa/native-roundtrip.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False),flush=True)
bm.free();evaluated.to_mesh_clear()
