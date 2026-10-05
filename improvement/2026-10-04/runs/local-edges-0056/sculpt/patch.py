"""Locally reflow a bounded quad net and add an independently editable shoulder rail.

Boundary points, rear, root tips and branch attachments are fixed. This is a
small authored vertex net, not a radial field, repeated noise or a groove cut.
"""
import bpy,bmesh,math,json,sys,argparse,hashlib,collections,shutil
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
p=argparse.ArgumentParser();p.add_argument('--version',default='edge-v01');p.add_argument('--controls');args=p.parse_args(sys.argv[sys.argv.index('--')+1:])
RUN=Path(__file__).resolve().parents[1];BASIS=RUN.parent/'wood-surface-0000';out=RUN/'models'/args.version
assert not out.with_suffix('.glb').exists();assert shutil.disk_usage(RUN).free>2*1024**3
source=json.loads((BASIS/'models/wood-v02.json').read_text())
coarse=json.loads((RUN.parent/'integrated-form-2245/models/form-v05.json').read_text())
soil=.393;vertices=[Vector(v) for v in source['control_vertices']];faces=[list(f) for f in source['control_faces']]
neighbours=collections.defaultdict(set)
for f in faces:
    for i,a in enumerate(f):b=f[(i+1)%len(f)];neighbours[a].add(b);neighbours[b].add(a)
def midpoint(a,b):
    found=neighbours[a]&neighbours[b];assert len(found)==1,(a,b,found);return next(iter(found))
rings=coarse['parent_rings'];grid=[]
for ri in range(9):
    row=[];i=1+ri//2
    for ci in range(13):
        j=8+ci//2
        if not ri%2 and not ci%2:k=rings[i][j]
        elif not ri%2:k=midpoint(rings[i][j],rings[i][j+1])
        elif not ci%2:k=midpoint(rings[i][j],rings[i+1][j])
        else:
            found=neighbours[midpoint(rings[i][j],rings[i][j+1])]&neighbours[midpoint(rings[i+1][j],rings[i+1][j+1])]&neighbours[midpoint(rings[i][j],rings[i+1][j])]
            assert len(found)==1;k=next(iter(found))
        row.append(k)
    grid.append(row)
patch_keys={frozenset([grid[i][j],grid[i][j+1],grid[i+1][j+1],grid[i+1][j]]) for i in range(8) for j in range(12)}
assert len(patch_keys)==96 and sum(frozenset(f) in patch_keys for f in faces)==96
boundary={grid[i][j] for i in range(9) for j in range(13) if i in [0,8] or j in [0,12]}
patch_ids={k for row in grid for k in row};old=[v.copy() for v in vertices]

# Explicit, unequal edge columns follow the shoulder and broad growth face.
# Each row stores x/y/z controls for columns 3..10. The z staggering prevents
# the lower face termination from collecting into one horizontal shelf.
design={
 'description':'Bounded front net, independently authored shoulder/face/transition controls and a short added shoulder rail; fixed perimeter',
 'row_columns':[3,4,5,6,7,8,9,10],
 'rows':{
 '1':[[-.454,-.131,.108],[-.401,-.170,.098],[-.310,-.188,.081],[-.204,-.204,.072],[-.102,-.211,.070],[-.001,-.214,.075],[.103,-.212,.084],[.197,-.200,.097]],
 '2':[[-.323,-.151,.161],[-.272,-.190,.143],[-.211,-.199,.129],[-.135,-.211,.124],[-.048,-.222,.127],[.041,-.222,.136],[.116,-.208,.148],[.180,-.185,.158]],
 '3':[[-.211,-.190,.211],[-.171,-.222,.194],[-.130,-.224,.188],[-.079,-.236,.186],[-.018,-.236,.195],[.045,-.223,.208],[.102,-.196,.215],[.154,-.164,.214]],
 '4':[[-.135,-.221,.264],[-.113,-.245,.247],[-.090,-.246,.252],[-.041,-.249,.264],[.012,-.240,.279],[.061,-.219,.286],[.108,-.190,.279],[.140,-.158,.280]],
 '5':[[-.113,-.208,.328],[-.098,-.229,.320],[-.072,-.223,.329],[-.033,-.228,.345],[.012,-.219,.352],[.053,-.198,.350],[.091,-.176,.342],[.127,-.148,.338]],
 '6':[[-.118,-.169,.398],[-.103,-.191,.398],[-.078,-.188,.409],[-.039,-.191,.422],[.006,-.184,.426],[.049,-.168,.421],[.084,-.150,.413],[.117,-.130,.409]],
 '7':[[-.135,-.124,.469],[-.108,-.139,.470],[-.080,-.140,.482],[-.042,-.142,.486],[-.006,-.135,.483],[.025,-.120,.482],[.052,-.103,.479],[.084,-.088,.479]]
 },
 'shoulder_rail':{'2':[-.295,-.204,.152],'3':[-.193,-.233,.201],'4':[-.122,-.251,.255],'5':[-.105,-.238,.324],'6':[-.111,-.199,.398]},
 'shoulder_split_column':3,
 'section_heights_above_soil':[.12,.30,.54]
}
if args.controls:design=json.loads(Path(args.controls).read_text())
for ri,points in design['rows'].items():
    for col,point in zip(design['row_columns'],points):vertices[grid[int(ri)][col]]=Vector((point[0],point[1],point[2]+soil))
added={};parents={};colors=[list(v) for v in source['colors']]
for ri,point in design['shoulder_rail'].items():
    i=int(ri);a,b=grid[i][3],grid[i][4];k=len(vertices);vertices.append(Vector((point[0],point[1],point[2]+soil)));colors.append([(source['colors'][a][j]+source['colors'][b][j])*.5 for j in range(4)]);added[i]=k;parents[k]=[a,b]

# Split just six adjacent patch cells. The rail ends join diagonally at
# staggered rows; the two ends are triangles, not holes or detached patches.
face_keys={frozenset(f):i for i,f in enumerate(faces)};replacement={}
for ri in range(1,7):
    bl,br,tl,tr=grid[ri][3],grid[ri][4],grid[ri+1][3],grid[ri+1][4]
    idx=face_keys[frozenset([bl,br,tr,tl])]
    if ri==1:parts=[[bl,br,tr,added[2]],[bl,added[2],tl]]
    elif ri==6:parts=[[bl,added[6],tr,tl],[added[6],br,tr]]
    else:parts=[[bl,added[ri],added[ri+1],tl],[added[ri],br,tr,added[ri+1]]]
    replacement[idx]=parts
new_faces=[];new_layers={key:[] for key in ['flow_uv','branch_uv','metric_uv']};loop=0
for index,face in enumerate(faces):
    lookup={key:{v:source[key][loop+j] for j,v in enumerate(face)} for key in new_layers}
    for parts in [replacement.get(index,[face])]:
        for part in parts:
            new_faces.append(part)
            for key in new_layers:
                for v in part:
                    if v in lookup[key]:new_layers[key].append(lookup[key][v])
                    else:
                        a,b=parents[v];assert a in lookup[key] and b in lookup[key]
                        new_layers[key].append([(lookup[key][a][j]+lookup[key][b][j])*.5 for j in range(2)])
    loop+=len(face)
assert len(vertices)==2319 and len(new_faces)==2318
outside={i for i in range(len(old)) if i not in patch_ids};assert all(vertices[i]==old[i] for i in outside|boundary)

bpy.ops.wm.open_mainfile(filepath=str(BASIS/'models/wood-v02-editable.blend'))
core=bpy.data.objects['Continuous aged trunk and primary branches']
old_groups={g.name:{v.index:next((x.weight for x in v.groups if x.group==g.index),0.) for v in core.data.vertices} for g in core.vertex_groups}
def evaluated_geometry(obj):
    bpy.context.view_layer.update();e=obj.evaluated_get(bpy.context.evaluated_depsgraph_get());mesh=e.to_mesh();mesh.calc_loop_triangles();points=[v.co.copy() for v in mesh.vertices];tri=[tuple(t.vertices) for t in mesh.loop_triangles];e.to_mesh_clear();return points,tri
baseline_points,baseline_tri=evaluated_geometry(core)
mesh=bpy.data.meshes.new('Locally reflowed front control net');mesh.from_pydata(vertices,[],new_faces);mesh.update();core.data=mesh
for polygon in mesh.polygons:polygon.use_smooth=True
col=mesh.color_attributes.new(name='Continuous growth masks',type='FLOAT_COLOR',domain='POINT');col.data.foreach_set('color',[n for c in colors for n in c]);mesh.color_attributes.active_color=col
for name,key in [('Main growth surface','flow_uv'),('Branch growth surface','branch_uv'),('Collar transition and calibre','metric_uv')]:
    layer=mesh.uv_layers.new(name=name)
    for target,value in zip(layer.data,new_layers[key]):target.uv=value
crease=mesh.attributes.new('crease_edge','FLOAT','EDGE')
core.vertex_groups.clear()
for name,weights in old_groups.items():
    group=core.vertex_groups.new(name=name)
    for k,value in weights.items():
        if value:group.add([k],value,'REPLACE')
    for k,(a,b) in parents.items():
        value=(weights[a]+weights[b])*.5
        if value:group.add([k],value,'REPLACE')
for name,ids in [('LOCAL · fixed perimeter',boundary),('LOCAL · central broad face',{grid[r][c] for r in range(1,8) for c in range(5,9)}),('LOCAL · thick shoulder',set(added.values())|{grid[r][c] for r in range(1,8) for c in [3,4]}),('LOCAL · wide transition',{grid[r][c] for r in range(1,8) for c in [9,10,11]})]:core.vertex_groups.new(name=name).add(sorted(ids),1,'REPLACE')
material=bpy.data.materials.new('Continuous grey brown wood');material.use_nodes=True;bs=material.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(.16,.115,.077,1);bs.inputs['Roughness'].default_value=.94;mesh.materials.append(material)
core['authoring_version']=args.version;core['source_control_record']=str(out.with_suffix('.json'));core['construction']='Bounded lower-front control net reflow with a short five-vertex shoulder rail. Fixed perimeter/rear/root tips/branch attachments.';core['status']='Local edge-layout candidate; requires five clay views, three cross-sections and independent visual review'
points,tri=evaluated_geometry(core)
bm=bmesh.new();bm.from_mesh(mesh);bm.free()
e=core.evaluated_get(bpy.context.evaluated_depsgraph_get());surface=e.to_mesh();bm=bmesh.new();bm.from_mesh(surface);volume=bm.calc_volume(signed=True)
tree=BVHTree.FromPolygons(points,tri,all_triangles=True,epsilon=1e-9);intersections=sum(i<j and set(tri[i]).isdisjoint(tri[j]) for i,j in tree.overlap(tree))
inspection={'control_vertices':len(mesh.vertices),'control_faces':len(mesh.polygons),'evaluated_vertices':len(points),'evaluated_triangles':len(tri),'volume':volume,'volume_ratio':volume/source['inspection']['volume'],'boundary_edges':sum(e.is_boundary for e in bm.edges),'nonmanifold_edges':sum(not e.is_manifold for e in bm.edges),'nonadjacent_intersections':intersections,'fixed_boundary_count':len(boundary),'fixed_boundary_max_error':max((vertices[k]-old[k]).length for k in boundary),'outside_patch_max_error':max((vertices[k]-old[k]).length for k in outside),'edited_old_controls':sum((vertices[k]-old[k]).length>1e-7 for k in range(len(old))),'added_control_vertices':5,'new_shoulder_rail':list(added.values()),'max_position_edit':max((vertices[k]-old[k]).length for k in range(len(old))),'subdivision':1}
assert not intersections and not inspection['boundary_edges'] and not inspection['nonmanifold_edges'] and .94<inspection['volume_ratio']<1.08,inspection
bm.free();e.to_mesh_clear()
groups={g.name:[[v.index,x.weight] for v in mesh.vertices for x in v.groups if x.group==g.index] for g in core.vertex_groups}
record={'version':args.version,'basis_native':str(BASIS/'models/wood-v02-editable.blend'),'basis_sha256':hashlib.sha256((BASIS/'models/wood-v02-editable.blend').read_bytes()).hexdigest(),'design':design,'grid_vertex_ids':grid,'fixed_boundary_ids':sorted(boundary),'outside_patch_ids':sorted(outside),'added_vertex_parents':parents,'control_vertices':[list(v.co) for v in mesh.vertices],'control_faces':[list(f.vertices) for f in mesh.polygons],'colors':[list(c.color) for c in col.data],**new_layers,'edge_creases':[v.value for v in crease.data],'vertex_groups':groups,'inspection':inspection}
out.with_suffix('.json').write_text(json.dumps(record,indent=2)+'\n');out.with_suffix('.controls.json').write_text(json.dumps(design,indent=2)+'\n')

# Slice perpendicular to the protected trunk growth centreline, not merely
# with horizontal world planes. Each result stores raw line intersections.
guide_source=json.loads((RUN.parent/'integrated-form-2245/models/form-v08.json').read_text())['controls'];heights=guide_source['main_heights'];centres=guide_source['main_centres']
def guide(z):
    k=next((i for i in range(len(heights)-1) if heights[i+1]>=z),len(heights)-2);t=max(0,min(1,(z-heights[k])/(heights[k+1]-heights[k])))
    return Vector((centres[k][0]*(1-t)+centres[k+1][0]*t,centres[k][1]*(1-t)+centres[k+1][1]*t,z+soil))
def slice_mesh(vertices,triangles,origin,normal,u,v):
    result=[]
    for face in triangles:
        ps=[vertices[k] for k in face];ds=[(p-origin).dot(normal) for p in ps];hits=[]
        for j in range(3):
            k=(j+1)%3
            if ds[j]*ds[k]<0:
                point=ps[j].lerp(ps[k],ds[j]/(ds[j]-ds[k]));q=point-origin;hits.append([q.dot(u),q.dot(v)])
        if len(hits)==2:result.append(hits)
    return result
sections=[]
for z in design['section_heights_above_soil']:
    origin=guide(z);normal=(guide(z+.015)-guide(z-.015)).normalized();u=Vector((1,0,0));u=(u-normal*u.dot(normal)).normalized();v=normal.cross(u)
    sections.append({'height_above_soil':z,'origin':list(origin),'normal':list(normal),'axis_x':list(u),'axis_y':list(v),'basis':slice_mesh(baseline_points,baseline_tri,origin,normal,u,v),'candidate':slice_mesh(points,tri,origin,normal,u,v)})
(RUN/'qa'/f'{args.version}-sections.json').write_text(json.dumps({'version':args.version,'basis':'wood-v02','method':'Intersection of evaluated triangle meshes with identical planes normal to the protected trunk centreline. Raw line segments; no smoothing or beautification.','sections':sections},indent=2)+'\n')
for obj in bpy.context.scene.objects:
    if obj.get('foliage_lod_template'):obj.hide_set(False);obj.hide_render=False
    obj.select_set(obj.type=='MESH' or obj.name=='Branch led scale foliage' or obj.name.startswith('Canopy spatial group'))
bpy.context.view_layer.objects.active=core
bpy.ops.export_scene.gltf(filepath=str(out.with_suffix('.glb')),export_format='GLB',use_selection=True,export_apply=True,export_yup=True,export_normals=True,export_materials='EXPORT',export_vertex_color='ACTIVE',export_all_vertex_colors=True,export_extras=True,export_gpu_instances=True,export_draco_mesh_compression_enable=True,export_draco_mesh_compression_level=6,export_draco_position_quantization=16,export_draco_normal_quantization=10,export_draco_texcoord_quantization=14)
print(json.dumps({'version':args.version,'inspection':inspection,'glb_bytes':out.with_suffix('.glb').stat().st_size}),flush=True)
