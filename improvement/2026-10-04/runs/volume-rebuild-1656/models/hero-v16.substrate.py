"""Instanced micro moss and embedded grit, using the actual soil height field."""
def moss_field(x,y):
 patch=.60*math.exp(-((x+.37)**2/.055+(y+.16)**2/.021))+.56*math.exp(-((x-.31)**2/.068+(y-.17)**2/.032))+.48*math.exp(-((x-.38)**2/.034+(y+.20)**2/.017))
 irregular=noise.noise_vector(Vector((x*15,y*15,2))).x*.19+noise.noise_vector(Vector((x*39,y*39,5))).x*.08
 return max(0,min(1,patch+irregular))
def soil_height(x,y):
 edge=1-smooth(.79,1,max(abs(x)/.755,abs(y)/.381))
 return SOIL+edge*(.018*math.exp(-(x*x+y*y)*8)+.019*moss_field(x,y)+.003*noise.noise_vector(Vector((x*33,y*33,1))).x)
def inside_soil(x,y):return not(abs(x)>.68 and abs(y)>.32 and (abs(x)-.68)**2+(abs(y)-.32)**2>.067**2)
moss_prototypes=[];grit_prototypes=[];grit_mat=simple_material('Loose mineral soil',(.14,.10,.06));rgen=random.Random(672)
for variant in range(6):
 v=[];f=[];col=[]
 for shoot in range(4):
  base=Vector((rgen.uniform(-.48,.48),rgen.uniform(-.48,.48),0));h=rgen.uniform(.6,1.05);phase=rgen.uniform(0,math.tau)
  for leaf in range(3):
   a=phase+leaf*math.tau/3;radial=Vector((math.cos(a),math.sin(a),0));side=Vector((-math.sin(a),math.cos(a),0));mid=base+radial*h*.24+Vector((0,0,h*.43));tip=base+radial*h*.43+Vector((0,0,h));i=len(v)
   v.extend([tuple(base),tuple(mid+side*h*.13),tuple(mid-side*h*.13),tuple(tip)]);f.extend([(i,i+2,i+1),(i,i+1,i+3),(i+1,i+2,i+3),(i+2,i,i+3)]);age=rgen.uniform(.35,.8);col.extend([(age,.05,.5,1),(age,.40,.5,1),(age,.3,.5,1),(age,.9,.5,1)])
 moss_prototypes.append(make_mesh(f'Root moss tuft {variant:02d}',v,f,LEAF,col))
 v=[(0,0,.65*rgen.uniform(.8,1.2)),(0,0,-.45)];f=[]
 for k in range(5):
  a=k*math.tau/5;r=rgen.uniform(.75,1.13);v.append((math.cos(a)*r,math.sin(a)*r,rgen.uniform(-.07,.08)))
 for k in range(5):f.extend([(0,2+k,2+(k+1)%5),(1,2+(k+1)%5,2+k)])
 grit_prototypes.append(make_mesh(f'Embedded mineral grain {variant:02d}',v,f,grit_mat))
rgen=random.Random(676);moss_count=0;grit_count=0
for attempt in range(30000):
 x=rgen.uniform(-.745,.745);y=rgen.uniform(-.37,.37)
 if not inside_soil(x,y):continue
 field=moss_field(x,y)
 if moss_count<2200 and rgen.random()<min(1,field*1.45):
  size=rgen.uniform(.0035,.0072)*(field+.55);ob=bpy.data.objects.new(f'Root moss shoots {moss_count:04d}',moss_prototypes[rgen.randrange(6)]);bpy.context.collection.objects.link(ob);ob.parent=foliage_group;ob.location=(x,y,soil_height(x,y)-.0002);ob.scale=(size,size,size);ob.rotation_euler.z=rgen.uniform(0,math.tau);moss_count+=1
 elif grit_count<2400 and rgen.random()<.44:
  size=rgen.uniform(.0016,.0043);ob=bpy.data.objects.new(f'Loose soil particles {grit_count:04d}',grit_prototypes[rgen.randrange(6)]);bpy.context.collection.objects.link(ob);ob.parent=foliage_group;ob.location=(x,y,soil_height(x,y)+size*.09);ob.scale=(size,size*rgen.uniform(.74,1.05),size);ob.rotation_euler=(rgen.uniform(-.13,.13),rgen.uniform(-.13,.13),rgen.uniform(0,math.tau));grit_count+=1
 if moss_count>=2200 and grit_count>=2400:break
meta['substrate_instances']={'moss_tufts':moss_count,'moss_shoots':moss_count*4,'grains':grit_count,'shared_moss_prototypes':6,'shared_grit_prototypes':6,'contact':'actual inherited soil field; grain lower half buried'}
progress(f'Substrate: {moss_count} moss tufts and {grit_count} embedded grains, shared geometry')
