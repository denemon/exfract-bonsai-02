import * as THREE from 'three';
import {RoundedBoxGeometry} from 'three/addons/geometries/RoundedBoxGeometry.js';
import {mergeGeometries,mergeVertices} from 'three/addons/utils/BufferGeometryUtils.js';

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
export function groundHeight(x,z){
 const moss=(x,z)=>Math.min((Math.hypot((x+2.38)/1.65,(z+1.12)/3.8)-1)*1.65,(Math.hypot((x+1.27)/.81,(z-.67)/.62)-1)*.62,(Math.hypot((x-2.06)/.73,(z+2.6)/2.5)-1)*.73);
  const m=THREE.MathUtils.smoothstep(-moss(x,z),-.03,.15);
  const swell=Math.exp(-((x+2.48)**2/1.1+(z+.78)**2/1.8))*.013+Math.exp(-((x+1.62)**2/.26+(z-.24)**2/.39))*.009;
  const h=-.022+m*(.015+swell+.003*Math.sin(x*8.4+z*5.3))+.0012*Math.sin(x*5.4)*Math.sin(z*4.3);
  return h;
}
export function groundGeometry(){
 const positions=[],uv=[],indices=[],n=128,xmin=-6,xmax=6,zmin=-7,zmax=7;
 for(let j=0;j<=n;j++)for(let i=0;i<=n;i++){
  const x=xmin+(xmax-xmin)*i/n,z=zmin+(zmax-zmin)*j/n;
  const h=groundHeight(x,z);
  positions.push(x,h,z);uv.push(i/n,j/n);
 }
 for(let j=0;j<n;j++)for(let i=0;i<n;i++){const a=j*(n+1)+i,b=a+1,c=a+n+1,d=c+1;indices.push(a,c,b,b,c,d);}
 const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(positions,3));g.setAttribute('uv',new THREE.Float32BufferAttribute(uv,2));g.setIndex(indices);g.computeVertexNormals();return g;
}
export function stoneGeometry(center,scale,seed){
 const g=new THREE.IcosahedronGeometry(1,6);const p=g.attributes.position;
 for(let i=0;i<p.count;i++){
  let x=p.getX(i),y=p.getY(i),z=p.getZ(i);
  const f=1+.085*Math.sin(x*6.4+z*4.7+seed)+.065*Math.cos(y*7.1-z*3.7+seed*.7)+.045*Math.sin(z*10.4+x*4.);
  x*=f;y*=1+.065*Math.sin(x*4+z*8+seed);z*=f;
  if(y>.57)y=.57+(y-.57)*.38;
  p.setXYZ(i,x*scale[0]+center[0]+y*.07,y*scale[1]+center[1],z*scale[2]+center[2]);
 }
 g.deleteAttribute('normal');g.deleteAttribute('uv');const welded=mergeVertices(g,1e-5);welded.computeVertexNormals();return welded;
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
 const rng=random(77013),wood=[],leaves=[];const UP=new THREE.Vector3(0,1,0);
 const addBranch=(points,r0,r1,steps=9,radial=6)=>{const b=branch(points.map(p=>p.toArray()),r0,r1,steps,radial);wood.push(b.g);return b;};
 function leafyShoot(a,b,width,count){
  const axis=b.clone().sub(a).normalize();const sideAxis=new THREE.Vector3().crossVectors(axis,UP);if(sideAxis.lengthSq()<.01)sideAxis.set(1,0,0);sideAxis.normalize();
  const middle=a.clone().lerp(b,.58).addScaledVector(UP,.022);
  const twig=addBranch([a,middle,b],width,.0006,5,5);
  const phase=rng();
  for(let i=0;i<count;i++){
   const t=.19+(i+.25+rng()*.35)/count*.79,p=twig.path.getPoint(t),side=i%2?1:-1;
   const direction=sideAxis.clone().multiplyScalar(side*(.72+rng()*.24)).addScaledVector(axis,.15+rng()*.38).addScaledVector(UP,.15+rng()*.42).normalize();
   const length=.036+rng()*.026;const roll=(rng()-.5)*.75;
   leaves.push({p,direction,roll,scale:[length*(.82+rng()*.2),length,length*(.88+rng()*.23)],color:new THREE.Color().setRGB(.73+phase*.11+rng()*.12,.78+phase*.10+rng()*.12,.61+phase*.10+rng()*.12)});
  }
 }
 // Each specimen has its own main axes and fork positions. Branches are not
 // alternating rungs generated from a common height sequence.
 const specimens=[
  {name:'Near left garden tree',origin:[-2.72,-.007,-3.55],height:2.43,spine:[[0,0,0],[-.018,.20,.013],[.025,.43,-.012],[-.016,.64,-.02],[.052,.84,-.04],[.033,1,-.025]],arms:[
   [.30,[-.13,.42,.026],[-.40,.61,.14]],
   [.41,[.14,.56,-.035],[.32,.74,-.13]],
   [.58,[-.13,.70,-.02],[-.31,.85,-.17]],
   [.72,[.16,.83,.02],[.26,1.035,.09]],
   [.83,[-.045,.98,.045],[-.16,1.12,.045]]]},
  {name:'Receding left tree',origin:[-4.85,-.02,-5.7],height:3.0,spine:[[0,0,0],[.043,.24,-.012],[.095,.47,-.01],[.055,.70,-.055],[.13,.92,-.04],[.19,1,.015]],arms:[
   [.26,[.20,.38,.045],[.37,.64,.12]],
   [.48,[-.025,.60,-.08],[-.18,.88,-.11]],
   [.61,[.19,.76,-.05],[.37,.87,-.18]],
   [.80,[.02,.93,.10],[-.075,1.12,.16]]]},
  {name:'Distant grove tree',origin:[-5.7,-.02,-8.3],height:3.4,spine:[[0,0,0],[-.052,.31,.06],[-.025,.51,.08],[-.092,.73,.14],[-.04,.90,.17],[-.10,1.07,.16]],arms:[
   [.39,[-.20,.48,.025],[-.37,.75,-.07]],
   [.49,[.08,.70,.11],[.23,.86,.03]],
   [.70,[-.18,.83,.20],[-.33,1.04,.18]],
   [.81,[.045,1.01,.19],[.16,1.19,.28]],
   [.91,[-.18,1.10,.11],[-.23,1.26,-.01]]]}];
 for(const [specimenIndex,s]of specimens.entries()){
  const o=new THREE.Vector3(...s.origin),at=p=>new THREE.Vector3(...p).multiplyScalar(s.height).add(o);
  const trunk=addBranch(s.spine.map(at),.050+specimenIndex*.004,.0044,20,9);
  const limbs=s.arms.map(([fraction,mid,end],k)=>addBranch([trunk.path.getPoint(fraction),at(mid),at(end)],.020*(1-k*.11),.0016,10,7));
  // The top itself bears shoots; the primary axis is not a bare needle.
  limbs.push({path:new THREE.CatmullRomCurve3([trunk.path.getPoint(.82),trunk.path.getPoint(.92),trunk.path.getPoint(1)])});
  limbs.forEach((limb,k)=>{
   const positions=k%3===0?[.34,.51,.74,.90]:k%3===1?[.42,.65,.84]:[.27,.49,.63,.81,.95];
   positions.forEach((t,j)=>{
    const a=limb.path.getPoint(t),axis=limb.path.getTangent(t),spread=new THREE.Vector3().crossVectors(axis,UP).normalize();
    const handed=(j+k+specimenIndex)%2?1:-1;
    const length=(.12+rng()*.16)*(1.-t*.25),b=a.clone().addScaledVector(axis,.06+rng()*.10).addScaledVector(spread,handed*length).addScaledVector(UP,.07+rng()*.09);
    const secondary=addBranch([a,a.clone().lerp(b,.45).addScaledVector(UP,-.018),b],.0032,.0010,6,5);
    const fork=secondary.path.getPoint(.48+rng()*.17);
    const c=b.clone().addScaledVector(axis,.035+rng()*.055).addScaledVector(spread,-handed*(.07+rng()*.11)).addScaledVector(UP,.028);
    leafyShoot(fork,c,.0017,10+Math.floor(rng()*6));
    leafyShoot(secondary.path.getPoint(.24),b,.0020,12+Math.floor(rng()*9));
    if(j%3===1)leafyShoot(b,b.clone().addScaledVector(axis,.11).addScaledVector(UP,.035),.0011,7);
   });
  });
 }
 // Low shrubs keep their footprints. Unequal woody axes carry terminal fans;
 // neither spherical surfaces nor uniform leaf-filled ellipsoids are used.
 for(const [x,z,size]of [[-2.21,-.92,.42],[-1.65,-2.78,.49],[-3.0,-2.0,.58]]){
  const phase=rng()*Math.PI*2;
  for(let k=0;k<11;k++){
   const angle=phase+k*2.39996+(rng()-.5)*.25,spread=.48+rng()*.47;
   const a=new THREE.Vector3(x+(rng()-.5)*.08,-.004,z+(rng()-.5)*.08);
   const b=new THREE.Vector3(x+Math.cos(angle)*size*spread,size*(.34+rng()*.49),z+Math.sin(angle)*size*spread);
   const stem=addBranch([a,a.clone().lerp(b,.54).add(new THREE.Vector3(0,.025,0)),b],.006,.0018,7,6);
   for(let j=0;j<4;j++){
    const t=.38+j*.17,start=stem.path.getPoint(t),az=angle+(j%2?1:-1)*(.6+rng()*.6),tip=start.clone().add(new THREE.Vector3(Math.cos(az)*(.12+rng()*.08),.06+rng()*.07,Math.sin(az)*(.12+rng()*.08)));
    leafyShoot(start,tip,.0018,11+Math.floor(rng()*7));
   }
  }
 }
 const woodMesh=new THREE.Mesh(mergeGeometries(wood.map(g=>g.toNonIndexed()),false),materials.treeBark);woodMesh.name='Irregular garden tree and shrub branching';woodMesh.castShadow=woodMesh.receiveShadow=true;scene.add(woodMesh);
 const leaf=new THREE.BufferGeometry();leaf.setAttribute('position',new THREE.Float32BufferAttribute([0,0,0,-.20,.015,.25,-.33,.048,.58,0,.045,1.13,.30,.035,.60,.19,.012,.25,0,.092,.55,0,-.021,.54],3));const indices=[];for(let j=0;j<6;j++){const k=(j+1)%6;indices.push(j,k,6,k,j,7);}leaf.setIndex(indices);leaf.computeVertexNormals();
 const mesh=new THREE.InstancedMesh(leaf,materials.leaves,leaves.length);mesh.name='Branch attached garden leaves';const transform=new THREE.Object3D(),forward=new THREE.Vector3(0,0,1);
 leaves.forEach((l,i)=>{transform.position.copy(l.p);transform.quaternion.setFromUnitVectors(forward,l.direction);transform.rotateZ(l.roll);transform.scale.set(...l.scale);transform.updateMatrix();mesh.setMatrixAt(i,transform.matrix);mesh.setColorAt(i,l.color);});mesh.castShadow=mesh.receiveShadow=true;mesh.instanceMatrix.needsUpdate=true;mesh.computeBoundingSphere();scene.add(mesh);
 return {design:'Three individually authored main axes and unequal forks; attached shoots face outward/upward; fixed tree/shrub origins',specimens:specimens.map(({name,origin,height,arms})=>({name,origin,height,mainArms:arms.length})),branchTriangles:woodMesh.geometry.attributes.position.count/3,leafInstances:leaves.length,leafTriangles:leaves.length*12};
}
