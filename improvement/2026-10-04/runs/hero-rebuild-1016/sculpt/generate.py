import bpy, math, random, os, json
from mathutils import Vector
from mathutils import noise
random.seed(8196)
OUT='/Users/kazuki.tanaka/dev0/exfract-bonsai-02/improvement/2026-10-04/runs/hero-rebuild-1016'
bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)
# Author in the same metre-based X/Y-up/Z coordinates as the garden.
def B(p): return Vector((p[0],-p[2],p[1]))
def srgb(v):return v/12.92 if v<.04045 else ((v+.055)/1.055)**2.4
def color(hex): return tuple(srgb(int(hex[i:i+2],16)/255) for i in (1,3,5))
def material(name,hex,roughness):
 m=bpy.data.materials.new(name);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*color(hex),1);p.inputs['Roughness'].default_value=roughness
 return m
dead=material('Weathered brown heartwood','#9f8c74',.89)
live=material('Living cinnamon bark','#79523c',.94)
leafmat=material('Juniper fine scale foliage','#ffffff',.86)
for m in [dead,live,leafmat]:
 n=m.node_tree.nodes.new('ShaderNodeVertexColor');n.layer_name='Tint';m.node_tree.links.new(n.outputs['Color'],m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'])
def make(name,verts,faces,mat,colors=None):
 me=bpy.data.meshes.new(name);me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(o);me.materials.append(mat)
 for p in me.polygons:p.use_smooth=True
 if colors:
  at=me.color_attributes.new(name='Tint',type='FLOAT_COLOR',domain='POINT');flat=[q for c in colors for q in (*c,1)];at.data.foreach_set('color',flat)
 return o
def cat(points,t):
 n=len(points)-1;k=min(n-1,int(t*n));u=t*n-k;p0=points[max(0,k-1)];p1=points[k];p2=points[k+1];p3=points[min(n,k+2)]
 return .5*((2*p1)+(-p0+p2)*u+(2*p0-5*p1+4*p2-p3)*u*u+(-p0+3*p1-3*p2+p3)*u*u*u)
def tube(name,coords,radii,mat=dead,steps=80,sides=24,twist=1.4,flat=1,lobes=.12):
 pts=[B(p) for p in coords];verts=[];faces=[]
 prev=Vector((0,1,0))
 for j in range(steps+1):
  t=j/steps;p=cat(pts,t);d=(cat(pts,min(1,t+.001))-cat(pts,max(0,t-.001))).normalized();n=prev.cross(d).normalized()
  if n.length<.5:n=d.cross(Vector((1,0,0))).normalized()
  b=d.cross(n).normalized();prev=b
  k=t*(len(radii)-1);k0=min(len(radii)-2,int(k));r=radii[k0]+(radii[k0+1]-radii[k0])*(k-k0)
  for i in range(sides):
   a=i/sides*math.tau+twist*t
   shape=1+lobes*math.sin(3*a+t*4)+lobes*.55*math.sin(5*a-t*3)+.045*math.sin(11*a+t*5)
   # A few deep open-ended longitudinal creases, not parallel applied cords.
   crease=.12*math.exp(-((math.sin(a*2+t*2.2))/.21)**2)
   rad=r*(shape-crease)
   v=p+n*(math.cos(a)*rad)+b*(math.sin(a)*rad*flat)
   verts.append(v)
   if j<steps:faces.append((j*sides+i,j*sides+(i+1)%sides,(j+1)*sides+(i+1)%sides,(j+1)*sides+i))
 faces.append(tuple(range(sides-1,-1,-1)));faces.append(tuple(steps*sides+i for i in range(sides)))
 return make(name,verts,faces,mat)
# A rooted, double-turn volume. The line travels backwards, then forward across itself.
core=tube('Heartwood sculpt',[(.02,.53,.01),(-.13,.76,-.10),(-.035,.99,-.10),(-.28,1.24,.01),(-.39,1.49,.05),(-.16,1.75,-.07),(.19,1.97,-.09),(.34,2.22,.04),(.32,2.69,-.01)],[.235,.215,.184,.178,.159,.127,.088,.050,.0015],steps=170,sides=36,twist=1.7,flat=.98,lobes=.115)
parts=[core]
root_data=[([(.04,.65,.02),(-.25,.55,.10),(-.59,.518,.26)],[.17,.096,.012]),([(-.07,.65,-.05),(-.36,.57,-.2),(-.59,.52,-.30)],[.13,.080,.01]),([(.04,.63,-.1),(.28,.55,-.29),(.43,.522,-.35)],[.12,.07,.009]),([(.10,.62,.08),(.36,.545,.18),(.65,.521,.14)],[.12,.083,.008])]
for p,r in root_data:parts.append(tube('Root flare',p,r,steps=45,sides=22,twist=1.8,lobes=.16))
# Unequal forks and broken jins grow out of the trunk, in different depth planes.
for p,r in [([(-.3,1.28,.0),(-.66,1.37,.01),(-.90,1.46,-.05),(-.91,1.60,-.11)],[.105,.079,.043,.001]),([(-.31,1.56,-.015),(-.51,1.82,-.13),(-.44,2.07,-.21)],[.10,.054,.0015]),([(.14,1.98,-.06),(.43,2.27,-.08),(.44,2.57,-.16)],[.077,.043,.001]),([(-.05,.89,-.04),(.24,1.06,.09),(.33,1.24,.03)],[.09,.061,.002])]:parts.append(tube('Broken deadwood fork',p,r,steps=50,sides=22,twist=2.2,lobes=.2))
bpy.ops.object.select_all(action='DESELECT')
for o in parts:o.select_set(True)
bpy.context.view_layer.objects.active=core;bpy.ops.object.join()
core.data.remesh_voxel_size=.007;bpy.ops.object.voxel_remesh()
sm=core.modifiers.new('Grown junctions','SMOOTH');sm.factor=.55;sm.iterations=3;bpy.ops.object.modifier_apply(modifier=sm.name)
# Deep irregular shari recess. The entrance opens toward the viewing side rather than drawing a painted stripe.
cut=tube('Shari recess cutter',[(.08,.78,.165),(-.09,.97,.19),(-.27,1.21,.17),(-.28,1.44,.175),(-.17,1.63,.135)],[.017,.048,.057,.035,.004],steps=75,sides=22,flat=1.30,twist=2.2,lobes=.21)
bpy.context.view_layer.objects.active=core
bo=core.modifiers.new('Recess inside the twisting wood','BOOLEAN');bo.operation='DIFFERENCE';bo.solver='EXACT';bo.object=cut
try:bpy.ops.object.modifier_apply(modifier=bo.name)
except Exception as e:print('BOOLEAN WARNING',e)
bpy.data.objects.remove(cut,do_unlink=True)
# Fine grain belongs to the volume and breaks up the light at grazing angles.
base=color('#9a8973');colors=[]
for v in core.data.vertices:
 x,y,z=v.co;f=noise.noise_vector(Vector((x*11,y*11,z*1.7))).x
 v.co+=v.normal*(.0008*math.sin(z*13+x*90+y*67)+.0013*f)
 tone=.89+.10*f+.045*math.sin(x*48+y*38+z*3)
 colors.append(tuple(c*tone for c in base))
at=core.data.color_attributes.new(name='Tint',type='FLOAT_COLOR',domain='POINT');at.data.foreach_set('color',[q for c in colors for q in (*c,1)])
for p in core.data.polygons:p.use_smooth=True
# Broad living vein twists from the rear of the root onto the front of the old wood.
veins=[]
veins.append(tube('Living vein',[(.19,.53,.13),(.32,.74,.17),(.21,.97,.21),(-.08,1.22,.20),(-.28,1.47,.175),(-.12,1.70,.06),(.25,1.91,.01),(.43,2.17,.035),(.49,2.48,.01)],[.091,.080,.069,.056,.046,.039,.031,.021,.006],live,steps=160,sides=24,twist=2.7,flat=.69,lobes=.18))
veins.append(tube('Living root',[(.23,.60,.12),(.48,.55,.26),(.7,.522,.31)],[.075,.044,.003],live,steps=45,sides=18,lobes=.13))
# Main living branches are articulated, forked and taper continuously into the leaf sprays.
branch_data=[
([(-.26,1.49,.13),(-.60,1.64,.13),(-.96,1.72,.20),(-1.25,1.89,.14)],[.052,.038,.023,.009]),
([(-.16,1.71,.04),(-.41,1.97,.0),(-.65,2.14,.04),(-.91,2.23,.07)],[.052,.036,.023,.008]),
([(.23,1.88,.01),(.61,1.63,.04),(1.03,1.67,.12),(1.31,1.79,.20)],[.05,.034,.024,.007]),
([(.35,2.17,.02),(.60,2.36,.07),(.89,2.51,.02),(1.1,2.54,-.07)],[.04,.032,.020,.005]),
([(.28,2.04,-.05),(.04,2.32,-.22),(.06,2.59,-.26),(.25,2.76,-.30)],[.034,.027,.016,.006]),
([(-.31,1.50,-.02),(-.68,1.80,-.29),(-1.01,1.98,-.40)],[.04,.025,.007]),
([(.26,1.98,-.09),(.67,2.09,-.35),(1.04,2.28,-.38)],[.035,.022,.006])]
for p,r in branch_data:veins.append(tube('Articulated branch',p,r,live,steps=55,sides=14,twist=1.2,lobes=.14))
for o in veins:
 cols=[];base=color('#80533a')
 for v in o.data.vertices:
  x,y,z=v.co;t=.9+.12*noise.noise_vector(Vector((x*12,y*12,z*2))).x+.06*math.sin(x*90+y*70+z*4);cols.append(tuple(c*t for c in base))
 at=o.data.color_attributes.new(name='Tint',type='FLOAT_COLOR',domain='POINT');at.data.foreach_set('color',[q for c in cols for q in (*c,1)])
# Canopy is a hierarchy: seven branches, unequal clusters, forked branchlets, three-dimensional scale sprays.
# Each cluster deliberately leaves a gap to its neighbour. Positions are irregular and have real depth.
lobes=[
 # dominant crown, rising at the left and descending to the right
 ((.19,2.72,-.24),(.28,.16,.25),185),((.46,2.78,-.10),(.34,.21,.29),260),((.77,2.70,.01),(.37,.22,.30),290),((1.01,2.56,.02),(.31,.19,.26),230),((.47,2.55,.26),(.32,.17,.26),210),((.16,2.52,.05),(.27,.15,.24),190),((.65,2.56,-.33),(.31,.18,.22),180),
 # rising left arm
 ((-.37,2.27,-.02),(.31,.18,.24),215),((-.66,2.34,.10),(.30,.20,.26),225),((-.94,2.21,.10),(.27,.19,.25),215),((-.73,2.15,-.20),(.26,.16,.24),150),
 # first left branch, draped but open beneath
 ((-1.15,1.94,.09),(.28,.18,.24),220),((-1.34,1.82,.17),(.23,.16,.24),160),((-.94,1.84,.31),(.27,.16,.25),180),((-.79,1.96,.19),(.25,.16,.22),170),((-1.05,2.05,-.32),(.26,.15,.25),155),
 # subordinate right branch, deliberately lower and smaller
 ((.75,1.70,.07),(.27,.15,.24),170),((1.02,1.78,.18),(.29,.18,.26),210),((1.29,1.78,.18),(.24,.17,.22),170),((1.43,1.67,.19),(.16,.12,.18),105),
 # rear supporting layers visible through and around the foreground
 ((.91,2.29,-.38),(.30,.17,.22),180),((.47,2.18,-.36),(.26,.15,.22),145),((-.37,2.40,-.29),(.25,.15,.21),145)]
verts=[];faces=[];cols=[];twigv=[];twigf=[];twigc=[]
leafbase=color('#486333')
def needle(a,b,width,col):
 d=(b-a).normalized();n=d.cross(Vector((0,0,1))).normalized()
 if n.length<.1:n=d.cross(Vector((1,0,0))).normalized()
 q=d.cross(n);mid=a.lerp(b,.26);i=len(verts)
 verts.extend([a,mid+n*width,mid+q*width*.63,mid-n*width,mid-q*width*.63,b]);cols.extend([col]*6)
 faces.extend([(i,i+2,i+1),(i,i+3,i+2),(i,i+4,i+3),(i,i+1,i+4),(i+1,i+2,i+5),(i+2,i+3,i+5),(i+3,i+4,i+5),(i+4,i+1,i+5)])
def spray(p,d,length,col):
 d=d.normalized();side=d.cross(Vector((0,0,1))).normalized()
 if side.length<.2:side=Vector((1,0,0))
 up=d.cross(side).normalized();needle(p,p+d*length,.0022,col)
 for k in range(5):
  t=.10+k*.158;root=p+d*length*t;reach=length*(.36-.036*k)
  for sign in [-1,1]:
   tip=root+d*length*.30+side*sign*reach+up*length*random.uniform(-.09,.1)
   needle(root,tip,.0048*(1-t*.45),col)
   q=root.lerp(tip,.48);tip2=q+d*length*.25+side*sign*reach*.40+up*length*.025
   needle(q,tip2,.0030*(1-t*.40),tuple(min(1,c*1.06) for c in col))
for li,(center,size,count) in enumerate(lobes):
 c=B(center);sx,sy,sz=size
 # Branchlet fans tie the smaller volumes to a branch rather than filling a sphere.
 anchor=c+Vector((-.06,.015,-sy*.85))
 for j in range(5):
  angle=j*1.37+li*.7;end=c+Vector((math.cos(angle)*sx*.78,math.sin(angle)*sz*.70,sy*.15))
  o=tube('Fine twig',[tuple((p.x,p.z,-p.y)) for p in [anchor,anchor.lerp(end,.55)-Vector((0,0,.035)),end]],[.007,.004,.0007],live,steps=8,sides=5,lobes=.05)
  # Bake branches later into one object.
  veins.append(o)
 for j in range(count):
  a=random.random()*math.tau;r=math.sqrt(random.random());z=random.uniform(-.74,.84)*math.sqrt(max(.02,1-r*r))
  lobed=1+.09*math.sin(a*3+li*.6)+.06*math.sin(a*5)
  p=c+Vector((math.cos(a)*r*sx*lobed,math.sin(a)*r*sz*lobed,z*sy))
  # Mostly upwards-outwards with quiet locally aligned fans; no radial hedgehog.
  d=Vector((math.cos(a)*.45+random.uniform(-.24,.24),math.sin(a)*.4+random.uniform(-.2,.2),random.uniform(.45,.90))).normalized()
  tone=random.uniform(.89,1.10)*(1+z*.13);co=tuple(v*tone for v in leafbase)
  spray(p,d,random.uniform(.069,.108),co)
fol=make('Canopy',verts,faces,leafmat,cols)
# Consolidate living wood while preserving distinct foliage for the tiny permitted breeze.
bpy.ops.object.select_all(action='DESELECT')
for o in veins:o.select_set(True)
bpy.context.view_layer.objects.active=veins[0];bpy.ops.object.join();veins[0].name='Living bark and branch hierarchy'
# Missing vertex colors on fine twig tips use a natural bark tone.
for o in [veins[0]]:
 at=o.data.color_attributes.get('Tint')
 if at:
  co=color('#80533a')
  for d in at.data:
   if max(d.color[:3])<.0001:d.color=(*co,1)
# Blender file is a complete editable geometry asset. Export is local, no remote dependency.
for o in bpy.context.scene.objects:o.select_set(o.type=='MESH')
bpy.context.scene.render.engine='CYCLES';bpy.context.scene.cycles.samples=32
os.makedirs(OUT+'/prototype/public/models',exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=OUT+'/sculpt/bonsai-structural-study.blend')
# Surface.py performs the final compressed export after UV and texture creation.
meta={'vertices':sum(len(o.data.vertices) for o in bpy.context.scene.objects if o.type=='MESH'),'polygons':sum(len(o.data.polygons) for o in bpy.context.scene.objects if o.type=='MESH'),'objects':[o.name for o in bpy.context.scene.objects],'foliage_sprays':sum(x[2] for x in lobes),'seed':8196,'source':'Original generated geometry; no downloaded assets'}
open(OUT+'/sculpt/asset-metadata.json','w').write(json.dumps(meta,indent=2));print(json.dumps(meta))
