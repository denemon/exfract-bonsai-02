import * as THREE from 'three';
import {groveShore} from './m20-grove-design.js';
function polyDistance(x,z,poly){let d=1e9,inside=false;for(let i=0,j=poly.length-1;i<poly.length;j=i++){const a=poly[i],b=poly[j],dx=b[0]-a[0],dz=b[1]-a[1],t=Math.max(0,Math.min(1,((x-a[0])*dx+(z-a[1])*dz)/(dx*dx+dz*dz)));d=Math.min(d,Math.hypot(x-a[0]-t*dx,z-a[1]-t*dz));if((a[1]>z)!==(b[1]>z)&&x<(b[0]-a[0])*(z-a[1])/(b[1]-a[1])+a[0])inside=!inside;}return inside?-d:d;}
const mix=(a,b,w)=>a*(1-w)+b*w,smooth=(a,b,x)=>{const t=Math.max(0,Math.min(1,(x-a)/(b-a)));return t*t*(3-2*t);};
function union(a,b,k){const h=Math.max(0,Math.min(1,.5+.5*(b-a)/k));return mix(b,a,h)-k*h*(1-h);}
export function makeSandRakeField(){const size=512,data=new Float32Array(size*size);let min=Infinity,max=-Infinity;
 for(let j=0;j<size;j++)for(let i=0;i<size;i++){
  const x=-6+(i+.5)/size*12,z=-7+(j+.5)/size*14,qx=Math.abs(x)-.63,qz=Math.abs(z)-.32;
  const display=Math.hypot(Math.max(qx,0),Math.max(qz,0))+Math.min(Math.max(qx,qz),0)-.15;
  const stone1=(Math.hypot((x+1.08)/.32,(z-.72)/.27)-1)*.27,stone2=(Math.hypot((x+1.10)/.43,(z+1.10)/.33)-1)*.33;
  const shore=polyDistance(x,z,groveShore);
  let phase=union(union(union(display,stone1,.22),stone2,.28),shore,.34);
  // The close court follows each buried footprint; broad foreground sweeps
  // resolve into quiet open bands rather than repeating isolated stone circles.
  const foreground=smooth(1.65,3.4,z),sweep=z-.95+.10*Math.sin(x*.57)+.026*x*x;
  phase=mix(phase,sweep,foreground);phase+=.006*Math.sin(x*1.8+z*.8)*smooth(.18,.9,phase);
  data[j*size+i]=phase;min=Math.min(min,phase);max=Math.max(max,phase);
 }

 // Smooth the complete world distance field, including closest-footprint
 // handoffs, rather than drawing a stack of isolated rounded object rings.
 // 90mm kernel leaves contacts intact: geometry and green field are unchanged.
 const radius=7,tmp=new Float32Array(data.length),out=new Float32Array(data.length);
 function filter(source,target,horizontal){const step=horizontal?12/size:14/size,weights=[];let total=0;for(let k=-radius;k<=radius;k++){const w=Math.exp(-.5*(k*step/.090)**2);weights.push(w);total+=w;}for(let y=0;y<size;y++)for(let x=0;x<size;x++){let value=0;for(let k=-radius;k<=radius;k++){const xx=horizontal?Math.max(0,Math.min(size-1,x+k)):x,yy=horizontal?y:Math.max(0,Math.min(size-1,y+k));value+=source[yy*size+xx]*weights[k+radius];}target[y*size+x]=value/total;}}
 filter(data,tmp,true);filter(tmp,out,false);min=Infinity;max=-Infinity;
 for(let y=0;y<size;y++)for(let x=0;x<size;x++){const worldX=-6+(x+.5)/size*12,worldZ=-7+(y+.5)/size*14,p=out[y*size+x];const phase=p-.034*Math.sin(p*1.55)+.005*Math.sin(worldX*.43+worldZ*.27);data[y*size+x]=phase;min=Math.min(min,phase);max=Math.max(max,phase);}
 const t=new THREE.DataTexture(data,size,size,THREE.RedFormat,THREE.FloatType);t.colorSpace=THREE.NoColorSpace;t.minFilter=t.magFilter=THREE.LinearFilter;t.generateMipmaps=false;t.flipY=false;t.needsUpdate=true;t.name='Authored dry-garden contour distance in world metres';t.userData={version:'raked-court-v02',spacingMetres:.066,spacingSmoothVariationPercent:5.3,worldConvergenceSmoothingMetres:.090,maximumApparentReliefMetres:.0014,worldDomain:[-6,-7,6,7],preservedTerrainHeight:true,greenAndSoilBoundaryProtected:true,noNewStoneObjects:true,flow:'continuous filtered contours around low display, two buried stones and actual moss shore; open foreground sweeps',distanceRange:[min,max]};return t;
}
