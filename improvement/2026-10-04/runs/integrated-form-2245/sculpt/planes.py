"""Broad, nonperiodic weathering on a subdivided shared cage. No texture."""
import bpy,bmesh,sys,json,math,argparse,shutil
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
p=argparse.ArgumentParser();p.add_argument('--base',default='form-v01');p.add_argument('--version',default='form-v02');p.add_argument('--amount',type=float,default=1);a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);r=Path(__file__).resolve().parents[1];src=json.loads((r/'models'/f'{a.base}.json').read_text());dest=r/'models'/a.version;assert not dest.with_suffix('.glb').exists();assert shutil.disk_usage(r).free>2*1024**3
bpy.ops.wm.open_mainfile(filepath=src['basis_native']);core=bpy.data.objects['Continuous aged trunk and primary branches'];me=bpy.data.meshes.new('Continuous cage with authored major planes');me.from_pydata(src['control_vertices'],[],src['control_faces']);me.update();core.data=me;core.vertex_groups.clear()
mat=bpy.data.materials.new('Continuous wood growth');mat.use_nodes=True;mat.diffuse_color=(.43,.39,.31,1);bs=mat.node_tree.nodes.get('Principled BSDF');bs.inputs['Roughness'].default_value=.93;bs.inputs['Base Color'].default_value=(.43,.39,.31,1);me.materials.append(mat)
col=me.color_attributes.new(name='Continuous growth masks',type='FLOAT_COLOR',domain='POINT');col.data.foreach_set('color',[v for x in src['colors'] for v in x]);me.color_attributes.active_color=col
main=me.attributes.new('parent influence','FLOAT','POINT');ids={i for ring in src['parent_rings'] for i in ring if i is not None};main.data.foreach_set('value',[1. if i in ids else 0. for i in range(len(me.vertices))]);
for f in me.polygons:f.use_smooth=True
bpy.context.view_layer.objects.active=core;core.select_set(True);core.modifiers[0].levels=1;bpy.ops.object.modifier_apply(modifier=core.modifiers[0].name);me=core.data;me.update();before=[list(v.co) for v in me.vertices]
def smooth(a,b,x):t=max(0,min(1,(x-a)/(b-a)));return t*t*(3-2*t)
def delta(a,b):return (a-b+math.pi)%(2*math.pi)-math.pi
def window(z,start,peak,end):return smooth(start,peak,z)*(1-smooth(peak,end,z))
original=json.loads((r.parent/'anatomy-2150/models/cage-v06.json').read_text())['controls']['sections'];centres=src['controls']['main_centres'];soil=src['soil']
if 'main_heights' in src['controls']:
 for row,height in zip(original,src['controls']['main_heights']):row[0]=height
def guide(z):
 k=next((i for i in range(len(original)-1) if original[i+1][0]>=z),len(original)-2);t=max(0,min(1,(z-original[k][0])/(original[k+1][0]-original[k][0])));return (Vector((*centres[k],0)).lerp(Vector((*centres[k+1],0)),t))
# Shorter and offset major channels end at different heights. Their lateral
# width and depth are authored independently. They do not cut holes or the
# main rear support; there is no repeated groove texture.
planes=[{'name':'root front cleft','start':.055,'peak':.31,'end':.68,'angle0':-1.64,'turn':-.58,'width0':.42,'width1':.54,'depth':.094},
{'name':'left root broad worn face','start':.10,'peak':.36,'end':.79,'angle0':-2.62,'turn':.18,'width0':.45,'width1':.34,'depth':.047},
{'name':'short shoulder hollow','start':.62,'peak':.88,'end':1.12,'angle0':-1.78,'turn':.4,'width0':.55,'width1':.70,'depth':.027},
{'name':'upper small worn hollow','start':1.02,'peak':1.28,'end':1.61,'angle0':-2.35,'turn':.58,'width0':.33,'width1':.25,'depth':.035},
{'name':'rear compression face','start':.2,'peak':.7,'end':1.22,'angle0':1.72,'turn':-.5,'width0':.54,'width1':.40,'depth':.041}]
influence=me.attributes.get('parent influence');colors=me.color_attributes.active_color;max_indent=0
for v in me.vertices:
 w=influence.data[v.index].value;z=v.co.z-soil
 if w<.01 or z<.055:continue
 centre=guide(z);off=Vector((v.co.x-centre.x,v.co.y-centre.y,0));radius=off.length
 if radius<.025:continue
 theta=math.atan2(off.y,off.x);indent=0
 for p in planes:
  t=max(0,min(1,(z-p['start'])/(p['end']-p['start'])));angle=p['angle0']+p['turn']*(t*t*(3-2*t));width=p['width0']*(1-t)+p['width1']*t;indent+=p['depth']*window(z,p['start'],p['peak'],p['end'])*math.exp(-.5*(delta(theta,angle)/width)**2)
 # Preserve every root perimeter vertex and bound inward removal to <26% of
 # local radius. A flatter weathered side still has a thick uncut rear body.
 indent=min(indent*a.amount,radius*.255)*w;max_indent=max(max_indent,indent);v.co-=off.normalized()*indent
 # A short surviving lip follows the diagonal shoulder without becoming a
 # detached strip: this moves the exact same connected surface outward.
 lip=0.*window(z,.50,.82,1.13)*math.exp(-.5*(delta(theta,-2.32+.70*(z-.5))/.25)**2)*w*a.amount;v.co+=off.normalized()*lip
 colors.data[v.index].color[2]=max(.15,min(.75,colors.data[v.index].color[2]-indent*2.2))
me.update();sub=core.modifiers.new('Editable major-plane interpolation','SUBSURF');sub.levels=1;sub.render_levels=1
for ob in bpy.context.scene.objects:
 if ob.type!='MESH' or ob==core:continue
 name='Unglazed ceramic' if ob.name.startswith(('Shallow','Low ceramic')) else 'Planted soil' if ob.name.startswith('Continuous planted') else 'Bedding stone';m=bpy.data.materials.get(name) or bpy.data.materials.new(name);ob.data.materials.clear();ob.data.materials.append(m)
uv=me.uv_layers.new(name='Coarse spatial coordinates')
for l in me.loops:p=me.vertices[l.vertex_index].co;uv.data[l.index].uv=(p.x,p.z)
core['authoring_version']=a.version;core['construction']='One connected edited cage; bounded nonperiodic major-plane shaping; no fine grain or detached living tissue';core['no_fine_grain']=True
bpy.context.view_layer.update();ev=core.evaluated_get(bpy.context.evaluated_depsgraph_get());e=ev.to_mesh();e.calc_loop_triangles();tri=[tuple(t.vertices) for t in e.loop_triangles];tree=BVHTree.FromPolygons([v.co for v in e.vertices],tri,all_triangles=True,epsilon=1e-9);pairs=[(i,j) for i,j in tree.overlap(tree) if i<j and not set(tri[i]).intersection(tri[j])];bm=bmesh.new();bm.from_mesh(e);inspection={'control_vertices':len(me.vertices),'control_faces':len(me.polygons),'evaluated_vertices':len(e.vertices),'triangles':len(tri),'volume':bm.calc_volume(signed=True),'boundary_edges':sum(x.is_boundary for x in bm.edges),'nonmanifold_edges':sum(not x.is_manifold for x in bm.edges),'nonadjacent_intersections':len(pairs),'maximum_indent':max_indent,'retained_volume_fraction_vs_form_v01':bm.calc_volume(signed=True)/src['inspection']['volume']};bm.free();ev.to_mesh_clear();assert not pairs and inspection['boundary_edges']==0 and inspection['nonmanifold_edges']==0 and inspection['retained_volume_fraction_vs_form_v01']>.85,inspection
meta={'version':a.version,'basis':a.base,'basis_native':src['basis_native'],'controls':src['controls'],'soil':soil,'branches':src['branches'],'subdivision':1,'control_vertices':[list(v.co) for v in me.vertices],'control_faces':[list(f.vertices) for f in me.polygons],'colors':[list(c.color) for c in colors.data],'before_major_planes':before,'planes':planes,'amount':a.amount,'inspection':inspection};dest.with_suffix('.json').write_text(json.dumps(meta,indent=2)+'\n')
for ob in bpy.context.scene.objects:ob.select_set(ob.type=='MESH')
bpy.ops.export_scene.gltf(filepath=str(dest.with_suffix('.glb')),export_format='GLB',use_selection=True,export_apply=True,export_yup=True,export_normals=True,export_materials='EXPORT',export_vertex_color='ACTIVE',export_extras=True,export_draco_mesh_compression_enable=False)
print(json.dumps({'version':a.version,'inspection':inspection,'glb_bytes':dest.with_suffix('.glb').stat().st_size}),flush=True)
