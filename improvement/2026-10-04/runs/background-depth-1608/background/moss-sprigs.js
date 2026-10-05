import * as THREE from 'three';
import {groundHeight,random} from './garden-geometry.js';
function geometry(){
 const ps=[],ix=[];
 // Three closed small moss fronds share a tuft base. Broad irregularly folded
 // leaves have physical thickness, not grass blades, tetrahedra or flat cards.
 for(let k=0;k<3;k++){
  const angle=k*2.399963,ca=Math.cos(angle),sa=Math.sin(angle),height=[1,.77,.88][k],width=[.36,.30,.33][k],p=[[0,0,0],[-width,.40,.03],[-width*.72,.73,.13],[.03,height,.23],[width*.86,.72,.14],[width*.92,.38,.015],[0,.57,.17],[0,.54,-.022]],off=ps.length/3;
  for(const [x,y,z]of p)ps.push(x*ca-z*sa,y,z*ca+x*sa);
  for(let n=0;n<6;n++){const m=(n+1)%6;ix.push(off+m,off+n,off+6,off+n,off+m,off+7);}
 }
 const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(ps,3));g.setIndex(ix);g.computeVertexNormals();return g;
}
export function mossSprigs(scene,field,mossTexture){
 const {data,width,height}=field.image,rng=random(41019),rows=[];
 const canvas=document.createElement('canvas');canvas.width=mossTexture.image.width;canvas.height=mossTexture.image.height;const ctx=canvas.getContext('2d',{willReadFrequently:true});ctx.drawImage(mossTexture.image,0,0);const pixels=ctx.getImageData(0,0,canvas.width,canvas.height).data,tw=canvas.width,th=canvas.height;
 const colourAt=(x,z)=>{const u=((x/.42)%1+1)%1,v=1-((z/.42)%1+1)%1,i=Math.min(tw-1,Math.floor(u*tw)),j=Math.min(th-1,Math.floor(v*th)),q=(j*tw+i)*4;return new THREE.Color().setRGB(pixels[q]/255,pixels[q+1]/255,pixels[q+2]/255,THREE.SRGBColorSpace).multiplyScalar(.91);};
 for(let z=-.38;z<2.38;z+=.035)for(let x=-3.64;x<-.81;x+=.035){
  const px=x+(rng()-.5)*.032,pz=z+(rng()-.5)*.032,i=Math.min(width-1,Math.max(0,Math.floor((px+6)/12*width))),j=Math.min(height-1,Math.max(0,Math.floor((pz+7)/14*height))),m=data[(j*width+i)*4]/255;
  if(m<.50||rng()>m*.82)continue;
  rows.push({x:px,z:pz,y:groundHeight(px,pz)-.001,height:.009+.008*rng(),turn:rng()*Math.PI*2,color:.83+.25*rng()});
 }
 const g=geometry(),material=new THREE.MeshStandardMaterial({color:'#ffffff',roughness:1,metalness:0}),mesh=new THREE.InstancedMesh(g,material,rows.length),obj=new THREE.Object3D();mesh.name='Field grounded uneven short moss fronds';
 rows.forEach((r,n)=>{obj.position.set(r.x,r.y,r.z);obj.rotation.set((rng()-.5)*.24,r.turn,(rng()-.5)*.29);obj.scale.set(r.height*2.35,r.height*.72,r.height*2.35);obj.updateMatrix();mesh.setMatrixAt(n,obj.matrix);mesh.setColorAt(n,colourAt(r.x,r.z).multiplyScalar(.94+r.color*.06));});
 mesh.castShadow=false;mesh.receiveShadow=true;mesh.instanceMatrix.needsUpdate=true;mesh.computeBoundingSphere();scene.add(mesh);
 return {instances:rows.length,triangles:g.index.count/3*rows.length,heightM:[.00648,.01224],widthM:[.025,.037],albedoCalibration:'Same existing ground mossMap sampled at world root UV, correct sRGB-to-linear conversion; not a new decorative colour',grounding:'Every root on the same triangle-interpolated terrain,1mm burial; density follows moss field, soil/gravel stay clear',shading:'Matte roughness1, no emission, no added AO or gloss; no unresolved millimetre cast-shadow dots, full scene shadows received'};
}
