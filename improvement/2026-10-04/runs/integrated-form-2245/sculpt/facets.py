"""Authored broad deadwood planes; no holes, texture or periodic grooves."""
import bpy,bmesh,sys,json,math,argparse,shutil
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
p=argparse.ArgumentParser();p.add_argument('--base',default='form-v06');p.add_argument('--version',default='form-v07');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);run=Path(__file__).resolve().parents[1];src=json.loads((run/'models'/f'{a.base}.json').read_text());dest=run/'models'/a.version;assert not dest.with_suffix('.glb').exists();assert shutil.disk_usage(run).free>2*1024**3
bpy.ops.wm.open_mainfile(filepath=src['basis_native']);core=bpy.data.objects['Continuous aged trunk and primary branches'];me=bpy.data.meshes.new('Shared broad deadwood planes');me.from_pydata(src['control_vertices'],[],src['control_faces']);me.update();core.data=me;core.vertex_groups.clear();core.modifiers[0].levels=1;core.modifiers[0].render_levels=1
original=json.loads((run.parent/'anatomy-2150/models/cage-v06.json').read_text())['controls']['sections'];heights=src['controls'].get('main_heights',[p[0] for p in original]);centres=src['controls']['main_centres'];calibre=src['controls']['calibre'];soil=src['soil'];before=[list(v.co) for v in me.vertices]
def smooth(a,b,x):t=max(0,min(1,(x-a)/(b-a)));return t*t*(3-2*t)
def window(z,a,b,c,d):return smooth(a,b,z)*(1-smooth(c,d,z))
def guide(z):
 k=next((i for i in range(len(heights)-1) if heights[i+1]>=z),len(heights)-2);t=max(0,min(1,(z-heights[k])/(heights[k+1]-heights[k])));centre=Vector((*centres[k],0)).lerp(Vector((*centres[k+1],0)),t);rx=(original[k][3]*calibre[k][0])*(1-t)+(original[k+1][3]*calibre[k+1][0])*t;ry=(original[k][4]*calibre[k][1])*(1-t)+(original[k+1][4]*calibre[k+1][1])*t;return centre,rx,ry
planes=[{'name':'broad lower weathered face','z':[.13,.27,.41,.63],'angle':-1.93,'turn':.4,'offset_fraction':.61}, {'name':'short diagonal parent face','z':[.66,.79,.91,1.1],'angle':-1.78,'turn':-.24,'offset_fraction':.66}, {'name':'unequal lateral compression plane','z':[.28,.37,.45,.62],'angle':2.53,'turn':.15,'offset_fraction':.78}]
changed=0;max_edit=0
for v in me.vertices:
 z=v.co.z-soil
 if z<.13 or z>1.1:continue
 centre,rx,ry=guide(z);q=Vector((v.co.x-centre.x,v.co.y-centre.y,0));territory=1-smooth(1.02,1.42,math.sqrt((q.x/rx)**2+(q.y/ry)**2))
 if territory<=0:continue
 prev=v.co.copy()
 for plane in planes:
  weight=window(z,*plane['z'])*territory
  if weight<=0:continue
  angle=plane['angle']+plane['turn']*(z-plane['z'][1]);normal=Vector((math.cos(angle),math.sin(angle),0));support=math.sqrt((rx*normal.x)**2+(ry*normal.y)**2);depth=q.dot(normal)-support*plane['offset_fraction']
  if depth>0:
   # Move the connected surface toward an explicit broad plane, with a
   # changing boundary and blended ends; keep the rear/adjacent body.
   move=min(depth,.060)*weight;v.co-=normal*move;q-=normal*move
 # One unequal adjacent outer boss. It is a mass, not a line, and has no
 # repeated companion on the opposite side of the tree.
 angle=math.atan2(q.y,q.x);gap=(angle+2.68+math.pi)%math.tau-math.pi;boss=.030*window(z,.18,.29,.35,.53)*math.exp(-.5*(gap/.48)**2)*territory;v.co+=q.normalized()*boss
 if (v.co-prev).length>1e-6:changed+=1;max_edit=max(max_edit,(v.co-prev).length)
# Shorten the terminal hook into a blunt continuation inside its real crown.
for v in me.vertices:
 if v.co.z>soil+1.48 and v.co.x>.31:
  w=smooth(soil+1.48,soil+1.55,v.co.z);v.co.x+=.11*w;v.co.z-=.003*w
me.update();colors=me.color_attributes.new(name='Continuous growth masks',type='FLOAT_COLOR',domain='POINT');colors.data.foreach_set('color',[n for row in src['colors'] for n in row]);me.color_attributes.active_color=colors
uv=me.uv_layers.new(name='Coarse spatial coordinates')
for l in me.loops:p=me.vertices[l.vertex_index].co;uv.data[l.index].uv=(p.x,p.z)
for f in me.polygons:f.use_smooth=True
m=bpy.data.materials.new('Continuous wood growth');m.use_nodes=True;m.diffuse_color=(.43,.39,.31,1);me.materials.append(m)
for ob in bpy.context.scene.objects:
 if ob.type!='MESH' or ob==core:continue
 name='Unglazed ceramic' if ob.name.startswith(('Shallow','Low ceramic')) else 'Planted soil' if ob.name.startswith('Continuous planted') else 'Bedding stone';mat=bpy.data.materials.get(name) or bpy.data.materials.new(name);ob.data.materials.clear();ob.data.materials.append(mat)
core['authoring_version']=a.version;core['construction']='Shared cage with individually authored broad weathered planes; no detached vein, hole or fine grain'
bpy.context.view_layer.update();ev=core.evaluated_get(bpy.context.evaluated_depsgraph_get());e=ev.to_mesh();e.calc_loop_triangles();tri=[tuple(t.vertices) for t in e.loop_triangles];tree=BVHTree.FromPolygons([v.co for v in e.vertices],tri,all_triangles=True,epsilon=1e-9);intersections=[(i,j) for i,j in tree.overlap(tree) if i<j and not set(tri[i]).intersection(tri[j])];bm=bmesh.new();bm.from_mesh(e);inspection={'control_vertices':len(me.vertices),'control_faces':len(me.polygons),'evaluated_vertices':len(e.vertices),'triangles':len(tri),'volume':bm.calc_volume(signed=True),'boundary_edges':sum(x.is_boundary for x in bm.edges),'nonmanifold_edges':sum(not x.is_manifold for x in bm.edges),'nonadjacent_intersections':len(intersections),'maximum_plane_edit':max_edit,'edited_vertices':changed,'retained_volume_vs_form_v06':bm.calc_volume(signed=True)/src['inspection']['volume']};bm.free();ev.to_mesh_clear();assert not intersections and inspection['boundary_edges']==0 and inspection['nonmanifold_edges']==0 and inspection['retained_volume_vs_form_v06']>.90,inspection
meta={**src,'version':a.version,'basis':a.base,'control_vertices':[list(v.co) for v in me.vertices],'control_faces':[list(f.vertices) for f in me.polygons],'inspection':inspection,'broad_planes':planes,'before_broad_planes':before};meta.pop('before_major_planes',None)
for centre,height in zip(meta['controls']['main_centres'],meta['controls']['main_heights']):
 if height>1.48 and centre[0]>.31:centre[0]+=.11*smooth(1.48,1.55,height)
meta['terminal_design']='Forward continuing blunt tip; no reverse horizontal motion at apex';dest.with_suffix('.json').write_text(json.dumps(meta,indent=2)+'\n')
for ob in bpy.context.scene.objects:ob.select_set(ob.type=='MESH')
bpy.context.view_layer.objects.active=core;bpy.ops.export_scene.gltf(filepath=str(dest.with_suffix('.glb')),export_format='GLB',use_selection=True,export_apply=True,export_yup=True,export_normals=True,export_materials='EXPORT',export_vertex_color='ACTIVE',export_extras=True,export_draco_mesh_compression_enable=False);print(json.dumps({'version':a.version,'inspection':inspection}),flush=True)
