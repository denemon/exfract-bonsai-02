import * as THREE from 'three';
const shore=[[-6,-6.9],[-2.7,-6.9],[-1.92,-5.7],[-1.80,-4.6],[-1.47,-3.62],[-1.48,-2.91],[-1.82,-2.17],[-1.52,-1.58],[-1.39,-.80],[-1.57,-.18],[-1.78,.38],[-1.41,.76],[-1.03,1.06],[-.80,1.59],[-1.27,1.88],[-1.14,2.19],[-2.45,2.40],[-3.52,2.11],[-4.59,1.43],[-6,.26]];
function distance(x,z,poly){let d=1e9,inside=false;for(let i=0,j=poly.length-1;i<poly.length;j=i++){const a=poly[i],b=poly[j],dx=b[0]-a[0],dz=b[1]-a[1],t=Math.max(0,Math.min(1,((x-a[0])*dx+(z-a[1])*dz)/(dx*dx+dz*dz)));d=Math.min(d,Math.hypot(x-a[0]-t*dx,z-a[1]-t*dz));if((a[1]>z)!==(b[1]>z)&&x<(b[0]-a[0])*(z-a[1])/(b[1]-a[1])+a[0])inside=!inside;}return inside?-d:d;}
const clamp=THREE.MathUtils.clamp,smooth=(a,b,x)=>{const t=clamp((x-a)/(b-a),0,1);return t*t*(3-2*t);};
// Unequal linked lobes rise behind the rock and turn back into a low foreground
// ridge; the broad shape and the organic layer use exactly the same field.
const hills=[[-2.01,-.66,.68,.63,.21],[-2.76,-1.75,.86,.62,.18],[-3.14,-3.30,1.05,.80,.19],[-2.25,-4.67,.51,.89,.15],[-2.21,.71,.80,.60,.19],[-1.55,1.40,.64,.44,.115],[-2.94,1.56,.97,.53,.155],[-3.70,1.20,.97,.39,.08]];
const hummocks=[[-1.74,.83,.15,.20,.036],[-1.40,1.27,.13,.17,.026],[-1.69,1.49,.24,.13,.032],[-2.42,1.60,.17,.25,.042],[-2.81,.71,.23,.14,.030],[-2.45,-.39,.14,.23,.031],[-3.12,-1.16,.19,.16,.034],[-2.26,-2.36,.23,.14,.037]];
export function makeSpatialTerrain(){const width=512,height=512,data=new Uint8Array(width*height*4);let maxHeight=0;
 for(let j=0;j<height;j++)for(let i=0;i<width;i++){
  const x=-6+(i+.5)/width*12,z=-7+(j+.5)/height*14,warp=.027*Math.sin(x*10.7+z*7.8)+.018*Math.sin(z*21.1-x*12.4),left=distance(x,z,shore)+warp,right=(Math.hypot((x-2.73)/.41,(z+5.18)/1.31)-1)*.41;
  const d=Math.min(left,right),cover=1-smooth(-.040,.030,d),edge=1-smooth(-.10,.065,d);let h=0;
  for(const [cx,cz,rx,rz,rise]of hills){const r=((x-cx)/rx)**2+((z-cz)/rz)**2;h+=rise*Math.exp(-r*1.9);}
  for(const [cx,cz,rx,rz,rise]of hummocks)h+=rise*Math.exp(-(((x-cx)/rx)**2+((z-cz)/rz)**2)*1.9);
  h=Math.min(.295,h)*edge;
  const linked=Math.sin(x*18.3+z*12.7)*Math.sin(x*10.1-z*18.8),fine=Math.sin(x*43.7+z*28.1)*Math.cos(x*22.4-z*52.3);
  h+=cover*(.0065*linked+.0031*fine);h=Math.max(0,h);
  const seat=(1-smooth(.74,.94,Math.abs(x)))*(1-smooth(.43,.67,Math.abs(z)));h*=1-seat;
  const soilA=Math.exp(-(((x+1.72)/.32)**2+((z+.54)/.57)**2)*1.6),soilB=Math.exp(-(((x+2.47)/.31)**2+((z+1.19)/.25)**2)*1.6),soilC=Math.exp(-(((x+1.23)/.35)**2+((z-1.14)/.12)**2)*1.7);
  const bare=Math.max(soilA,soilB,soilC),moss=cover*(.96-.76*bare)*(.89+.08*linked+.035*fine),organic=edge*(1-moss)*.86;
  const k=(j*width+i)*4;data[k]=Math.round(clamp(moss,0,1)*255);data[k+1]=Math.round(clamp(organic,0,1)*255);data[k+2]=Math.round(clamp(h/.30,0,1)*255);data[k+3]=255;maxHeight=Math.max(maxHeight,h);
 }
 const texture=new THREE.DataTexture(data,width,height,THREE.RGBAFormat);texture.colorSpace=THREE.NoColorSpace;texture.magFilter=texture.minFilter=THREE.LinearFilter;texture.generateMipmaps=false;texture.flipY=false;texture.needsUpdate=true;texture.name='Depth-v01 connected ridge/moss/soil field';texture.userData={version:'depth-v01',maximumAuthoredRise:maxHeight,generatedDataBytes:data.byteLength,scatteredSmallStoneObjects:0};return texture;
}
