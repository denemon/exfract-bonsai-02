"""Restore compact control cages, verify them, and save one editable native scene."""
import bpy,bmesh,json,sys,argparse,hashlib,shutil
from pathlib import Path
from mathutils import Vector
p=argparse.ArgumentParser();p.add_argument('--candidate',default='cage-v06');p.add_argument('--out',required=True);a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);run=Path(__file__).resolve().parents[1];dest=Path(a.out).resolve();assert not dest.exists();assert dest.parent==run/'models';assert shutil.disk_usage(run).free>2*1024**3
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
def restore(meta):
 me=bpy.data.meshes.new(meta['version']+' control cage');me.from_pydata(meta['control_vertices'],[],meta['control_faces']);me.update();bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free();ob=bpy.data.objects.new('Continuous aged trunk and primary branches',me);bpy.context.collection.objects.link(ob)
 sub=ob.modifiers.new('Editable cage · Catmull-Clark 2','SUBSURF');sub.levels=meta['controls']['subdivision'];sub.render_levels=sub.levels
 for f in me.polygons:f.use_smooth=True
 return ob
checks=[]
for path in sorted((run/'models').glob('cage-v[0-9][0-9].json')):
 meta=json.loads(path.read_text());ob=restore(meta);evaluated=ob.evaluated_get(bpy.context.evaluated_depsgraph_get());me=evaluated.to_mesh();bm=bmesh.new();bm.from_mesh(me);result={'version':meta['version'],'control_vertices':len(ob.data.vertices),'control_faces':len(ob.data.polygons),'evaluated_vertices':len(me.vertices),'evaluated_faces':len(me.polygons),'signed_volume':bm.calc_volume(signed=True),'boundary_edges':sum(e.is_boundary for e in bm.edges),'nonmanifold_edges':sum(not e.is_manifold for e in bm.edges)};bm.free();expected=meta['evaluated_inspection'];assert result['evaluated_vertices']==expected['vertices'] and result['evaluated_faces']==expected['faces'] and abs(result['signed_volume']-expected['signed_volume'])<1e-6 and result['boundary_edges']==0 and result['nonmanifold_edges']==0;checks.append(result);evaluated.to_mesh_clear();old=ob.data;bpy.data.objects.remove(ob,do_unlink=True);bpy.data.meshes.remove(old)
(run/'qa/compact-restore-check.json').write_text(json.dumps({'restored_compact_cages':checks,'native_duplicates_written':False},indent=2)+'\n')
meta=json.loads((run/'models'/(a.candidate+'.json')).read_text());core=restore(meta);core['authoring_version']=a.candidate;core['status']='Accepted low-resolution solid framework only; aged bonsai and finished garden remain incomplete';core['source_control_record']=str(run/'models'/(a.candidate+'.json'));core['web_scale']=.66
root=core.vertex_groups.new(name='ROOT · continuous buried buttresses');root.add([v.index for v in core.data.vertices if v.co.z<=meta['controls']['soil']+.32],1,'REPLACE')
child_vertices=set()
for branch in meta['branch_topology']:
 ids=set(branch['shared_boundary_vertices']);new={i for row in branch['new_rings'] for i in row};ids.update(new);child_vertices.update(new);group=core.vertex_groups.new(name='BRANCH · '+branch['name']);group.add(sorted(ids),1,'REPLACE')
group=core.vertex_groups.new(name='TRUNK · continuous parent');group.add([v.index for v in core.data.vertices if v.index not in child_vertices],1,'REPLACE')
base=Path(meta['support_reference'])
# Exact known support hash; no old wood is imported.
assert hashlib.sha256(base.read_bytes()).hexdigest()=='ca3eb2b5f1e55ba51671ecfafa20ff0d48076756f3dda7467da0e7e0bb6d5b08'
with bpy.data.libraries.load(str(base),link=False) as (source,target):target.objects=[n for n in source.objects if n.startswith(('Shallow unglazed pot','Low ceramic foot','Low split natural bedding stone','Continuous planted soil'))]
for ob in target.objects:
 if ob:bpy.context.collection.objects.link(ob)
neutral=bpy.data.materials.new('Neutral clay — no grain, normal map or AO');neutral.diffuse_color=(.43,.43,.41,1);neutral.use_nodes=True;shader=neutral.node_tree.nodes.get('Principled BSDF');shader.inputs['Base Color'].default_value=(.43,.43,.41,1);shader.inputs['Roughness'].default_value=1
for ob in bpy.context.scene.objects:
 if ob.type=='MESH':ob.data.materials.clear();ob.data.materials.append(neutral)
cam=bpy.data.objects.new('Inspection camera',bpy.data.cameras.new('Inspection camera'));bpy.context.collection.objects.link(cam);cam.location=(2.4,-4.0,2.65);target=Vector((0,0,1.12));cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.lens=55;bpy.context.scene.camera=cam
for name,location,energy,size in [('Soft inspection key',(-3,-4,6),600,5),('Soft inspection fill',(4,1,3),240,4)]:
 data=bpy.data.lights.new(name,'AREA');data.energy=energy;data.shape='DISK';data.size=size;ob=bpy.data.objects.new(name,data);bpy.context.collection.objects.link(ob);ob.location=location;ob.rotation_euler=(target-ob.location).to_track_quat('-Z','Y').to_euler()
scene=bpy.context.scene;scene.unit_settings.system='METRIC';scene.unit_settings.scale_length=.66;scene.render.resolution_x=1440;scene.render.resolution_y=900
for ob in scene.objects:ob.select_set(ob==core)
bpy.context.view_layer.objects.active=core
for screen in bpy.data.screens:
 for area in screen.areas:
  if area.type=='VIEW_3D':
   space=area.spaces.active;space.shading.type='SOLID';space.shading.color_type='MATERIAL';space.shading.show_cavity=False;space.region_3d.view_location=target;space.region_3d.view_rotation=cam.rotation_euler.to_quaternion();space.region_3d.view_distance=4.3
text=bpy.data.texts.new('READ ME — coarse geometry only');text.write('This is the selected cage-v06 coarse anatomical framework. The editable wood object has 554 control vertices and an unapplied Catmull-Clark modifier. Root, parent trunk and each primary branch have named vertex groups. The scene is self-contained neutral clay, with inspection camera and lights. No final bark, deadwood damage, living vein, foliage or garden finish is included. Runtime v23 is preserved separately. Future manual cage edits should be saved to a new version; the procedural controls recreate this snapshot only. Web scale: 0.66 metre per authoring unit.\n')
bpy.ops.wm.save_as_mainfile(filepath=str(dest),compress=True)
# Read the saved native file back, rather than infer success from the save call.
bpy.ops.wm.open_mainfile(filepath=str(dest));restored=bpy.data.objects['Continuous aged trunk and primary branches'];assert len(restored.data.vertices)==meta['control_inspection']['vertices'];assert len(restored.data.polygons)==meta['control_inspection']['faces'];assert restored.modifiers[0].type=='SUBSURF' and restored.modifiers[0].levels==2;assert len(restored.vertex_groups)==2+len(meta["branch_topology"])
result={'native_file':str(dest),'bytes':dest.stat().st_size,'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'version':a.candidate,'reopened':True,'editable_control_vertices':len(restored.data.vertices),'editable_control_faces':len(restored.data.polygons),'unapplied_subdivision':2,'named_vertex_groups':[g.name for g in restored.vertex_groups],'compact_versions_restored':len(checks),'self_contained_geometry':True}
(run/'qa/native-roundtrip.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False),flush=True)
