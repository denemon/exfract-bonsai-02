"""Connected branch -> secondary fork -> terminal spray -> scale leaf topology.
Positions follow the woody network; no ellipsoid/sphere sampling is used.
Executed by generate.py inside Blender with its shared materials and functions.
"""
random.seed(271041)
lv=[];lf=[];lc=[];lu=[];tv=[];tf=[];tc=[];tu=[];topology=[];spray_count=0;leaf_count=0

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
 for j in range(6):
  t=j/6;p=base+direction*length*t;bl=length*(.23-.08*t)
  for sign in [-1,1]:
   tip=p+direction*bl+side*sign*length*.075+up*length*(.045 if j%2 else -.025)
   scale_leaf(p,tip,length*.021,age,phase+sign*.28)

def spray(base,direction,length,seed):
 global spray_count
 direction=direction.normalized();side=direction.cross(Vector((0,0,1))).normalized()
 if side.length<.2:side=Vector((1,0,0))
 up=direction.cross(side).normalized();age=random.uniform(.22,.92)
 leafy_axis(base,direction,length,age,seed)
 for j in range(4):
  t=.11+j*.19;p=base+direction*length*t
  for sign in [-1,1]:
   d=(direction*.61+side*sign*(.76-.1*j)+up*random.uniform(-.05,.20)).normalized()
   leafy_axis(p,d,length*(.53-.074*j),age,seed+sign*.2)
 spray_count+=1

for branch_index,(name,coords,radii,seed) in enumerate(branches):
 points=[Vector(p) for p in coords];small='subordinate' in name
 for anchor_index,t in enumerate([.34,.53,.72,.91]):
  if small and anchor_index==0:continue
  anchor=cat(points,t);d=(cat(points,min(1,t+.01))-cat(points,max(0,t-.01))).normalized();flat=Vector((d.x,d.y,0)).normalized();side=Vector((-flat.y,flat.x,0))
  for sign in [-1,1]:
   length=random.uniform(.23,.33)*(1-.20*t)*(.73 if small else 1)
   end=anchor+flat*length*.62+side*sign*length*.65+Vector((0,0,length*random.uniform(.28,.52)))
   bend=anchor.lerp(end,.5)+Vector((0,0,-.018));tube_batch([anchor,bend,end],[.009*(1-t*.4),.0013],seed)
   topology.append({'primary':name,'attachment':t,'end':list(end),'depth_sign':sign})
   sec=[anchor,bend,end];dd=(end-anchor).normalized();ss=dd.cross(Vector((0,0,1))).normalized()
   for terminal_index,tt in enumerate([.30,.49,.68,.86,1.0]):
    p=cat(sec,tt)
    for sign2 in [-1,1]:
     l=random.uniform(.09,.16)*(.82 if small else 1)
     direction=(dd*.54+ss*sign2*.71+Vector((0,0,random.uniform(.24,.65)))).normalized()
     tip=p+direction*l
     tube_batch([p,p.lerp(tip,.5)-Vector((0,0,.007)),tip],[.0038,.0005],seed)
     # Opposed shoots grow from each terminal; uneven lengths create the pruning outline.
     for shoot_index,st in enumerate([.42,1.0]):
      root=p.lerp(tip,st);sd=(direction+ss*((-1 if shoot_index%2 else 1)*.36)+Vector((0,0,.25))).normalized()
      spray(root,sd,random.uniform(.057,.086)*(.86 if small else 1),seed+tt)

twigs=make('Terminal branch hierarchy',tv,tf,WOOD)
foliage=make('Branch led scale foliage',lv,lf,LEAF)
for obj,colors,uvcoords in [(twigs,tc,tu),(foliage,lc,lu)]:
 at=obj.data.color_attributes.new(name='Growth masks',type='FLOAT_COLOR',domain='POINT');at.data.foreach_set('color',[v for c in colors for v in c]);layer=obj.data.uv_layers.new(name='Growth UV')
 for poly in obj.data.polygons:
  for loop in poly.loop_indices:layer.data[loop].uv=uvcoords[obj.data.loops[loop].vertex_index]
 obj.location.z=SOIL
(OUT/f'hero-{opt.version}.foliage-topology.json').write_text(json.dumps({'primary_branches':len(branches),'secondary_supports':topology,'sprays':spray_count,'scale_leaves':leaf_count,'distribution':'Connected branch hierarchy; no sphere or ellipsoid placement'},indent=2))
progress(f'Branch-led foliage: {spray_count} sprays, {leaf_count} scale leaves')
