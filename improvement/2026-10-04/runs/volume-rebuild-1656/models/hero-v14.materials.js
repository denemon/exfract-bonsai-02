import * as THREE from 'three';
const noiseGLSL=`
float hash31(vec3 p){p=fract(p*.1031);p+=dot(p,p.yzx+33.33);return fract((p.x+p.y)*p.z);}
float n3(vec3 p){vec3 i=floor(p),f=fract(p);f=f*f*(3.-2.*f);return mix(mix(mix(hash31(i),hash31(i+vec3(1,0,0)),f.x),mix(hash31(i+vec3(0,1,0)),hash31(i+vec3(1,1,0)),f.x),f.y),mix(mix(hash31(i+vec3(0,0,1)),hash31(i+vec3(1,0,1)),f.x),mix(hash31(i+vec3(0,1,1)),hash31(i+vec3(1,1,1)),f.x),f.y),f.z);}
float fb(vec3 p){return n3(p)*.57+n3(p*2.07+3.2)*.28+n3(p*4.13-1.7)*.15;}
vec3 woodSpace(vec3 p,vec3 growth){vec3 t=normalize(growth);vec3 n=normalize(vec3(t.y,-t.x,0.)+vec3(.00001,0.,0.));vec3 b=cross(t,n);return vec3(dot(p,n),dot(p,b),dot(p,t));}
`;
function extend(material,name,fragment,normalFragment=''){
 const directed=name.startsWith('spatial-wood');if(directed)material.defines={...material.defines,USE_UV1:'',USE_UV2:''};
 material.onBeforeCompile=shader=>{
  shader.vertexShader='varying vec3 vLocal; varying vec2 vFlow;\n'+(directed?'varying vec3 vGrowth; varying float vTrust;\n':'')+shader.vertexShader;
  shader.vertexShader=shader.vertexShader.replace('#include <begin_vertex>','#include <begin_vertex>\nvLocal=position;vFlow=uv;'+(directed?'vGrowth=vec3(uv1.x,1.-uv1.y,uv2.x);vTrust=1.-uv2.y;':''));
  shader.fragmentShader='varying vec3 vLocal; varying vec2 vFlow;\n'+(directed?'varying vec3 vGrowth; varying float vTrust;\n':'')+noiseGLSL+shader.fragmentShader;
  shader.fragmentShader=shader.fragmentShader.replace('#include <color_fragment>','#include <color_fragment>\n'+fragment);
  if(normalFragment)shader.fragmentShader=shader.fragmentShader.replace('#include <normal_fragment_maps>','#include <normal_fragment_maps>\n'+normalFragment);
 };
 material.customProgramCacheKey=()=>name;
 return material;
}
export function makeMaterials(){
 const wood=new THREE.MeshStandardMaterial({color:'#ffffff',vertexColors:true,roughness:.90,metalness:0});
 extend(wood,'spatial-wood-v3',`
 float living=clamp(vColor.r,0.,1.);float age=clamp(vColor.b,0.,1.);
 vec3 w=woodSpace(vLocal,vGrowth);float warp=fb(vLocal*6.);
 float trust=clamp(vTrust,0.,1.);float flow=vFlow.x+warp*.006;
 float fibre=mix(fb(vLocal*110.),fb(vec3(flow*360.,vFlow.y*8.,.3)),trust);
 float ridges=mix(fb(vLocal*18.),fb(vec3(flow*41.,vFlow.y*2.7,.8)),trust);
 float checks=pow(smoothstep(.60,.84,n3(vec3(flow*154.,vFlow.y*4.4,7.))),3.)*(.2+.8*n3(vLocal*31.))*trust;
 vec3 heart=mix(vec3(.235,.228,.205),vec3(.460,.442,.397),.20+fibre*.40+ridges*.24)*(.87+age*.22);
 vec3 bark=mix(vec3(.066,.025,.010),vec3(.245,.092,.033),fibre*.44+ridges*.29+age*.21);
 diffuseColor.rgb=mix(heart,bark,living)*(1.-checks*.42);
 `,`
 float wg=fb(vec3(vFlow.x*165.,vFlow.y*4.6,.9));
 float wh=(wg-.5)*.00055*clamp(vTrust,0.,1.)+(fb(vLocal*210.)-.5)*.00006;
 vec3 sp=-vViewPosition;vec3 sx=dFdx(sp),sy=dFdy(sp);vec3 r1=cross(sy,normal),r2=cross(normal,sx);float det=dot(sx,r1);
 normal=normalize(abs(det)*normal-sign(det)*(dFdx(wh)*r1+dFdy(wh)*r2));
 `);
 const leaf=new THREE.MeshStandardMaterial({color:'#ffffff',vertexColors:true,roughness:.78,metalness:0});
 extend(leaf,'scale-leaf-v2',`
 float age=clamp(vColor.r,0.,1.),tip=clamp(vColor.g,0.,1.);
 diffuseColor.rgb=mix(vec3(.028,.064,.018),vec3(.13,.205,.060),age*.66+tip*.24);
 diffuseColor.rgb*=.96+fb(vLocal*13.)*.08;
 `);
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
 return {wood,leaf,ceramic,stone,soil,grit,twig:new THREE.MeshStandardMaterial({color:'#493728',roughness:.94}),clay:new THREE.MeshStandardMaterial({color:'#b2afa5',roughness:1})};
}
export function applyHeroMaterials(hero,m,clay=false){
 hero.traverse(o=>{if(!o.isMesh)return;o.castShadow=true;o.receiveShadow=true;
  const n=o.material.name;
  o.material=clay?m.clay:n.includes('twig')?m.twig:n.includes('wood')?m.wood:n.includes('foliage')?m.leaf:n.includes('ceramic')?m.ceramic:n.toLowerCase().includes('loose')?m.grit:n.includes('soil')?m.soil:m.stone;
 });
}
