"""Two bounded local repairs; compact candidate mesh instead of full scene copies."""
import bpy,bmesh,sys,argparse,json,math,shutil,time,hashlib
from pathlib import Path
import numpy as np
p=argparse.ArgumentParser();p.add_argument('--base',required=True);p.add_argument('--out',required=True);p.add_argument('--variant',choices=['a','b'],required=True);a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);out=Path(a.out).resolve();out.mkdir(exist_ok=True);prefix=out/('local-'+a.variant)
assert not prefix.with_suffix('.glb').exists();assert shutil.disk_usage(out).free>2*1024**3
start=time.monotonic();bpy.ops.wm.open_mainfile(filepath=str(Path(a.base).resolve()));core=bpy.data.objects['Continuous aged trunk and primary branches'];me=core.data;SOIL=.393

def smooth(lo,hi,x):
 t=max(0,min(1,(x-lo)/(hi-lo)));return t*t*(3-2*t)
# A broad root buttress becomes subterranean smoothly; do not simply cover it
# with extra moss, crop it, or cut off an exposed point with a visible flat cap.
changed=0
for v in me.vertices:
 x,y,z=v.co;z-=SOIL
 if z<.26:
  radius=math.sqrt((x+.01)**2+(y*.94)**2);spread=smooth(.19,.51,radius);upper=1-smooth(.045,.25,z)
  strength=.86*spread*upper
  v.co.z=SOIL-.064+(z+.064)*(1-strength)
  if strength>.005:changed+=1
me.update()
# Each loss has a different plan, width and depth. No repeated periodic groove.
cutters=[
 {'name':'Irregular lower deadwood hollow','centre':[-.060,.285],'size':[.145,.355],
  'outline':[[-.44,-.51],[.17,-.45],[.41,-.25],[.36,-.03],[.51,.12],[.21,.48],[-.11,.52],[-.28,.32],[-.39,.05],[-.29,-.14]],
  'rings':[[-.60,1.18,0,0],[-.225,1,0,0],[-.082,.57,.014,.031],[-.049,.15,.018,.045]]},
 {'name':'Open broken shoulder edge','centre':[-.463,.633],'size':[.285,.116],
  'outline':[[-.55,-.18],[-.34,-.43],[-.08,-.33],[.18,-.54],[.49,-.13],[.46,.09],[.11,.46],[-.14,.23],[-.43,.45]],
  'rings':[[-.58,1.10,0,0],[-.16,1,0,0],[.022,.72,.032,-.018],[.064,.08,.058,-.013]]},
 {'name':'Unequal upper split','centre':[-.121,1.043],'size':[.101,.246],
  'outline':[[-.34,-.51],[.16,-.47],[.32,-.11],[.53,.11],[.15,.46],[-.14,.51],[-.29,.18],[-.48,-.07]],
  'rings':[[-.55,1.16,0,0],[-.193,1,0,0],[-.060,.57,.015,.004],[.014,.10,.019,-.018]]}
]
collection=bpy.data.collections.new('Authored local deadwood loss tools');bpy.context.scene.collection.children.link(collection);collection.hide_render=True
for record in cutters:
 verts=[];faces=[];cx,cz=record['centre'];sx,sz=record['size'];n=len(record['outline'])
 for y,scale,ox,oz in record['rings']:
  for x,z in record['outline']:verts.append((cx+x*sx*scale+ox,y,SOIL+cz+z*sz*scale+oz))
 for row in range(len(record['rings'])-1):
  for k in range(n):j=row*n+k;l=row*n+(k+1)%n;faces.append((j,l,l+n,j+n))
 faces.append(tuple(range(n-1,-1,-1)));faces.append(tuple((len(record['rings'])-1)*n+i for i in range(n)))
 mesh=bpy.data.meshes.new(record['name']);mesh.from_pydata(verts,[],faces);mesh.update();bm=bmesh.new();bm.from_mesh(mesh);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bmesh.ops.triangulate(bm,faces=list(bm.faces));bm.to_mesh(mesh);bm.free()
 ob=bpy.data.objects.new(record['name'],mesh);collection.objects.link(ob);bpy.context.view_layer.objects.active=core
 mod=core.modifiers.new(record['name'],'BOOLEAN');mod.operation='DIFFERENCE';mod.solver='EXACT';mod.object=ob;bpy.ops.object.modifier_apply(modifier=mod.name);ob.hide_render=True;ob.hide_set(True)
 print(record['name'],len(core.data.vertices),flush=True)
# Only soften the new cut boundary by less than a surface sample. Unequal broad
# faces and the carved openings remain real geometry.
me=core.data;bm=bmesh.new();bm.from_mesh(me);bmesh.ops.triangulate(bm,faces=list(bm.faces));bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free();me.update()
for face in me.polygons:face.use_smooth=True
bm=bmesh.new();bm.from_mesh(me);bm.verts.ensure_lookup_table();seen=set();components=[]
for vertex in bm.verts:
 if vertex.index in seen:continue
 stack=[vertex];seen.add(vertex.index);count=0
 while stack:
  cur=stack.pop();count+=1
  for edge in cur.link_edges:
   q=edge.other_vert(cur)
   if q.index not in seen:seen.add(q.index);stack.append(q)
 components.append(count)
inspection={'vertices':len(bm.verts),'faces':len(bm.faces),'boundary_edges':sum(e.is_boundary for e in bm.edges),'nonmanifold_edges':sum(not e.is_manifold for e in bm.edges),'signed_volume':bm.calc_volume(signed=True),'components':sorted(components,reverse=True),'root_vertices_changed':changed};bm.free()
assert inspection['boundary_edges']==0 and inspection['nonmanifold_edges']==0 and len(components)==1,inspection
core['authoring_version']='local-'+a.variant;core['construction']='preserved continuous volume with locally sculpted root descent and individually authored deadwood losses'
positions=np.empty((len(me.vertices),3),dtype=np.float32);me.vertices.foreach_get('co',positions.ravel());faces=np.array([f.vertices[:] for f in me.polygons],dtype=np.int32);np.savez_compressed(prefix.with_suffix('.mesh.npz'),positions=positions,faces=faces)
meta=json.loads(Path(a.base).with_suffix('.json').read_text());meta.update(version='local-'+a.variant,source=str(Path(a.base).resolve()),inspection=inspection,local_cutters=cutters,root_repair='z=-.064+(z+.064)*(1-.86*radial_falloff*height_falloff)',seconds_before_export=time.monotonic()-start)
prefix.with_suffix('.json').write_text(json.dumps(meta,indent=2)+'\n')
for ob in bpy.context.scene.objects:ob.select_set(ob.type=='MESH' and ob.name not in [r['name'] for r in cutters])
bpy.context.view_layer.objects.active=core;mod=core.modifiers.new('Runtime wood budget','DECIMATE');mod.ratio=min(1,170000/len(me.polygons))
bpy.ops.export_scene.gltf(filepath=str(prefix.with_suffix('.glb')),export_format='GLB',use_selection=True,export_yup=True,export_normals=True,export_materials='EXPORT',export_apply=True,export_vertex_color='ACTIVE',export_all_vertex_colors=True,export_extras=True,export_draco_mesh_compression_enable=True,export_draco_mesh_compression_level=6,export_draco_position_quantization=16,export_draco_normal_quantization=10,export_draco_texcoord_quantization=12)
shutil.copy2(prefix.with_suffix('.glb'),out.parent/'site/public/models/hero.glb');shutil.copy2(__file__,prefix.with_suffix('.operation.py'));print(json.dumps({'inspection':inspection,'seconds':time.monotonic()-start,'mesh_npz_bytes':prefix.with_suffix('.mesh.npz').stat().st_size,'glb_bytes':prefix.with_suffix('.glb').stat().st_size}),flush=True)
