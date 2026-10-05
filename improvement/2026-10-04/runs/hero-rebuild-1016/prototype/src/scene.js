import * as THREE from 'three';
import { mergeGeometries, mergeVertices } from 'three/addons/utils/BufferGeometryUtils.js';
import { RoundedBoxGeometry } from 'three/addons/geometries/RoundedBoxGeometry.js';

// Give moss its own diffuse grain while keeping one continuous ground surface.
// This callback captures only its texture, so construction arrays can be collected.
function blendMossSurface(material,mossMap){
 material.onBeforeCompile=shader=>{
  shader.uniforms.gardenMossMap={value:mossMap};
  shader.vertexShader='attribute float mossCover; varying float vMossCover; varying vec2 vGardenUV;\n'+shader.vertexShader;
  shader.vertexShader=shader.vertexShader.replace('#include <begin_vertex>','#include <begin_vertex>\nvMossCover=mossCover;vGardenUV=uv;');
  shader.fragmentShader='uniform sampler2D gardenMossMap; varying float vMossCover; varying vec2 vGardenUV;\n'+shader.fragmentShader;
  shader.fragmentShader=shader.fragmentShader.replace('#include <map_fragment>',`#ifdef USE_MAP
   vec4 mineralGrain=texture2D(map,vMapUv);
   vec4 mossGrain=texture2D(gardenMossMap,vGardenUV*18.0);
   diffuseColor*=mix(mineralGrain,mossGrain*1.25,clamp(vMossCover,0.0,1.0));
  #endif`);
 };
 material.customProgramCacheKey=()=> 'garden-continuous-moss-v1';
}

// All scene dimensions are metres. A seeded composition makes live and still views identical.
export function createGarden(hero){
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
   if(kind==='moss')v=.52+.45*f+.17*(n-.5);
   if(kind==='soil')v=.47+.36*f+.17*n;
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
 for(const [name,material]of Object.entries(m))material.name=name;
 const subject=new THREE.Group();subject.name='bonsai';subject.scale.setScalar(.62);scene.add(subject);
 // One physical scale: the pot is 1.15m wide; the original sculpt shares its planted base.
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
 // A shared, continuous field keeps soil, moss and gravel on the same surface.
 const field=(x,z)=>Math.sin(x*1.73+Math.sin(z*1.17))*.48+Math.sin(z*3.41-x*2.27)*.28+Math.sin(x*7.13+z*5.91)*.16+Math.sin(x*15.7-z*12.3)*.08;
 const rockMaterial=m.stone.clone();rockMaterial.vertexColors=true;
 function stone(pos,scale,rotation=0,material=rockMaterial,parent=scene){
  const g=mergeVertices(new THREE.IcosahedronGeometry(1,7)),p=g.attributes.position,colors=[];
  const phase=pos[0]*2.31+pos[2]*1.77;
  for(let i=0;i<p.count;i++){
   let x=p.getX(i),y=p.getY(i),z=p.getZ(i);
   // Broad fracture planes, a sloping crown, and smaller worn irregularities.
   x=Math.min(x,.81-.23*y+.08*z);x=Math.max(x,-.79+.13*y-.12*z);
   z=Math.min(z,.78+.13*y+.11*x);z=Math.max(z,-.81+.15*x-.07*y);
   y=Math.min(y,.67+.19*x-.09*z);y=Math.max(y,-.81+.10*x);
   const wear=.025*field(x*2+phase,z*2-y),seam=.012*Math.sin(y*27+x*4+phase);
   p.setXYZ(i,x*(1+wear)+seam,y+wear*.55,z*(1+wear*.8));
   const grain=.87+.055*field(x*3+phase,z*3+y*2),vein=.032*Math.exp(-Math.pow((y+.18*x+.06*z-.11)*39,2));
   colors.push(grain+vein,grain+vein,grain*.98+vein);
  }
  if(material.vertexColors)g.setAttribute('color',new THREE.Float32BufferAttribute(colors,3));
  g.computeVertexNormals();const o=mesh(g,material,parent);o.position.set(...pos);o.scale.set(...scale);o.rotation.set(.09,rotation,.06);return o;
 }
 // The foundation extends below the gravel; the upper stone has a softened, worn arris.
 const foundationMaterial=m.stone.clone();foundationMaterial.color.set('#767b70');
 const foundation=mesh(new RoundedBoxGeometry(2.03,.23,1.23,3,.015),foundationMaterial,subject);foundation.position.set(0,.055,0);
 const slabG=new RoundedBoxGeometry(2.28,.16,1.43,5,.025),slabP=slabG.attributes.position;
 for(let i=0;i<slabP.count;i++){
  const x=slabP.getX(i),y=slabP.getY(i),z=slabP.getZ(i),edge=Math.max(Math.abs(x)/1.14,Math.abs(z)/.715);
  slabP.setXYZ(i,x,y+.0022*field(x*5,z*5)*(edge>.85?1:.25),z);
 }
 slabG.computeVertexNormals();
 const slab=mesh(slabG,m.stone,subject);slab.position.set(0,.18,0);slab.rotation.y=.04;
 // Shallow rectangular unglazed ceramic, with gently softened corners and a rolled lip.
 function ovalRing(y,rx,rz,radius,material){const g=new THREE.TorusGeometry(1,radius,8,100);g.rotateX(Math.PI/2);g.scale(rx,1,rz);const o=mesh(g,material,subject);o.position.y=y;return o;}
 function roundedRectRing(rx,rz,y){const out=[];for(let i=0;i<96;i++){const a=i/96*Math.PI*2,co=Math.cos(a),si=Math.sin(a);out.push(new THREE.Vector3(rx*Math.sign(co)*Math.pow(Math.abs(co),.21),y,rz*Math.sign(si)*Math.pow(Math.abs(si),.21)))}return out;}
 const levels=[[.78,.42,.286],[.79,.43,.315],[.91,.51,.526],[.925,.52,.55],[.895,.49,.558],[.871,.468,.522],[.76,.41,.322]],potPositions=[],potUV=[],potIndices=[];
 levels.forEach(([rx,rz,y],j)=>roundedRectRing(rx,rz,y).forEach((p,i)=>{potPositions.push(p.x,p.y,p.z);potUV.push(i/96,j/6);if(j<levels.length-1){const a=j*96+i,b=j*96+(i+1)%96;potIndices.push(a,a+96,b,b,a+96,b+96)}}));
 const potG=new THREE.BufferGeometry();potG.setAttribute('position',new THREE.Float32BufferAttribute(potPositions,3));potG.setAttribute('uv',new THREE.Float32BufferAttribute(potUV,2));potG.setIndex(potIndices);potG.computeVertexNormals();mesh(potG,m.ceramic,subject);
 for(const x of [-.56,.56])for(const z of [-.30,.30]){const foot=mesh(new RoundedBoxGeometry(.22,.054,.16,2,.012),m.ceramic,subject);foot.position.set(x,.283,z);}
 // Original sculpted asset: noncoplanar root mass, split heartwood and living branch hierarchy.
 hero.name='bonsai-sculpt';hero.traverse(o=>{if(o.isMesh){o.castShadow=o.receiveShadow=true;}});subject.add(hero);
 const canopy=hero.getObjectByName('Canopy');if(canopy){canopy.material.color.setScalar(1.65);canopy.material.roughness=.92;}if(!canopy)throw new Error('Sculpted canopy is missing');foliageGroups.push(canopy);
 // Preserve the planted canopy's seed while using its old clump positions as low soil relief.
 const soilMounds=[];
 for(let i=0;i<24;i++)soilMounds.push({x:rr(-.70,.70),z:rr(-.32,.32),rx:rr(.04,.14),h:rr(.008,.028),rz:rr(.04,.10),angle:rand()*6});
 const soilP=[],soilUV=[],soilC=[],soilI=[],soilRings=25,soilSides=96;
 const soilBrown=new THREE.Color('#594c36'),soilMoss=new THREE.Color('#4a5731');
 for(let j=0;j<=soilRings;j++){
  const r=j/soilRings,ring=roundedRectRing(.865*r,.46*r,0);
  for(let i=0;i<soilSides;i++){
   const {x,z}=ring[i];let y=.516+.021*Math.exp(-(x*x+z*z)*15);
   for(const t of soilMounds)y+=t.h*.16*Math.exp(-((x-t.x)**2/t.rx**2+(z-t.z)**2/t.rz**2)*.7)*(1-r*.7);
   y+=.002*field(x*12,z*12)*(1-r);
   const growth=Math.exp(-((x+.34)**2/.14+(z+.18)**2/.05))*.74+Math.exp(-((x-.46)**2/.025+(z-.22)**2/.03))*.52;
   const c=soilBrown.clone().lerp(soilMoss,Math.min(1,growth));c.multiplyScalar(.94+.09*field(x*5,z*5));
   soilP.push(x,y,z);soilUV.push(x*2,z*2);soilC.push(c.r,c.g,c.b);
   if(j<soilRings){const a=j*soilSides+i,b=j*soilSides+(i+1)%soilSides;soilI.push(a,b,a+soilSides,b,b+soilSides,a+soilSides);}
  }
 }
 const soilG=new THREE.BufferGeometry();soilG.setAttribute('position',new THREE.Float32BufferAttribute(soilP,3));soilG.setAttribute('uv',new THREE.Float32BufferAttribute(soilUV,2));soilG.setAttribute('color',new THREE.Float32BufferAttribute(soilC,3));soilG.setIndex(soilI);soilG.computeVertexNormals();
 const soilMaterial=m.soil.clone();soilMaterial.color.set('#ffffff');soilMaterial.vertexColors=true;soilMaterial.map=soilMaterial.map.clone();soilMaterial.map.repeat.set(.7,.7);soilMaterial.bumpMap=soilMaterial.map;soilMaterial.bumpScale=.008;mesh(soilG,soilMaterial,subject);
 // One continuous terrain replaces overlapping moss disks and their floating rim.
 const islands=[[-1.9,-.85,1.38,1.0],[-1.1,-3.3,3.9,1.55],[1.8,1.80,1.05,.78],[3.9,-1.0,1.9,2.0]];
 function terrainAt(x,z){
  let mass=0,core=0;
  for(const [cx,cz,rx,rz]of islands){
   const d=Math.hypot((x-cx+.10*field(x*.7,z*.7))/rx,(z-cz+.08*field(z*.8,x*.8))/rz);
   const edge=1+.10*field(x*.95+cx,z*.9-cz)+.04*field(x*2.2,z*2.2);
   const inward=(edge-d)*Math.min(rx,rz);
   mass=Math.max(mass,THREE.MathUtils.smoothstep(inward,-.045,.11));
   core=Math.max(core,THREE.MathUtils.smoothstep(inward,0,.8));
  }
  const gravel=-.025+.002*field(x*.7,z*.7),h=gravel+core*.085+mass*(.014+.008*field(x*1.8,z*1.8)+.002*field(x*6,z*6)+.0015*field(x*13,z*13));
  return {h,mass,core};
 }
 const terrainG=new THREE.PlaneGeometry(26,26,240,240);terrainG.rotateX(-Math.PI/2);
 const terrainP=terrainG.attributes.position,terrainUV=terrainG.attributes.uv,terrainC=[],terrainMoss=[],gravelColor=new THREE.Color('#a3a092'),mossColor=new THREE.Color('#53663e'),edgeColor=new THREE.Color('#666449');
 const groundAxis=v=>{const a=Math.abs(v)/13;return Math.sign(v)*(a<.8?a/.8*5.8:5.8+(a-.8)/.2*7.2)};
 for(let i=0;i<terrainP.count;i++){
  const x=groundAxis(terrainP.getX(i)),z=groundAxis(terrainP.getZ(i)),t=terrainAt(x,z);terrainP.setXYZ(i,x,t.h,z);terrainUV.setXY(i,(x+13)/26,(13-z)/26);
  const c=gravelColor.clone().lerp(edgeColor,THREE.MathUtils.smoothstep(t.mass,0,.45)).lerp(mossColor,THREE.MathUtils.smoothstep(t.mass,.20,1));
  c.multiplyScalar(1+(.018+.15*t.mass)*field(x*3.1,z*3.1));terrainC.push(c.r,c.g,c.b);terrainMoss.push(t.mass);
 }
 terrainG.setAttribute('color',new THREE.Float32BufferAttribute(terrainC,3));terrainG.setAttribute('mossCover',new THREE.Float32BufferAttribute(terrainMoss,1));terrainG.computeVertexNormals();
 const terrainMaterial=m.gravel.clone();terrainMaterial.color.set('#ffffff');terrainMaterial.vertexColors=true;terrainMaterial.bumpScale=.0035;blendMossSurface(terrainMaterial,m.moss.map);mesh(terrainG,terrainMaterial);
 const dummy=new THREE.Object3D();
 // The main stone shows its broad bedding face; smaller stones continue its line into the ground.
 stone([-2.05,.10,-.95],[.55,.46,.44],.4);stone([-2.44,.025,-.58],[.34,.24,.34],-1.2);stone([-1.85,.025,-.40],[.25,.18,.24],1.2);
 stone([1.7,.045,1.80],[.49,.29,.39],.7);stone([2.20,-.005,1.65],[.23,.15,.18],-.5);
 // Millimetre-scale moss tips follow the same height field, including its feathered edge.
 const tufts=new THREE.InstancedMesh(new THREE.ConeGeometry(.004,.006,5),mat('#536440'),4200);
 for(let i=0;i<4200;i++){
  const isl=islands[i%islands.length],a=rr(0,Math.PI*2),r=Math.sqrt(rand())*.96,x=isl[0]+Math.cos(a)*isl[2]*r,z=isl[1]+Math.sin(a)*isl[3]*r,t=terrainAt(x,z);
  dummy.position.set(x,t.h+.002,z);dummy.scale.setScalar(rr(.4,1.2)*t.mass);dummy.rotation.set(rr(-.3,.3),rr(0,6),rr(-.3,.3));dummy.updateMatrix();tufts.setMatrixAt(i,dummy.matrix);
 }tufts.receiveShadow=true;scene.add(tufts);
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
  for(let k=0;k<5;k++)box([x,.68+k*.50,-4.88],[2.19,.025,.04],m.cedar);
  for(let k=0;k<5;k++)box([x-1.02+k*.51,1.75,-4.87],[.014,2.16,.031],m.cedar);
 }
 box([1.45,2.96,-3.67],[10.45,.24,.22],m.timber);box([1.45,3.16,-3.67],[10.7,.10,.30],m.cedar);
 box([1.48,3.33,-4.40],[11.4,.17,3.25],m.timber);box([1.48,3.47,-4.42],[11.6,.12,3.43],mat('#555750'));
 for(let i=0;i<30;i++)box([-4.0+i*.38,3.25,-4.18],[.054,.14,2.8],m.cedar);
 box([6.7,1.75,-4.4],[.30,3.15,2.0],m.plaster);
 const architecture=new THREE.Group();architecture.name='ryokan';
 for(const piece of [...scene.children].slice(archStart))architecture.add(piece);
 architecture.position.set(.10,0,-3.1);architecture.rotation.y=-.06;architecture.scale.x=.78;scene.add(architecture);
 // A lower return wing gives the portrait view the same architectural depth as the wide view.
 const wingStart=scene.children.length;
 box([-4.72,.15,-1.15],[1.55,.30,6.55],m.stone);
 for(let i=0;i<35;i++)box([-4.62,.345,-4.30+i*.184],[1.74,.06,.176],i%6===0?m.cedar:m.timber);
 box([-3.75,.275,-1.15],[.10,.20,6.63],m.timber);
 box([-5.27,1.49,-1.15],[.18,2.31,6.6],m.plaster);
 for(const z of [-3.25,-1.05,1.15]){
  box([-5.12,1.40,z],[.035,1.85,1.97],m.paper);
  for(const y of [.50,1.12,1.76,2.32])box([-5.085,y,z],[.04,.021,2.03],m.timber);
  for(let k=0;k<4;k++)box([-5.07,1.41,z-.91+k*.606],[.04,1.88,.014],m.timber);
 }
 for(const z of [-4.35,-2.15,.05,2.05]){
  box([-3.92,1.51,z],[.12,2.35,.12],m.cedar);box([-3.92,.40,z],[.22,.12,.22],m.stone);
 }
 box([-3.92,2.72,-1.13],[.16,.19,6.70],m.timber);
 box([-4.60,2.84,-1.13],[2.45,.13,7.10],m.cedar);
 box([-4.60,2.94,-1.13],[2.55,.075,7.18],mat('#41453f'));
 for(let i=0;i<25;i++)box([-4.48,2.78,-4.52+i*.285],[2.30,.10,.045],m.cedar);
 const returnWing=new THREE.Group();returnWing.name='return-engawa';
 for(const piece of [...scene.children].slice(wingStart))returnWing.add(piece);returnWing.position.set(-2.6,0,-3.5);scene.add(returnWing);
 // The far wall closes the courtyard behind the specimen without flattening the open room.
 box([-3.6,.46,-10.0],[9.0,.94,.32],m.plaster);
 box([-3.6,.955,-10.0],[9.1,.07,.44],m.stone);
 // Left boundary recedes with irregular stones, plaster coping and a timber wicket.
 box([-8.5,.65,-2.6],[.32,1.3,10.8],m.plaster);box([-8.5,1.32,-2.6],[.50,.07,10.9],m.stone);
 for(let i=0;i<30;i++)stone([-8.3,.14,-7.8+i*.34],[.22,.25,.18],rand()*6);
 box([-5.5,.18,-10.0],[2.0,.36,.50],m.stone);
 for(let i=0;i<19;i++)box([-6.43+i*.103,1.32,-10.0],[.037,2.15,.04],m.timber);
 for(const y of [.36,1.3,2.31])box([-5.48,y,-10.03],[2.06,.065,.09],m.timber);
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
 for(const [x,z,h]of [[-4.2,-10.8,4.7],[-7.3,-9.5,4.5],[-7.8,-13,5.6],[8.2,-12.0,5.0],[7.7,-7.0,4.2]])backgroundTree(x,z,h);
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
 scene.add(new THREE.HemisphereLight('#a0afbc','#555344',1.25));
 const key=new THREE.DirectionalLight('#c0ccdd',.55);key.position.set(-3.5,7,5);key.target.position.set(0,0,-1);
 key.castShadow=true;key.shadow.mapSize.set(2048,2048);key.shadow.camera.left=-8;key.shadow.camera.right=8;key.shadow.camera.top=8;key.shadow.camera.bottom=-8;key.shadow.camera.near=.1;key.shadow.camera.far=22;key.shadow.bias=-.00025;key.shadow.normalBias=.02;key.shadow.radius=4;scene.add(key,key.target);
 const fill=new THREE.DirectionalLight('#a9b8c8',.60);fill.position.set(4,4,-1);scene.add(fill);
 const gardenLight=new THREE.SpotLight('#f3e3c9',52,13,.67,.96,2);gardenLight.position.set(-3.2,3.7,3.0);gardenLight.target.position.set(0,.96,0);gardenLight.castShadow=true;gardenLight.shadow.mapSize.set(1024,1024);gardenLight.shadow.bias=-.0002;gardenLight.shadow.normalBias=.018;gardenLight.shadow.radius=4;scene.add(gardenLight,gardenLight.target);
 m.paper.emissive.set('#c2945d');m.paper.emissiveIntensity=.028;
 const roomLight=new THREE.PointLight('#f4d3a5',2.6,5,2);roomLight.position.set(.72,2.3,-10.1);scene.add(roomLight);
 const verandaLight=new THREE.PointLight('#edcda5',1.7,4.2,2);verandaLight.position.set(2.2,2.75,-7.4);scene.add(verandaLight);
 const wingLight=new THREE.PointLight('#edcfaa',1.3,3.8,2);wingLight.position.set(-7.3,2.05,-4.15);scene.add(wingLight);
 scene.updateMatrixWorld(true);
 // Batch static masonry and joinery by material; preserve the single moving shoot mesh.
 function batch(parent){
  const groups=new Map();
  for(const o of [...parent.children])if(o.isMesh&&!o.isInstancedMesh&&!foliageGroups.includes(o)){
   const k=o.material.uuid+(o.geometry.attributes.color?'c':'');if(!groups.has(k))groups.set(k,[]);groups.get(k).push(o);
  }
  for(const objects of groups.values())if(objects.length>1){
   const geoms=objects.map(o=>{let g=o.geometry.clone();g.applyMatrix4(o.matrix);if(g.index){const indexed=g;g=g.toNonIndexed();indexed.dispose();}return g});
   const combined=mergeGeometries(geoms);if(combined){for(const o of objects){parent.remove(o);o.geometry.dispose();}mesh(combined,objects[0].material,parent);}geoms.forEach(g=>g.dispose());
  }
 }
 batch(scene);batch(subject);batch(architecture);batch(returnWing);scene.updateMatrixWorld(true);
 const bounds=new THREE.Box3().setFromObject(subject);
 return {scene,subject,bounds,foliageGroups,key,textures};
}
