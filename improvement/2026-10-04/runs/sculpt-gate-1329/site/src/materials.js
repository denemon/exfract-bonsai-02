import * as THREE from 'three';
const noiseGLSL=`
float hash31(vec3 p){p=fract(p*.1031);p+=dot(p,p.yzx+33.33);return fract((p.x+p.y)*p.z);}
float n3(vec3 p){vec3 i=floor(p),f=fract(p);f=f*f*(3.-2.*f);return mix(mix(mix(hash31(i),hash31(i+vec3(1,0,0)),f.x),mix(hash31(i+vec3(0,1,0)),hash31(i+vec3(1,1,0)),f.x),f.y),mix(mix(hash31(i+vec3(0,0,1)),hash31(i+vec3(1,0,1)),f.x),mix(hash31(i+vec3(0,1,1)),hash31(i+vec3(1,1,1)),f.x),f.y),f.z);}
float fb(vec3 p){return n3(p)*.57+n3(p*2.07+3.2)*.28+n3(p*4.13-1.7)*.15;}
`;
function extend(material,name,fragment,normalFragment=''){
 material.onBeforeCompile=shader=>{
  shader.vertexShader='varying vec3 vLocal; varying vec2 vFlow;\n'+shader.vertexShader;
  shader.vertexShader=shader.vertexShader.replace('#include <begin_vertex>','#include <begin_vertex>\nvLocal=position;vFlow=uv;');
  shader.fragmentShader='varying vec3 vLocal; varying vec2 vFlow;\n'+noiseGLSL+shader.fragmentShader;
  shader.fragmentShader=shader.fragmentShader.replace('#include <color_fragment>','#include <color_fragment>\n'+fragment);
  if(normalFragment)shader.fragmentShader=shader.fragmentShader.replace('#include <normal_fragment_maps>','#include <normal_fragment_maps>\n'+normalFragment);
 };
 material.customProgramCacheKey=()=>name;
 return material;
}
export function makeMaterials(){
 const wood=new THREE.MeshStandardMaterial({color:'#ffffff',vertexColors:true,roughness:.90,metalness:0});
 extend(wood,'continuous-wood-v3',`
 float living=clamp(vColor.r,0.,1.);float age=clamp(vColor.b,0.,1.);
 float warp=fb(vec3(vFlow.x*7.,vFlow.y*1.5,vColor.g*9.));
 float flow=vFlow.x+warp*.038+sin(vFlow.y*4.1+vColor.g*8.)*.014;
 float fibre=fb(vec3(flow*260.,vFlow.y*7.,.3));
 float ridges=smoothstep(.22,.78,fb(vec3(flow*52.,vFlow.y*2.,2.)));
 float checks=pow(smoothstep(.49,.79,n3(vec3(flow*185.,vFlow.y*3.,7.))),3.)*(.2+.8*n3(vec3(flow*27.,vFlow.y*12.,7.)));
 vec3 heart=mix(vec3(.095,.079,.055),vec3(.305,.280,.237),.16+fibre*.54+ridges*.23);
 vec3 bark=mix(vec3(.055,.028,.013),vec3(.18,.088,.039),fibre*.45+ridges*.28+age*.20);
 diffuseColor.rgb=mix(heart,bark,living)*(1.-checks*.39);
 `,`
 float wg=fb(vec3(vFlow.x*95.,vFlow.y*3.,vColor.g*4.));
 float wh=(wg-.5)*.00035;
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
 return {wood,leaf,ceramic,stone,soil,grit,clay:new THREE.MeshStandardMaterial({color:'#b2afa5',roughness:1})};
}
export function applyHeroMaterials(hero,m,clay=false){
 hero.traverse(o=>{if(!o.isMesh)return;o.castShadow=true;o.receiveShadow=true;
  const n=o.material.name;
  o.material=clay?m.clay:n.includes('wood')?m.wood:n.includes('foliage')?m.leaf:n.includes('ceramic')?m.ceramic:n.toLowerCase().includes('loose')?m.grit:n.includes('soil')?m.soil:m.stone;
 });
}
