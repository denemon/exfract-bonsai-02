"""Recover all three compact variants in memory without touching saved models."""
import bpy,bmesh,json,hashlib
from pathlib import Path
from mathutils.bvhtree import BVHTree
RUN=Path(__file__).resolve().parents[1]
results=[]
for path in sorted((RUN/'models').glob('wood-v[0-9][0-9].json')):
    d=json.loads(path.read_text());mesh=bpy.data.meshes.new('Candidate control recovery')
    mesh.from_pydata(d['control_vertices'],[],d['control_faces']);mesh.update()
    color=mesh.color_attributes.new(name='Continuous growth masks',type='FLOAT_COLOR',domain='POINT')
    color.data.foreach_set('color',[v for row in d['colors'] for v in row])
    crease=mesh.attributes.new('crease_edge','FLOAT','EDGE')
    for e,value in zip(crease.data,d['edge_creases']):e.value=value
    layers={}
    for key in ['flow_uv','branch_uv','metric_uv']:
        if key not in d:continue
        layer=mesh.uv_layers.new(name=key)
        assert len(layer.data)==len(d[key])
        for loop,value in zip(layer.data,d[key]):loop.uv=value
        layers[key]=len(layer.data)
    obj=bpy.data.objects.new('Candidate control recovery',mesh);bpy.context.collection.objects.link(obj)
    sub=obj.modifiers.new('Unapplied surface interpolation','SUBSURF');sub.levels=1;sub.render_levels=1
    ev=obj.evaluated_get(bpy.context.evaluated_depsgraph_get());surface=ev.to_mesh();surface.calc_loop_triangles()
    bm=bmesh.new();bm.from_mesh(surface)
    volume=bm.calc_volume(signed=True);boundary=sum(e.is_boundary for e in bm.edges);nonmanifold=sum(not e.is_manifold for e in bm.edges)
    tri=[tuple(t.vertices) for t in surface.loop_triangles]
    tree=BVHTree.FromPolygons([v.co.copy() for v in surface.vertices],tri,all_triangles=True,epsilon=1e-9)
    intersections=sum(i<j and set(tri[i]).isdisjoint(tri[j]) for i,j in tree.overlap(tree))
    neighbours=[set() for _ in surface.vertices]
    for e in surface.edges:a,b=e.vertices;neighbours[a].add(b);neighbours[b].add(a)
    remaining=set(range(len(neighbours)));components=[]
    while remaining:
        todo=[remaining.pop()];count=0
        while todo:
            k=todo.pop();count+=1;new=neighbours[k]&remaining;remaining.difference_update(new);todo.extend(new)
        components.append(count)
    expected=d['inspection']
    assert len(mesh.vertices)==expected['control_vertices'] and len(mesh.polygons)==expected['control_faces']
    assert len(surface.vertices)==expected['evaluated_vertices'] and len(tri)==expected['evaluated_triangles']
    assert abs(volume-expected['volume'])<1e-7 and boundary==nonmanifold==intersections==0 and len(components)==1
    results.append({'record':str(path.relative_to(RUN)),'record_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'restored':True,'control_vertices':len(mesh.vertices),'control_faces':len(mesh.polygons),'uv_layers':layers,'subdivision':1,'evaluated_vertices':len(surface.vertices),'evaluated_triangles':len(tri),'volume':volume,'volume_error':abs(volume-expected['volume']),'components':components,'boundary_edges':boundary,'nonmanifold_edges':nonmanifold,'nonadjacent_intersections':intersections})
    bm.free();ev.to_mesh_clear();bpy.data.objects.remove(obj,do_unlink=True);bpy.data.meshes.remove(mesh)
assert len(results)==3
(RUN/'qa/compact-restore.json').write_text(json.dumps({'passed':True,'method':'Restore positions, faces, surface colors, all UV loops and edge crease weights. Evaluate subdivision 1; verify recorded volume/counts, single closed manifold component and nonadjacent triangle BVH intersections. No saved native is modified.','records':results},indent=2)+'\n')
print(json.dumps(results),flush=True)
