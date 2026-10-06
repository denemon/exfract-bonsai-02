import * as THREE from 'three';
export const balancedPerformance=()=>new URLSearchParams(location.search).get('perf')!=='original';
const fract=x=>x-Math.floor(x);
function eh(x,y,z){x=fract(x*.1031);y=fract(y*.1031);z=fract(z*.1031);const d=x*(y+33.33)+y*(z+33.33)+z*(x+33.33);x+=d;y+=d;z+=d;return fract((x+y)*z);}
let textures;
export function physicalDetailTextures(){
 if(textures)return textures;
 const N=64,data=new Uint8Array(N*N*N);for(let z=0;z<N;z++)for(let y=0;y<N;y++)for(let x=0;x<N;x++)data[x+N*(y+N*z)]=Math.round(eh(x,y,z)*255);
 const spatial=new THREE.Data3DTexture(data,N,N,N);spatial.format=THREE.RedFormat;spatial.type=THREE.UnsignedByteType;spatial.minFilter=spatial.magFilter=THREE.LinearFilter;spatial.wrapS=spatial.wrapT=spatial.wrapR=THREE.RepeatWrapping;spatial.generateMipmaps=false;spatial.unpackAlignment=1;spatial.needsUpdate=true;
 const varied=new URLSearchParams(location.search).get('gravel')==='varied',size=varied?384:256,cells=64,channels=varied?4:2,grain=new Uint8Array(size*size*channels);
 for(let y=0;y<size;y++)for(let x=0;x<size;x++){
  const px=(x+.5)*cells/size,py=(y+.5)*cells/size,cx=Math.floor(px),cy=Math.floor(py),fx=fract(px),fy=fract(py);let nearest=4,shade=.5;
  for(let j=-1;j<=1;j++)for(let i=-1;i<=1;i++){
   const xx=(cx+i+cells)%cells,yy=(cy+j+cells)%cells,dx=i+eh(xx,yy,4.2)-fx,dy=j+eh(xx,yy,8.1)-fy,d=Math.hypot(dx,dy);if(d<nearest){nearest=d;shade=eh(xx,yy,11.4);}
  }
  const k=(x+y*size)*channels;grain[k]=Math.round(Math.min(nearest/1.5,1)*255);grain[k+1]=Math.round(shade*255);
  if(varied){const radius=.33+.22*shade,coverage=Math.max(0,Math.min(1,(radius-nearest)/.075)),relief=Math.pow(Math.max(0,1-nearest/radius),.44)*(.58+.36*shade);grain[k+1]=Math.round((coverage*(.16+.75*shade)+(1-coverage)*(.45+.12*shade))*255);grain[k+2]=Math.round(relief*255);grain[k+3]=Math.round(coverage*255);}
 }
 const mineral=new THREE.DataTexture(grain,size,size,varied?THREE.RGBAFormat:THREE.RGFormat);mineral.colorSpace=THREE.NoColorSpace;mineral.minFilter=THREE.LinearMipmapLinearFilter;mineral.magFilter=THREE.LinearFilter;mineral.wrapS=mineral.wrapT=THREE.RepeatWrapping;mineral.generateMipmaps=true;mineral.needsUpdate=true;
 mineral.userData.physicalDesign=varied?{tileMetres:.448,meanCellMetres:.007,maximumReliefMetres:.0033,individualRadiiFromUnequalCellSeeds:true,materialOnly:true}:{tileMetres:.384,meanCellMetres:.006};textures={spatial,mineral};return textures;
}
export const sampledNoise=`
float eh(vec3 p){p=fract(p*.1031);p+=dot(p,p.yzx+33.33);return fract((p.x+p.y)*p.z);}
float en(vec3 p){vec3 i=floor(p),f=fract(p);f=f*f*(3.-2.*f);return texture(uSpatialNoise,(mod(i,64.)+f+.5)/64.).r;}
float ef(vec3 p){return en(p)*.62+en(p*2.13+3.7)*.26+en(p*4.27-2.6)*.12;}
vec2 mineralGrain(vec2 p){return texture2D(uGravelDetail,p/64.).rg*vec2(1.5,1.);}
float mineralRelief(vec2 p){return texture2D(uGravelDetail,p/64.).b*.0033;}
`;
export function backgroundShadowFilter(material){
 if(!balancedPerformance()||material.userData.backgroundPcfTaps===4)return material;
 material.userData.backgroundPcfTaps=4;
 const previous=material.onBeforeCompile,key=material.customProgramCacheKey.bind(material);
 material.onBeforeCompile=s=>{
  previous.call(material,s);
  const chunk=THREE.ShaderChunk.shadowmap_pars_fragment;
  if(!chunk.includes('sampleIndex<8;')||!chunk.includes('shadow*=0.125;'))throw Error('Pinned eight-tap shadow contract changed');
  const four=chunk.replace('sampleIndex<8;','sampleIndex<4;').replace('vogelDiskSample(sampleIndex,8,','vogelDiskSample(sampleIndex,4,').replace('shadow*=0.125;','shadow*=0.25;');
  s.fragmentShader=s.fragmentShader.replace('#include <shadowmap_pars_fragment>',four);
 };
 material.customProgramCacheKey=()=>key()+'-background-4tap-v20';return material;
}
