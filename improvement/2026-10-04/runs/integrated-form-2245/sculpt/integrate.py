"""Restore editable major-form cage and grow a representative attached canopy."""
import bpy,bmesh,json,sys,argparse,random,math,shutil,time,hashlib
import numpy as np
from pathlib import Path
from mathutils import Vector,Quaternion,noise
from mathutils.bvhtree import BVHTree
p=argparse.ArgumentParser();p.add_argument('--base',default='form-v04');p.add_argument('--version',default='integrated-v01');p.add_argument('--native',action='store_true');p.add_argument('--canopy-controls');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);run=Path(__file__).resolve().parents[1];out=run/'models';prefix=out/a.version;assert not prefix.with_suffix('.glb').exists();assert shutil.disk_usage(run).free>2*1024**3;started=time.monotonic();src=json.loads((out/f'{a.base}.json').read_text());SOIL=src['soil'];meta={'version':a.version,'wood_basis':a.base,'source':src['basis_native'],'wood_inspection':src['inspection']}
def progress(s):print(f'{time.monotonic()-started:.1f}s {s}',flush=True)
def smooth(a,b,x):t=max(0,min(1,(x-a)/(b-a)));return t*t*(3-2*t)
bpy.ops.wm.open_mainfile(filepath=src['basis_native']);core=bpy.data.objects['Continuous aged trunk and primary branches'];me=bpy.data.meshes.new('Editable major growth planes');me.from_pydata(src['control_vertices'],[],src['control_faces']);me.update();core.data=me;core.vertex_groups.clear();core.modifiers[0].name='Unapplied shared-surface subdivision';core.modifiers[0].levels=src.get('subdivision',1);core.modifiers[0].render_levels=core.modifiers[0].levels
for f in me.polygons:f.use_smooth=True
col=me.color_attributes.new(name='Continuous growth masks',type='FLOAT_COLOR',domain='POINT');col.data.foreach_set('color',[x for c in src['colors'] for x in c]);me.color_attributes.active_color=col
uv=me.uv_layers.new(name='Coarse spatial coordinates')
for loop in me.loops:p=me.vertices[loop.vertex_index].co;uv.data[loop.index].uv=(p.x,p.z)
wood=bpy.data.materials.new('Continuous wood growth');wood.use_nodes=True;wood.diffuse_color=(.43,.39,.31,1);bs=wood.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(.43,.39,.31,1);bs.inputs['Roughness'].default_value=.93;me.materials.append(wood);core['authoring_version']=a.version;core['construction']='shared cage major planes and continuous living/dead surface attributes';core['wood_basis']=a.base;core['source_control_record']=str(out/f'{a.base}.json');core['status']='integrated editing study; aged deadwood and whole garden unfinished'
for title,indices in [('ROOT · retained ground contact',[v.index for v in me.vertices if v.co.z<SOIL+.20]),('LOWER TRUNK · full support volume',[v.index for v in me.vertices if SOIL+.15<v.co.z<SOIL+.85]),('UPPER TRUNK · major growth planes',[v.index for v in me.vertices if v.co.z>=SOIL+.85])]:
 group=core.vertex_groups.new(name=title);group.add(indices,1,'REPLACE')
for ob in bpy.context.scene.objects:
 if ob.type!='MESH' or ob==core:continue
 name='Unglazed ceramic' if ob.name.startswith(('Shallow','Low ceramic')) else 'Planted soil' if ob.name.startswith('Continuous planted') else 'Bedding stone';m=bpy.data.materials.get(name) or bpy.data.materials.new(name);m.diffuse_color=(.18,.12,.08,1);ob.data.materials.clear();ob.data.materials.append(m)
# The field for contact details comes from the real support soil surface.
soil=bpy.data.objects['Continuous planted soil'];soil_tree=BVHTree.FromPolygons([soil.matrix_world@v.co for v in soil.data.vertices],[f.vertices[:] for f in soil.data.polygons]);
def exact_soil_height(x,y):
 hit,_,_,_=soil_tree.ray_cast(Vector((x,y,2)),Vector((0,0,-1)));return hit.z if hit is not None else SOIL

def sample_route(points,count=55):
 ps=[Vector(p) for p in points];res=[]
 for k in range(count):
  t=k/(count-1)*(len(ps)-1);i=min(len(ps)-2,int(t));u=t-i;p0=ps[max(0,i-1)];p1=ps[i];p2=ps[i+1];p3=ps[min(len(ps)-1,i+2)];q=.5*((2*p1)+(-p0+p2)*u+(2*p0-5*p1+4*p2-p3)*u*u+(-p0+3*p1-3*p2+p3)*u*u*u);res.append([*q,.02])
 return res
routes={b['name']:[b['root']]+[row[:3] for row in b['sections']] for b in src['branches']};routes['apex']=[[*centre,z] for centre,z in zip(src['controls']['main_centres'][10:],src['controls']['main_heights'][10:])] if 'main_heights' in src['controls'] else [[.115,-.09,1.10],[.10,.015,1.34],[.143,.06,1.49],[.163,.045,1.58],[.265,.078,1.665],[.302,.095,1.735]]
regions=[
('left lower primary',[-.99,-.17,.883],[.39,.27,.185],380,'First left living branch',0),
('left lower rear fork',[-.94,.105,.95],[.29,.215,.16],230,'First left living branch',0),
('left rear primary',[-.67,.285,1.27],[.35,.24,.195],380,'Rear ascending primary',1),
('upper left primary',[-.41,-.07,1.565],[.335,.235,.185],330,'Upper left primary',2),
('apex',[.19,.075,1.795],[.38,.285,.225],450,'apex',3),
('crown right primary',[.85,-.045,1.30],[.365,.265,.20],390,'Right crown primary',4),
('subordinate low right',[.82,-.085,.55],[.275,.215,.145],230,'Subordinate low right',5),
('rear crown fork',[.30,.30,1.66],[.29,.23,.18],170,'apex',3)]
if a.canopy_controls:regions=json.loads(Path(a.canopy_controls).read_text())
meta['canopy_controls']=regions;meta['paths']=[];CANOPY_REGIONS=[];REGION_GROUP=[]
for name,centre,extent,count,parent,group in regions:
 points=routes[parent]
 if name=='left lower rear fork':points=points[:4]+[[-.78,.035,.86],[-.93,.11,.94]]
 if name=='rear crown fork':points=points[:-3]+[[.22,.26,1.45],[.36,.34,1.53]]
 meta['paths'].append({'name':name,'parent_branch':parent,'control':points,'sampled':sample_route(points)});CANOPY_REGIONS.append((name,centre,extent,count));REGION_GROUP.append(group)
progress('Restored connected editable wood and explicit branch-led canopy routes')
exec((Path(__file__).parent/'canopy.py').read_text(),globals())
meta['seconds_before_export']=time.monotonic()-started;meta['native_saved']=bool(a.native);meta['files_have_no_generated_image_background']=True
for ob in bpy.context.scene.objects:ob.select_set(ob.type=='MESH' or ob.name=='Branch led scale foliage' or ob.name.startswith('Canopy spatial group'))
bpy.context.view_layer.objects.active=core
if a.native:
 for text in list(bpy.data.texts):bpy.data.texts.remove(text)
 text=bpy.data.texts.new('READ ME — integrated editable study');text.write('The main wood is one continuous shared control cage with unapplied subdivision. Continuous growth masks distinguish living tissue and deadwood on this same surface. Fine grain is deliberately absent. Leaves are individually attached volumetric scale-shoot instances on a twig hierarchy; their prototype meshes are shared. This is a study of major forms and representative canopy integration, not a premium finished garden. Save future changes to a new file.\n')
 bpy.ops.wm.save_as_mainfile(filepath=str(prefix.with_suffix('.blend')),compress=True)
bpy.ops.export_scene.gltf(filepath=str(prefix.with_suffix('.glb')),export_format='GLB',use_selection=True,export_apply=True,export_yup=True,export_normals=True,export_materials='EXPORT',export_vertex_color='ACTIVE',export_all_vertex_colors=True,export_extras=True,export_gpu_instances=True,export_draco_mesh_compression_enable=True,export_draco_mesh_compression_level=6,export_draco_position_quantization=16,export_draco_normal_quantization=10,export_draco_texcoord_quantization=12)
meta['glb_bytes']=prefix.with_suffix('.glb').stat().st_size;meta['seconds_total']=time.monotonic()-started;prefix.with_suffix('.json').write_text(json.dumps(meta,indent=2)+'\n');progress(f'Exported {a.version}: {meta["glb_bytes"]} bytes')
