import * as THREE from 'three';
import terrainDesign from './terrain-design.json';
import {RoundedBoxGeometry} from 'three/addons/geometries/RoundedBoxGeometry.js';
import {mergeGeometries,mergeVertices,toCreasedNormals} from 'three/addons/utils/BufferGeometryUtils.js';

export function random(seed=7241){let s=seed;return ()=>{s=(Math.imul(s,1664525)+1013904223)>>>0;return s/4294967296;};}
export function batches(scene,materials){
 const groups=new Map();
 const add=(geometry,material)=>{
  if(!geometry.getAttribute('grainPosition'))geometry.setAttribute('grainPosition',geometry.attributes.position.clone());
  if(!geometry.getAttribute('grainNormal'))geometry.setAttribute('grainNormal',geometry.attributes.normal.clone());
  if(!geometry.getAttribute('boardSeed'))geometry.setAttribute('boardSeed',new THREE.Float32BufferAttribute(new Float32Array(geometry.attributes.position.count).fill(.5),1));
  if(!groups.has(material))groups.set(material,[]);groups.get(material).push(geometry.index?geometry.toNonIndexed():geometry);
 };
 const box=(p,size,key,angle=0,yaw=0)=>{
  const g=new RoundedBoxGeometry(...size,1,Math.min(.005,...size.map(v=>v*.11)));
  g.setAttribute('grainPosition',g.attributes.position.clone());g.setAttribute('grainNormal',g.attributes.normal.clone());
  const seed=((Math.sin(p[0]*23.71+p[1]*17.17+p[2]*39.03)*43758.5)%1+1)%1;
  g.setAttribute('boardSeed',new THREE.Float32BufferAttribute(new Float32Array(g.attributes.position.count).fill(seed),1));
  g.rotateZ(angle);g.rotateY(yaw);g.translate(...p);add(g,key);
 };
 const done=()=>{let triangles=0;for(const [key,gs]of groups){const g=mergeGeometries(gs,false);const mesh=new THREE.Mesh(g,materials[key]);mesh.name='Garden architecture '+key;mesh.castShadow=mesh.receiveShadow=true;scene.add(mesh);triangles+=g.attributes.position.count/3;gs.forEach(x=>x.dispose());}return {drawCalls:groups.size,triangles};};
 return {add,box,done};
}
let terrainPixels=null,terrainWidth=0,terrainHeight=0;
export function setGroundField(image){
 const canvas=document.createElement('canvas');canvas.width=image.width;canvas.height=image.height;
 const ctx=canvas.getContext('2d',{willReadFrequently:true});ctx.drawImage(image,0,0);
 const data=ctx.getImageData(0,0,canvas.width,canvas.height);terrainPixels=data.data;terrainWidth=canvas.width;terrainHeight=canvas.height;
 if(terrainWidth!==terrainDesign.size||terrainHeight!==terrainDesign.size)throw Error('Ground field dimensions changed');
}
function fieldHeight(x,z){
 if(!terrainPixels)return terrainDesign.baseY;
 const [xmin,zmin,xmax,zmax]=terrainDesign.domain;
 const u=THREE.MathUtils.clamp((x-xmin)/(xmax-xmin)*terrainWidth-.5,0,terrainWidth-1),v=THREE.MathUtils.clamp((zmax-z)/(zmax-zmin)*terrainHeight-.5,0,terrainHeight-1);
 const i=Math.floor(u),j=Math.floor(v),a=u-i,b=v-j;
 const h=(i,j)=>terrainPixels[(Math.min(j,terrainHeight-1)*terrainWidth+Math.min(i,terrainWidth-1))*4+2]/255;
 const rise=(1-b)*THREE.MathUtils.lerp(h(i,j),h(i+1,j),a)+b*THREE.MathUtils.lerp(h(i,j+1),h(i+1,j+1),a);
 return terrainDesign.baseY+rise*terrainDesign.heightScale;
}
function gridSegments(parts){
 const values=[];for(const [start,end,step]of parts){const n=Math.ceil((end-start)/step);for(let i=0;i<n;i++)values.push(start+(end-start)*i/n);}values.push(parts.at(-1)[1]);return values;
}
const groundX=gridSegments([[-6,-4,.20],[-4,-1,.05],[-1,6,.18]]),groundZ=gridSegments([[-7,-3.7,.20],[-3.7,3,.055],[3,7,.20]]);
function groundCell(values,x){let lo=0,hi=values.length-1;while(hi-lo>1){const mid=(lo+hi)>>1;if(values[mid]>x)hi=mid;else lo=mid;}return Math.min(lo,values.length-2);}
export function groundHeight(x,z){
 if(x<groundX[0]||x>groundX.at(-1)||z<groundZ[0]||z>groundZ.at(-1))return -.029;
 const i=groundCell(groundX,x),j=groundCell(groundZ,z),x0=groundX[i],x1=groundX[i+1],z0=groundZ[j],z1=groundZ[j+1],u=(x-x0)/(x1-x0),v=(z-z0)/(z1-z0);
 const a=fieldHeight(x0,z0),b=fieldHeight(x1,z0),c=fieldHeight(x0,z1),d=fieldHeight(x1,z1);
 return u+v<=1?a+u*(b-a)+v*(c-a):d+(1-u)*(c-d)+(1-v)*(b-d);
}
export function groundGeometry(){
 const positions=[],uv=[],indices=[],nx=groundX.length-1,nz=groundZ.length-1;
 for(let j=0;j<=nz;j++)for(let i=0;i<=nx;i++){const x=groundX[i],z=groundZ[j];positions.push(x,fieldHeight(x,z),z);uv.push((x+6)/12,(z+7)/14);}
 for(let j=0;j<nz;j++)for(let i=0;i<nx;i++){const a=j*(nx+1)+i,b=a+1,c=a+nx+1,d=c+1;indices.push(a,c,b,b,c,d);}
 const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(positions,3));g.setAttribute('uv',new THREE.Float32BufferAttribute(uv,2));g.setIndex(indices);g.computeVertexNormals();return g;
}
export function stoneGeometry(center,scale,seed){
 const g=new THREE.IcosahedronGeometry(1,12),p=g.attributes.position;
 const planes=[[.08,1.,.12,.62],[1.,.10,.16,.89],[-.93,.14,.22,.94],[.12,.28,1.,.88],[-.50,.24,-.91,.95],[.82,.50,.22,.86],[-.37,.64,.72,.74]];
 for(let i=0;i<p.count;i++){
  let x=p.getX(i),y=p.getY(i),z=p.getZ(i);
  const f=1.+.065*Math.sin(x*4.8+z*3.9+seed)+.045*Math.cos(y*6.1-z*3.1+seed*.7);
  x*=f;z*=f;y*=1.+.045*Math.sin(x*4.+z*7.+seed);
  for(const [nx,ny,nz,limit]of planes){const dot=nx*x+ny*y+nz*z;if(dot>limit){const t=(dot-limit)/(nx*nx+ny*ny+nz*nz);x-=nx*t;y-=ny*t;z-=nz*t;}}
  p.setXYZ(i,x*scale[0]+center[0]+y*.06,y*scale[1]+center[1],z*scale[2]+center[2]);
 }
 g.deleteAttribute('normal');g.deleteAttribute('uv');const welded=mergeVertices(g,1e-5);welded.computeVertexNormals();const creased=toCreasedNormals(welded,.35);welded.dispose();return creased;
}
function branch(points,r0,r1,steps=13,radial=7){
 const path=new THREE.CatmullRomCurve3(points.map(p=>new THREE.Vector3(...p))),frames=path.computeFrenetFrames(steps,false);const ps=[],indices=[];
 for(let j=0;j<=steps;j++){
  const t=j/steps,c=path.getPoint(t),radius=THREE.MathUtils.lerp(r0,r1,Math.pow(t,.82));
  for(let i=0;i<radial;i++){const a=i/radial*Math.PI*2,variation=1+.11*Math.cos(a*3+j*.29)+.05*Math.sin(a*5-j*.4);const q=c.clone().addScaledVector(frames.normals[j],Math.cos(a)*radius*variation).addScaledVector(frames.binormals[j],Math.sin(a)*radius*variation*.91);ps.push(...q);}
 }
 for(let j=0;j<steps;j++)for(let i=0;i<radial;i++){const a=j*radial+i,b=j*radial+(i+1)%radial,c=a+radial,d=b+radial;indices.push(a,b,c,b,d,c);}
 const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(ps,3));g.setIndex(indices);g.computeVertexNormals();g.setAttribute('uv',new THREE.Float32BufferAttribute(new Float32Array(ps.length/3*2),2));return {g,path};
}
export function planting(scene,materials){
 const rng=random(90812),wood=[],rootCenters=[],leafGroups={maple:[],distant:[],shrub:[]},UP=new THREE.Vector3(0,1,0);
 const addBranch=(points,r0,r1,steps=7,radial=5)=>{const b=branch(points.map(p=>p.toArray()),r0,r1,steps,radial);wood.push(b.g);return b;};
 const leaf=(p,direction,length,kind,roll,shade)=>leafGroups[kind].push({p,direction,roll,length,color:new THREE.Color().setRGB(.75*shade,.84*shade,.64*shade)});
 function shortShoot(a,b,kind,exposure=1,leafSize=.052){
  const middle=a.clone().lerp(b,.55).addScaledVector(UP,.016),twig=addBranch([a,middle,b],kind==='shrub'?.0015:.0017,.00045,3,3);
  const axis=b.clone().sub(a).normalize(),across=new THREE.Vector3().crossVectors(axis,UP);if(across.lengthSq()<.01)across.set(1,0,0);across.normalize();
  // Bud clusters are deliberately short and unequal. Some inner nodes stay bare,
  // while outward terminal buds carry a little more leaf area toward open sky.
  const nodes=exposure<.65?[.38,.74,.91]:[.21,.48,.67,.87,.97];
  nodes.forEach((t,j)=>{
   const p=twig.path.getPoint(t),sign=j%2?1:-1;
   const direction=axis.clone().multiplyScalar(.28+.34*rng()).addScaledVector(across,sign*(.53+.24*rng())).addScaledVector(UP,.12+.34*rng()).normalize();
   const l=leafSize*(.74+.26*rng())*(j===nodes.length-1?.77:1);
   leaf(p,direction,l,kind,(rng()-.5)*1.13,.88+rng()*.18);
   if(j===1||j===3){const mate=direction.clone().addScaledVector(across,-sign*1.25).addScaledVector(axis,.38).normalize();leaf(p.clone().addScaledVector(axis,.003),mate,l*.82,kind,(rng()-.5)*.85,.88+rng()*.12);}
  });
 }
 // Physical, individually authored branch axes; the trees are not scale/seed
 // variants of one recursively repeated skeleton.
 const specimens=[
  {name:'Open layered maple',origin:[-2.72,0,-3.55],kind:'maple',spine:[[0,0,0],[.05,.39,.02],[-.02,.86,.07],[.11,1.29,.02],[.17,1.80,.05],[.20,2.15,-.08],[.11,2.48,-.10]],arms:[
   [.33,[[-.28,1.09,.06],[-.65,1.38,.22],[-1.00,1.47,.27]]],
   [.47,[[.30,1.30,.27],[.52,1.63,.45],[.83,1.88,.38]]],
   [.59,[[-.18,1.76,-.18],[-.45,2.03,-.38],[-.86,2.19,-.26]]],
   [.73,[[.05,2.04,.29],[-.28,2.37,.36],[-.59,2.49,.46]]],
   [.83,[[.48,2.29,.13],[.73,2.35,.21],[.96,2.45,.14]]]],size:.064},
  {name:'Receding inclined tree',origin:[-4.85,0,-5.7],kind:'distant',spine:[[0,0,0],[.12,.51,-.05],[.25,1.06,-.06],[.15,1.66,.05],[.34,2.26,.13],[.53,2.92,.05]],arms:[
   [.38,[[.57,1.26,.28],[.87,1.68,.32],[1.17,1.98,.16]]],
   [.55,[[-.21,1.80,-.16],[-.69,2.16,-.32],[-.97,2.53,-.31]]],
   [.74,[[.65,2.33,-.12],[1.03,2.50,-.30],[1.31,2.67,-.19]]],
   [.87,[[.15,2.70,.31],[-.08,3.02,.43],[-.33,3.16,.49]]]],size:.072},
  {name:'Distant broken canopy',origin:[-5.7,0,-8.3],kind:'distant',spine:[[0,0,0],[-.18,.86,.14],[-.10,1.42,.22],[-.29,2.04,.35],[-.13,2.66,.45],[-.33,3.25,.39]],arms:[
   [.35,[[-.60,1.37,.20],[-.97,1.90,.02],[-1.31,2.23,-.16]]],
   [.53,[[.27,2.05,.24],[.62,2.44,-.02],[.89,2.74,-.19]]],
   [.69,[[-.63,2.55,.51],[-1.00,2.89,.38],[-1.27,3.09,.12]]],
   [.80,[[.14,2.98,.61],[.44,3.39,.75],[.80,3.51,.83]]],
   [.89,[[-.65,3.36,.18],[-.82,3.66,-.02],[-1.05,3.74,-.19]]]],size:.079}
 ];
 const growthPlans=[
  [[.22,-1,.23,.62],[.40,1,.30,1],[.65,-1,.28,.9],[.81,1,.29,1],[.95,-1,.22,.9]],
  [[.29,1,.31,1],[.45,-1,.23,.55],[.69,1,.28,1],[.90,-1,.26,1]],
  [[.18,-1,.23,.5],[.46,1,.31,.9],[.57,-1,.27,1],[.80,1,.26,.8],[.95,-1,.19,1]],
  [[.34,1,.28,1],[.55,-1,.30,.8],[.75,1,.23,1],[.93,-1,.21,.9]],
  [[.27,-1,.29,.75],[.48,1,.33,1],[.74,-1,.28,.85],[.90,1,.25,1]]
 ];
 for(const [si,s]of specimens.entries()){
  const base=new THREE.Vector3(s.origin[0],groundHeight(s.origin[0],s.origin[2])-.004,s.origin[2]),at=p=>new THREE.Vector3(...p).add(base);
  const trunk=addBranch(s.spine.map(at),si===0?.040:.040,.0037,20,8);rootCenters.push({name:s.name,position:base.toArray()});
  const limbs=s.arms.map(([t,points],k)=>addBranch([trunk.path.getPoint(t),...points.map(at)],.0135-k*.0013,.0017,9,6));
  limbs.push({path:new THREE.CatmullRomCurve3([trunk.path.getPoint(.82),trunk.path.getPoint(.93),trunk.path.getPoint(1)])});
  limbs.forEach((limb,k)=>{
   const plan=growthPlans[(k+si)%growthPlans.length];
   plan.forEach(([t,handed,span,exposure],j)=>{
    const a=limb.path.getPoint(t),axis=limb.path.getTangent(t),side=new THREE.Vector3().crossVectors(axis,UP).normalize();span*=si===0?.68:.83;
    const b=a.clone().addScaledVector(axis,span*.68).addScaledVector(side,handed*span).addScaledVector(UP,.055+(j%3)*.035);
    const fork=addBranch([a,a.clone().lerp(b,.43).addScaledVector(UP,-.016),b],.0034,.0009,5,4);
    // Leaves along the middle forks interrupt exposed wood, not only its tips.
    const shootNodes=exposure<.65?[.45,.87]:[.19,.47,.78,.98];
    shootNodes.forEach((u,ii)=>{
     const p=fork.path.getPoint(u),advance=fork.path.getTangent(u),sign=(ii+j)%2?1:-1;
     const end=p.clone().addScaledVector(advance,.071+(ii%2)*.032).addScaledVector(axis,sign*.058).addScaledVector(UP,.039);
     shortShoot(p,end,s.kind,exposure,s.size);
    });
    if(j===1||j===3){const p=limb.path.getPoint(Math.max(.10,t-.12));shortShoot(p,p.clone().addScaledVector(axis,.14).addScaledVector(side,-handed*.07).addScaledVector(UP,.07),s.kind,.7,s.size*.92);}
   });
   if(si===0){
    const innerGroups=[[[.14,-1,.18],[.54,1,.17]],[[.10,1,.20],[.35,-1,.18],[.62,1,.15]],[[.19,-1,.15],[.49,1,.21]],[[.27,1,.17],[.56,-1,.18]],[[.12,-1,.18],[.43,1,.19]],[[.15,1,.15],[.59,-1,.13]]][k];
    for(const [t,handed,reach]of innerGroups){
     for(let arm=0;arm<2;arm++){
      const a=limb.path.getPoint(t+arm*.027),axis=limb.path.getTangent(t),side=new THREE.Vector3().crossVectors(axis,UP).normalize();
      const tip=a.clone().addScaledVector(axis,reach*(arm?.55:.87)).addScaledVector(side,handed*reach*(arm?-.45:.49)).addScaledVector(UP,arm?.105:.052);
      const fork=addBranch([a,a.clone().lerp(tip,.48).addScaledVector(UP,.02),tip],.0025,.00055,4,4);
      for(const [j,u]of [.16,.56,.94].entries()){
       const q=fork.path.getPoint(u),end=q.clone().addScaledVector(axis,.06).addScaledVector(side,(j%2?-1:1)*.043).addScaledVector(UP,.036);
       shortShoot(q,end,'maple',1,.061);
      }
     }
    }
   }
  });
 }
 // Low multi-axial shrubs: sprawling old wood supports unequal little crowns.
 // The three shrubs have different forks and heights; none radiates from one dot.
 const shrubs=[
  {origin:[-2.24,-.97],scale:1,axes:[
   [[-.17,0,-.08],[-.11,.10,-.03],[.10,.17,.02],[.32,.23,-.01]],
   [[.01,0,.01],[-.12,.12,.08],[-.31,.25,.14],[-.43,.27,.10]],
   [[-.07,0,-.02],[-.02,.18,-.12],[.10,.31,-.25],[.21,.30,-.32]],
   [[.04,0,.02],[.02,.14,.13],[.17,.20,.28],[.24,.19,.35]]]},
  {origin:[-2.07,-3.12],scale:.95,axes:[
   [[-.06,0,-.03],[-.17,.15,-.10],[-.32,.29,-.15],[-.48,.26,-.09]],
   [[.01,0,.05],[.13,.11,.14],[.28,.21,.18],[.44,.28,.11]],
   [[.06,0,-.02],[.05,.16,-.13],[-.07,.35,-.28],[-.19,.38,-.33]],
   [[-.03,0,.03],[-.12,.11,.19],[-.05,.18,.32],[.12,.20,.39]]]},
  {origin:[-3.08,-2.12],scale:1.15,axes:[
   [[-.08,0,-.01],[-.22,.11,.04],[-.39,.26,.18],[-.52,.25,.27]],
   [[.03,0,-.06],[.18,.15,-.16],[.39,.28,-.20],[.53,.31,-.15]],
   [[-.01,0,.03],[.02,.18,.12],[.16,.32,.27],[.34,.36,.34]],
   [[.02,0,-.02],[-.05,.19,-.13],[-.20,.41,-.29],[-.37,.43,-.30]],
   [[.04,0,.01],[.14,.11,.06],[.33,.18,.03],[.51,.17,-.02]]]}
 ];
 for(const [si,s]of shrubs.entries()){
  const [x,z]=s.origin,base=new THREE.Vector3(x,groundHeight(x,z)-.005,z);
  for(const [k,points]of s.axes.entries()){
   const rootX=x+points[0][0]*.63*s.scale,rootZ=z+points[0][2]*.64*s.scale,rootY=groundHeight(rootX,rootZ)-.007;
   const stem=addBranch(points.map(p=>new THREE.Vector3(x+p[0]*.63*s.scale,rootY+p[1]*.78*s.scale,z+p[2]*.64*s.scale)),.007,.0015,7,5);
   rootCenters.push({name:'Low shrub '+si+' axis '+k,position:[rootX,rootY,rootZ]});
   const nodes=k%2?[.32,.56,.82,.97]:[.23,.48,.71,.91];
   nodes.forEach((t,j)=>{
    const a=stem.path.getPoint(t),axis=stem.path.getTangent(t),side=new THREE.Vector3().crossVectors(axis,UP).normalize(),sign=(j+k+si)%2?1:-1;
    const end=a.clone().addScaledVector(axis,.13).addScaledVector(side,sign*(.12+(k%2)*.06)).addScaledVector(UP,.035+(j%2)*.032);
    const twig=addBranch([a,a.clone().lerp(end,.52).addScaledVector(UP,.025),end],.0024,.0007,4,4);
    for(const [ii,u]of [.31,.67,.97].entries()){
     const p=twig.path.getPoint(u),tip=p.clone().addScaledVector(axis,(ii%2?-.045:.065)).addScaledVector(side,sign*.051).addScaledVector(UP,.037);
     shortShoot(p,tip,'shrub',j===0?.56:1,.041+(si===2?.004:0));
    }
   });
  }
 }
 const woodMesh=new THREE.Mesh(mergeGeometries(wood.map(g=>g.toNonIndexed()),false),materials.treeBark);woodMesh.name='Individually authored garden branching';woodMesh.castShadow=woodMesh.receiveShadow=true;scene.add(woodMesh);
 function leafGeometry(kind){
  const outline=kind==='maple'?[[0,0,0],[-.18,.006,.24],[-.46,-.002,.24],[-.27,.013,.41],[-.54,.004,.68],[-.20,.021,.58],[0,.006,1.04],[.22,.018,.57],[.51,-.005,.72],[.28,.014,.40],[.44,-.005,.24],[.16,.007,.22]]:[[0,0,0],[-.19,.015,.23],[-.32,.03,.56],[0,.005,1.08],[.31,.015,.63],[.18,.01,.26]];
  const ps=outline.flat(),n=outline.length;ps.push(0,.072,.48,0,-.022,.46);const ix=[];for(let j=0;j<n;j++){const k=(j+1)%n;ix.push(j,k,n,k,j,n+1);}const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(ps,3));g.setIndex(ix);g.computeVertexNormals();return g;
 }
 const groupStats=[];const transform=new THREE.Object3D(),forward=new THREE.Vector3(0,0,1);
 for(const [kind,leaves]of Object.entries(leafGroups)){
  const geo=leafGeometry(kind),mesh=new THREE.InstancedMesh(geo,materials.leaves,leaves.length);mesh.name=kind==='maple'?'Branch attached garden leaves':'Branch attached '+kind+' garden leaves';
  leaves.forEach((l,i)=>{transform.position.copy(l.p);transform.quaternion.setFromUnitVectors(forward,l.direction);transform.rotateZ(l.roll);transform.scale.set(l.length*(kind==='shrub'?1.24:1),l.length,l.length);transform.updateMatrix();mesh.setMatrixAt(i,transform.matrix);mesh.setColorAt(i,l.color);});mesh.castShadow=mesh.receiveShadow=true;mesh.instanceMatrix.needsUpdate=true;mesh.computeBoundingSphere();scene.add(mesh);groupStats.push({kind,instances:leaves.length,trianglesPerLeaf:geo.index.count/3,triangles:geo.index.count/3*leaves.length});
 }
 return {rootCenters,design:'Three authored axes with concentrated inner short branches concealing selected arms; compact multi-axial shrubs return toward the stones; closed distant leaves retain a lower triangle count',specimens:specimens.map(({name,origin,kind,arms})=>({name,origin,kind,primaryArms:arms.length})),shrubOrigins:shrubs.map(s=>s.origin),branchTriangles:woodMesh.geometry.attributes.position.count/3,leafInstances:groupStats.reduce((s,g)=>s+g.instances,0),leafTriangles:groupStats.reduce((s,g)=>s+g.triangles,0),leafGroups:groupStats,rootGroundHeightSamples:[...specimens.map(s=>[s.origin[0],s.origin[2]]),...shrubs.map(s=>s.origin)].map(([x,z])=>({x,z,groundY:groundHeight(x,z)}))};
}
