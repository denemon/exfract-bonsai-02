"""Check the actual subdivided solid for non-adjacent intersections and thickness."""
import bpy,json,sys,argparse,math
from pathlib import Path
from mathutils.bvhtree import BVHTree
p=argparse.ArgumentParser();p.add_argument('candidate');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);base=Path(a.candidate);meta=json.loads(base.with_suffix('.json').read_text())
mesh=bpy.data.meshes.new('Verification only');mesh.from_pydata(meta['control_vertices'],[],meta['control_faces']);mesh.update();o=bpy.data.objects.new('Verification only',mesh);bpy.context.collection.objects.link(o);sub=o.modifiers.new('Subdivision','SUBSURF');sub.levels=meta['controls']['subdivision'];evaluated=o.evaluated_get(bpy.context.evaluated_depsgraph_get());me=evaluated.to_mesh();me.calc_loop_triangles();positions=[v.co.copy() for v in me.vertices];triangles=[tuple(t.vertices) for t in me.loop_triangles];tree=BVHTree.FromPolygons(positions,triangles,all_triangles=True,epsilon=1e-9);contacts=[]
for i,j in tree.overlap(tree):
 if i<j and set(triangles[i]).isdisjoint(triangles[j]):contacts.append((i,j))
sections=[]
for level in [.02,.10,.20,.30,.40,.50]:
 z=meta['controls']['soil']+level;crossings=[]
 for tri in triangles:
  vs=[positions[i] for i in tri]
  for v,w in zip(vs,vs[1:]+vs[:1]):
   if (v.z<z<w.z) or (w.z<z<v.z):crossings.append(v+(w-v)*((z-v.z)/(w.z-v.z)))
 if crossings:
  width=max(p.x for p in crossings)-min(p.x for p in crossings);depth=max(p.y for p in crossings)-min(p.y for p in crossings);sections.append({'height_above_soil':level,'width':width,'depth':depth,'depth_over_width':depth/width})
result={'version':meta['version'],'evaluated_triangle_count':len(triangles),'nonadjacent_surface_intersections':len(contacts),'intersection_pairs_first10':contacts[:10],'measured_lower_sections':sections,'method':'Blender BVHTree self-overlap excluding triangles sharing any vertex, epsilon 1e-9; exact mesh/height-plane intersections for width/depth'}
base.with_suffix('.solid-check.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result),flush=True);evaluated.to_mesh_clear();assert not contacts,'Non-adjacent intersections require inspection'
