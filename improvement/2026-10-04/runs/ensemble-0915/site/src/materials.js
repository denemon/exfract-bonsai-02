import * as THREE from 'three';
const noiseGLSL=`
float hash31(vec3 p){p=fract(p*.1031);p+=dot(p,p.yzx+33.33);return fract((p.x+p.y)*p.z);}
float n3(vec3 p){vec3 i=floor(p),f=fract(p);f=f*f*(3.-2.*f);return mix(mix(mix(hash31(i),hash31(i+vec3(1,0,0)),f.x),mix(hash31(i+vec3(0,1,0)),hash31(i+vec3(1,1,0)),f.x),f.y),mix(mix(hash31(i+vec3(0,0,1)),hash31(i+vec3(1,0,1)),f.x),mix(hash31(i+vec3(0,1,1)),hash31(i+vec3(1,1,1)),f.x),f.y),f.z);}
float fb(vec3 p){return n3(p)*.57+n3(p*2.07+3.2)*.28+n3(p*4.13-1.7)*.15;}
vec3 barkNormal(vec3 geometric,vec3 surfacePosition,vec2 uv,vec3 mapValue,float strength){
 vec3 a=dFdx(surfacePosition),b=dFdy(surfacePosition);vec2 ta=dFdx(uv),tb=dFdy(uv);
 vec3 bp=cross(b,geometric),ap=cross(geometric,a);
 vec3 tangent=bp*ta.x+ap*tb.x,bitangent=bp*ta.y+ap*tb.y;
 float scale=inversesqrt(max(max(dot(tangent,tangent),dot(bitangent,bitangent)),1e-12));
 vec3 n=mapValue*2.-1.;n.xy*=strength;
 return normalize(mat3(tangent*scale,bitangent*scale,geometric)*n);
}
vec3 woodSpace(vec3 p,vec3 growth){vec3 t=normalize(growth);vec3 n=normalize(vec3(t.y,-t.x,0.)+vec3(.00001,0.,0.));vec3 b=cross(t,n);return vec3(dot(p,n),dot(p,b),dot(p,t));}
`;
function extend(material,name,fragment,normalFragment='',uniforms={}){
 const directed=name.startsWith('bark-');if(directed)material.defines={...material.defines,USE_UV1:'',USE_UV2:''};
 material.onBeforeCompile=shader=>{
  Object.assign(shader.uniforms,uniforms);
  shader.vertexShader='varying vec3 vLocal; varying vec2 vFlow;\n'+(directed?'varying vec2 vBranchFlow; varying float vBranchWeight; varying float vCalibre;\n':'')+shader.vertexShader;
  shader.vertexShader=shader.vertexShader.replace('#include <begin_vertex>','#include <begin_vertex>\nvLocal=position;vFlow=uv;'+(directed?'vFlow=vec2(uv.x,1.-uv.y);vBranchFlow=vec2(uv1.x,1.-uv1.y);vBranchWeight=uv2.x;vCalibre=1.-uv2.y;':''));
  shader.fragmentShader='varying vec3 vLocal; varying vec2 vFlow;\n'+(directed?'varying vec2 vBranchFlow; varying float vBranchWeight; varying float vCalibre;\nuniform sampler2D barkColor; uniform sampler2D barkNormalMap; uniform sampler2D barkHeight; uniform sampler2D barkRough;\n':'')+noiseGLSL+shader.fragmentShader;
  shader.fragmentShader=shader.fragmentShader.replace('#include <color_fragment>','#include <color_fragment>\n'+fragment);
  if(directed)shader.fragmentShader=shader.fragmentShader.replace('#include <aomap_fragment>','#include <aomap_fragment>\n#ifdef USE_COLOR_ALPHA\nreflectedLight.indirectDiffuse *= clamp(vColor.a,.32,1.);\n#endif');
  if(normalFragment)shader.fragmentShader=shader.fragmentShader.replace('#include <normal_fragment_maps>','#include <normal_fragment_maps>\n'+normalFragment);
 };
 material.customProgramCacheKey=()=>name;
 return material;
}
export async function makeMaterials(){
 const plain=new URLSearchParams(location.search).get('wood')==='plain';
 const wood=new THREE.MeshStandardMaterial({color:'#ffffff',vertexColors:true,roughness:.94,metalness:0});
 if(plain){
  extend(wood,'natural-grey-brown-control',`
   float weather=fb(vLocal*vec3(6.,4.,5.));
   diffuseColor.rgb=mix(vec3(.091,.066,.043),vec3(.158,.129,.095),weather*.74+.18);diffuseColor.a=1.;
  `);
 }else{
  const loader=new THREE.TextureLoader();
  const [color,normal,height,rough]=await Promise.all(['color','normal','height','roughness'].map(n=>loader.loadAsync('/bark/'+n+'.webp')));
  color.colorSpace=THREE.SRGBColorSpace;
  for(const texture of [color,normal,height,rough]){texture.wrapS=texture.wrapT=THREE.RepeatWrapping;texture.anisotropy=4;}
  extend(wood,'bark-connected-cedar-v2',`
   vec2 mainUV=vFlow/.72+vec2(.07,.11),branchUV=vBranchFlow/.72+vec2(.38,.11);
   float blend=clamp(vBranchWeight,0.,1.),scar=clamp(vColor.g,0.,1.);
   vec3 sampled=mix(texture2D(barkColor,mainUV).rgb,texture2D(barkColor,branchUV).rgb,blend);
   float luminance=dot(sampled,vec3(.2126,.7152,.0722));
   sampled=mix(sampled,vec3(luminance),.15);
   sampled=clamp(sampled*1.24,vec3(.018),vec3(.30,.265,.205));
   diffuseColor.rgb=sampled*mix(.96,1.065,scar);
   float dust=(1.-smoothstep(.39,.455,vLocal.y))*.24;
   diffuseColor.rgb=mix(diffuseColor.rgb,vec3(.049,.033,.016),dust);diffuseColor.a=1.;
  `,`
   float heightValue=mix(texture2D(barkHeight,mainUV).r,texture2D(barkHeight,branchUV).r,blend);
   float strength=(.46+.10*heightValue)*(1.-scar*.36);
   vec3 trunkNormal=barkNormal(normal,-vViewPosition,mainUV,texture2D(barkNormalMap,mainUV).rgb,strength);
   vec3 branchNormal=barkNormal(normal,-vViewPosition,branchUV,texture2D(barkNormalMap,branchUV).rgb,strength);
   normal=normalize(mix(trunkNormal,branchNormal,blend));
   float roughValue=mix(texture2D(barkRough,mainUV).r,texture2D(barkRough,branchUV).r,blend);
   roughnessFactor=clamp(.86+.13*roughValue,.90,.99);
  `,{barkColor:{value:color},barkNormalMap:{value:normal},barkHeight:{value:height},barkRough:{value:rough}});
 }
 const leafFragment=`
 float age=clamp(vColor.r,0.,1.),tip=clamp(vColor.g,0.,1.);
 diffuseColor.rgb=mix(vec3(.035,.090,.025),vec3(.15,.250,.073),age*.66+tip*.24);
 diffuseColor.rgb*=.96+fb(vLocal*13.)*.08;
 `;
 const leaf=extend(new THREE.MeshStandardMaterial({color:'#ffffff',vertexColors:true,roughness:.78,metalness:0}),'scale-leaf-v2',leafFragment);
 const leafLow=extend(new THREE.MeshStandardMaterial({color:'#ffffff',vertexColors:true,roughness:.78,metalness:0}),'scale-leaf-low-pcf8-v1',leafFragment);
 const before=leafLow.onBeforeCompile;leafLow.onBeforeCompile=shader=>{before(shader);let chunk=THREE.ShaderChunk.shadowmap_pars_fragment;if(chunk.includes('sampleIndex<16')){chunk=chunk.replace('sampleIndex<16','sampleIndex<8').replace('vogelDiskSample(sampleIndex,16,0.0)','vogelDiskSample(sampleIndex,8,0.0)').replace('shadow *= 0.0625','shadow *= 0.125');shader.fragmentShader=shader.fragmentShader.replace('#include <shadowmap_pars_fragment>',chunk);}};
 
 const ceramic=extend(new THREE.MeshStandardMaterial({color:'#6f5140',roughness:.86}),'unglazed-clay-v1',`
 float pore=fb(vLocal*370.);float kiln=fb(vLocal*5.+vec3(4,2,1));
 diffuseColor.rgb*=.78+.30*kiln+.16*pore;
 `,`
 float ch=(fb(vLocal*610.)-.5)*.00016;vec3 sp=-vViewPosition;vec3 sx=dFdx(sp),sy=dFdy(sp);vec3 r1=cross(sy,normal),r2=cross(normal,sx);float det=dot(sx,r1);normal=normalize(abs(det)*normal-sign(det)*(dFdx(ch)*r1+dFdy(ch)*r2));
 `);
 const stone=extend(new THREE.MeshStandardMaterial({color:'#ffffff',roughness:.97}),'bedding-stone-v2',`
 float mineral=fb(vLocal*8.);float grain=fb(vLocal*260.);float pale=smoothstep(.66,.82,n3(vLocal*37.));diffuseColor.rgb=mix(vec3(.065,.075,.076),vec3(.20,.205,.182),mineral*.82+grain*.22)+vec3(pale*.028);
 `,`
 float sh=(fb(vLocal*72.)-.5)*.0022+(n3(vLocal*280.)-.5)*.00035;vec3 sp=-vViewPosition;vec3 sx=dFdx(sp),sy=dFdy(sp);vec3 r1=cross(sy,normal),r2=cross(normal,sx);float det=dot(sx,r1);normal=normalize(abs(det)*normal-sign(det)*(dFdx(sh)*r1+dFdy(sh)*r2));
 `);
 const soil=extend(new THREE.MeshStandardMaterial({color:'#ffffff',roughness:1,vertexColors:true}),'root-soil-v2',`
 float coverage=smoothstep(.14,.48,vColor.r);float grain=fb(vLocal*280.);
 diffuseColor.rgb=mix(vec3(.032,.023,.012),vec3(.046,.074,.015),coverage)*(.72+grain*.5);
 `);
 const grit=extend(new THREE.MeshStandardMaterial({color:'#655344',roughness:1}),'root-grit-v1',`diffuseColor.rgb*=.65+fb(vLocal*100.)*.65;`);
 return {wood,leaf,leafLow,ceramic,stone,soil,grit,twig:new THREE.MeshStandardMaterial({color:'#493728',roughness:.94}),clay:new THREE.MeshStandardMaterial({color:'#b2afa5',roughness:1})};
}
export function applyHeroMaterials(hero,m,clay=false){
 hero.traverse(o=>{if(!o.isMesh)return;o.castShadow=true;o.receiveShadow=true;
  const n=o.material.name;if(!clay&&n.includes('foliage'))o.userData.foliageMaterials={high:m.leaf,low:m.leafLow};
  o.material=clay?m.clay:n.includes('twig')?m.twig:n.includes('wood')?m.wood:n.includes('foliage')?m.leaf:n.includes('ceramic')?m.ceramic:n.toLowerCase().includes('loose')?m.grit:n.includes('soil')?m.soil:m.stone;
 });
}
