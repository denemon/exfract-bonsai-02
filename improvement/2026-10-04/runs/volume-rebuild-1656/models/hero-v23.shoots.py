"""Fine closed scale leaves, with a separately authored distant representation."""
def source_shoot(variant,detailed):
 rng=random.Random(991+variant*313);v=[];f=[];col=[];sm=[];axes=[]
 main=[Vector((math.sin(k*.9+variant)*.015,math.cos(k*.8+variant)*.022,k/5)) for k in range(6)]
 tube(v,f,main,[.024*(1-k/6)*.8 for k in range(6)],4,col,sm);axes.append((main,7 if detailed else 5))
 levels=[.13,.22,.31,.40,.49,.58,.67,.76,.85] if detailed else [.19,.37,.55,.73]
 for level,z in enumerate(levels):
  phase=level*1.16+rng.uniform(-.25,.25)+variant*.43
  for side in [0,1]:
   angle=phase+side*math.pi+rng.uniform(-.3,.3);length=(1-z)*rng.uniform(.41,.60);base=Vector((0,0,z));radial=Vector((math.cos(angle),math.sin(angle),0));tip=base+radial*length*.80+Vector((0,0,length*.68))
   bend=base.lerp(tip,.52)+Vector((rng.uniform(-.015,.015),rng.uniform(-.015,.015),.028));axis=[base,bend,tip]
   tube(v,f,axis,[.016*(1-z*.5),.010,.003],4,col,sm);axes.append((axis,4 if detailed else 3))
 leaf_start=len(v);leaf_count=0
 for axis,rows in axes:
  for row in range(rows):
   t=(row+.6)/(rows+.35);q=t*(len(axis)-1);j=min(len(axis)-2,int(q));u=q-j;point=axis[j].lerp(axis[j+1],u);tangent=(axis[j+1]-axis[j]).normalized();n=tangent.cross(Vector((0,1,0)))
   if n.length<.1:n=tangent.cross(Vector((1,0,0)))
   n.normalize();b=tangent.cross(n).normalized();phase=row*1.38+variant*.47
   for k in range(4):
    angle=phase+k*math.pi/2+rng.uniform(-.12,.12);radial=n*math.cos(angle)+b*math.sin(angle);side=tangent.cross(radial).normalized();length=rng.uniform(.068,.098) if detailed else rng.uniform(.112,.155);length*=1-t*.24;width=length*(rng.uniform(.25,.31) if detailed else rng.uniform(.28,.36))
    root=point+radial*.009;tip=root+tangent*length*.86+radial*length*.36;left=root+side*width;right=root-side*width;under=root-tangent*length*.23-radial*length*.075
    i=len(v);v.extend([tuple(left),tuple(right),tuple(tip),tuple(under)]);f.extend([(i,i+1,i+2),(i,i+3,i+1),(i+1,i+3,i+2),(i+2,i+3,i)]);sm.extend([False]*4)
    age=rng.uniform(.37,.88);col.extend([(age,.27,.5,1),(age,.32,.5,1),(age,.90,.5,1),(age,.05,.5,1)]);leaf_count+=1
 return v,f,col,sm,axes,leaf_start,leaf_count

prototypes=[];prototype_info=[]
for variant in range(12):
 high,hf,hc,hs,_,_,high_count=source_shoot(variant,True)
 mesh=make_mesh(f'Volumetric scale shoot {variant:02d}',high,hf,LEAF,hc,hs);prototypes.append(mesh)
 v,_,col,_,axes,leaf_start,leaf_count=source_shoot(variant,False);lv=[];lf=[];lc=[];ls=[]
 for ai,(axis,_) in enumerate(axes):
  coords=[axis[0],axis[-1]] if ai else [axis[0],axis[len(axis)//2],axis[-1]];radius=.014 if ai else .019
  tube(lv,lf,coords,[radius*(1-j/len(coords)*.85) for j in range(len(coords))],3,lc,ls)
 for li in range(leaf_count):
  if (li+variant)%2:continue
  source=leaf_start+li*4;root=(Vector(v[source])+Vector(v[source+1]))*.5;i=len(lv)
  lv.extend([tuple(root+(Vector(v[source+k])-root)*1.36) for k in range(4)]);lc.extend(col[source:source+4]);lf.extend([(i,i+1,i+2),(i,i+3,i+1),(i+1,i+3,i+2),(i+2,i+3,i)]);ls.extend([False]*4)
 low=make_mesh(f'Volumetric scale shoot low {variant:02d}',lv,lf,LEAF,lc,ls);template=bpy.data.objects.new(f'Foliage detail template {variant:02d}',low);bpy.context.collection.objects.link(template);template['foliage_lod_template']=True;template['foliage_variant']=variant
 prototype_info.append({'prototype':variant,'vertices':len(high),'triangles':sum(len(face)-2 for face in hf),'individual_scale_leaves':high_count,'low_triangles':sum(len(face)-2 for face in lf),'low_closed_scale_leaves':leaf_count//2})
