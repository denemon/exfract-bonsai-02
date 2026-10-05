import bpy,bmesh,json,sys,hashlib,struct
from pathlib import Path
from mathutils import Vector
run=Path(__file__).resolve().parents[1];path=run/'models/integrated-v03.blend';source=run/'models/form-v08.json';meta=json.loads(source.read_text());bpy.ops.wm.open_mainfile(filepath=str(path));core=bpy.data.objects['Continuous aged trunk and primary branches'];me=core.data;assert len(me.vertices)==meta['inspection']['control_vertices'];assert len(me.polygons)==meta['inspection']['control_faces'];assert core.modifiers[0].type=='SUBSURF' and core.modifiers[0].levels==1
error=max((v.co-Vector(p)).length for v,p in zip(me.vertices,meta['control_vertices']));assert error<1e-6
core['source_control_record']=str(source);core['status']='Selected integrated study; aged deadwood macro-form and finished garden remain incomplete';core['wood_basis']='form-v08'
for branch in meta['branches']:
 points=[Vector((p[0],p[1],p[2]+meta['soil'])) for p in [branch['root']]+[row[:3] for row in branch['sections']]];radii=[.10]+[max(row[3:]) for row in branch['sections']];ids=[]
 for vertex in me.vertices:
  for i in range(len(points)-1):
   edge=points[i+1]-points[i];t=max(0,min(1,(vertex.co-points[i]).dot(edge)/max(1e-8,edge.length_squared)));distance=(vertex.co-(points[i]+edge*t)).length;radius=(radii[i]*(1-t)+radii[i+1]*t)*1.42
   if distance<radius:ids.append(vertex.index);break
 group=core.vertex_groups.new(name='BRANCH · '+branch['name']);group.add(ids,1,'REPLACE')
for ob in bpy.context.scene.objects:
 if ob.get('foliage_lod_template'):ob.hide_render=True;ob.hide_set(True)
# Native editor preview uses the same continuous surface mask; the browser
# remains the rendering source of truth for the final night scene.
mat=core.active_material;mat.use_nodes=True;nodes=mat.node_tree.nodes;links=mat.node_tree.links;bs=nodes.get('Principled BSDF');attr=nodes.new('ShaderNodeVertexColor');attr.layer_name='Continuous growth masks';separate=nodes.new('ShaderNodeSeparateColor');ramp=nodes.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].position=.32;ramp.color_ramp.elements[1].position=.72;mix=nodes.new('ShaderNodeMixRGB');mix.inputs[1].default_value=(.39,.38,.34,1);mix.inputs[2].default_value=(.20,.059,.016,1);links.new(attr.outputs['Color'],separate.inputs['Color']);links.new(separate.outputs['Red'],ramp.inputs['Fac']);links.new(ramp.outputs['Color'],mix.inputs[0]);links.new(mix.outputs[0],bs.inputs['Base Color']);bs.inputs['Roughness'].default_value=.93
for ob in bpy.context.scene.objects:ob.select_set(ob==core)
bpy.context.view_layer.objects.active=core;bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=str(path),compress=True);bpy.ops.wm.open_mainfile(filepath=str(path));core=bpy.data.objects['Continuous aged trunk and primary branches'];assert len(core.data.vertices)==2314 and core.modifiers[0].levels==1;ev=core.evaluated_get(bpy.context.evaluated_depsgraph_get());mesh=ev.to_mesh();bm=bmesh.new();bm.from_mesh(mesh);volume=bm.calc_volume(signed=True);assert abs(volume-meta['inspection']['volume'])<1e-6;assert not any(e.is_boundary or not e.is_manifold for e in bm.edges);bm.free();ev.to_mesh_clear();hidden_templates=sum(bool(ob.get('foliage_lod_template') and ob.hide_render and ob.hide_get()) for ob in bpy.context.scene.objects);assert hidden_templates==12
report={'native_file':str(path),'native_bytes':path.stat().st_size,'native_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'reopened':True,'editable_control_vertices':len(core.data.vertices),'editable_control_faces':len(core.data.polygons),'unapplied_subdivision':core.modifiers[0].levels,'max_position_error_vs_selected_control':error,'evaluated_volume_matches':True,'hidden_lod_templates':hidden_templates,'vertex_groups':[g.name for g in core.vertex_groups],'source_control_record':core['source_control_record'],'self_contained_geometry':True,'native_preview_growth_mask':True}
(run/'qa/native-roundtrip.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,ensure_ascii=False),flush=True)
