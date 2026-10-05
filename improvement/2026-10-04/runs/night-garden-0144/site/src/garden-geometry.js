import * as THREE from 'three';
import {RoundedBoxGeometry} from 'three/addons/geometries/RoundedBoxGeometry.js';
import {mergeGeometries,mergeVertices} from 'three/addons/utils/BufferGeometryUtils.js';

export function random(seed=7241){let s=seed;return ()=>{s=(Math.imul(s,1664525)+1013904223)>>>0;return s/4294967296;};}
export function batches(scene,materials){
 const groups=new Map();
 const add=(geometry,material)=>{if(!groups.has(material))groups.set(material,[]);groups.get(material).push(geometry.index?geometry.toNonIndexed():geometry);};
 const box=(p,size,key,angle=0,yaw=0)=>{
  const g=new RoundedBoxGeometry(...size,1,Math.min(.005,...size.map(v=>v*.11)));g.rotateZ(angle);g.rotateY(yaw);g.translate(...p);add(g,key);
 };
 const done=()=>{let triangles=0;for(const [key,gs]of groups){const g=mergeGeometries(gs,false);const mesh=new THREE.Mesh(g,materials[key]);mesh.name='Garden architecture '+key;mesh.castShadow=mesh.receiveShadow=true;scene.add(mesh);triangles+=g.attributes.position.count/3;gs.forEach(x=>x.dispose());}return {drawCalls:groups.size,triangles};};
 return {add,box,done};
}
export function groundGeometry(){
 const positions=[],uv=[],indices=[],n=112,xmin=-6,xmax=6,zmin=-7,zmax=7;
 const moss=(x,z)=>Math.min((Math.hypot((x+2.38)/1.65,(z+1.12)/3.8)-1)*1.65,(Math.hypot((x+1.27)/.81,(z-.67)/.62)-1)*.62,(Math.hypot((x-2.06)/.73,(z+2.6)/2.5)-1)*.73);
 for(let j=0;j<=n;j++)for(let i=0;i<=n;i++){
  const x=xmin+(xmax-xmin)*i/n,z=zmin+(zmax-zmin)*j/n;
  const m=THREE.MathUtils.smoothstep(-moss(x,z),-.03,.15);
  const h=-.022+m*(.014+.004*Math.sin(x*9+z*7))+.0012*Math.sin(x*5.4)*Math.sin(z*4.3);
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
export function planting(scene,materials,layout){
 const rng=random(77013),wood=[],leaves=[];
 const sprig=(a,b,calibre,density=8)=>{
  const c=a.clone().lerp(b,.54).add(new THREE.Vector3(0,.05,0));
  const q=branch([a.toArray(),c.toArray(),b.toArray()],calibre,.001,6,5);wood.push(q.g);
  for(let i=1;i<=density;i++){
   const t=i/(density+1),p=q.path.getPoint(t),side=i%2?1:-1;
   const length=.045+rng()*.021;const dir=b.clone().sub(a).normalize();
   const lateral=new THREE.Vector3(-dir.z,.14,dir.x).multiplyScalar(side*.027);p.add(lateral);
   leaves.push({p,rotation:[rng()*.8-.4,rng()*Math.PI*2,side*(.4+rng()*.7)],scale:[length*(.65+rng()*.25),length,length*(.8+rng()*.4)],color:new THREE.Color().setRGB(.52+rng()*.22,.67+rng()*.23,.42+rng()*.18)});
  }
 };
 const tree=(origin,height)=>{
  const o=new THREE.Vector3(...origin), trunk=branch([[0,0,0],[.04,height*.35,-.04],[-.06,height*.64,.04],[.08,height*.82,-.06],[.02,height,0]].map(p=>new THREE.Vector3(...p).add(o).toArray()),.052,.005,20,9);wood.push(trunk.g);
  const limbs=[[-1.04,.72,.25],[.87,.84,-.16],[-.75,.99,-.5],[.93,1.12,.37],[-.62,1.29,.14],[.60,1.44,-.34],[-.42,1.59,-.1],[.37,1.68,.23]];
  for(let k=0;k<limbs.length;k++){
   let [dx,hh,dz]=limbs[k];dx*=.78+rng()*.36;hh*=.94+rng()*.11;dz+=(rng()-.5)*.32;const root=trunk.path.getPoint(.29+k*.071),end=o.clone().add(new THREE.Vector3(dx*height/2.4,hh*height/1.7,dz));const mid=root.clone().lerp(end,.46).add(new THREE.Vector3(0,-.10,0));
   const limb=branch([root.toArray(),mid.toArray(),end.toArray()],.027-k*.002,.0025,12,7);wood.push(limb.g);
   for(let i=1;i<8;i++){
    const t=.2+i*.096,a=limb.path.getPoint(t),axis=end.clone().sub(root).normalize(),side=i%2?1:-1;
    const lateral=new THREE.Vector3(-axis.z,.38,axis.x).normalize().multiplyScalar(side*(.14+rng()*.14));lateral.y=Math.abs(lateral.y)+.04;
    const b=a.clone().add(lateral).addScaledVector(axis,.15+rng()*.08);
    sprig(a,b,.0035,14);
    sprig(b.clone().lerp(a,.5),b.clone().add(new THREE.Vector3(.04,.035,.10*side)),.0022,10);
   }
  }
 };
 tree([-2.72,-.007,-3.55],2.43);
 tree([-4.85,-.02,-5.7],3.0);tree([-5.7,-.02,-8.3],3.4);
 for(const [x,z,size]of [[-2.21,-.92,.42],[-1.65,-2.78,.49],[-3.0,-2.0,.58]]){
  for(let k=0;k<34;k++){
   const angle=rng()*Math.PI*2,r=.05+rng()*.14,a=new THREE.Vector3(x+Math.cos(angle)*r,-.004,z+Math.sin(angle)*r);
   const b=new THREE.Vector3(x+Math.cos(angle)*size*(.65+rng()*.25),size*(.3+rng()*.5),z+Math.sin(angle)*size);
   sprig(a,b,.0035,11);
   sprig(a.clone().lerp(b,.55),b.clone().add(new THREE.Vector3(Math.cos(angle+1)*.12,.055,Math.sin(angle+1)*.12)),.002,7);
  }
 }
 const woodMesh=new THREE.Mesh(mergeGeometries(wood.map(g=>g.toNonIndexed()),false),materials.vertical);woodMesh.name='Irregular garden tree and shrub branching';woodMesh.castShadow=woodMesh.receiveShadow=true;scene.add(woodMesh);
 // Closed thin almond leaves; visible thickness, midrib, tapered ends.
 const leaf=new THREE.BufferGeometry();leaf.setAttribute('position',new THREE.Float32BufferAttribute([0,0,0,-.24,.026,.29,-.34,.043,.60,0,.022,1.13,.34,.043,.60,.24,.026,.29,0,.082,.55,0,-.021,.54],3));const leafIndex=[];for(let j=0;j<6;j++){const k=(j+1)%6;leafIndex.push(j,k,6,k,j,7);}leaf.setIndex(leafIndex);leaf.computeVertexNormals();
 const mesh=new THREE.InstancedMesh(leaf,materials.leaves,leaves.length);mesh.name='Branch attached garden leaves';const transform=new THREE.Object3D();
 leaves.forEach((l,i)=>{transform.position.copy(l.p);transform.rotation.set(...l.rotation);transform.scale.set(...l.scale);transform.updateMatrix();mesh.setMatrixAt(i,transform.matrix);mesh.setColorAt(i,l.color);});mesh.castShadow=mesh.receiveShadow=true;mesh.instanceMatrix.needsUpdate=true;mesh.computeBoundingSphere();scene.add(mesh);
 return {branchTriangles:woodMesh.geometry.attributes.position.count/3,leafInstances:leaves.length,leafTriangles:leaves.length*12};
}
