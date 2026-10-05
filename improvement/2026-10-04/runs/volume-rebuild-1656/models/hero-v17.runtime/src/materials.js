import * as THREE from 'three';
const noiseGLSL=`
float hash31(vec3 p){p=fract(p*.1031);p+=dot(p,p.yzx+33.33);return fract((p.x+p.y)*p.z);}
float n3(vec3 p){vec3 i=floor(p),f=fract(p);f=f*f*(3.-2.*f);return mix(mix(mix(hash31(i),hash31(i+vec3(1,0,0)),f.x),mix(hash31(i+vec3(0,1,0)),hash31(i+vec3(1,1,0)),f.x),f.y),mix(mix(hash31(i+vec3(0,0,1)),hash31(i+vec3(1,0,1)),f.x),mix(hash31(i+vec3(0,1,1)),hash31(i+vec3(1,1,1)),f.x),f.y),f.z);}
float fb(vec3 p){return n3(p)*.57+n3(p*2.07+3.2)*.28+n3(p*4.13-1.7)*.15;}
vec3 woodSpace(vec3 p,vec3 growth){vec3 t=normalize(growth);vec3 n=normalize(vec3(t.y,-t.x,0.)+vec3(.00001,0.,0.));vec3 b=cross(t,n);return vec3(dot(p,n),dot(p,b),dot(p,t));}
`;
function extend(material,name,fragment,normalFragment='',uniforms={}){
 const directed=name.startsWith('spatial-wood');if(directed)material.defines={...material.defines,USE_UV1:'',USE_UV2:''};
 material.onBeforeCompile=shader=>{
  Object.assign(shader.uniforms,uniforms);
  shader.vertexShader='varying vec3 vLocal; varying vec2 vFlow;\n'+(directed?'varying vec3 vGrowth; varying float vTrust;\n':'')+shader.vertexShader;
  shader.vertexShader=shader.vertexShader.replace('#include <begin_vertex>','#include <begin_vertex>\nvLocal=position;vFlow=uv;'+(directed?'vGrowth=vec3(uv1.x,1.-uv1.y,uv2.x);vTrust=1.-uv2.y;':''));
  shader.fragmentShader='varying vec3 vLocal; varying vec2 vFlow;\n'+(directed?'varying vec3 vGrowth; varying float vTrust; uniform sampler2D woodGrain;\n':'')+noiseGLSL+shader.fragmentShader;
  shader.fragmentShader=shader.fragmentShader.replace('#include <color_fragment>','#include <color_fragment>\n'+fragment);
  if(normalFragment)shader.fragmentShader=shader.fragmentShader.replace('#include <normal_fragment_maps>','#include <normal_fragment_maps>\n'+normalFragment);
 };
 material.customProgramCacheKey=()=>name;
 return material;
}
export async function makeMaterials(){
 const grain=await new THREE.TextureLoader().loadAsync('/textures/wood-grain.webp');grain.wrapS=grain.wrapT=THREE.RepeatWrapping;grain.colorSpace=THREE.NoColorSpace;grain.anisotropy=4;
 const wood=new THREE.MeshStandardMaterial({color:'#ffffff',vertexColors:true,roughness:.90,metalness:0});
 extend(wood,'spatial-wood-v4-tiled',`
 float age=clamp(vColor.b,0.,1.);float trust=clamp(vTrust,0.,1.);
 vec4 data=texture2D(woodGrain,vFlow*vec2(1.,.68));
 float stain=n3(vLocal*9.);float fibre=mix(.5,data.r,trust);
 float living=smoothstep(.25,.74,vColor.r+(stain-.5)*.075);
 vec3 heart=mix(vec3(.220,.216,.198),vec3(.490,.476,.427),fibre*.72+age*.19)*(.91+data.a*.13);
 vec3 bark=mix(vec3(.068,.024,.008),vec3(.243,.084,.025),fibre*.69+age*.14);
 diffuseColor.rgb=mix(heart,bark,living)*(1.-data.b*trust*.44);
 `,`
 float wh=(texture2D(woodGrain,vFlow*vec2(1.,.68)).g-.5)*.00022*clamp(vTrust,0.,1.);
 vec3 sp=-vViewPosition;vec3 sx=dFdx(sp),sy=dFdy(sp);vec3 r1=cross(sy,normal),r2=cross(normal,sx);float det=dot(sx,r1);
 normal=normalize(abs(det)*normal-sign(det)*(dFdx(wh)*r1+dFdy(wh)*r2));
 `,{woodGrain:{value:grain}});
 const leaf=new THREE.MeshStandardMaterial({color:'#ffffff',vertexColors:true,roughness:.78,metalness:0});
 extend(leaf,'scale-leaf-v2',`
 float age=clamp(vColor.r,0.,1.),tip=clamp(vColor.g,0.,1.);
 diffuseColor.rgb=mix(vec3(.035,.090,.025),vec3(.15,.250,.073),age*.66+tip*.24);
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
