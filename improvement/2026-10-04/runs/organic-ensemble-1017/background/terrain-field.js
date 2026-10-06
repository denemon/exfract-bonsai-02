import * as THREE from 'three';
const shore=[[-6,-6.98],[-2.36,-6.98],[-1.89,-5.32],[-1.78,-4.25],[-1.56,-3.42],[-1.68,-2.42],[-1.08,-1.47],[-1.08,-.87],[-1.66,-.25],[-1.68,.31],[-1.25,.55],[-.97,.80],[-1.14,1.08],[-1.88,1.25],[-2.72,1.20],[-3.63,.82],[-4.92,.73],[-6,.02]];
function distance(x,z,poly){let d=1e9,inside=false;for(let i=0,j=poly.length-1;i<poly.length;j=i++){const a=poly[i],b=poly[j],dx=b[0]-a[0],dz=b[1]-a[1],t=Math.max(0,Math.min(1,((x-a[0])*dx+(z-a[1])*dz)/(dx*dx+dz*dz)));d=Math.min(d,Math.hypot(x-a[0]-t*dx,z-a[1]-t*dz));if((a[1]>z)!==(b[1]>z)&&x<(b[0]-a[0])*(z-a[1])/(b[1]-a[1])+a[0])inside=!inside;}return inside?-d:d;}
const clamp=THREE.MathUtils.clamp,smooth=(a,b,x)=>{const t=clamp((x-a)/(b-a),0,1);return t*t*(3-2*t);};
const hills=[[-1.96,-.58,.62,.53,.13],[-2.74,-1.64,.80,.62,.13],[-3.51,-4.64,1.2,.90,.15],[-2.72,-3.10,1.18,.77,.11],[-2.25,.53,.75,.42,.078],[-3.25,.62,1.06,.44,.09],[-4.35,-.34,1.03,.90,.067]];
function seeded(){let s=280137;return ()=>{s=(Math.imul(s,1664525)+1013904223)>>>0;return s/4294967296;};}
export function makeSpatialTerrain(){const width=512,height=512,data=new Uint8Array(width*height*4),cushion=new Float32Array(width*height),density=new Float32Array(width*height),rng=seeded(),baselineDensity=new URLSearchParams(location.search).get('terrain-density')==='baseline',organicNear=new URLSearchParams(location.search).get('near-shape')!=='baseline';let accepted=0,maxHeight=0;
 // Overlapping unequal, low organic lobes are merged into one continuous field,
 // with irregular elongated footprints and blended edges, not scattered spheres.
 for(let n=0;n<165;n++){
  const x=-4.7+rng()*3.40,z=-5.8+rng()*6.84;if(distance(x,z,shore)>-.045)continue;accepted++;
  const rx=.11+rng()*.19,rz=.10+rng()*.20,rise=.020+rng()*.046,shear=(rng()-.5)*.65;
  const i0=Math.max(0,Math.floor((x-rx*2.3+6)/12*width)),i1=Math.min(width-1,Math.ceil((x+rx*2.3+6)/12*width)),j0=Math.max(0,Math.floor((z-rz*2.1+7)/14*height)),j1=Math.min(height-1,Math.ceil((z+rz*2.1+7)/14*height));
  for(let j=j0;j<=j1;j++)for(let i=i0;i<=i1;i++){
   const dx=(-6+(i+.5)/width*12-x)/rx,dz=(-7+(j+.5)/height*14-z)/rz,q=(dx+dz*shear)**2+dz*dz,w=Math.exp(-q*1.42),k=j*width+i;
   cushion[k]=Math.max(cushion[k],rise*w)+Math.min(cushion[k],rise*w)*.055;density[k]=Math.max(density[k],w*(.73+rng()*.18));
  }
 }
 for(let j=0;j<height;j++)for(let i=0;i<width;i++){
  const x=-6+(i+.5)/width*12,z=-7+(j+.5)/height*14,k=(j*width+i)*4,warp=.019*Math.sin(x*15.7+z*10.4)+.012*Math.sin(z*24.1-x*18.4),left=distance(x,z,shore)+warp,right=(Math.hypot((x-5.93)/.39,(z+5.34)/1.48)-1)*.39,d=Math.min(left,right);
  const cover=1-smooth(-.045,.015,d),edge=1-smooth(-.10,.040,d);let h=0;
  for(const [cx,cz,rx,rz,rise]of hills)h+=rise*Math.exp(-(((x-cx)/rx)**2+((z-cz)/rz)**2)*1.9);
  const local=cushion[j*width+i],grain=Math.sin(x*54.3+z*37.8)*Math.sin(x*39.1-z*63.4);
  h=(Math.min(.205,h)+local+.0028*grain)*edge;
  const seat=(1-smooth(.74,.94,Math.abs(x)))*(1-smooth(.43,.67,Math.abs(z)));h*=1-seat;
  if(x>1.1&&z< -3.15)h*=.16;
  const scar=Math.exp(-(((x+1.46)/.25)**2+((z+.73)/.32)**2)*1.6),rootGap=Math.exp(-(((x+2.11)/.18)**2+((z-1.03)/.09)**2)*1.5),dense=.69+.24*density[j*width+i]+.04*grain;
  let moss=cover*(1-.78*Math.max(scar,rootGap))*dense,organic=edge*(1-moss)*.76;
  const near=smooth(-3.3,-2.85,z)*(1-smooth(1.35,1.65,z))*smooth(-4.,-3.6,x)*(1-smooth(-.80,-.62,x));
  const seatProtected=(Math.abs(x)<.94&&Math.abs(z)<.67)?0:1,weight=near*seatProtected;
  const fineCover=1-smooth(-.058,.025,d),fineEdge=1-smooth(-.09,.04,d);
  const newHeight=(Math.min(.205,h/(edge||1)-local)*.83+local*.48+.0012*grain)*fineEdge;
  const rootWear=Math.exp(-(((x+1.50)/.17)**2+((z-.52)/.14)**2)*1.8)*.42+Math.exp(-(((x+1.66)/.20)**2+((z+1.6)/.17)**2)*1.8)*.33+Math.exp(-(((x+3.08)/.22)**2+((z+2.12)/.18)**2)*1.8)*.27;
  const fineMoss=fineCover*(1-.78*Math.max(scar,rootGap))*(.61+.27*density[j*width+i]+.035*grain)*(1-rootWear);
  h=THREE.MathUtils.lerp(h,Math.max(0,newHeight-.011*rootWear),weight);moss=THREE.MathUtils.lerp(moss,fineMoss,weight);organic=THREE.MathUtils.lerp(organic,fineEdge*(1-fineMoss)*.82,weight);
  if(!baselineDensity&&weight>0){
   let shaded=0,rootOpen=0;
   for(const [cx,cz,rx,rz]of [organicNear?[-1.25,.36,.29,.20]:[-1.50,.52,.25,.16],[-1.66,-1.60,.28,.18],[-3.08,-2.12,.34,.21]]){
    const q=((x-cx)/rx)**2+((z-cz)/rz)**2;
    if(q<1)shaded=Math.max(shaded,(1-q)**3);
    const rootQ=((x-cx)/.065)**2+((z-cz)/.057)**2;
    if(rootQ<1)rootOpen=Math.max(rootOpen,(1-rootQ)**3);
   }
   moss=clamp(moss+weight*fineCover*(.065*shaded-.14*rootOpen),0,1);
   organic=clamp(organic+weight*fineEdge*(.16*rootOpen-.025*shaded),0,1);
  }
  if(organicNear&&!baselineDensity){const q=((x+1.25)/.25)**2+((z-.36)/.20)**2;if(q<1){const soil=(1-q)**3;organic=clamp(organic+.29*soil,0,1);moss=clamp(moss*(1-.27*soil),0,1);}}
  data[k]=Math.round(clamp(moss,0,1)*255);data[k+1]=Math.round(clamp(organic,0,1)*255);data[k+2]=Math.round(clamp(h/.30,0,1)*255);data[k+3]=Math.round(clamp(.38+.60*density[j*width+i],0,1)*255);maxHeight=Math.max(maxHeight,h);
 }
 const t=new THREE.DataTexture(data,width,height,THREE.RGBAFormat);t.colorSpace=THREE.NoColorSpace;t.minFilter=t.magFilter=THREE.LinearFilter;t.generateMipmaps=false;t.flipY=false;t.needsUpdate=true;t.name='Connected low moss cushion/shore/density/soil field';t.userData={version:organicNear?'occupied-rootsoil-v02':baselineDensity?'near-shore-v02':'rootshade-density-v01',blueHeightExactlyR30:true,localizedRootAndCanopyDensityOnly:true,nearDomain:[-4,-3.3,-.62,1.65],seatRearFieldBytesProtected:true,shoreTransitionMM:[40,90],noNewTuftOrStoneObjects:true,maximumAuthoredRise:maxHeight,interlockedLobes:accepted,generatedDataBytes:data.byteLength,scatteredSmallStoneObjects:0};return t;
}
