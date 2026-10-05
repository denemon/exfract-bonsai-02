import * as THREE from 'three';
const noiseGLSL=`
float hash31(vec3 p){p=fract(p*.1031);p+=dot(p,p.yzx+33.33);return fract((p.x+p.y)*p.z);}
float n3(vec3 p){vec3 i=floor(p),f=fract(p);f=f*f*(3.-2.*f);return mix(mix(mix(hash31(i),hash31(i+vec3(1,0,0)),f.x),mix(hash31(i+vec3(0,1,0)),hash31(i+vec3(1,1,0)),f.x),f.y),mix(mix(hash31(i+vec3(0,0,1)),hash31(i+vec3(1,0,1)),f.x),mix(hash31(i+vec3(0,1,1)),hash31(i+vec3(1,1,1)),f.x),f.y),f.z);}
float fb(vec3 p){return n3(p)*.57+n3(p*2.07+3.2)*.28+n3(p*4.13-1.7)*.15;}
vec2 cellHash(vec2 cell){cell.x=mod(cell.x,48.);return vec2(hash31(vec3(cell,2.13)),hash31(vec3(cell,7.91)));}
vec3 barkSurface(vec2 flow,vec3 point){
 float angle=flow.x*6.2831853;vec3 periodic=vec3(cos(angle)*2.7,sin(angle)*2.7,flow.y*3.1);
 float warp=fb(periodic+vec3(1.7,3.2,0.));
 vec2 p=vec2(flow.x*48.+(warp-.5)*3.8,flow.y*19.+(n3(periodic*1.7)-.5)*2.0);
 vec2 cell=floor(p),f=fract(p);float first=99.,second=99.,grainId=0.;
 for(int y=-1;y<=1;y++)for(int x=-1;x<=1;x++){
  vec2 offset=vec2(float(x),float(y));vec2 hash=cellHash(cell+offset);vec2 q=offset+(.17+hash*.66)-f;
  float d=dot(q,q);if(d<first){second=first;first=d;grainId=hash.x;}else if(d<second){second=d;}
 }
 float distance=sqrt(second)-sqrt(first);float aa=max(fwidth(distance)*.65,.003);
 float edge=1.-smoothstep(.020-aa,.064+aa,distance);
 float flake=(1.-edge)*(.58+.30*grainId+.12*n3(periodic*9.));
 float fibre=n3(vec3(cos(angle)*109.,sin(angle)*109.,flow.y*7.3+warp));
 fibre*=.45+.55*n3(vec3(cos(angle)*21.,sin(angle)*21.,flow.y*33.));
 return vec3(edge,flake,fibre);
}
vec3 woodSpace(vec3 p,vec3 growth){vec3 t=normalize(growth);vec3 n=normalize(vec3(t.y,-t.x,0.)+vec3(.00001,0.,0.));vec3 b=cross(t,n);return vec3(dot(p,n),dot(p,b),dot(p,t));}
`;
function extend(material,name,fragment,normalFragment='',uniforms={}){
 const directed=name.startsWith('bark-');if(directed)material.defines={...material.defines,USE_UV1:''};
 material.onBeforeCompile=shader=>{
  Object.assign(shader.uniforms,uniforms);
  shader.vertexShader='varying vec3 vLocal; varying vec2 vFlow;\n'+(directed?'varying float vCalibre;\n':'')+shader.vertexShader;
  shader.vertexShader=shader.vertexShader.replace('#include <begin_vertex>','#include <begin_vertex>\nvLocal=position;vFlow=uv;'+(directed?'vFlow=vec2(uv.x,1.-uv.y);vCalibre=uv1.x;':''));
  shader.fragmentShader='varying vec3 vLocal; varying vec2 vFlow;\n'+(directed?'varying float vCalibre;\n':'')+noiseGLSL+shader.fragmentShader;
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
  extend(wood,'bark-connected-weather-v1',`
   vec3 surface=barkSurface(vFlow,vLocal);
   float scar=clamp(vColor.g,0.,1.);
   float variation=fb(vLocal*vec3(9.,4.,8.));
   vec3 bark=mix(vec3(.076,.049,.030),vec3(.160,.119,.078),variation*.65+surface.y*.29);
   vec3 aged=mix(vec3(.106,.084,.060),vec3(.169,.146,.112),variation*.63+surface.y*.28);
   diffuseColor.rgb=mix(bark,aged,scar*.76)*mix(1.,.59,surface.x*(1.-scar*.40));
   float dust=(1.-smoothstep(.39,.455,vLocal.y))*.36;
   diffuseColor.rgb=mix(diffuseColor.rgb,vec3(.049,.033,.016),dust);diffuseColor.a=1.;
  `,`
   float scarNormal=clamp(vColor.g,0.,1.);
   float barkHeight=surface.y*(.0009+.004*clamp(vCalibre,.02,.24))*(1.-scarNormal*.54)+surface.z*.00030;
   vec3 sp=-vViewPosition;vec3 sx=dFdx(sp),sy=dFdy(sp);vec3 r1=cross(sy,normal),r2=cross(normal,sx);float det=dot(sx,r1);
   normal=normalize(abs(det)*normal-sign(det)*(dFdx(barkHeight)*r1+dFdy(barkHeight)*r2));
   roughnessFactor=clamp(.91+surface.x*.06+(variation-.5)*.05,.86,.99);
  `);
 }
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
