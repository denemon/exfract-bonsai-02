"""Branch → twig → volumetric scale-shoot canopy. No filled leaf balls or cards."""
import numpy as np
from mathutils import Quaternion

def simple_material(name,colour):
 m=bpy.data.materials.new(name);m.diffuse_color=(*colour,1);m.use_nodes=True;bs=next(n for n in m.node_tree.nodes if n.type=='BSDF_PRINCIPLED');bs.inputs['Base Color'].default_value=(*colour,1);bs.inputs['Roughness'].default_value=.86;return m
LEAF=simple_material('Living scale foliage',(.08,.16,.035));TWIG=simple_material('Living twig bark',(.16,.09,.035))
foliage_group=bpy.data.objects.new('Branch led scale foliage',None);bpy.context.collection.objects.link(foliage_group)

def make_mesh(name,vertices,faces,mat,colours=None,smooth_faces=None):
 mesh=bpy.data.meshes.new(name);mesh.from_pydata(vertices,[],faces);mesh.update();mesh.materials.append(mat)
 if colours:
  attr=mesh.color_attributes.new(name='Growth masks',type='FLOAT_COLOR',domain='POINT');attr.data.foreach_set('color',[value for row in colours for value in row])
 uv=mesh.uv_layers.new(name='Growth UV')
 for loop in mesh.loops:
  p=mesh.vertices[loop.vertex_index].co;uv.data[loop.index].uv=(p.x,p.z)
 if smooth_faces:
  for face,sm in zip(mesh.polygons,smooth_faces):face.use_smooth=sm
 bm=bmesh.new();bm.from_mesh(mesh);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(mesh);bm.free();mesh.update();return mesh

def tube(vertices,faces,coords,radii,sides=5,colours=None,smooth_faces=None):
 start=len(vertices)
 for j,point in enumerate(coords):
  point=Vector(point);t=(Vector(coords[min(j+1,len(coords)-1)])-Vector(coords[max(j-1,0)])).normalized();n=t.cross(Vector((0,1,0)))
  if n.length<.1:n=t.cross(Vector((1,0,0)))
  n.normalize();b=t.cross(n).normalized()
  for k in range(sides):
   angle=k/sides*math.tau;vertices.append(tuple(point+(n*math.cos(angle)+b*math.sin(angle))*radii[j]))
   if colours:colours.append((.27,.16+j/len(coords)*.35,.5,1))
  if j:
   for k in range(sides):
    faces.append((start+(j-1)*sides+k,start+(j-1)*sides+(k+1)%sides,start+j*sides+(k+1)%sides,start+j*sides+k))
    if smooth_faces is not None:smooth_faces.append(True)
 faces.append(tuple(start+k for k in range(sides-1,-1,-1)));faces.append(tuple(start+(len(coords)-1)*sides+k for k in range(sides)))
 if smooth_faces is not None:smooth_faces.extend([False,False])

prototypes=[];prototype_info=[]
for variant in range(12):
 rng=random.Random(991+variant*313);v=[];f=[];col=[];sm=[];axes=[]
 main=[Vector((math.sin(k*.9+variant)*.015,math.cos(k*.8+variant)*.022,k/5)) for k in range(6)]
 tube(v,f,main,[.024*(1-k/6)*.8 for k in range(6)],4,col,sm);axes.append((main,5))
 for level,z in enumerate([.19,.37,.55,.73]):
  phase=level*1.16+rng.uniform(-.25,.25)+variant*.43
  for side in [0,1]:
   angle=phase+side*math.pi+rng.uniform(-.3,.3);length=(1-z)*rng.uniform(.41,.60);base=Vector((0,0,z));radial=Vector((math.cos(angle),math.sin(angle),0));tip=base+radial*length*.80+Vector((0,0,length*.68))
   bend=base.lerp(tip,.52)+Vector((rng.uniform(-.015,.015),rng.uniform(-.015,.015),.028));axis=[base,bend,tip]
   tube(v,f,axis,[.016*(1-z*.5),.010,.003],4,col,sm);axes.append((axis,3))
 leaf_count=0
 for axis,rows in axes:
  for row in range(rows):
   t=(row+.6)/(rows+.35);q=t*(len(axis)-1);j=min(len(axis)-2,int(q));u=q-j;point=axis[j].lerp(axis[j+1],u);tangent=(axis[j+1]-axis[j]).normalized();n=tangent.cross(Vector((0,1,0)))
   if n.length<.1:n=tangent.cross(Vector((1,0,0)))
   n.normalize();b=tangent.cross(n).normalized();phase=row*1.38+variant*.47
   for k in range(4):
    angle=phase+k*math.pi/2+rng.uniform(-.12,.12);radial=n*math.cos(angle)+b*math.sin(angle);side=tangent.cross(radial).normalized();length=rng.uniform(.065,.103)*(1-t*.28);width=length*rng.uniform(.20,.30)
    root=point+radial*.009;tip=root+tangent*length*.86+radial*length*.36;left=root+side*width;right=root-side*width;under=root-tangent*length*.23-radial*length*.075
    i=len(v);v.extend([tuple(left),tuple(right),tuple(tip),tuple(under)]);f.extend([(i,i+1,i+2),(i,i+3,i+1),(i+1,i+3,i+2),(i+2,i+3,i)]);sm.extend([False]*4)
    age=rng.uniform(.37,.88);col.extend([(age,.27,.5,1),(age,.32,.5,1),(age,.90,.5,1),(age,.05,.5,1)]);leaf_count+=1
 mesh=make_mesh(f'Volumetric scale shoot {variant:02d}',v,f,LEAF,col,sm);prototypes.append(mesh);prototype_info.append({'prototype':variant,'vertices':len(v),'triangles':sum(len(face)-2 for face in f),'individual_scale_leaves':leaf_count})

# Leaf distribution is constrained by irregular, overlapping subcrowns. These
# volumes guide growth; none of them becomes a visible mesh.
regions=[
 ('left lower front fork',(-1.055,-.21,1.015),(.39,.27,.17),330),
 ('left lower primary',(-1.13,.12,1.065),(.36,.26,.18),230),
 ('left middle front fork',(-.82,-.025,1.26),(.36,.25,.18),270),
 ('left rear primary',(-.98,.30,1.295),(.32,.23,.17),180),
 ('upper left primary',(-.50,-.025,1.545),(.34,.28,.19),240),
 ('upper left rear fork',(-.43,.27,1.59),(.31,.24,.17),170),
 ('apex',(.35,.17,1.84),(.35,.31,.22),320),
 ('apex front fork',(.075,-.12,1.77),(.28,.25,.18),210),
 ('crown right primary',(.90,.06,1.45),(.34,.30,.18),250),
 ('crown forward fork',(.78,-.29,1.455),(.37,.24,.19),240),
 ('crown rear fork',(.87,.38,1.43),(.31,.26,.17),180),
 ('rear crown',(.38,.50,1.645),(.31,.28,.19),180),
 ('subordinate low right',(.78,.035,.53),(.25,.235,.13),150),
 ('low right forward fork',(.76,-.20,.545),(.245,.20,.15),140),
]
route_by_name={r['name']:r for r in meta['paths']};twig_v=[];twig_f=[];twig_sm=[];records=[];shoot_count=0
for region_index,(name,centre,extent,desired) in enumerate(regions):
 rng=random.Random(516+region_index*173);nrng=np.random.default_rng(519+region_index*331);centre=np.array(centre);extent=np.array(extent);route=route_by_name[name]
 nodes=[np.array(route['control'][-2][:3]),np.array(route['control'][-1][:3])];parents=[-1,0]
 lobes=np.array([[-.30,-.07,-.12],[.27,-.16,.05],[.04,.27,.02],[.21,.10,-.16],[-.045,-.20,.22]])
 targets=[]
 for k in range(150+desired//3):
  lobe=lobes[k%len(lobes)]+nrng.normal(0,.045,3);spread=nrng.normal(0,.32,3);spread[2]*=.75
  sample=centre+extent*(lobe+spread);sample[2]=max(centre[2]-extent[2]*.58,min(centre[2]+extent[2]*.84,sample[2]));targets.append(sample)
 targets=np.array(targets)
 for iteration in range(110):
  if not len(targets):break
  points=np.array(nodes);delta=targets[:,None,:]-points[None,:,:];distance=(delta*delta).sum(axis=2);nearest=distance.argmin(axis=1);d=distance[np.arange(len(targets)),nearest]
  keep=d>.032**2;targets=targets[keep];nearest=nearest[keep];d=d[keep]
  if not len(targets):break
  influence=d<.31**2;active=targets[influence];assigned=nearest[influence]
  if not len(active):
   k=int(d.argmin());active=targets[k:k+1];assigned=nearest[k:k+1]
  additions=[]
  for parent in np.unique(assigned):
   directions=active[assigned==parent]-nodes[parent];directions/=np.maximum(np.linalg.norm(directions,axis=1)[:,None],1e-8);direction=directions.mean(axis=0)
   if parents[parent]>=0:
    prior=nodes[parent]-nodes[parents[parent]];prior/=max(np.linalg.norm(prior),1e-8);direction+=prior*.18
   direction[2]+=.08;direction/=max(np.linalg.norm(direction),1e-8);new=nodes[parent]+direction*.027
   if np.min(np.sum((points-new)**2,axis=1))<.014**2:continue
   additions.append((new,int(parent)))
  if not additions:break
  for new,parent in additions:nodes.append(new);parents.append(parent)
  if len(nodes)>850:break
 children=[[] for _ in nodes]
 for node,parent in enumerate(parents):
  if parent>=0:children[parent].append(node)
 descendants=[0]*len(nodes)
 for node in range(len(nodes)-1,-1,-1):descendants[node]=sum(descendants[c] for c in children[node]) if children[node] else 1
 radii=[min(.011,.00145*count**.48) for count in descendants]
 # Each continuous chain has a shared taper; separate chains overlap inside
 # their parent fork by a fraction of the radius.
 starts=[0]+[i for i,c in enumerate(children) if len(c)>1]
 for start_node in starts:
  for child in children[start_node]:
   chain=[start_node,child]
   while len(children[chain[-1]])==1:chain.append(children[chain[-1]][0])
   coords=[Vector(nodes[i])+Vector((0,0,SOIL)) for i in chain];rs=[radii[i] for i in chain];tube(twig_v,twig_f,coords,rs,5,smooth_faces=twig_sm)
 pool=[]
 for node in range(2,len(nodes)):
  if not children[node]:pool.extend([node]*4)
  elif descendants[node]<=2:pool.append(node)
 if not pool:raise RuntimeError('A canopy region did not grow terminal branches: '+name)
 rng.shuffle(pool);sprays=[]
 for j in range(desired):
  node=pool[j%len(pool)];parent=parents[node];point=Vector(nodes[node]);previous=Vector(nodes[parent]);direction=(point-previous).normalized();t=rng.uniform(.63,1.0);root=previous.lerp(point,t)
  random_up=Vector((rng.uniform(-.65,.65),rng.uniform(-.65,.65),rng.uniform(.45,1.0))).normalized();growth=(direction*.36+random_up*.64).normalized();length=rng.uniform(.068,.093)*(1+(.04 if region_index in [0,6] else 0))
  mesh=prototypes[rng.randrange(len(prototypes))];ob=bpy.data.objects.new(f'Canopy sprays {shoot_count:04d}',mesh);bpy.context.collection.objects.link(ob);ob.parent=foliage_group;ob.location=root+Vector((0,0,SOIL));ob.rotation_mode='QUATERNION';ob.rotation_quaternion=growth.to_track_quat('Z','Y')@Quaternion(Vector((0,0,1)),rng.uniform(0,math.tau));ob.scale=(length*rng.uniform(.80,1.10),length*rng.uniform(.82,1.13),length);shoot_count+=1
  sprays.append({'node':node,'edge_fraction':t,'length':length})
 records.append({'parent_route':name,'centre':centre.tolist(),'extent':extent.tolist(),'node_count':len(nodes),'terminal_nodes':sum(not c for c in children),'sprigs':desired,'remaining_attractors':len(targets),'root_attachment':nodes[0].tolist(),'nodes':[n.tolist() for n in nodes],'parents':parents,'spray_attachments':sprays})
 progress(f'Canopy {name}: {len(nodes)} twig nodes; {desired} rooted scale shoots')

twig_mesh=make_mesh('Terminal branch hierarchy',twig_v,twig_f,TWIG,smooth_faces=twig_sm);twigs=bpy.data.objects.new('Terminal twig hierarchy',twig_mesh);bpy.context.collection.objects.link(twigs);twigs.parent=foliage_group
# Reuse only actual substrate-detail geometry as contact dressing; no garden
# background is added during the hero gate.
support=Path(__file__).resolve().parents[2]/'sculpt-gate-1329/models/hero-v27.blend'
with bpy.data.libraries.load(str(support),link=False) as (source,target):target.objects=[n for n in source.objects if n.startswith(('Root moss shoots','Loose mineral soil particles'))]
for obj in target.objects:
 if obj:bpy.context.collection.objects.link(obj)
topology={'method':'space-colonized tertiary twig hierarchy with individually attached 3D scale shoots','no_visible_distribution_volumes':True,'no_alpha_cards':True,'prototypes':prototype_info,'shoot_instances':shoot_count,'regions':records,'twig_vertices':len(twig_v),'twig_triangles':sum(len(f)-2 for f in twig_f)}
(out/(prefix.name+'.canopy-topology.json')).write_text(json.dumps(topology,indent=2));meta['canopy_summary']={'shoot_instances':shoot_count,'regions':len(regions),'twig_vertices':len(twig_v),'twig_triangles':topology['twig_triangles'],'leaf_triangles':sum(prototype_info[i%12]['triangles'] for i in range(shoot_count))};progress(f'Canopy complete: {shoot_count} scale-shoot instances')
