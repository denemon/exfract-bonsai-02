import * as THREE from 'three';

export const noise=`
float eh(vec3 p){p=fract(p*.1031);p+=dot(p,p.yzx+33.33);return fract((p.x+p.y)*p.z);}
float en(vec3 p){vec3 i=floor(p),f=fract(p);f=f*f*(3.-2.*f);return mix(mix(mix(eh(i),eh(i+vec3(1,0,0)),f.x),mix(eh(i+vec3(0,1,0)),eh(i+vec3(1,1,0)),f.x),f.y),mix(mix(eh(i+vec3(0,0,1)),eh(i+vec3(1,0,1)),f.x),mix(eh(i+vec3(0,1,1)),eh(i+vec3(1,1,1)),f.x),f.y),f.z);}
float ef(vec3 p){return en(p)*.62+en(p*2.13+3.7)*.26+en(p*4.27-2.6)*.12;}
float ellipse(vec2 p,vec2 centre,vec2 radius){return (length((p-centre)/radius)-1.)*min(radius.x,radius.y);}
float gardenMoss(vec2 p){
 float d=min(ellipse(p,vec2(-2.38,-1.12),vec2(1.65,3.8)),ellipse(p,vec2(-1.27,.67),vec2(.81,.62)));
 d=min(d,ellipse(p,vec2(2.06,-2.6),vec2(.73,2.5)));
 d+=.12*(ef(vec3(p*4.7,2.8))-.48)+.026*(en(vec3(p*36.,6.))- .5);
 return 1.-smoothstep(-.033,.028,d);
}
vec2 grainCell(vec2 p){vec2 q=p*290.,cell=floor(q),f=fract(q);float best=2.,tone=0.;
 for(int j=-1;j<=1;j++)for(int i=-1;i<=1;i++){vec2 o=vec2(float(i),float(j));vec2 r=vec2(eh(vec3(cell+o,2.)),eh(vec3(cell+o,8.)));vec2 v=o+.15+.7*r-f;float d=dot(v,v);if(d<best){best=d;tone=r.x;}}
 return vec2(sqrt(best),tone);
}
vec3 envBump(vec3 n,float height,vec3 position){vec3 a=dFdx(position),b=dFdy(position);vec3 r1=cross(b,n),r2=cross(n,a);float d=dot(a,r1);return normalize(abs(d)*n-sign(d)*(dFdx(height)*r1+dFdy(height)*r2));}
`;
function surface(name,base,fragment,bump='',roughness=.94){
 const m=new THREE.MeshStandardMaterial({color:base,roughness,metalness:0});
 m.onBeforeCompile=s=>{
  s.vertexShader='varying vec3 vEnv;\n'+s.vertexShader;
  s.vertexShader=s.vertexShader.replace('#include <begin_vertex>','#include <begin_vertex>\nvEnv=position;');
  s.fragmentShader='varying vec3 vEnv;\n'+noise+s.fragmentShader;
  s.fragmentShader=s.fragmentShader.replace('#include <color_fragment>','#include <color_fragment>\n'+fragment);
  if(bump)s.fragmentShader=s.fragmentShader.replace('#include <normal_fragment_maps>','#include <normal_fragment_maps>\n'+bump);
 };
 m.customProgramCacheKey=()=>name;return m;
}
export function gardenMaterials(){
 const ground=surface('garden-mineral-and-moss-v1','#ffffff',`
  vec2 cell=grainCell(vEnv.xz);float m=gardenMoss(vEnv.xz);float broad=ef(vEnv*3.4),fine=en(vEnv*520.);
  vec3 mineral=mix(vec3(.074,.082,.088),vec3(.19,.194,.182),cell.y*.58+broad*.28);
  mineral*=.84+.25*smoothstep(.04,.44,cell.x);
  vec3 moss=mix(vec3(.013,.027,.006),vec3(.060,.084,.016),ef(vEnv*75.)*.68+fine*.22);
  diffuseColor.rgb=mix(mineral,moss,m);
  vec2 r=abs(vEnv.xz)-vec2(.69,.39);float contact=max(r.x,r.y);
  float baseAO=1.-.46*exp(-max(contact,0.)*24.);
  float rock1=1.-.30*exp(-max(ellipse(vEnv.xz,vec2(-1.87,-1.54),vec2(.55,.40)),0.)*12.);
  float rock2=1.-.22*exp(-max(ellipse(vEnv.xz,vec2(-2.8,-2.70),vec2(.40,.35)),0.)*10.);
  diffuseColor.rgb*=baseAO*rock1*rock2;
 `,`
  float gritRelief=.0009*(1.-smoothstep(.08,.5,cell.x));
  float mossRelief=(en(vEnv*420.)-.5)*.0010+(ef(vEnv*110.)-.5)*.0012;
  normal=envBump(normal,mix(gritRelief,mossRelief,m),-vViewPosition);
 `,1);
 function wood(axis,name,color){return surface(name,color,`
  vec3 q=vEnv.${axis};float age=ef(q*vec3(23.,.63,25.));float fibre=ef(q*vec3(380.,3.,310.));
  float weave=en(q*vec3(130.,1.9,114.)+vec3(ef(q*2.)*4.));
  diffuseColor.rgb*=.64+age*.42+fibre*.18+weave*.10;
 `,`normal=envBump(normal,(fibre-.5)*.00032+(weave-.5)*.00018,-vViewPosition);`,.84);}
 const vertical=wood('xyz','cedar-posts-v1','#58412f');
 const horizontal=wood('yxz','cedar-floor-v1','#66503c');
 const lengthwise=wood('xzy','cedar-eaves-v1','#453727');
 const rearWood=wood('xyz','aged-cedar-boundary-v1','#615347');
 const plaster=surface('lime-plaster-v1','#807c6f',`float lime=ef(vEnv*72.);diffuseColor.rgb*=.90+lime*.18;`,`normal=envBump(normal,(lime-.5)*.00023,-vViewPosition);`,1);
 const stone=surface('garden-weathered-rock-v1','#ffffff',`
  float broad=ef(vEnv*5.7),grain=ef(vEnv*180.);float vein=smoothstep(.63,.70,ef(vEnv*vec3(8.,42.,13.)));
  diffuseColor.rgb=mix(vec3(.032,.041,.046),vec3(.145,.16,.15),broad*.7+grain*.28)+vec3(.024)*vein;
  float mossBand=(1.-smoothstep(.05,.29,vEnv.y+(ef(vEnv*14.)-.5)*.22));
  diffuseColor.rgb=mix(diffuseColor.rgb,vec3(.028,.043,.009)*(.65+grain*.7),mossBand*.74);
 `,`normal=envBump(normal,(ef(vEnv*94.)-.5)*.0019+(en(vEnv*330.)-.5)*.00028,-vViewPosition);`,.98);
 const foundation=surface('garden-foundation-v1','#3c4140',`float f=ef(vEnv*34.);diffuseColor.rgb*=.8+f*.38;`,`normal=envBump(normal,(f-.5)*.0006,-vViewPosition);`,.99);
 const roof=surface('quiet-charcoal-roof-v1','#282e31',`float clay=ef(vEnv*32.);diffuseColor.rgb*=.74+clay*.40;`,`normal=envBump(normal,(clay-.5)*.00018,-vViewPosition);`,.9);
 const paper=new THREE.MeshStandardMaterial({color:'#c2aa80',roughness:1,emissive:'#b18b53',emissiveIntensity:.09});
 const leaves=new THREE.MeshStandardMaterial({color:'#405a26',vertexColors:true,roughness:.89});
 return {ground,vertical,horizontal,lengthwise,rearWood,plaster,stone,foundation,roof,paper,leaves};
}
