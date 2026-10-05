import * as THREE from 'three';
const shore=[[-6,-6.9],[-2.8,-6.9],[-1.9,-5.5],[-1.75,-4.1],[-1.33,-3.5],[-1.29,-2.6],[-1.65,-1.9],[-1.31,-1.25],[-1.40,-.35],[-1.61,.27],[-1.73,.95],[-1.00,1.75],[-1.55,2.50],[-3.4,2.3],[-4.5,1.47],[-6,.3]];
function signedDistance(x,z,poly){let d=1e9,inside=false;for(let i=0,j=poly.length-1;i<poly.length;j=i++){const a=poly[i],b=poly[j],dx=b[0]-a[0],dz=b[1]-a[1],t=Math.max(0,Math.min(1,((x-a[0])*dx+(z-a[1])*dz)/(dx*dx+dz*dz)));d=Math.min(d,Math.hypot(x-a[0]-t*dx,z-a[1]-t*dz));if((a[1]>z)!==(b[1]>z)&&x<(b[0]-a[0])*(z-a[1])/(b[1]-a[1])+a[0])inside=!inside;}return inside?-d:d;}
const clamp=THREE.MathUtils.clamp,smooth=(a,b,x)=>{const t=clamp((x-a)/(b-a),0,1);return t*t*(3-2*t);};
const hills=[[-1.96,-.59,.65,.56,.19],[-2.72,-1.72,.82,.61,.13],[-3.12,-3.56,1.05,.87,.14],[-2.13,-4.65,.48,.8,.12],[-2.27,1.19,.77,.5,.13],[-3.67,1.63,1.24,.45,.09],[1.63,-4.4,.42,1.4,.06]];
export function makeSpatialTerrain(){const width=512,height=512,data=new Uint8Array(width*height*4);let maxHeight=0;
 for(let j=0;j<height;j++)for(let i=0;i<width;i++){const x=-6+(i+.5)/width*12,z=-7+(j+.5)/height*14,warp=.047*Math.sin(x*9.1+z*6.8)+.021*Math.sin(z*23.7-x*11.2),left=signedDistance(x,z,shore)+warp,right=(Math.hypot((x-1.55)/.36,(z+4.50)/1.71)-1)*.36+.023*Math.sin(z*12+x*7);const d=Math.min(left,right),cover=1-smooth(-.06,.06,d),edge=1-smooth(-.13,.14,d);let h=0;
  for(const [cx,cz,rx,rz,rise]of hills){const r=((x-cx)/rx)**2+((z-cz)/rz)**2;h+=rise*Math.exp(-r*2.2);}
  h=Math.min(.245,h)*edge;h+=cover*(.0042*Math.sin(x*24+z*17)+.0030*Math.sin(x*41-z*31));h=Math.max(0,h);const seat=(1-smooth(.72,.96,Math.abs(x)))*(1-smooth(.42,.68,Math.abs(z)));h*=1-seat;
  const bareA=Math.exp(-(((x+1.48)/.34)**2+((z+.34)/.65)**2)*2),bareB=Math.exp(-(((x+2.66)/.39)**2+((z+1.30)/.25)**2)*2);const moss=cover*(.94-.68*Math.max(bareA,bareB))*(.93+.07*Math.sin(x*37+z*21));const organic=edge*(1-moss)*.86;const k=(j*width+i)*4;data[k]=Math.round(clamp(moss,0,1)*255);data[k+1]=Math.round(clamp(organic,0,1)*255);data[k+2]=Math.round(clamp(h/.30,0,1)*255);data[k+3]=255;maxHeight=Math.max(maxHeight,h);
 }
 const texture=new THREE.DataTexture(data,width,height,THREE.RGBAFormat);texture.colorSpace=THREE.NoColorSpace;texture.magFilter=texture.minFilter=THREE.LinearFilter;texture.generateMipmaps=false;texture.flipY=false;texture.needsUpdate=true;texture.name='Spatial v01 continuous moss and relief data';texture.userData={version:'spatial-v01',maximumAuthoredRise:maxHeight,generatedDataBytes:data.byteLength,scatteredSmallStoneObjects:0};return texture;
}
