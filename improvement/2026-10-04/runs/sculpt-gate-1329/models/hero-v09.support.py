"""Low split bedding stone, planted substrate, and true miniature moss shoots."""
# A split stone has a quiet bearing surface and an unequal, partly buried edge.
sr=random.Random(182);sides=100;v=[];f=[]
corners=[(1.08,.43),(.69,.65),(-.59,.63),(-1.05,.43),(-1.11,-.13),(-.99,-.59),(-.42,-.67),(.76,-.60),(1.06,-.36),(1.13,.13)]
outline=[]
for k in range(sides):
 t=k/sides*len(corners);j=int(t);u=t-j;a=Vector((*corners[j],0));b=Vector((*corners[(j+1)%len(corners)],0));p=a.lerp(b,u);outline.append(tuple(p))
for layer,(scale,z) in enumerate([(1.005,-.062),(1.015,.014),(.978,.109),(.92,.153)]):
 for k,(x,y,_) in enumerate(outline):
  n=noise.noise_vector(Vector((x*6.2,y*6.2,layer*.7))).x
  asym=.014*math.sin(k*.67)+.009*math.sin(k*1.37)
  edge_z=z+(.012*n if layer<3 else .004*n)
  v.append((x*(scale+asym+.022*n)-.015,y*(scale+asym+.02*n)+.015,edge_z))
  if layer<3:f.append((layer*sides+k,layer*sides+(k+1)%sides,(layer+1)*sides+(k+1)%sides,(layer+1)*sides+k))
for ring in range(1,8):
 factor=1-ring/8
 for k in range(sides):
  x,y,z=v[3*sides+k];v.append((x*factor,y*factor,.153+.0015*noise.noise_vector(Vector((x*21,y*21,2))).x))
  a=(3+ring-1)*sides+k;b=(3+ring-1)*sides+(k+1)%sides;c=(3+ring)*sides+(k+1)%sides;d=(3+ring)*sides+k
  f.append((a,b,c,d))
f.append(tuple(10*sides+k for k in range(sides)));f.append(tuple(range(sides-1,-1,-1)))
stone=make('Low split natural bedding stone',v,f,STONE,smooth=False)
be=stone.modifiers.new('Minute softened fracture edges','BEVEL');be.width=.003;be.segments=1;bpy.context.view_layer.objects.active=stone;bpy.ops.object.modifier_apply(modifier=be.name)

def moss_field(x,y):
 patch=.60*math.exp(-((x+.37)**2/.055+(y+.16)**2/.021))+.56*math.exp(-((x-.31)**2/.068+(y-.17)**2/.032))+.48*math.exp(-((x-.38)**2/.034+(y+.20)**2/.017))
 irregular=noise.noise_vector(Vector((x*15,y*15,2))).x*.19+noise.noise_vector(Vector((x*39,y*39,5))).x*.08
 return max(0,min(1,patch+irregular))
def soil_height(x,y):
 edge=1-smooth(.79,1,max(abs(x)/.755,abs(y)/.381))
 return SOIL+edge*(.018*math.exp(-(x*x+y*y)*8)+.019*moss_field(x,y)+.003*noise.noise_vector(Vector((x*33,y*33,1))).x)
sv=[];sf=[];rings=40;sides=96
for j in range(rings+1):
 factor=j/rings
 for x,y,_ in rounded_ring(.755*factor,.381*factor,.074*factor,SOIL,count=sides):sv.append((x,y,soil_height(x,y)))
 for k in range(sides):
  if j<rings:sf.append((j*sides+k,(j+1)*sides+k,(j+1)*sides+(k+1)%sides,j*sides+(k+1)%sides))
soil=make('Continuous planted soil',sv,sf,SOILMAT);at=soil.data.color_attributes.new(name='Root moss coverage',type='FLOAT_COLOR',domain='POINT');at.data.foreach_set('color',[value for x,y,z in sv for value in (moss_field(x,y),.5,.5,1)])

MOSS=material('Root moss foliage',(.10,.14,.02),.96);GRIT=material('Loose mineral soil',(.09,.065,.03),1)
mv=[];mf=[];mc=[];mu=[];gv=[];gf=[];rng=random.Random(680)
for j in range(35000):
 x=rng.uniform(-.746,.746);y=rng.uniform(-.371,.371)
 if abs(x)>.68 and abs(y)>.32 and ((abs(x)-.68)**2+(abs(y)-.32)**2)>.067**2:continue
 field=moss_field(x,y);z=soil_height(x,y)
 if rng.random()<field*1.8:
  base=Vector((x,y,z));h=rng.uniform(.002,.007)*(field+.55);phase=rng.uniform(0,math.tau)
  for k in range(3):
   a=phase+k*math.tau/3;side=Vector((math.cos(a),math.sin(a),0));q=Vector((-math.sin(a),math.cos(a),0));tip=base+side*h*.45+Vector((0,0,h));mid=base.lerp(tip,.55);i=len(mv);width=h*.15
   mv.extend([base,mid+q*width,mid+side*width*.4,mid-q*width,tip]);mf.extend([(i,i+2,i+1),(i,i+3,i+2),(i,i+1,i+4),(i+1,i+2,i+4),(i+2,i+3,i+4),(i+3,i,i+4)])
   age=rng.uniform(.25,.95);mc.extend([(age,.1,.5,1),(age,.3,.5,1),(age,.5,.5,1),(age,.3,.5,1),(age,.8,.5,1)]);mu.extend([(0,0),(.3,.2),(.5,.3),(.7,.2),(.5,1)])
 elif rng.random()<.26:
  r=rng.uniform(.0015,.004);i=len(gv);phase=rng.uniform(0,math.tau)
  gv.append((x,y,z+r*.8))
  for k in range(5):
   a=phase+k*math.tau/5;gv.append((x+math.cos(a)*r,y+math.sin(a)*r,z-r*.2))
  for k in range(5):gf.append((i,i+1+k,i+1+(k+1)%5))
moss=make('Root moss shoots',mv,mf,MOSS);at=moss.data.color_attributes.new(name='Growth masks',type='FLOAT_COLOR',domain='POINT');at.data.foreach_set('color',[v for c in mc for v in c]);uv=moss.data.uv_layers.new(name='Growth UV')
for poly in moss.data.polygons:
 for loop in poly.loop_indices:uv.data[loop].uv=mu[moss.data.loops[loop].vertex_index]
make('Loose mineral soil particles',gv,gf,GRIT,smooth=False)
progress(f'Root contact: {len(mv)//15} moss shoots, {len(gv)//6} mineral particles')
