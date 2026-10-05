"""Individually authored broad wood-loss faces on the intact shared volume."""
import bpy,bmesh,sys,json,math,argparse,shutil
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
p=argparse.ArgumentParser();p.add_argument('--base',default='form-v09');p.add_argument('--version',default='form-v10');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);run=Path(__file__).resolve().parents[1];src=json.loads((run/'models'/f'{a.base}.json').read_text());dest=run/'models'/a.version;assert not dest.with_suffix('.glb').exists();assert shutil.disk_usage(run).free>2*1024**3
bpy.ops.wm.open_mainfile(filepath=src['basis_native']);core=bpy.data.objects['Continuous aged trunk and primary branches'];me=bpy.data.meshes.new('Editable hand-authored broad loss faces');me.from_pydata(src['control_vertices'],[],src['control_faces']);me.update();core.data=me;core.vertex_groups.clear()
for f in me.polygons:f.use_smooth=True
color=me.color_attributes.new(name='Continuous growth masks',type='FLOAT_COLOR',domain='POINT');color.data.foreach_set('color',[v for c in src['colors'] for v in c]);me.color_attributes.active_color=color
attr=me.attributes.new('parent influence','FLOAT','POINT');main={i for row in src['parent_rings'] for i in row if i is not None};attr.data.foreach_set('value',[1. if i in main else 0. for i in range(len(me.vertices))])
bpy.context.view_layer.objects.active=core;core.select_set(True);core.modifiers[0].levels=2;bpy.ops.object.modifier_apply(modifier=core.modifiers[0].name);me=core.data;me.update();before=[list(v.co) for v in me.vertices];influence=me.attributes['parent influence'];soil=src['soil'];control=src['controls'];centres=control['main_centres'];heights=control['main_heights']
def smooth(a,b,x):t=max(0,min(1,(x-a)/(b-a)));return t*t*(3-2*t)
def guide(z):
 k=next((i for i in range(len(heights)-1) if heights[i+1]>=z),len(heights)-2);u=max(0,min(1,(z-heights[k])/(heights[k+1]-heights[k])));return Vector((*centres[k],0)).lerp(Vector((*centres[k+1],0)),u)
def delta(a,b):return (a-b+math.pi)%math.tau-math.pi
faces=[
{'name':'lower left broad loss','path':[[.14,-2.62],[.28,-2.50],[.41,-2.20],[.50,-1.94]],'width':[.23,.36],'depth':.025,'lip':.005},
{'name':'lower front short spall','path':[[.085,-1.65],[.20,-1.73],[.34,-1.52],[.43,-1.30]],'width':[.25,.18],'depth':.023,'lip':.003},
{'name':'small inner worn plane','path':[[.21,-1.02],[.30,-1.10],[.40,-1.30],[.51,-1.2]],'width':[.21,.16],'depth':.012,'lip':0},
{'name':'lower curl face','path':[[.42,-2.22],[.58,-2.0],[.68,-1.76],[.76,-1.65]],'width':[.38,.27],'depth':.030,'lip':.004},
{'name':'outside shoulder loss','path':[[.63,-2.66],[.8,-2.60],[.96,-2.2],[1.03,-1.88]],'width':[.23,.32],'depth':.024,'lip':.004},
{'name':'upper diagonal face','path':[[.83,-1.45],[.93,-1.65],[1.1,-1.88],[1.22,-2.05]],'width':[.32,.24],'depth':.023,'lip':.003},
{'name':'short upper worn face','path':[[1.16,-1.25],[1.28,-1.32],[1.40,-1.03]],'width':[.32,.20],'depth':.017,'lip':0},
{'name':'rear base loss','path':[[.13,1.8],[.30,1.96],[.53,1.7]],'width':[.38,.28],'depth':.022,'lip':.004},
{'name':'rear shoulder loss','path':[[.54,2.2],[.8,1.8],[.98,1.95]],'width':[.29,.37],'depth':.019,'lip':0}]
max_edit=0;edits=0
for vertex in me.vertices:
 z=vertex.co.z-soil;w=influence.data[vertex.index].value
 if z<.075 or w<.03:continue
 centre=guide(z);radial=Vector((vertex.co.x-centre.x,vertex.co.y-centre.y,0));radius=radial.length
 if radius<.04:continue
 angle=math.atan2(radial.y,radial.x);amount=0
 for face in faces:
  path=face['path'];z0=path[0][0];z1=path[-1][0]
  if not z0<z<z1:continue
  index=next(i for i in range(len(path)-1) if path[i+1][0]>=z);u=(z-path[index][0])/(path[index+1][0]-path[index][0]);u=u*u*(3-2*u);axis=path[index][1]*(1-u)+path[index+1][1]*u;t=(z-z0)/(z1-z0);width=face['width'][0]*(1-t)+face['width'][1]*t;across=delta(angle,axis)/width
  if abs(across)>1.6:continue
  end=smooth(0,.17,t)*(1-smooth(.73,1,t));basin=max(0,1-abs(across)**1.5)**1.25;lip=math.exp(-((across-.95)/.29)**2)*face['lip'];amount+=(lip-face['depth']*basin)*end
 # A pair of differently sized broad retained shoulders, not repeating ribs.
 amount+=.012*math.exp(-((z-.36)/.10)**2-(delta(angle,-2.77)/.39)**2)+.010*math.exp(-((z-.99)/.09)**2-(delta(angle,-2.33)/.51)**2)
 amount=max(-radius*.14,min(radius*.10,amount))*w
 if abs(amount)>1e-6:vertex.co+=radial.normalized()*amount;edits+=1;max_edit=max(max_edit,abs(amount))
me.update();sub=core.modifiers.new('Unapplied surface interpolation','SUBSURF');sub.levels=1;sub.render_levels=1
uv=me.uv_layers.new(name='Coarse spatial coordinates')
for l in me.loops:p=me.vertices[l.vertex_index].co;uv.data[l.index].uv=(p.x,p.z)
mat=bpy.data.materials.new('Continuous wood growth');mat.use_nodes=True;mat.diffuse_color=(.43,.39,.31,1);me.materials.append(mat)
for ob in bpy.context.scene.objects:
 if ob.type!='MESH' or ob==core:continue
 name='Unglazed ceramic' if ob.name.startswith(('Shallow','Low ceramic')) else 'Planted soil' if ob.name.startswith('Continuous planted') else 'Bedding stone';m=bpy.data.materials.get(name) or bpy.data.materials.new(name);ob.data.materials.clear();ob.data.materials.append(m)
core['authoring_version']=a.version;core['construction']='One shared volume, nine individually authored large loss faces, no periodic grain, no new holes'
bpy.context.view_layer.update();ev=core.evaluated_get(bpy.context.evaluated_depsgraph_get());e=ev.to_mesh();e.calc_loop_triangles();tri=[tuple(t.vertices) for t in e.loop_triangles];tree=BVHTree.FromPolygons([v.co for v in e.vertices],tri,all_triangles=True,epsilon=1e-9);cross=[(i,j) for i,j in tree.overlap(tree) if i<j and not set(tri[i]).intersection(tri[j])];bm=bmesh.new();bm.from_mesh(e);inspection={'control_vertices':len(me.vertices),'control_faces':len(me.polygons),'evaluated_vertices':len(e.vertices),'triangles':len(tri),'volume':bm.calc_volume(signed=True),'boundary_edges':sum(x.is_boundary for x in bm.edges),'nonmanifold_edges':sum(not x.is_manifold for x in bm.edges),'nonadjacent_intersections':len(cross),'maximum_surface_edit':max_edit,'edited_vertices':edits,'retained_volume_vs_form_v09':bm.calc_volume(signed=True)/src['inspection']['volume']};bm.free();ev.to_mesh_clear();assert not cross and inspection['boundary_edges']==0 and inspection['nonmanifold_edges']==0 and inspection['retained_volume_vs_form_v09']>.93,inspection
meta={**src,'version':a.version,'basis':a.base,'subdivision':1,'control_vertices':[list(v.co) for v in me.vertices],'control_faces':[list(f.vertices) for f in me.polygons],'colors':[list(c.color) for c in me.color_attributes.active_color.data],'before_spalls':before,'loss_faces':faces,'inspection':inspection};meta.pop('parent_rings',None);dest.with_suffix('.json').write_text(json.dumps(meta,indent=2)+'\n')
for ob in bpy.context.scene.objects:ob.select_set(ob.type=='MESH')
bpy.context.view_layer.objects.active=core;bpy.ops.export_scene.gltf(filepath=str(dest.with_suffix('.glb')),export_format='GLB',use_selection=True,export_apply=True,export_yup=True,export_normals=True,export_materials='EXPORT',export_vertex_color='ACTIVE',export_extras=True,export_draco_mesh_compression_enable=False);print(json.dumps({'version':a.version,'inspection':inspection}),flush=True)
