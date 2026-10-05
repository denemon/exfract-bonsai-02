from pathlib import Path
import bpy,bmesh,json,hashlib,argparse,sys
from mathutils import Vector
RUN=Path(__file__).resolve().parents[2]
parser=argparse.ArgumentParser();parser.add_argument('--source',type=Path,default=RUN/'assets/source');parser.add_argument('--output',type=Path,required=True);args=parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
R=args.output;assert not R.exists(),'Choose a new empty output directory';(R/'assets/editable').mkdir(parents=True);(R/'site/public/rocks').mkdir(parents=True);(R/'qa').mkdir();manifest=R/'site/public/rocks/geometry-manifest.json';previous=None;rows=[]
def topology(obj):
 bm=bmesh.new();bm.from_mesh(obj.data);data={'vertices':len(bm.verts),'edges':len(bm.edges),'faces':len(bm.faces),'boundary_edges':sum(e.is_boundary for e in bm.edges),'wire_edges':sum(e.is_wire for e in bm.edges)};bm.free();return data
for asset,target in [('boulder_01',23000),('rock_09',12416)]:
 bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False);bpy.data.orphans_purge(do_recursive=True)
 source=args.source/asset/(asset+'_1k.gltf');bpy.ops.import_scene.gltf(filepath=str(source),merge_vertices=True)
 obj=next(o for o in bpy.context.scene.objects if o.type=='MESH');bpy.context.view_layer.objects.active=obj;obj.select_set(True);bpy.ops.object.transform_apply(location=True,rotation=True,scale=True)
 before=topology(obj);bm=bmesh.new();bm.from_mesh(obj.data);bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=max(obj.dimensions)*1e-6);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(obj.data);bm.free();welded=topology(obj)
 for face in obj.data.polygons:face.use_smooth=True
 if obj.data.has_custom_normals:obj.data.normals_split_custom_set([(0.,0.,0.)]*len(obj.data.loops))
 triangles=sum(len(f.vertices)-2 for f in obj.data.polygons)
 if triangles>target:
  mod=obj.modifiers.new('Coherent surface simplification','DECIMATE');mod.ratio=target/triangles;mod.use_collapse_triangulate=True;bpy.ops.object.modifier_apply(modifier=mod.name)
 final=topology(obj);assert final['boundary_edges']<=welded['boundary_edges']+20,(asset,welded,final)
 points=[v.co for v in obj.data.vertices];lo=Vector([min(p[i]for p in points)for i in range(3)]);hi=Vector([max(p[i]for p in points)for i in range(3)]);centre=(lo+hi)*.5;centre.z=lo.z;scale=1/max(hi.x-lo.x,hi.y-lo.y)
 for v in obj.data.vertices:v.co=(v.co-centre)*scale
 obj.name=asset+'_coherent_weathered_volume';obj['source_url']='https://polyhaven.com/a/'+asset;obj['license']='CC0';obj['purpose']='Shape/UV editable. Original PBR glTF preserved in assets/source; runtime PBR in garden-rocks.js.'
 obj.data.materials.clear();bpy.data.orphans_purge(do_recursive=True);bpy.context.preferences.filepaths.save_version=0;native=R/'assets/editable'/(asset+'.blend');bpy.ops.wm.save_as_mainfile(filepath=str(native))
 glb=R/'site/public/rocks'/(asset+'.glb');bpy.ops.export_scene.gltf(filepath=str(glb),export_format='GLB',use_selection=True,export_materials='NONE',export_texcoords=True,export_normals=True,export_draco_mesh_compression_enable=True,export_draco_mesh_compression_level=6,export_draco_position_quantization=16,export_draco_normal_quantization=12,export_draco_texcoord_quantization=14)
 rows.append({'id':asset,'topology_imported':before,'topology_welded':welded,'topology_final':final,'runtime_triangles':sum(len(f.vertices)-2 for f in obj.data.polygons),'native':str(native.relative_to(R)),'native_bytes':native.stat().st_size,'native_sha256':hashlib.sha256(native.read_bytes()).hexdigest(),'glb':str(glb.relative_to(R)),'glb_bytes':glb.stat().st_size,'glb_sha256':hashlib.sha256(glb.read_bytes()).hexdigest(),'normalization':'Bottom z=0, centered XY, longest horizontal extent=1; glTF Y-up export','geometry_only':True})
record={'diagnosis':'The first decimation used UV-split disconnected vertices; clay/no-normal browser captures showed a geometry defect. Import with vertex merging, weld identical positions, recalculate coherent normals, then simplify. Original source bytes retained.','before':previous,'after':rows}
(R/'qa/rock-conversion-diagnosis.json').write_text(json.dumps(record,indent=2)+'\n');manifest.write_text(json.dumps({'assets':rows,'method':record['diagnosis']},indent=2)+'\n');print('ROCK_REPAIR '+json.dumps(rows))
