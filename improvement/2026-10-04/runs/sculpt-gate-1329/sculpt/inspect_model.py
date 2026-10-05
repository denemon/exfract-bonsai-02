"""Read-only Blender geometry inspection; writes a separate verification report."""
import bpy,bmesh,json,sys,argparse
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--out',required=True);opt=p.parse_args(sys.argv[sys.argv.index('--')+1:])
report={'file':bpy.data.filepath,'wood':{},'surfaces':[]}
wood=bpy.data.objects['Continuous aged trunk and primary branches'];bm=bmesh.new();bm.from_mesh(wood.data);bm.verts.ensure_lookup_table();seen=set();components=[]
for v in bm.verts:
 if v.index in seen:continue
 stack=[v];seen.add(v.index);size=0
 while stack:
  current=stack.pop();size+=1
  for edge in current.link_edges:
   other=edge.other_vert(current)
   if other.index not in seen:seen.add(other.index);stack.append(other)
 components.append(size)
report['wood']={'vertices':len(bm.verts),'faces':len(bm.faces),'components':sorted(components,reverse=True),'boundary_edges':sum(e.is_boundary for e in bm.edges),'non_manifold_edges':sum(not e.is_manifold for e in bm.edges),'signed_volume_m3':bm.calc_volume(signed=True),'uv_layers':[x.name for x in wood.data.uv_layers],'material_fields':[x.name for x in wood.data.color_attributes],'dimensions_m':list(wood.dimensions)};bm.free()
for obj in bpy.context.scene.objects:
 if obj.type!='MESH' or not any(x in obj.name for x in ['pot','bedding stone','ceramic foot']):continue
 bm=bmesh.new();bm.from_mesh(obj.data);report['surfaces'].append({'name':obj.name,'vertices':len(bm.verts),'boundary_edges':sum(e.is_boundary for e in bm.edges),'non_manifold_edges':sum(not e.is_manifold for e in bm.edges),'signed_volume_m3':bm.calc_volume(signed=True)});bm.free()
instances=[o for o in bpy.context.scene.objects if o.type=='MESH' and o.name.startswith('Branch led scale foliage ')]
report['foliage']={'instances':len(instances),'unique_meshes':len({o.data.name for o in instances}),'distribution':'Connected woody branch hierarchy; authored in foliage.py'}
Path(opt.out).write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
