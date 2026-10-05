import * as THREE from 'three';
export const noise=`
float eh(vec3 p){p=fract(p*.1031);p+=dot(p,p.yzx+33.33);return fract((p.x+p.y)*p.z);}
float en(vec3 p){vec3 i=floor(p),f=fract(p);f=f*f*(3.-2.*f);return mix(mix(mix(eh(i),eh(i+vec3(1,0,0)),f.x),mix(eh(i+vec3(0,1,0)),eh(i+vec3(1,1,0)),f.x),f.y),mix(mix(eh(i+vec3(0,0,1)),eh(i+vec3(1,0,1)),f.x),mix(eh(i+vec3(0,1,1)),eh(i+vec3(1,1,1)),f.x),f.y),f.z);}
float ef(vec3 p){return en(p)*.62+en(p*2.13+3.7)*.26+en(p*4.27-2.6)*.12;}
float ellipse(vec2 p,vec2 centre,vec2 radius){return (length((p-centre)/radius)-1.)*min(radius.x,radius.y);}
float gardenDistance(vec2 p){float d=min(ellipse(p,vec2(-2.38,-1.12),vec2(1.65,3.8)),ellipse(p,vec2(-1.27,.67),vec2(.81,.62)));d=min(d,ellipse(p,vec2(2.06,-2.6),vec2(.73,2.5)));return d+.16*(ef(vec3(p*4.7,2.8))-.48)+.022*(en(vec3(p*32.,6.))-.5);}
vec3 envBump(vec3 n,float height,vec3 position){vec3 a=dFdx(position),b=dFdy(position);vec3 r1=cross(b,n),r2=cross(n,a);float d=dot(a,r1);return normalize(abs(d)*n-sign(d)*(dFdx(height)*r1+dFdy(height)*r2));}
`;
function surface(name,base,fragment,bump='',roughness=.94,local=false,uniforms={}){
 const m=new THREE.MeshStandardMaterial({color:base,roughness,metalness:0});
 m.onBeforeCompile=s=>{
  Object.assign(s.uniforms,uniforms);
  const vary=local?'varying vec3 vGrain;varying vec3 vGrainNormal;varying float vBoard;':'';
  s.vertexShader='varying vec3 vEnv;\n'+vary+(local?'attribute vec3 grainPosition;attribute vec3 grainNormal;attribute float boardSeed;':'')+s.vertexShader;
  s.vertexShader=s.vertexShader.replace('#include <begin_vertex>','#include <begin_vertex>\nvEnv=position;'+(local?'vGrain=grainPosition;vGrainNormal=grainNormal;vBoard=boardSeed;':''));
  s.fragmentShader='varying vec3 vEnv;\n'+vary+(uniforms.uMineral?'uniform sampler2D uMineral;uniform sampler2D uMoss;':'')+noise+s.fragmentShader;
  s.fragmentShader=s.fragmentShader.replace('#include <color_fragment>','#include <color_fragment>\n'+fragment);
  if(bump)s.fragmentShader=s.fragmentShader.replace('#include <normal_fragment_maps>','#include <normal_fragment_maps>\n'+bump);
 };
 m.customProgramCacheKey=()=>name;return m;
}
export async function gardenMaterials(){
 const loader=new THREE.TextureLoader();const maps=await Promise.all(['mineral','moss'].map(n=>loader.loadAsync('/garden/'+n+'.png')));
 for(const t of maps){t.colorSpace=THREE.SRGBColorSpace;t.wrapS=t.wrapT=THREE.RepeatWrapping;t.anisotropy=4;}
 const ground=surface('dry-mineral-moss-v2','#ffffff',`
  vec4 mineralMap=texture2D(uMineral,vEnv.xz/.36),mossMap=texture2D(uMoss,vEnv.xz/.22);
  float distanceToMoss=gardenDistance(vEnv.xz),m=1.-smoothstep(-.021,.027,distanceToMoss);
  float broad=en(vEnv*3.4),cushion=en(vEnv*13.);vec3 mineral=mineralMap.rgb*(.96+.08*broad);
  vec3 moss=mossMap.rgb*(.84+.22*cushion);float fray=smoothstep(.4,.68,mossMap.a);
  float edge=1.-smoothstep(0.,.063,abs(distanceToMoss));
  vec3 soil=vec3(.031,.024,.014)*(.83+.29*cushion);
  diffuseColor.rgb=mix(mineral,moss,m);diffuseColor.rgb=mix(diffuseColor.rgb,soil,edge*(.11+.14*(1.-fray)));
  vec2 r=abs(vEnv.xz)-vec2(.66,.34);float contact=length(max(r,0.))-.08;
  float baseAO=1.-.52*exp(-max(contact,0.)*29.);
  float rock1=1.-.30*exp(-max(ellipse(vEnv.xz,vec2(-1.87,-1.54),vec2(.55,.40)),0.)*12.);
  float rock2=1.-.22*exp(-max(ellipse(vEnv.xz,vec2(-2.8,-2.70),vec2(.40,.35)),0.)*10.);
  diffuseColor.rgb*=baseAO*rock1*rock2;
 `,`normal=envBump(normal,mix(mineralMap.a*.00085,mossMap.a*.0024,m),-vViewPosition);`,1,false,{uMineral:{value:maps[0]},uMoss:{value:maps[1]}});
 function wood(axis,name,color){return surface(name,color,`
  vec3 q=vGrain.${axis};vec3 face=abs(vGrainNormal.${axis});
  q.x+=vBoard*.71;q.z+=vBoard*.39;
  float age=en(q*vec3(11.,.43,13.));float warp=en(q*vec3(6.,.56,7.));
  float fibre=en(q*vec3(265.,1.6,239.)+vec3(warp*.65,0.,warp*.81));
  float weave=en(q*vec3(76.,.8,88.)+vec3(warp*.35,0.,warp*.5));
  float rings=sin(length(q.xz+vec2(.017,.061))*250.+age*1.1)*.5+.5;
  float endFace=smoothstep(.66,.94,face.y);
  float lengthGrain=.89+age*.12+fibre*.055+weave*.045;
  float endGrain=.81+age*.13+rings*.10;
  diffuseColor.rgb*=mix(lengthGrain,endGrain,endFace)*(.946+.096*vBoard);
  diffuseColor.rgb*=.91+.09*smoothstep(.11,.33,vEnv.y);
 `,`normal=envBump(normal,mix((fibre-.5)*.00017+(weave-.5)*.00010,(rings-.5)*.00010,endFace),-vViewPosition);`,.91,true);}
 const vertical=wood('xyz','long-grain-post-v2','#60503d');
 const horizontal=wood('yxz','long-grain-floor-v2','#695541');
 const lengthwise=wood('xzy','long-grain-beam-v2','#594737');
 const rearWood=wood('xyz','aged-cedar-boundary-v2','#635745');
 const plaster=surface('lime-plaster-v2','#8a8271',`
  float lime=en(vEnv*86.);diffuseColor.rgb*=.956+lime*.072;
  float floorOcclusion=.72+.28*smoothstep(.33,.91,vEnv.y);
  float ceilingOcclusion=1.-.17*exp(-abs(vEnv.y-2.63)*7.);
  diffuseColor.rgb*=floorOcclusion*ceilingOcclusion;
 `,`normal=envBump(normal,(lime-.5)*.00013,-vViewPosition);`,1);
 const stone=surface('quiet-weathered-rock-v2','#ffffff',`
  float broad=ef(vEnv*5.7),grain=en(vEnv*150.);
  diffuseColor.rgb=mix(vec3(.037,.046,.048),vec3(.15,.163,.154),broad*.72+grain*.22);
  float mossBand=1.-smoothstep(.05,.24,vEnv.y+(en(vEnv*14.)-.5)*.13);
  diffuseColor.rgb=mix(diffuseColor.rgb,vec3(.033,.050,.016)*(.87+grain*.23),mossBand*.75);
 `,`normal=envBump(normal,(en(vEnv*93.)-.5)*.0012+(en(vEnv*247.)-.5)*.0002,-vViewPosition);`,.98);
 const treeBark=surface('background-bark-v2','#5a5040',`
  float bark=en(vEnv*vec3(135.,5.,127.));float older=en(vEnv*vec3(15.,1.3,19.));diffuseColor.rgb*=.82+older*.22+bark*.13;
 `,`normal=envBump(normal,(bark-.5)*.0008,-vViewPosition);`,.97);
 const foundation=surface('grounded-foundation-v2','#404540',`float f=en(vEnv*39.);diffuseColor.rgb*=.88+f*.20;diffuseColor.rgb*=.63+.37*smoothstep(-.02,.11,vEnv.y);`,`normal=envBump(normal,(f-.5)*.0005,-vViewPosition);`,.99);
 const roof=surface('quiet-charcoal-roof-v2','#292e2f',`float clay=en(vEnv*35.);diffuseColor.rgb*=.90+clay*.16;`,`normal=envBump(normal,(clay-.5)*.00012,-vViewPosition);`,.96);
 const paper=new THREE.MeshStandardMaterial({color:'#bfa881',roughness:1});
 const leaves=new THREE.MeshStandardMaterial({color:'#758052',vertexColors:false,roughness:.92});
 const mossTuft=new THREE.MeshStandardMaterial({color:'#506429',roughness:1});
 return {mossTuft,ground,vertical,horizontal,lengthwise,rearWood,plaster,stone,foundation,roof,paper,leaves,treeBark,maps:maps.map(t=>({url:t.image.src,width:t.image.width,height:t.image.height}))};
}
