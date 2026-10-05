"""Recover compact candidate controls in memory; never alter saved geometry."""
import bpy, bmesh, json, hashlib
from pathlib import Path
from mathutils.bvhtree import BVHTree

RUN=Path('/Users/kazuki.tanaka/dev0/exfract-bonsai-02/improvement/2026-10-04/runs/integrated-form-2245')
results=[]
for source in sorted((RUN/'models').glob('form-v[0-9][0-9].json')):
    d=json.loads(source.read_text())
    assert len(d['control_vertices'])==len(d['colors'])
    level=d.get('subdivision',2 if len(d['control_vertices'])<1000 else 1)
    mesh=bpy.data.meshes.new('Read-only compact recovery')
    mesh.from_pydata(d['control_vertices'],[],d['control_faces']);mesh.update()
    colors=mesh.color_attributes.new(name='Continuous growth masks',type='FLOAT_COLOR',domain='POINT')
    colors.data.foreach_set('color',[value for color in d['colors'] for value in color])
    obj=bpy.data.objects.new('Read-only compact recovery',mesh);bpy.context.collection.objects.link(obj)
    sub=obj.modifiers.new('Unapplied shared subdivision','SUBSURF');sub.levels=level;sub.render_levels=level
    evaluated=obj.evaluated_get(bpy.context.evaluated_depsgraph_get());surface=evaluated.to_mesh();surface.calc_loop_triangles()
    bm=bmesh.new();bm.from_mesh(surface)
    volume=bm.calc_volume(signed=True)
    boundary=sum(edge.is_boundary for edge in bm.edges)
    nonmanifold=sum(not edge.is_manifold for edge in bm.edges)
    positions=[v.co.copy() for v in surface.vertices];triangles=[tuple(t.vertices) for t in surface.loop_triangles]
    tree=BVHTree.FromPolygons(positions,triangles,all_triangles=True,epsilon=1e-9)
    intersections=sum(i<j and set(triangles[i]).isdisjoint(triangles[j]) for i,j in tree.overlap(tree))
    neighbours=[set() for _ in positions]
    for edge in surface.edges:
        a,b=edge.vertices;neighbours[a].add(b);neighbours[b].add(a)
    remaining=set(range(len(positions)));components=[]
    while remaining:
        todo=[remaining.pop()];count=0
        while todo:
            k=todo.pop();count+=1;new=neighbours[k]&remaining;remaining.difference_update(new);todo.extend(new)
        components.append(count)
    recorded=d['inspection']
    assert len(mesh.vertices)==recorded['control_vertices']
    assert len(mesh.polygons)==recorded['control_faces']
    assert len(positions)==recorded['evaluated_vertices']
    assert len(triangles)==recorded['triangles']
    assert abs(volume-recorded['volume'])<1e-7
    assert boundary==nonmanifold==intersections==0 and len(components)==1
    row={'record':str(source.relative_to(RUN)),'sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'control_vertices':len(mesh.vertices),'control_faces':len(mesh.polygons),'unapplied_subdivision':level,'evaluated_vertices':len(positions),'evaluated_triangles':len(triangles),'volume':volume,'volume_error':abs(volume-recorded['volume']),'components':components,'boundary_edges':boundary,'nonmanifold_edges':nonmanifold,'nonadjacent_intersections':intersections,'restored':True}
    results.append(row);print(json.dumps(row),flush=True)
    bm.free();evaluated.to_mesh_clear();bpy.data.objects.remove(obj,do_unlink=True);bpy.data.meshes.remove(mesh)
assert len(results)==10
report={'method':'Recreate control vertices/faces/colors from each JSON, apply its recorded Catmull-Clark evaluation in memory, compare volumes and counts, test edge manifoldness, components and BVH self-overlap excluding triangles sharing vertices. No native file is written.','passed':True,'records':results}
(RUN/'qa/compact-restore.json').write_text(json.dumps(report,indent=2)+'\n')
