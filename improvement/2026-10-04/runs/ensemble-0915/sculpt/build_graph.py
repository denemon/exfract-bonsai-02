from pathlib import Path
import bpy,bmesh,json,sys,math,argparse
from mathutils import Vector
from mathutils.bvhtree import BVHTree
p=argparse.ArgumentParser();p.add_argument('--version',required=True);p.add_argument('--controls',type=Path,required=True);a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);R=Path(__file__).resolve().parents[1];d=json.loads(a.controls.read_text());out=R/'models'/a.version;assert not out.with_suffix('.glb').exists();bpy.ops.wm.read_factory_settings(use_empty=True)
verts=[];faces=[]
paths=[d['main_ids']]+[[p['base']]+p['points'] for p in d['paths']]
for pi,ids in enumerate(paths):
 rows=[d['points'][i] for i in ids];centers=[];radii=[]
 for j in range(len(rows)-1):
  A=rows[max(j-1,0)];B=rows[j];C=rows[j+1];D=rows[min(j+2,len(rows)-1)];n=max(3,math.ceil((Vector(B[:3])-Vector(C[:3])).length/.026))
  for k in range(n):
   t=k/n
   v=[.5*((2*B[c])+(-A[c]+C[c])*t+(2*A[c]-5*B[c]+4*C[c]-D[c])*t*t+(-A[c]+3*B[c]-3*C[c]+D[c])*t*t*t) for c in range(3)]
   centers.append(Vector(v));radii.append([B[c]*(1-t)+C[c]*t for c in [3,4]])
 centers.append(Vector(rows[-1][:3]));radii.append(rows[-1][3:]);start=len(verts);N=16
 for j,(center,radius) in enumerate(zip(centers,radii)):
  tangent=(centers[min(j+1,len(centers)-1)]-centers[max(0,j-1)]).normalized();x=tangent.cross(Vector((0,1,0))).normalized();y=tangent.cross(x).normalized();height=center.z
  for k in range(N):
   angle=math.tau*k/N;twist=height*1.5+pi*.7;grain=1+.085*math.sin(3*angle+twist)+.04*math.cos(5*angle-height*2)
   v=center+x*(radius[0]*math.cos(angle)*grain)+y*(radius[1]*math.sin(angle)*grain)
   verts.append(tuple(v))
 for j in range(len(centers)-1):
  for k in range(N): faces.append((start+j*N+k,start+j*N+(k+1)%N,start+(j+1)*N+(k+1)%N,start+(j+1)*N+k))
 faces.append(tuple(start+k for k in reversed(range(N))));faces.append(tuple(start+(len(centers)-1)*N+k for k in range(N)))
mesh=bpy.data.meshes.new('Joined authored variable contours');mesh.from_pydata(verts,[],faces);mesh.update();o=bpy.data.objects.new('Continuous aged trunk and primary branches',mesh);bpy.context.collection.objects.link(o);bpy.context.view_layer.objects.active=o;o.select_set(True)
# Build a single closed volume at junctions. The stored graph is the editable
# source, not the disconnected input contour shells. Skin failed its manifold gate.
rem=o.modifiers.new('Shared volume junction union','REMESH');rem.mode='VOXEL';rem.voxel_size=.0075;rem.use_smooth_shade=True;bpy.ops.object.modifier_apply(modifier=rem.name)
smooth=o.modifiers.new('Local volume interpolation','SMOOTH');smooth.factor=.60;smooth.iterations=3;bpy.ops.object.modifier_apply(modifier=smooth.name)
me=o.data;me.calc_loop_triangles();ratio=min(1,17500/len(me.loop_triangles));dec=o.modifiers.new('Structural surface budget','DECIMATE');dec.ratio=ratio;dec.use_collapse_triangulate=True;bpy.ops.object.modifier_apply(modifier=dec.name);control=o.data
for face in control.polygons:face.use_smooth=True
for name in ['Growth direction','Branch growth direction','Branch blend and calibre']:control.uv_layers.new(name=name)
color=control.color_attributes.new(name='Continuous growth masks',type='FLOAT_COLOR',domain='POINT')
for row in color.data:row.color=(.65,.15,.35,1)
for loop in control.loops:
 v=control.vertices[loop.vertex_index].co;uv=(math.atan2(v.y,v.x)/math.tau+.5,(v.z-.393))
 for layer in control.uv_layers:layer.data[loop.index].uv=uv if layer.name!='Branch blend and calibre'else(0,.4)
o['authoring_version']=a.version;o['construction']='New38-node graph; unequal twisted contours, volumetric shared junction union; six coupled crowns, structural gate';o['controls_source']=str(a.controls)
mat=bpy.data.materials.new('Continuous wood structural placeholder');mat.diffuse_color=(.23,.17,.12,1);control.materials.append(mat)
bpy.context.view_layer.update();control.calc_loop_triangles();tri=[tuple(t.vertices)for t in control.loop_triangles];bm=bmesh.new();bm.from_mesh(control);volume=bm.calc_volume(signed=True);boundary=sum(e.is_boundary for e in bm.edges);nonmanifold=sum(not e.is_manifold for e in bm.edges);bm.free();tree=BVHTree.FromPolygons([v.co.copy()for v in control.vertices],tri,all_triangles=True,epsilon=1e-8);intersections=sum(i<j and set(tri[i]).isdisjoint(tri[j])for i,j in tree.overlap(tree));bounds={'min':[min(v.co[k]for v in control.vertices)for k in range(3)],'max':[max(v.co[k]for v in control.vertices)for k in range(3)]}
inspection={'graph_vertices':len(d['points']),'graph_edges':len(d['edges']),'control_vertices':len(control.vertices),'control_faces':len(control.polygons),'subdivision_level':0,'evaluated_triangles':len(tri),'signed_volume':volume,'boundary_edges':boundary,'nonmanifold_edges':nonmanifold,'nonadjacent_intersections':intersections,'bounds_blender':bounds};assert boundary==nonmanifold==intersections==0 and volume>0 and len(tri)<=18540,inspection
record={'version':a.version,'construction':'Graph and variable contours with connected volumetric junctions, not old S-cage','controls':d,'control_positions':[list(v.co)for v in control.vertices],'control_faces':[list(f.vertices)for f in control.polygons],'inspection':inspection,'low_detail_only':True,'native_saved':False};out.with_suffix('.json').write_text(json.dumps(record,indent=2)+'\n')
bpy.ops.export_scene.gltf(filepath=str(out.with_suffix('.glb')),export_format='GLB',use_selection=True,export_apply=True,export_extras=True,export_vertex_color='ACTIVE',export_draco_mesh_compression_enable=True,export_draco_mesh_compression_level=6,export_draco_position_quantization=15,export_draco_normal_quantization=11,export_draco_texcoord_quantization=13)
print(json.dumps({'version':a.version,'inspection':inspection,'glb_bytes':out.with_suffix('.glb').stat().st_size}),flush=True)
