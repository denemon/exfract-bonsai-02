"""Preserve editable control paths, attach fixed support, export the coarse solid."""
import bpy,bmesh,sys,argparse,json,struct,math,shutil,time
from pathlib import Path
from mathutils import Vector
p=argparse.ArgumentParser();p.add_argument('--prefix',required=True);p.add_argument('--support',required=True);a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);prefix=Path(a.prefix);meta=json.loads(prefix.with_suffix('.json').read_text());start=time.monotonic()
for suffix in ['.blend','.glb']:
 if prefix.with_suffix(suffix).exists():raise FileExistsError('Use a new version')
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
with bpy.data.libraries.load(a.support,link=False) as (source,target):
 target.objects=[name for name in source.objects if name.startswith(('Shallow unglazed pot','Low ceramic foot','Low split natural bedding stone','Continuous planted soil'))]
for o in target.objects:
 if o:bpy.context.collection.objects.link(o)
wood=bpy.data.materials.new('Sculpted wood shader');wood.diffuse_color=(.30,.28,.24,1);wood.use_nodes=True
bsdf=wood.node_tree.nodes.get('Principled BSDF');bsdf.inputs['Base Color'].default_value=(.30,.28,.24,1);bsdf.inputs['Roughness'].default_value=.90
data=prefix.with_suffix('.triangles.f32').read_bytes();flat=struct.unpack('<'+'f'*(len(data)//4),data);vertices=[flat[i:i+3] for i in range(0,len(flat),3)];faces=[(i,i+1,i+2) for i in range(0,len(vertices),3)]
me=bpy.data.meshes.new('Implicit solid surface');me.from_pydata(vertices,[],faces);me.update();core=bpy.data.objects.new('Continuous aged trunk and primary branches',me);bpy.context.collection.objects.link(core);me.materials.append(wood)
bm=bmesh.new();bm.from_mesh(me);bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=.00002);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces))
bm.verts.ensure_lookup_table();seen=set();pieces=[]
for vertex in bm.verts:
 if vertex.index in seen:continue
 stack=[vertex];seen.add(vertex.index);piece=[]
 while stack:
  cur=stack.pop();piece.append(cur)
  for edge in cur.link_edges:
   nxt=edge.other_vert(cur)
   if nxt.index not in seen:seen.add(nxt.index);stack.append(nxt)
 pieces.append(piece)
pieces.sort(key=len,reverse=True);removed=[]
for piece in pieces[1:]:
 low=Vector(tuple(min(v.co[i] for v in piece) for i in range(3)));high=Vector(tuple(max(v.co[i] for v in piece) for i in range(3)))
 # Only a fragment smaller than two sampling cells on every axis qualifies.
 cell=Vector(meta['step']);assert len(piece)<=12 and all(high[i]-low[i]<cell[i]*2 for i in range(3)),{'disconnected_piece':len(piece),'low':list(low),'high':list(high),'cell':list(cell)}
 removed.append({'vertices':len(piece),'bounds':[list(low),list(high)],'diagonal':(high-low).length})
 bmesh.ops.delete(bm,geom=piece,context='VERTS')
meta['removed_subvoxel_fragments']=removed
if bm.calc_volume(signed=True)<0:bmesh.ops.reverse_faces(bm,faces=list(bm.faces))
bm.to_mesh(me);bm.free();me.update();bpy.context.view_layer.objects.active=core;core.select_set(True)
# Smooth sampling stair-steps only; broad growth junctions already belong to the field.
mod=core.modifiers.new('Sampling relaxation','SMOOTH');mod.factor=.55;mod.iterations=8;bpy.ops.object.modifier_apply(modifier=mod.name)
for v in me.vertices:v.co.z+=meta['soil_height']
for face in me.polygons:face.use_smooth=True
uv=me.uv_layers.new(name='Coarse inspection coordinates');color=me.color_attributes.new(name='Wood masks',type='FLOAT_COLOR',domain='POINT')
color.data.foreach_set('color',[v for _ in me.vertices for v in (0,.5,.5,1)])
for loop in me.loops:
 pos=me.vertices[loop.vertex_index].co;uv.data[loop.index].uv=(pos.x,pos.z)
controls=bpy.data.collections.new('Editable growth volumes — hidden in render');bpy.context.scene.collection.children.link(controls);controls.hide_render=True
for route in meta['paths']:
 curve=bpy.data.curves.new(route['name'],'CURVE');curve.dimensions='3D';spline=curve.splines.new('POLY');spline.points.add(len(route['control'])-1)
 for pt,value in zip(spline.points,route['control']):pt.co=(*value[:2],value[2]+meta['soil_height'],1);pt.radius=value[3]
 ob=bpy.data.objects.new(route['name'],curve);controls.objects.link(ob);ob.hide_render=True;ob.hide_set(True);ob['blend width']=route['blend'];ob['depth factor']=route['depth'];ob['radius stored on control points']=True
bm=bmesh.new();bm.from_mesh(me);bm.verts.ensure_lookup_table();seen=set();components=[]
for vertex in bm.verts:
 if vertex.index in seen:continue
 stack=[vertex];seen.add(vertex.index);count=0
 while stack:
  cur=stack.pop();count+=1
  for edge in cur.link_edges:
   nxt=edge.other_vert(cur)
   if nxt.index not in seen:seen.add(nxt.index);stack.append(nxt)
 components.append(count)
boundary=[v.co for e in bm.edges if e.is_boundary for v in e.verts]
inspection={'vertices':len(bm.verts),'faces':len(bm.faces),'components':sorted(components,reverse=True),'boundary_edges':sum(e.is_boundary for e in bm.edges),'nonmanifold_edges':sum(not e.is_manifold for e in bm.edges),'signed_volume':bm.calc_volume(signed=True),'boundary_z_range':[min(v.z for v in boundary),max(v.z for v in boundary)] if boundary else None};bm.free()
prefix.with_suffix('.inspection.json').write_text(json.dumps(inspection,indent=2))
assert inspection['boundary_edges']==0 and inspection['nonmanifold_edges']==0,inspection
assert len(components)==1,inspection
meta['inspection']=inspection
core['authoring_version']=meta['version'];core['construction']='one implicit wood volume'
for ob in bpy.context.scene.objects:ob.select_set(ob.type=='MESH')
bpy.context.view_layer.objects.active=core
bpy.ops.wm.save_as_mainfile(filepath=str(prefix.with_suffix('.blend')),compress=True)
if len(me.polygons)>140000:
 reduction=core.modifiers.new('Coarse runtime surface budget','DECIMATE');reduction.ratio=140000/len(me.polygons)
bpy.ops.export_scene.gltf(filepath=str(prefix.with_suffix('.glb')),export_format='GLB',use_selection=True,export_yup=True,export_normals=True,export_materials='EXPORT',export_apply=True,export_vertex_color='ACTIVE',export_all_vertex_colors=True,export_extras=True,export_draco_mesh_compression_enable=True,export_draco_mesh_compression_level=6,export_draco_position_quantization=16,export_draco_normal_quantization=10,export_draco_texcoord_quantization=12)
meta['glb_bytes']=prefix.with_suffix('.glb').stat().st_size;meta['assembly_seconds']=time.monotonic()-start;prefix.with_suffix('.json').write_text(json.dumps(meta,indent=2));shutil.copy2(__file__,prefix.parent/(prefix.name+'.assemble.py'));print(json.dumps({'inspection':inspection,'glb_bytes':meta['glb_bytes'],'seconds':meta['assembly_seconds']}))
