"""Connected branch -> secondary fork -> terminal spray -> scale leaf topology.
Positions follow the woody network; no ellipsoid/sphere sampling is used.
Executed by generate.py inside Blender with its shared materials and functions.
"""
random.seed(271041)
lv=[];lf=[];lc=[];lu=[];tv=[];tf=[];tc=[];tu=[];topology=[];spray_count=0;leaf_count=0;prototypes=[];instances=[]

def tube_batch(points,radii,seed):
 points=[Vector(p) for p in points];start=len(tv);steps=6;sides=5
 for j in range(steps+1):
  t=j/steps;p=cat(points,t);d=(cat(points,min(1,t+.01))-cat(points,max(0,t-.01))).normalized();n=d.cross(Vector((0,0,1))).normalized()
  if n.length<.2:n=d.cross(Vector((0,1,0))).normalized()
  q=d.cross(n).normalized();r=radii[0]*(1-t)+radii[-1]*t
  for k in range(sides):
   a=k/sides*math.tau;tv.append(p+n*math.cos(a)*r+q*math.sin(a)*r);tc.append((.89,seed,.5,1));tu.append((k/sides,t*.2))
   if j<steps:tf.append((start+j*sides+k,start+j*sides+(k+1)%sides,start+(j+1)*sides+(k+1)%sides,start+(j+1)*sides+k))

def scale_leaf(base,tip,width,age,twist=0):
 global leaf_count
 d=(tip-base).normalized();n=d.cross(Vector((0,0,1))).normalized()
 if n.length<.2:n=d.cross(Vector((0,1,0))).normalized()
 q=d.cross(n).normalized();n=n*math.cos(twist)+q*math.sin(twist);q=d.cross(n);mid=base.lerp(tip,.32);i=len(lv)
 lv.extend([base,mid+n*width,mid+q*width*.48,mid-n*width,tip])
 lf.extend([(i,i+2,i+1),(i,i+3,i+2),(i,i+1,i+4),(i+1,i+2,i+4),(i+2,i+3,i+4),(i+3,i,i+4)])
 lc.extend([(age,0,.5,1),(age,.3,.5,1),(age,.55,.5,1),(age,.3,.5,1),(age,.9,.5,1)]);lu.extend([(0,0),(.3,.2),(.5,.3),(.7,.2),(.5,1)]);leaf_count+=1

def leafy_axis(base,direction,length,age,phase):
 direction=direction.normalized();side=direction.cross(Vector((0,0,1))).normalized()
 if side.length<.2:side=Vector((1,0,0))
 up=direction.cross(side).normalized()
 # A continuous four-sided scale shoot carries small, appressed scales. The
 # axis has real thickness; the silhouette no longer relies on large kite leaves.
 start=len(lv);steps=8;sides=4
 for j in range(steps+1):
  t=j/steps;p=base+direction*length*t+up*length*.045*math.sin(t*math.pi);radius=length*(.025*(1-t)+.0015)*(1.13 if j%2==0 else .87)
  for k in range(sides):
   a=k/sides*math.tau+phase*.12;lv.append(p+side*math.cos(a)*radius+up*math.sin(a)*radius);lc.append((age,t*.8,.5,1));lu.append((k/sides,t))
   if j<steps:lf.extend([(start+j*sides+k,start+j*sides+(k+1)%sides,start+(j+1)*sides+(k+1)%sides),(start+j*sides+k,start+(j+1)*sides+(k+1)%sides,start+(j+1)*sides+k)])
 for j in range(6):
  t=(j+.2)/6;p=base+direction*length*t+up*length*.045*math.sin(t*math.pi);bl=length*(.135-.045*t)
  for sign in [-1,1]:
   tip=p+direction*bl+side*sign*length*.035+up*length*(.033 if j%2 else -.025)
   scale_leaf(p,tip,length*.026,age,phase+sign*.28)

def prototype_spray(base,direction,length,seed):
 direction=direction.normalized();side=direction.cross(Vector((0,0,1))).normalized()
 if side.length<.2:side=Vector((1,0,0))
 up=direction.cross(side).normalized();age=random.uniform(.22,.92)
 leafy_axis(base,direction,length,age,seed)
 for j in range(4):
  t=.09+j*.20;p=base+direction*length*t
  for sign in [-1,1]:
   d=(direction*random.uniform(.48,.72)+side*sign*(.76-.08*j)+up*random.uniform(-.20,.24)).normalized()
   leafy_axis(p,d,length*(.64-.083*j)*random.uniform(.88,1.12),age,seed+sign*.2)

for variant in range(12):
 lv=[];lf=[];lc=[];lu=[];before=leaf_count
 prototype_spray(Vector((0,0,0)),Vector((1,0,0)),1,.11+variant*.077)
 obj=make(f'Scale shoot prototype {variant:02}',lv,lf,LEAF)
 at=obj.data.color_attributes.new(name='Growth masks',type='FLOAT_COLOR',domain='POINT');at.data.foreach_set('color',[v for c in lc for v in c]);layer=obj.data.uv_layers.new(name='Growth UV')
 for poly in obj.data.polygons:
  for loop in poly.loop_indices:layer.data[loop].uv=lu[obj.data.loops[loop].vertex_index]
 prototypes.append((obj.data,leaf_count-before));bpy.data.objects.remove(obj,do_unlink=True)

foliage_group=bpy.data.objects.new('Branch led scale foliage',None);bpy.context.collection.objects.link(foliage_group)
def spray(base,direction,length,seed):
 global spray_count
 data,scales=random.choice(prototypes);obj=bpy.data.objects.new(f'Branch led scale foliage {spray_count:04}',data);bpy.context.collection.objects.link(obj);obj.parent=foliage_group;obj.location=base+Vector((0,0,SOIL));obj.rotation_mode='QUATERNION';obj.rotation_quaternion=Vector((1,0,0)).rotation_difference(direction.normalized()) @ Quaternion(Vector((1,0,0)),random.uniform(-.55,.55));obj.scale=(length,length*random.uniform(.84,1.17),length*random.uniform(.88,1.14));instances.append(obj);spray_count+=1

for branch_index,(name,coords,radii,seed) in enumerate(branches):
 points=[Vector(p) for p in coords];small='subordinate' in name
 for anchor_index,t in enumerate([.42,.57,.72,.86,.99]):
  if small and anchor_index==0:continue
  anchor=cat(points,t);d=(cat(points,min(1,t+.01))-cat(points,max(0,t-.01))).normalized();flat=Vector((d.x,d.y,0)).normalized();side=Vector((-flat.y,flat.x,0))
  for sign in [-1,1]:
   length=random.uniform(.24,.36)*(1-.12*t)*(.73 if small else 1)
   end=anchor+flat*length*.26+side*sign*length*.86+Vector((0,0,length*random.uniform(.12,.45)))
   bend=anchor.lerp(end,.5)+Vector((0,0,-.018));tube_batch([anchor,bend,end],[.009*(1-t*.4),.0013],seed)
   topology.append({'primary':name,'attachment':t,'end':list(end),'depth_sign':sign})
   sec=[anchor,bend,end];dd=(end-anchor).normalized();ss=dd.cross(Vector((0,0,1))).normalized()
   for terminal_index,tt in enumerate([.32,.50,.69,.86,1.0]):
    p=cat(sec,tt)
    for sign2 in [-1,1]:
     l=random.uniform(.11,.18)*(.82 if small else 1)
     direction=(dd*random.uniform(.25,.65)+ss*sign2*random.uniform(.45,.90)+Vector((0,0,random.uniform(-.06,.46)))).normalized()
     tip=p+direction*l
     tube_batch([p,p.lerp(tip,.5)-Vector((0,0,.007)),tip],[.0038,.0005],seed)
     # Opposed shoots grow from each terminal; uneven lengths create the pruning outline.
     for shoot_index,st in enumerate([.20,.46,.72,1.0]):
      root=p.lerp(tip,st);sd=(direction+ss*random.uniform(-.70,.70)+Vector((0,0,random.uniform(-.28,.42)))).normalized()
      spray(root,sd,random.uniform(.085,.144)*(.86 if small else 1),seed+tt)

twigs=make('Terminal branch hierarchy',tv,tf,WOOD)
for obj,colors,uvcoords in [(twigs,tc,tu)]:
 at=obj.data.color_attributes.new(name='Growth masks',type='FLOAT_COLOR',domain='POINT');at.data.foreach_set('color',[v for c in colors for v in c]);layer=obj.data.uv_layers.new(name='Growth UV')
 for poly in obj.data.polygons:
  for loop in poly.loop_indices:layer.data[loop].uv=uvcoords[obj.data.loops[loop].vertex_index]
 obj.location.z=SOIL
counts={data.name:count for data,count in prototypes}
(OUT/f'hero-{opt.version}.foliage-topology.json').write_text(json.dumps({'primary_branches':len(branches),'secondary_supports':topology,'sprays':spray_count,'scale_leaves':sum(counts[o.data.name] for o in instances),'volumetric_axes':len(instances)*9,'prototype_count':len(prototypes),'representation':'EXT_mesh_gpu_instancing of true volumetric scale shoots','distribution':'Connected branch hierarchy; no sphere or ellipsoid placement'},indent=2))
progress(f'Branch-led foliage: {spray_count} instanced sprays, {len(prototypes)} volumetric prototypes')
