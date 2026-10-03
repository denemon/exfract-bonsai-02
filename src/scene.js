import * as THREE from 'three';
import { mergeGeometries, mergeVertices } from 'three/addons/utils/BufferGeometryUtils.js';
import { RoundedBoxGeometry } from 'three/addons/geometries/RoundedBoxGeometry.js';

// All scene dimensions are metres. A seeded composition makes live and still views identical.
export function createGarden(){
 const scene=new THREE.Scene();
 scene.fog=new THREE.Fog('#111b2c',22,42);
 const rand=(()=>{let s=72819;return()=>{s=(Math.imul(s,1664525)+1013904223)>>>0;return s/4294967296}})();
 const rr=(a,b)=>a+(b-a)*rand();
 const V=(a)=>new THREE.Vector3(...a);
 const textures={};
 function texture(kind,size=512){
  if(textures[kind])return textures[kind];
  const c=document.createElement('canvas');c.width=c.height=size;const ctx=c.getContext('2d');
  const im=ctx.createImageData(size,size);
  const grids=[8,24,64].map(n=>({n,v:Array.from({length:n*n},()=>rand())}));
  function noise(x,y,g){const gx=x/size*g.n,gy=y/size*g.n,ix=Math.floor(gx),iy=Math.floor(gy),tx=gx-ix,ty=gy-iy;const at=(a,b)=>g.v[((b+g.n)%g.n)*g.n+(a+g.n)%g.n];const u=tx*tx*(3-2*tx),v=ty*ty*(3-2*ty);return THREE.MathUtils.lerp(THREE.MathUtils.lerp(at(ix,iy),at(ix+1,iy),u),THREE.MathUtils.lerp(at(ix,iy+1),at(ix+1,iy+1),u),v);}
  for(let y=0;y<size;y++)for(let x=0;x<size;x++){
   const i=(y*size+x)*4;const n=rand();
   const f=noise(x,y,grids[0])*.45+noise(x,y,grids[1])*.32+noise(x,y,grids[2])*.23;
   let v=.77+.20*f+.06*(n-.5);
   if(kind==='wood')v=.80+.04*Math.sin(x*.50+2*Math.sin(y*.009)+Math.sin(x*.017))+.07*(n-.5)+.09*f;
   if(kind==='dead')v=.83+.045*Math.sin(x*.70+2*Math.sin(y*.011))+.08*f+.09*(n-.5);
   if(kind==='gravel')v=.84+.18*(n-.5)+.04*f;
   if(kind==='stone')v=.70+.22*f+.06*(n-.5);
   if(kind==='moss')v=.62+.25*f+.15*(n-.5);
   if(kind==='soil')v=.5+.35*n;
   if(kind==='plaster')v=.91+.03*(n-.5)+.035*f;
   im.data[i]=im.data[i+1]=im.data[i+2]=Math.max(0,Math.min(255,v*255));im.data[i+3]=255;
  }ctx.putImageData(im,0,0);
  const t=new THREE.CanvasTexture(c);t.wrapS=t.wrapT=THREE.RepeatWrapping;t.colorSpace=THREE.SRGBColorSpace;t.anisotropy=4;
  textures[kind]=t;return t;
 }
 const mat=(color,roughness=1,extra={})=>new THREE.MeshStandardMaterial({color,roughness,metalness:0,...extra});
 function textured(color,kind,repeat,bump){const t=texture(kind).clone();t.needsUpdate=true;t.repeat.set(...repeat);return mat(color,1,{map:t,bumpMap:t,bumpScale:bump});}
 const m={dead:textured('#86725d','dead',[1,2],.008),bark:textured('#714b36','wood',[1,2],.008),
  stone:textured('#8b8b7b','stone',[2,2],.006),gravel:textured('#a3a092','gravel',[24,24],.006),
  moss:textured('#4c6036','moss',[4,4],.005),timber:textured('#655848','wood',[3,1],.003),
  cedar:textured('#665542','wood',[2,1],.007),plaster:textured('#d2c7ac','plaster',[4,4],.012),
  ceramic:textured('#897366','stone',[3,2],.002),soil:textured('#514533','soil',[4,4],.005),
  dark:mat('#292d24'),paper:textured('#ccbb94','plaster',[4,4],.003)};
 const subject=new THREE.Group();subject.name='bonsai';subject.scale.setScalar(.62);scene.add(subject);
 // One physical scale: the complete specimen is 1.78m high; the pot is 1.15m wide.
 // Architecture remains life size and sits beyond the garden, rather than sharing its scale.
 const foliageGroups=[];
 function mesh(geometry,material,parent=scene){const o=new THREE.Mesh(geometry,material);o.castShadow=o.receiveShadow=true;parent.add(o);return o;}
 function box(pos,scale,material,parent=scene){const o=mesh(new THREE.BoxGeometry(...scale),material,parent);o.position.set(...pos);return o;}
 function line(points,radii,material,parent=scene,{ribs=.08,flatten=1,sides=12,steps=56,twist=.7}={}){
  const curve=new THREE.CatmullRomCurve3(points.map(V));const f=curve.computeFrenetFrames(steps,false);const p=[],uv=[],idx=[];
  for(let j=0;j<=steps;j++){
   const t=j/steps,q=curve.getPointAt(t),k=t*(radii.length-1),k0=Math.floor(k),r=THREE.MathUtils.lerp(radii[k0],radii[Math.min(k0+1,radii.length-1)],k-k0);
   for(let i=0;i<=sides;i++){
    const a=i/sides*Math.PI*2+twist*t,rad=r*(1+ribs*Math.sin(i/sides*Math.PI*10+t*7)+ribs*.4*Math.sin(i*3+t*33));
    const v=q.clone().addScaledVector(f.normals[j],Math.cos(a)*rad).addScaledVector(f.binormals[j],Math.sin(a)*rad*flatten);
    p.push(v.x,v.y,v.z);uv.push(i/sides,t*3);
    if(j<steps&&i<sides){const n=j*(sides+1)+i;idx.push(n,n+1,n+sides+1,n+1,n+sides+2,n+sides+1);}
   }
  }const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(p,3));g.setAttribute('uv',new THREE.Float32BufferAttribute(uv,2));g.setIndex(idx);g.computeVertexNormals();mesh(g,material,parent);return curve;
 }
 function stone(pos,scale,rotation=0,material=m.stone,parent=scene){
  const g=mergeVertices(new THREE.IcosahedronGeometry(1,3)),p=g.attributes.position;
  for(let i=0;i<p.count;i++){const x=p.getX(i),y=p.getY(i),z=p.getZ(i);const d=1+.1*Math.sin(x*7+y*4+z*6)+.08*Math.sin(x*3-z*9);p.setXYZ(i,x*d,y*d,z*d)}
  g.computeVertexNormals();const o=mesh(g,material,parent);o.position.set(...pos);o.scale.set(...scale);o.rotation.set(.09,rotation,.06);return o;
 }
 // The base is deliberately low, with its lower course embedded in gravel.
 box([0,.075,0],[2.03,.17,1.23],m.stone,subject);
 const slab=mesh(new RoundedBoxGeometry(2.28,.16,1.43,3,.035),m.stone,subject);slab.position.set(0,.195,0);slab.rotation.y=.04;
 // Shallow rectangular unglazed ceramic, with gently softened corners and a rolled lip.
 function ovalRing(y,rx,rz,radius,material){const g=new THREE.TorusGeometry(1,radius,8,100);g.rotateX(Math.PI/2);g.scale(rx,1,rz);const o=mesh(g,material,subject);o.position.y=y;return o;}
 function roundedRectRing(rx,rz,y){const out=[];for(let i=0;i<96;i++){const a=i/96*Math.PI*2,co=Math.cos(a),si=Math.sin(a);out.push(new THREE.Vector3(rx*Math.sign(co)*Math.pow(Math.abs(co),.21),y,rz*Math.sign(si)*Math.pow(Math.abs(si),.21)))}return out;}
 const levels=[[.78,.42,.286],[.79,.43,.315],[.91,.51,.526],[.925,.52,.55],[.895,.49,.558],[.871,.468,.522],[.76,.41,.322]],potPositions=[],potUV=[],potIndices=[];
 levels.forEach(([rx,rz,y],j)=>roundedRectRing(rx,rz,y).forEach((p,i)=>{potPositions.push(p.x,p.y,p.z);potUV.push(i/96,j/6);if(j<levels.length-1){const a=j*96+i,b=j*96+(i+1)%96;potIndices.push(a,a+96,b,b,a+96,b+96)}}));
 const potG=new THREE.BufferGeometry();potG.setAttribute('position',new THREE.Float32BufferAttribute(potPositions,3));potG.setAttribute('uv',new THREE.Float32BufferAttribute(potUV,2));potG.setIndex(potIndices);potG.computeVertexNormals();mesh(potG,m.ceramic,subject);
 for(const x of [-.56,.56])for(const z of [-.30,.30])box([x,.282,z],[.22,.066,.16],m.ceramic,subject);
 const soilShape=new THREE.Shape();roundedRectRing(.865,.46,0).forEach((p,i)=>i?soilShape.lineTo(p.x,p.z):soilShape.moveTo(p.x,p.z));soilShape.closePath();const soil=mesh(new THREE.ShapeGeometry(soilShape),m.soil,subject);soil.rotation.x=-Math.PI/2;soil.position.y=.521;
 // Grooved shari: noncircular cross sections, a large leftward bow and a broad living vein.
 const trunkPoints=[[.06,.52,.02],[-.15,.78,.015],[-.47,1.13,-.02],[-.55,1.59,-.04],[-.27,1.94,-.025],[.14,2.16,.00],[.5,2.36,.03],[.64,2.64,.02]];
 const trunkRadii=[.24,.20,.19,.16,.126,.096,.070,.016];
 const trunkCurve=line(trunkPoints,trunkRadii,m.dead,subject,{flatten:.60,ribs:.17,sides:20,steps:140,twist:2.1});
 const vein=[[.17,.525,.09],[.05,.77,.12],[-.32,1.08,.103],[-.44,1.47,.054],[-.27,1.78,.079],[.1,2.00,.079],[.5,2.19,.12],[.72,2.33,.10]];
 line(vein,[.063,.047,.038,.030,.027,.023,.020,.005],m.bark,subject,{ribs:.20,sides:14,steps:120,flatten:.62,twist:2.7});
 // Longitudinal deadwood flutes split and travel around the sculpted form.
 const trunkFrames=trunkCurve.computeFrenetFrames(60,false);
 for(let i=0;i<14;i++){
  const pts=[];for(let j=0;j<=60;j++){const t=j/60,k=t*7,n=Math.min(6,Math.floor(k)),a=i/14*Math.PI*2+2.1*t,r=THREE.MathUtils.lerp(trunkRadii[n],trunkRadii[n+1],k-n)*(1+.17*Math.sin(i/14*Math.PI*10+t*7));const p=trunkCurve.getPointAt(t).addScaledVector(trunkFrames.normals[j],Math.cos(a)*r).addScaledVector(trunkFrames.binormals[j],Math.sin(a)*r*.60);pts.push(p.toArray());}
  line(pts,[.010,.008,.006,.006,.005,.003,.002,.0002],i%4===0?mat('#6f5f4d'):m.dead,subject,{sides:5,steps:85,flatten:.55,ribs:.18});
 }
 // Radial roots merge into uneven soil and a small moss mantle inside the pot.
 for(let i=0;i<8;i++){let a=i*.78;line([[.09,.69,0],[Math.cos(a)*.20,.56,Math.sin(a)*.16],[Math.cos(a)*rr(.37,.61),.524,Math.sin(a)*rr(.25,.36)]],[.057,.047,.003],i%3===0?m.dead:m.bark,subject,{sides:10,steps:30});}
 for(let i=0;i<24;i++)stone([rr(-.70,.70),.524,rr(-.32,.32)],[rr(.04,.14),rr(.008,.028),rr(.04,.10)],rand()*6,m.soil,subject);
 const pads=[
  {c:[.73,2.52,.04],s:[.88,.28,.44],n:420}, {c:[1.09,2.25,.18],s:[.57,.21,.37],n:225},
  {c:[.20,2.64,-.08],s:[.47,.21,.33],n:180}, {c:[-.97,1.83,.07],s:[.65,.21,.39],n:310},
  {c:[-1.35,1.59,.21],s:[.33,.13,.28],n:95}, {c:[.90,1.26,.16],s:[.61,.15,.37],n:185},
  {c:[1.40,1.83,-.12],s:[.35,.12,.26],n:90}, {c:[-.29,2.17,-.27],s:[.35,.12,.29],n:80},
  {c:[.53,2.23,-.43],s:[.42,.17,.30],n:105}, {c:[-1.12,1.96,-.34],s:[.31,.12,.24],n:70}
 ];
 const branches=[
  [[-.4,1.49,-.02],[-.72,1.61,.03],[-1.05,1.67,.04],[-1.44,1.63,.17]],
  [[-.25,1.91,0],[.27,2.11,.13],[.72,2.23,.10],[1.32,2.23,.08]],
  [[-.19,1.03,.03],[.12,1.11,.0],[.63,1.13,.14],[1.16,1.24,.10]],
  [[.1,2.15,0],[.3,2.40,-.03],[.75,2.54,0],[1.28,2.49,.02]],
  [[-.47,1.51,-.07],[-.74,1.72,-.33],[-1.12,1.95,-.36]],
  [[.18,2.14,-.05],[.35,2.20,-.35],[.80,2.26,-.40]],
  [[.39,2.25,0],[.91,2.02,-.17],[1.4,1.87,-.16]]
 ];branches.forEach((p,i)=>line(p,[.052,.038,.018,.002].slice(0,p.length),i===0?m.dead:m.bark,subject,{sides:10,steps:45,ribs:.15}));
 line([[-.53,1.33,-.02],[-.93,1.45,-.11],[-1.13,1.49,-.08],[-1.05,1.57,-.09]],[.057,.042,.022,.001],m.dead,subject,{steps:40,sides:10});
 line([[.5,2.35,-.01],[.67,2.68,-.05],[.62,2.87,-.10]],[.043,.017,.001],m.dead,subject,{sides:9,steps:45});
 line([[-.51,1.64,-.02],[-.60,1.94,-.15],[-.68,2.03,-.20]],[.032,.015,.001],m.dead,subject,{sides:9,steps:35});
 // Juniper-like foliage is made from individually tapered solid shoots, not leaf cards or spheres.
 const shootPositions=[],shootColors=[];const shootMaterial=mat('#ffffff',.91,{vertexColors:true});
 function shoot(a,b,width,color){
  const dir=b.clone().sub(a).normalize();const n=new THREE.Vector3(0,1,0).cross(dir).normalize();if(n.lengthSq()<.1)n.set(1,0,0);
  const v=new THREE.Vector3().crossVectors(dir,n).normalize();
  const l=a.clone().addScaledVector(n,width),r=a.clone().addScaledVector(n,-width),u=a.clone().addScaledVector(v,width*.72),d=a.clone().addScaledVector(v,-width*.6);
  for(const tri of [[l,u,b],[u,r,b],[r,d,b],[d,l,b]])for(const p of tri){shootPositions.push(p.x,p.y,p.z);shootColors.push(color.r,color.g,color.b);}
 }
 function sprig(center,length,dir){
  const col=new THREE.Color().setHSL(rr(.23,.29),rr(.36,.52),rr(.065,.145));
  const a=center.clone(),b=a.clone().addScaledVector(dir,length);
  for(let k=0;k<5;k++){
   const t=k/5,p=a.clone().lerp(b,t),side=new THREE.Vector3(Math.cos(k*2.45),rr(.12,.7),Math.sin(k*2.45)).normalize();
   const end=p.clone().addScaledVector(dir,length*.23).addScaledVector(side,length*rr(.20,.40));
   shoot(p,end,rr(.006,.010),col);
   for(let l=0;l<3;l++){const q=p.clone().lerp(end,l/3);const tip=q.clone().addScaledVector(side,length*.10).addScaledVector(dir,length*.18);shoot(q,tip,rr(.002,.0035),col.clone().multiplyScalar(rr(.88,1.14)));}
  }shoot(a,b,.004,col);
 }
 for(const pad of pads){
  const [cx,cy,cz]=pad.c,[sx,sy,sz]=pad.s;
  for(let i=0;i<pad.n;i++){
   const a=rand()*Math.PI*2,r=Math.sqrt(rand()),x=Math.cos(a)*r,z=Math.sin(a)*r;
   const lobes=1+.10*Math.sin(a*5)+.12*Math.sin(a*3+cy*7);
   const p=new THREE.Vector3(cx+x*sx*lobes,cy+rr(-.8,.7)*sy*Math.sqrt(1-r*r)+.025*Math.sin(x*11+z*4),cz+z*sz*lobes);
   const dir=new THREE.Vector3(x*.8+rr(-.4,.4),rr(.1,.6),z*.7+rr(-.3,.3)).normalize();
   for(let j=0;j<6;j++)sprig(p.clone().add(new THREE.Vector3(rr(-.03,.03),rr(-.025,.025),rr(-.035,.035))),rr(.055,.11),dir.clone().add(new THREE.Vector3(rr(-.5,.5),rr(-.3,.3),rr(-.5,.5))).normalize());
  }
 }
 const shoots=new THREE.BufferGeometry();shoots.setAttribute('position',new THREE.Float32BufferAttribute(shootPositions,3));shoots.setAttribute('color',new THREE.Float32BufferAttribute(shootColors,3));shoots.computeVertexNormals();
 const foliage=mesh(shoots,shootMaterial,subject);foliage.name='fine-foliage';foliageGroups.push(foliage);
 // Irregular soil-to-moss islands, including a thin sparse transition into gravel.
 const ground=mesh(new THREE.PlaneGeometry(26,26),m.gravel);ground.rotation.x=-Math.PI/2;ground.position.y=-.025;
 const islands=[[-1.9,-.85,1.38,1.0],[-1.1,-3.3,3.9,1.55],[1.8,1.80,1.05,.78],[3.9,-1.0,1.9,2.0]];
 function mossHeight(x,z){let h=-.05;for(const [cx,cz,rx,rz]of islands){const d=Math.hypot((x-cx)/rx,(z-cz)/rz);const a=Math.atan2(z-cz,x-cx);const edge=1+.09*Math.sin(a*5+cx)+.065*Math.sin(a*9);if(d<edge)h=Math.max(h,.022+.12*Math.pow(1-d/edge,1.5));}return h;}
 for(const [cx,cz,rx,rz]of islands){
  const p=[],uv=[],idx=[],colors=[],rings=22,sides=120;
  for(let j=0;j<=rings;j++)for(let i=0;i<=sides;i++){
   const a=i/sides*Math.PI*2,r=j/rings,edge=1+.09*Math.sin(a*5+cx)+.065*Math.sin(a*9);
   const x=cx+Math.cos(a)*rx*r*edge,z=cz+Math.sin(a)*rz*r*edge,y=.015+.12*Math.pow(1-r,1.5)+.015*Math.sin(x*7+z*2)*Math.sin(z*8)*r;
   p.push(x,y,z);uv.push(x*.55,z*.55);const c=new THREE.Color('#4c6036').lerp(new THREE.Color('#b5b0a0'),THREE.MathUtils.smoothstep(r,.90,1));colors.push(c.r,c.g,c.b);
   if(j<rings&&i<sides){const n=j*(sides+1)+i;idx.push(n,n+1,n+sides+1,n+1,n+sides+2,n+sides+1);}
  }const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(p,3));g.setAttribute('uv',new THREE.Float32BufferAttribute(uv,2));g.setAttribute('color',new THREE.Float32BufferAttribute(colors,3));g.setIndex(idx);g.computeVertexNormals();const mossSurface=m.moss.clone();mossSurface.color.set('#ffffff');mossSurface.vertexColors=true;mesh(g,mossSurface);
 }
 const dummy=new THREE.Object3D();
 // A restrained three-stone grouping, embedded rather than perched on the ground.
 stone([-1.42,.20,-.72],[.46,.34,.39],.4);stone([-1.92,.08,-.39],[.28,.20,.32],-1.2);stone([-1.35,.075,-.17],[.22,.16,.20],1.2);
 stone([1.7,.12,1.80],[.44,.25,.35],.7);stone([2.20,.035,1.65],[.19,.11,.16],-.5);
 // Sparse living moss tufts break the boundary without a manufactured lawn edge.
 const tufts=new THREE.InstancedMesh(new THREE.ConeGeometry(.006,.014,4),mat('#52653a'),4200);
 for(let i=0;i<4200;i++){const isl=islands[i%islands.length],a=rr(0,Math.PI*2),r=Math.sqrt(rand())*.96,x=isl[0]+Math.cos(a)*isl[2]*r,z=isl[1]+Math.sin(a)*isl[3]*r;dummy.position.set(x,Math.max(.024,mossHeight(x,z))+.01,z);dummy.scale.setScalar(rr(.4,1.2));dummy.rotation.set(rr(-.3,.3),rr(0,6),rr(-.3,.3));dummy.updateMatrix();tufts.setMatrixAt(i,dummy.matrix)}tufts.receiveShadow=true;scene.add(tufts);
 // Engawa: deck boards, foundation, deep openings, posts, double beams and layered eaves.
 const archStart=scene.children.length;
 box([1.55,.19,-4.48],[10.0,.38,2.15],m.stone);
 for(let i=0;i<48;i++)box([-3.35+i*.208,.425,-4.45],[.199,.065,2.2],i%5===0?m.cedar:m.timber);
 box([1.55,.33,-3.33],[10.1,.27,.12],m.timber);
 box([-2.04,1.65,-5.32],[2.72,2.45,.24],m.plaster);
 box([4.02,1.65,-5.32],[5.38,2.45,.24],m.plaster);
 // An open room recedes three metres, with solid side reveals and a separate back screen.
 box([.25,.44,-6.08],[2.28,.12,3.5],m.cedar);
 box([.25,3.02,-6.1],[2.50,.16,3.9],m.timber);
 box([-.94,1.7,-6.3],[.18,2.52,3.0],m.plaster);
 box([1.47,1.7,-6.3],[.18,2.52,3.0],m.plaster);
 box([.25,1.75,-7.82],[2.50,2.45,.16],m.paper);
 for(let i=0;i<7;i++)box([-.82+i*.36,1.75,-7.71],[.018,2.3,.035],m.timber);
 for(const y of [.63,1.25,1.88,2.49,2.90])box([.25,y,-7.70],[2.23,.02,.04],m.timber);
 box([.25,.66,-7.15],[1.7,.16,.48],m.cedar);
 for(const x of [-.43,.93])box([x,.52,-7.15],[.07,.24,.33],m.timber);
 for(const x of [-3.25,-.90,1.45,3.80,6.15]){
  box([x,1.84,-3.66],[.15,2.90,.15],m.timber);box([x,.52,-3.66],[.25,.15,.25],m.stone);
 }
 // The room has a floor, ceiling and side reveals; openings contain paper screens recessed 65 cm.
 box([1.52,.47,-4.7],[9.7,.09,1.8],m.cedar);box([1.52,3.05,-4.60],[10.1,.18,2.1],m.timber);
 for(const x of [-2.10,2.6,4.95]){
  box([x,1.78,-5.15],[2.20,2.35,.08],m.dark);
  box([x-.53,1.72,-4.93],[1.02,2.2,.045],m.paper);box([x+.55,1.72,-4.93],[1.02,2.2,.045],m.paper);
  for(const a of [-1.08,0,1.08])box([x+a,1.75,-4.885],[.035,2.31,.045],m.timber);
  for(let k=0;k<9;k++)box([x,.68+k*.252,-4.88],[2.19,.025,.04],m.cedar);
  for(let k=0;k<9;k++)box([x-1.02+k*.25,1.75,-4.87],[.014,2.16,.031],m.cedar);
 }
 box([1.45,2.96,-3.67],[10.45,.24,.22],m.timber);box([1.45,3.16,-3.67],[10.7,.10,.30],m.cedar);
 box([1.48,3.33,-4.40],[11.4,.17,3.25],m.timber);box([1.48,3.47,-4.42],[11.6,.12,3.43],mat('#555750'));
 for(let i=0;i<30;i++)box([-4.0+i*.38,3.25,-4.18],[.054,.14,2.8],m.cedar);
 box([6.7,1.75,-4.4],[.30,3.15,2.0],m.plaster);
 const architecture=new THREE.Group();architecture.name='ryokan';
 for(const piece of [...scene.children].slice(archStart))architecture.add(piece);
 architecture.position.set(1.8,0,-1.4);architecture.rotation.y=-.07;scene.add(architecture);
 // A lower return wing gives the portrait view the same architectural depth as the wide view.
 const wingStart=scene.children.length;
 box([-4.72,.15,-1.15],[1.55,.30,6.55],m.stone);
 for(let i=0;i<35;i++)box([-4.62,.345,-4.30+i*.184],[1.74,.06,.176],i%6===0?m.cedar:m.timber);
 box([-3.75,.275,-1.15],[.10,.20,6.63],m.timber);
 box([-5.27,1.49,-1.15],[.18,2.31,6.6],m.plaster);
 for(const z of [-3.25,-1.05,1.15]){
  box([-5.12,1.40,z],[.035,1.85,1.97],m.paper);
  for(const y of [.50,.80,1.12,1.44,1.76,2.07,2.32])box([-5.085,y,z],[.04,.021,2.03],m.timber);
  for(let k=0;k<7;k++)box([-5.07,1.41,z-.91+k*.303],[.04,1.88,.014],m.timber);
 }
 for(const z of [-4.35,-2.15,.05,2.05]){
  box([-3.92,1.51,z],[.12,2.35,.12],m.cedar);box([-3.92,.40,z],[.22,.12,.22],m.stone);
 }
 box([-3.92,2.72,-1.13],[.16,.19,6.70],m.timber);
 box([-4.60,2.84,-1.13],[2.45,.13,7.10],m.cedar);
 box([-4.60,2.94,-1.13],[2.55,.075,7.18],mat('#41453f'));
 for(let i=0;i<25;i++)box([-4.48,2.78,-4.52+i*.285],[2.30,.10,.045],m.cedar);
 const returnWing=new THREE.Group();returnWing.name='return-engawa';
 for(const piece of [...scene.children].slice(wingStart))returnWing.add(piece);scene.add(returnWing);
 // The far wall closes the courtyard behind the specimen without flattening the open room.
 box([-3.15,.81,-8.0],[8.3,1.65,.26],m.plaster);
 box([-3.15,1.67,-8.0],[8.4,.09,.42],m.stone);
 // Left boundary recedes with irregular stones, plaster coping and a timber wicket.
 box([-5.4,.90,-.4],[.30,1.8,10],m.plaster);box([-5.4,1.83,-.4],[.49,.10,10.2],m.stone);
 for(let i=0;i<30;i++)stone([-5.2,.14,-5.1+i*.34],[.22,.25,.18],rand()*6);
 box([-4.27,.18,-5.25],[2.0,.36,.50],m.stone);
 for(let i=0;i<19;i++)box([-5.2+i*.103,1.32,-5.25],[.037,2.15,.04],m.timber);
 for(const y of [.36,1.3,2.31])box([-4.25,y,-5.28],[2.06,.065,.09],m.timber);
 // Background vegetation consists of branching stems and small angled solid leaves.
 const bgLeaves=[],bgColors=[];
 function leaf(center,dir,size,color){
  const n=new THREE.Vector3(dir.z*.7,.4,-dir.x).normalize().multiplyScalar(size*.30),a=center.clone(),b=a.clone().addScaledVector(dir,size),mid=a.clone().lerp(b,.46).add(new THREE.Vector3(0,.015,0));
  for(const tri of [[a,mid.clone().add(n),b],[a,b,mid.clone().sub(n)]])for(const p of tri){bgLeaves.push(p.x,p.y,p.z);bgColors.push(color.r,color.g,color.b)}
 }
 function backgroundTree(x,z,h){
  const root=[x,.0,z];line([root,[x-.1,h*.38,z+.05],[x+.17,h*.72,z-.13],[x+.1,h,z]],[.083,.057,.027,.003],m.bark,scene,{sides:8,steps:30});
  for(let i=0;i<14;i++){
   const a=i*2.4,level=rr(.43,.95),reach=rr(.6,1.35)*(1-level*.40),cx=x+Math.cos(a)*reach,cz=z+Math.sin(a)*reach,cy=h*level;
   line([[x,h*level*.9,z],[cx,cy,cz]],[.020,.002],m.bark,scene,{sides:6,steps:8});
   for(let j=0;j<240;j++){const t=rand()*Math.PI*2,r=Math.sqrt(rand()),p=new THREE.Vector3(cx+Math.cos(t)*r*.65,cy+rr(-.30,.31),cz+Math.sin(t)*r*.55);leaf(p,new THREE.Vector3(rr(-1,1),rr(.0,.35),rr(-1,1)).normalize(),rr(.08,.19),new THREE.Color().setHSL(rr(.20,.29),rr(.22,.42),rr(.09,.20)));}
  }
 }
 for(const [x,z,h]of [[-3.6,-5.7,3.6],[-4.2,-8.0,4.4],[-6.2,-6.0,4.8],[-6.8,-9.2,5.5],[8.2,-7.4,4.8],[7.3,-4.6,3.7]])backgroundTree(x,z,h);
 const bgG=new THREE.BufferGeometry();bgG.setAttribute('position',new THREE.Float32BufferAttribute(bgLeaves,3));bgG.setAttribute('color',new THREE.Float32BufferAttribute(bgColors,3));bgG.computeVertexNormals();mesh(bgG,mat('#ffffff',.92,{vertexColors:true,side:THREE.DoubleSide}));
 // A quiet, fixed star field. The horizon has airglow; stars never blink or move.
 const skyCanvas=document.createElement('canvas');skyCanvas.width=4096;skyCanvas.height=2048;
 const skyContext=skyCanvas.getContext('2d'),skyGradient=skyContext.createLinearGradient(0,0,0,2048);
 skyGradient.addColorStop(0,'#070d1e');skyGradient.addColorStop(.35,'#101e36');skyGradient.addColorStop(.50,'#253044');skyGradient.addColorStop(.64,'#101b2c');skyGradient.addColorStop(1,'#080d17');
 skyContext.fillStyle=skyGradient;skyContext.fillRect(0,0,4096,2048);
 for(let i=0;i<1400;i++){
  const x=rr(0,4096),y=rr(12,982),radius=rr(.35,1.15),opacity=rr(.30,.78)*(1-THREE.MathUtils.smoothstep(y,820,990));
  skyContext.fillStyle=`rgba(208,219,239,${opacity})`;skyContext.beginPath();skyContext.arc(x,y,radius,0,Math.PI*2);skyContext.fill();
 }
 const skyTexture=new THREE.CanvasTexture(skyCanvas);skyTexture.mapping=THREE.EquirectangularReflectionMapping;skyTexture.colorSpace=THREE.SRGBColorSpace;scene.background=skyTexture;
 // Cool moonlight, warm concealed garden light and paper screens share one night exposure.
 scene.add(new THREE.HemisphereLight('#a0afbc','#44453c',.95));
 const key=new THREE.DirectionalLight('#c0ccdd',.78);key.position.set(-3.5,7,5);key.target.position.set(0,0,-1);
 key.castShadow=true;key.shadow.mapSize.set(2048,2048);key.shadow.camera.left=-8;key.shadow.camera.right=8;key.shadow.camera.top=8;key.shadow.camera.bottom=-8;key.shadow.camera.near=.1;key.shadow.camera.far=22;key.shadow.bias=-.00025;key.shadow.normalBias=.02;key.shadow.radius=4;scene.add(key,key.target);
 const fill=new THREE.DirectionalLight('#9eafbd',.40);fill.position.set(4,4,-1);scene.add(fill);
 const gardenLight=new THREE.SpotLight('#f3e3c9',34,11,.58,.92,2);gardenLight.position.set(-2.2,3.0,2.0);gardenLight.target.position.set(0,.96,0);gardenLight.castShadow=true;gardenLight.shadow.mapSize.set(1024,1024);gardenLight.shadow.bias=-.0002;gardenLight.shadow.normalBias=.018;gardenLight.shadow.radius=4;scene.add(gardenLight,gardenLight.target);
 m.paper.emissive.set('#c2945d');m.paper.emissiveIntensity=.028;
 const roomLight=new THREE.PointLight('#f4d3a5',2.6,5,2);roomLight.position.set(2.52,2.3,-8.05);scene.add(roomLight);
 const verandaLight=new THREE.PointLight('#edcda5',1.7,4.2,2);verandaLight.position.set(4.6,2.75,-5.5);scene.add(verandaLight);
 const wingLight=new THREE.PointLight('#edcfaa',1.3,3.8,2);wingLight.position.set(-4.7,2.05,-.65);scene.add(wingLight);
 scene.updateMatrixWorld(true);
 // Batch static masonry and joinery by material; preserve the single moving shoot mesh.
 function batch(parent){
  const groups=new Map();
  for(const o of [...parent.children])if(o.isMesh&&!o.isInstancedMesh&&!foliageGroups.includes(o)){
   const k=o.material.uuid+(o.geometry.attributes.color?'c':'');if(!groups.has(k))groups.set(k,[]);groups.get(k).push(o);
  }
  for(const objects of groups.values())if(objects.length>1){
   const geoms=objects.map(o=>{let g=o.geometry.clone();g.applyMatrix4(o.matrix);if(g.index)g=g.toNonIndexed();return g});
   const combined=mergeGeometries(geoms);if(combined){for(const o of objects)parent.remove(o);mesh(combined,objects[0].material,parent);}geoms.forEach(g=>g.dispose());
  }
 }
 batch(scene);batch(subject);batch(architecture);batch(returnWing);scene.updateMatrixWorld(true);
 const bounds=new THREE.Box3().setFromObject(subject);
 return {scene,subject,bounds,foliageGroups,key,textures};
}
