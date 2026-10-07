import {selectedSettings} from './selected-settings.js';
import {makeSandRakeField} from './m32-sand-rake-field.js';
import {balancedPerformance,physicalDetailTextures,sampledNoise,backgroundShadowFilter} from './m17-procedural-detail.js';
import {makeSpatialTerrain} from './m33-terrain-field.js';
import * as THREE from 'three';
export const noise=`
float eh(vec3 p){p=fract(p*.1031);p+=dot(p,p.yzx+33.33);return fract((p.x+p.y)*p.z);}
float en(vec3 p){vec3 i=floor(p),f=fract(p);f=f*f*(3.-2.*f);return mix(mix(mix(eh(i),eh(i+vec3(1,0,0)),f.x),mix(eh(i+vec3(0,1,0)),eh(i+vec3(1,1,0)),f.x),f.y),mix(mix(eh(i+vec3(0,0,1)),eh(i+vec3(1,0,1)),f.x),mix(eh(i+vec3(0,1,1)),eh(i+vec3(1,1,1)),f.x),f.y),f.z);}
float ef(vec3 p){return en(p)*.62+en(p*2.13+3.7)*.26+en(p*4.27-2.6)*.12;}
vec2 mineralGrain(vec2 p){vec2 c=floor(p),f=fract(p);float nearest=4.,shade=.5;for(int j=-1;j<=1;j++)for(int i=-1;i<=1;i++){vec2 q=vec2(float(i),float(j)),cell=c+q;vec2 seed=vec2(eh(vec3(cell,4.2)),eh(vec3(cell,8.1)));float d=length(q+seed-f);if(d<nearest){nearest=d;shade=eh(vec3(cell,11.4));}}return vec2(nearest,shade);}
float ellipse(vec2 p,vec2 centre,vec2 radius){return (length((p-centre)/radius)-1.)*min(radius.x,radius.y);}
float gardenDistance(vec2 p){float d=min(ellipse(p,vec2(-2.38,-1.12),vec2(1.65,3.8)),ellipse(p,vec2(-1.27,.67),vec2(.81,.62)));d=min(d,ellipse(p,vec2(2.06,-2.6),vec2(.73,2.5)));return d+.16*(ef(vec3(p*4.7,2.8))-.48)+.022*(en(vec3(p*32.,6.))-.5);}
vec3 envBump(vec3 n,float height,vec3 position){vec3 a=dFdx(position),b=dFdy(position);vec3 r1=cross(b,n),r2=cross(n,a);float d=dot(a,r1);return normalize(abs(d)*n-sign(d)*(dFdx(height)*r1+dFdy(height)*r2));}
`;
function surface(name,base,fragment,bump='',roughness=.94,local=false,uniforms={}){
 const balanced=balancedPerformance(),hashDetail=selectedSettings().get('grain')==='hash';if(balanced){const t=physicalDetailTextures();uniforms={...uniforms,uSpatialNoise:{value:t.spatial,kind:'sampler3D'},uGravelDetail:{value:t.mineral}};}
 const m=new THREE.MeshStandardMaterial({color:base,roughness,metalness:0});
 m.onBeforeCompile=s=>{
  Object.assign(s.uniforms,uniforms);
  const vary=local?'varying vec3 vGrain;varying vec3 vGrainNormal;varying float vBoard;':'';
  s.vertexShader='varying vec3 vEnv;\n'+vary+(local?'attribute vec3 grainPosition;attribute vec3 grainNormal;attribute float boardSeed;':'')+'\n'+s.vertexShader;
  s.vertexShader=s.vertexShader.replace('#include <begin_vertex>','#include <begin_vertex>\nvEnv=position;'+(local?'vGrain=grainPosition;vGrainNormal=grainNormal;vBoard=boardSeed;':''));
  s.fragmentShader='varying vec3 vEnv;\n'+vary+Object.keys(uniforms).map(n=>'uniform '+(uniforms[n].kind||'sampler2D')+' '+n+';').join('')+(balanced?(hashDetail?noise.slice(0,noise.indexOf('vec2 mineralGrain'))+sampledNoise.slice(sampledNoise.indexOf('vec2 mineralGrain')):sampledNoise)+noise.slice(noise.indexOf('float ellipse')):noise)+s.fragmentShader;
  s.fragmentShader=s.fragmentShader.replace('#include <color_fragment>','#include <color_fragment>\n'+fragment);
  if(bump)s.fragmentShader=s.fragmentShader.replace('#include <normal_fragment_maps>','#include <normal_fragment_maps>\n'+bump);
 };
 m.customProgramCacheKey=()=>name+(selectedSettings().get('background-finish')==='refined'?'-refined-v20':'-baseline')+(balanced?(hashDetail?'-hash-grain-detail':'-sampled-detail'):'-procedural-original');return backgroundShadowFilter(m);
}
export async function gardenMaterials(){
 const balanced=balancedPerformance();const refined=selectedSettings().get('background-finish')==='refined';
 const finish=selectedSettings().get("finish")==="material-v01";
 const loader=new THREE.TextureLoader();const maps=await Promise.all([loader.loadAsync('garden/mineral.webp'),loader.loadAsync(refined?(balanced?'materials/moss-color.webp':'materials/moss-photogrammetry.webp'):'garden/moss.webp')]);
 const mossHeight=balanced&&refined?await loader.loadAsync('materials/moss-height.webp'):maps[1];mossHeight.wrapS=mossHeight.wrapT=THREE.RepeatWrapping;mossHeight.colorSpace=balanced&&refined?THREE.NoColorSpace:maps[1].colorSpace;mossHeight.anisotropy=4;
 maps.push(makeSpatialTerrain());
 for(const t of maps.slice(0,2)){t.colorSpace=THREE.SRGBColorSpace;t.wrapS=t.wrapT=THREE.RepeatWrapping;t.anisotropy=4;}
 maps[2].colorSpace=THREE.NoColorSpace;maps[2].wrapS=maps[2].wrapT=THREE.ClampToEdgeWrapping;maps[2].minFilter=maps[2].magFilter=THREE.LinearFilter;maps[2].generateMipmaps=false;
 const mistSand=selectedSettings().get('mist-sand')!=='baseline',earthWall=selectedSettings().get('tsuiji-finish')!=='flat';
 const dryGarden=selectedSettings().get('sand')!=='baseline',rakeField=dryGarden?makeSandRakeField():null;
 const ground=surface(dryGarden?(mistSand?'mist-greywhite-raked-court-v50':'raked-dry-court-v41'):'continuous-near-grown-ground-v30-v02','#ffffff',`
  vec2 fieldUV=(vEnv.xz-vec2(-6.,-7.))/vec2(12.,14.);
  vec3 field=texture2D(uTerrain,fieldUV).rgb;
  float inside=step(0.,fieldUV.x)*step(fieldUV.x,1.)*step(0.,fieldUV.y)*step(fieldUV.y,1.);
  vec4 mineralMap=texture2D(uMineral,vEnv.xz/.36),mossMap=texture2D(uMoss,vEnv.xz/${refined?'.45':'.42'});
  float physicalMossHeight=${balanced&&refined?'texture2D(uMossHeight,vEnv.xz/.45).r':'mossMap.a'};
  float nearGarden=smoothstep(-3.3,-2.85,vEnv.z)*(1.-smoothstep(1.35,1.65,vEnv.z))*smoothstep(-4.,-3.6,vEnv.x)*(1.-smoothstep(-.80,-.62,vEnv.x));
  float m=${refined?'mix(smoothstep(.13,.78,field.r),smoothstep(.22,.98,field.r),nearGarden)':'field.r'}*inside,organic=field.g*inside;
  float broad=en(vEnv*3.4);vec3 mineral=mineralMap.rgb*(.96+.08*broad);
  ${refined?'vec2 gravelGrain=mineralGrain(vEnv.xz/.006);float grainWeight=1.-smoothstep(.005,.016,length(fwidth(vEnv)));mineral*=mix(1.,.82+.30*gravelGrain.y,grainWeight);float gravelHeight=.0012*pow(max(0.,1.-gravelGrain.x/.59),1.6)*grainWeight;':'float gravelHeight=0.;'}
  ${finish?'float luma=dot(mineral,vec3(.2126,.7152,.0722));mineral=mix(mineral,vec3(luma)*vec3(.98,1.00,1.025),.28);':''}
  ${dryGarden?`float sandWeight=${mistSand?'1.-inside*smoothstep(.015,.07,max(field.r,field.g))':'inside*(1.-smoothstep(.015,.07,max(field.r,field.g)))'};
  float rakeDistance=texture2D(uRakeDistance,fieldUV).r,rakePhase=rakeDistance/.066;
  float rakeFootprint=fwidth(rakePhase),rakeVisible=1.-smoothstep(.20,.68,rakeFootprint);
  float rakeWave=cos(rakePhase*6.28318530718);
  float rakeRelief=${mistSand?.00042:.00070}*rakeWave*rakeVisible;
  float quietGrain=${mistSand?".992+.016*broad+.003*(mineralMap.r-mineralMap.g)":".965+.045*broad+(.018*(mineralMap.r-mineralMap.g))"};
  vec3 dryMineral=${mistSand?"vec3(.31,.324,.339)":"vec3(.47,.455,.42)"}*quietGrain*(1.-${mistSand?.012:.026}*(.5-.5*rakeWave)*rakeVisible);
  mineral=mix(mineral,dryMineral,sandWeight);`:''}
  float mossFine=en(vEnv*vec3(171.,28.,183.));float mossPatch=en(vEnv*vec3(23.,5.,19.));
  vec3 moss=mossMap.rgb*${refined?'vec3(.75,.90,.61)*(.87+.11*mossPatch+.07*physicalMossHeight)':'(.83+.17*broad)'};
  vec3 soil=vec3(.043,.036,.022)*(.80+.30*physicalMossHeight);
  diffuseColor.rgb=mix(mineral,soil,organic*.91);
  diffuseColor.rgb=mix(diffuseColor.rgb,moss,m);
  vec2 r=abs(vEnv.xz)-vec2(.66,.34);float contact=length(max(r,0.))-.08;
  float baseAO=1.-.52*exp(-max(contact,0.)*29.);
  float rock1=1.-.22*exp(-max(ellipse(vEnv.xz,vec2(-1.87,-1.54),vec2(.55,.40)),0.)*12.);
  float rock2=1.-.17*exp(-max(ellipse(vEnv.xz,vec2(-2.8,-2.70),vec2(.40,.35)),0.)*10.);
  diffuseColor.rgb*=baseAO;
 `,`normal=envBump(normal,mix(${dryGarden?`mix(mineralMap.a*${finish?.0023:.0010}+gravelHeight,(mineralMap.a-.5)*${mistSand?.00008:.00026}+rakeRelief,sandWeight)`:`mineralMap.a*${finish?.0023:.0010}+gravelHeight`},physicalMossHeight*${refined?'mix(.013,.0055,nearGarden)':finish?.0068:.0034}${refined?'+(mossFine-.5)*.0008/(1.+length(fwidth(vEnv))*120.)':''},m),-vViewPosition);`,1,false,{uMineral:{value:maps[0]},uMoss:{value:maps[1]},uTerrain:{value:maps[2]},uMossHeight:{value:mossHeight},...(dryGarden?{uRakeDistance:{value:rakeField}}:{})});
 ground.userData.mossTexture=maps[1];ground.userData.dryGarden=rakeField?.userData||null;ground.userData.mistSand={active:mistSand,targetLinear:[.31,.324,.339],rakePathExactlyR42:true,rakeAmplitudeMeters:mistSand?.00042:.00070,broadVariationAmplitude:mistSand?.016:.045,onlyMineralFinishChanged:true,emission:0,wetGloss:0};
 function wood(axis,name,color){return surface(name,color,`
  vec3 q=vGrain.${axis};vec3 face=abs(vGrainNormal.${axis});
  q.x+=vBoard*.71;q.z+=vBoard*.39;
  float age=en(q*vec3(11.,.43,13.));float warp=en(q*vec3(6.,.56,7.));
  float fibre=en(q*vec3(265.,1.6,239.)+vec3(warp*.65,0.,warp*.81));
  float weave=en(q*vec3(76.,.8,88.)+vec3(warp*.35,0.,warp*.5));
  float rings=sin(length(q.xz+vec2(.017,.061))*250.+age*1.1)*.5+.5;
  float endFace=smoothstep(.66,.94,face.y);
  float lengthGrain=${finish?".78+age*.23+fibre*.075+weave*.045":".89+age*.12+fibre*.055+weave*.045"};
  float endGrain=.81+age*.13+rings*.10;
  diffuseColor.rgb*=mix(lengthGrain,endGrain,endFace)*(.946+.096*vBoard);
  diffuseColor.rgb*=.91+.09*smoothstep(.11,.33,vEnv.y);
 `,`normal=envBump(normal,mix((fibre-.5)*${refined?.00055:finish?.00032:.00017}+(weave-.5)*${refined?.00023:finish?.00016:.00010},(rings-.5)*${refined?.00029:finish?.00020:.00010},endFace),-vViewPosition);`,.91,true);}
 const vertical=wood('xyz','long-grain-post-v2','#60503d');
 const horizontal=wood('yxz','long-grain-floor-v2','#695541');
 const lengthwise=wood('xzy','long-grain-beam-v2','#594737');
 const rearWood=earthWall?surface('tsuiji-earth-charcoal-v50','#89877f',`
  float earthBroad=en(vEnv*vec3(.92,.71,1.1));
  float earthGrain=en(vEnv*vec3(91.,83.,87.));
  float packedLayer=sin(vEnv.y*25.+.17*en(vec3(vEnv.x*.63,1.4,vEnv.z)));
  float earthRain=en(vEnv*vec3(4.1,.24,2.7));
  float timberFibres=en(vEnv*vec3(91.,.8,77.));
  vec3 clay=diffuseColor.rgb*(.931+.058*earthBroad+.018*earthGrain+.008*packedLayer);
  clay*=1.-.027*earthRain*smoothstep(1.24,1.91,vEnv.y);
  clay*=.91+.09*smoothstep(.14,.44,vEnv.y);
  vec3 charredTimber=vec3(.017,.020,.0205)*(.95+.07*timberFibres);
  vec3 footing=vec3(.087,.094,.090)*(.93+.09*earthGrain);
  diffuseColor.rgb=vBoard<.5?clay:(vBoard<1.5?charredTimber:footing);
 `,`float wallHeight=vBoard<.5?((earthGrain-.5)*.00015+packedLayer*.00016):(vBoard<1.5?(timberFibres-.5)*.00018:(earthGrain-.5)*.00040);normal=envBump(normal,wallHeight,-vViewPosition);`,.99,true):surface('tsuiji-neutral-shape-v01','#77766e','', '',1,true);
 if(earthWall){const previous=rearWood.onBeforeCompile;rearWood.onBeforeCompile=s=>{previous.call(rearWood,s);s.fragmentShader=s.fragmentShader.replace('#include <roughnessmap_fragment>','#include <roughnessmap_fragment>\nroughnessFactor=vBoard<.5?.99:(vBoard<1.5?.95:1.);');};}
 rearWood.userData.tsuiji={active:earthWall,earthBaseSRGB:'#89877f',timberLinear:[.017,.020,.0205],materialRegions:'constant per closed geometry piece boardSeed0 earth /1 charcoal timber /2 stone footing',earthRoughness:.99,timberRoughness:.95,footingRoughness:1,tinySurfaceHeightMeters:.00040,noEmission:true,noWetGloss:true,ageingAmplitudeSmall:true};

 const plaster=surface('lime-plaster-v2','#8a8271',`
  float lime=en(vEnv*86.);diffuseColor.rgb*=.956+lime*.072;
  float floorOcclusion=.72+.28*smoothstep(.33,.91,vEnv.y);
  float ceilingOcclusion=1.-.17*exp(-abs(vEnv.y-2.63)*7.);
  diffuseColor.rgb*=floorOcclusion*ceilingOcclusion;
 `,`normal=envBump(normal,(lime-.5)*.00013,-vViewPosition);`,1);
 const stone=surface('weathered-fracture-contact-v1','#ffffff',`
  float broad=ef(vEnv*4.3),grain=en(vEnv*112.);
  float seam=smoothstep(.39,.47,ef(vec3(vEnv.x*5.2,vEnv.y*18.+vEnv.z*4.,vEnv.z*6.6)));
  diffuseColor.rgb=mix(vec3(.052,.059,.055),vec3(.19,.193,.167),broad*.71+grain*.17)*(.88+.12*seam);
  vec3 field=texture2D(uTerrain,(vEnv.xz-vec2(-6.,-7.))/vec2(12.,14.)).rgb;
  float soilY=-.022+field.b*.30;
  float rootZone=1.-smoothstep(.012,.097,vEnv.y-soilY+(en(vEnv*15.)-.5)*.020);
  vec3 moss=texture2D(uMoss,vEnv.xz/.42).rgb;
  diffuseColor.rgb=mix(diffuseColor.rgb,moss*.88,rootZone*field.r*.78);
 `,`normal=envBump(normal,(en(vEnv*93.)-.5)*.0013+(en(vEnv*247.)-.5)*.0002,-vViewPosition);`,.98,false,{uTerrain:{value:maps[2]},uMoss:{value:maps[1]}});
 const treeBark=surface('background-bark-v2','#5a5040',`
  float bark=en(vEnv*vec3(135.,5.,127.));float older=en(vEnv*vec3(15.,1.3,19.));diffuseColor.rgb*=.82+older*.22+bark*.13;
 `,`normal=envBump(normal,(bark-.5)*.0008,-vViewPosition);`,.97);
 const foundation=surface('grounded-foundation-v3','#55584f',`float f=en(vEnv*39.);diffuseColor.rgb*=.88+f*.20;diffuseColor.rgb*=.63+.37*smoothstep(-.02,.11,vEnv.y);`,`normal=envBump(normal,(f-.5)*.0005,-vViewPosition);`,.99);
 const roof=surface('quiet-charcoal-roof-v2','#292e2f',`float clay=en(vEnv*35.);diffuseColor.rgb*=.90+clay*.16;`,`normal=envBump(normal,(clay-.5)*.00012,-vViewPosition);`,.96);
 const tatami=surface('quiet-woven-floor-v1','#79735b',`
  float fibre=en(vEnv*vec3(19.,2.,480.));float broad=en(vEnv*4.);
  diffuseColor.rgb*=.93+fibre*.042+broad*.046;
 `,`normal=envBump(normal,(fibre-.5)*.00012,-vViewPosition);`,1);
 const matBorder=new THREE.MeshStandardMaterial({color:'#33392d',roughness:1});
 const alcove=surface('deep-alcove-lime-v1','#89816e',`
  float lime=en(vEnv*86.);diffuseColor.rgb*=.95+lime*.055;
  diffuseColor.rgb*=.81+.19*smoothstep(.38,1.10,vEnv.y);
 `,`normal=envBump(normal,(lime-.5)*.00012,-vViewPosition);`,1);
 const paperFinish=selectedSettings().get('surface')==='shoji-v01';
 const paper=paperFinish?surface('dry-rice-fibre-paper-v20','#c9bea8',`
  float paperFibre=en(vGrain*vec3(239.,61.,211.));float paperThread=en(vGrain*vec3(57.,231.,49.));
  diffuseColor.rgb*=.944+.041*paperFibre+.015*paperThread;
 `,`normal=envBump(normal,(paperFibre-.5)*.000025+(paperThread-.5)*.000018,-vViewPosition);`,.98,true):new THREE.MeshStandardMaterial({color:refined?'#ab9b7e':'#bfa881',roughness:1});
 if(paperFinish){
  const previous=paper.onBeforeCompile,key=paper.customProgramCacheKey.bind(paper);
  paper.onBeforeCompile=s=>{
   previous.call(paper,s);
   const chunk=THREE.ShaderChunk.lights_physical_pars_fragment,old='reflectedLight.directDiffuse += irradiance * BRDF_Lambert( material.diffuseContribution );';
   if(!chunk.includes(old))throw Error('Physical paper diffuse contract changed');
   // Dry thin paper scatters a modest fraction of backside illumination from
   // the same finite light sources, with their existing shadow attenuation.
   const next=old+'\nfloat paperBack=saturate(-dot(geometryNormal,directLight.direction));reflectedLight.directDiffuse+=paperBack*.18*directLight.color*vec3(1.,.96,.90)*BRDF_Lambert(material.diffuseContribution);';
   s.fragmentShader=s.fragmentShader.replace('#include <lights_physical_pars_fragment>',chunk.replace(old,next));
  };
  paper.customProgramCacheKey=()=>key()+'-thin-paper-scattering-v20';
  paper.userData.finish='0.5mm dry washi model, authored fine fibres,18% backside irradiance scattering; no emission/transmission framebuffer';
 }

 const leaves=new THREE.MeshStandardMaterial({color:'#758052',vertexColors:false,roughness:.92});
 const mossTuft=new THREE.MeshStandardMaterial({color:'#506429',roughness:1});
 for(const material of [matBorder,paper,leaves,mossTuft])backgroundShadowFilter(material);
 return {tatami,matBorder,alcove,terrain:maps[2],mossTuft,ground,vertical,horizontal,lengthwise,rearWood,plaster,stone,foundation,roof,paper,leaves,treeBark,maps:maps.map(t=>({url:t.image.src,width:t.image.width,height:t.image.height}))};
}
