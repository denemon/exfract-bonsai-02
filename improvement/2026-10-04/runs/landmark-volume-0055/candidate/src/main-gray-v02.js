import {createRenderPartition} from './render-partition.js';
import './style.css';
import * as THREE from 'three';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';
import {DRACOLoader} from 'three/addons/loaders/DRACOLoader.js';
import {makeMaterials,applyHeroMaterials} from '../../../ancient-volume-0810/site/src/materials.js';

import {createScene as createBestScene,loadGardenAssets as loadBestAssets} from '../../../depth-balance-1905/background/scene.js';
import {prepareFoliageLOD} from '../../../ancient-volume-0810/site/src/foliage-lod.js';
import {configureShadowFilter} from './shadow-filter.js';
const query=new URLSearchParams(location.search);for(const [key,value]of Object.entries({'room-light':'proposed',canopy:'depth-v01',finish:'material-v01',composition:'pavilion-designed','background-finish':'refined','background-light':'refined',perf:'balanced',grain:'hash',surface:'shoji-v01',space:'r20'}))if(!query.has(key))query.set(key,value);history.replaceState(null,'',location.pathname+'?'+query+location.hash);const study=query.get('study')||'garden';
const exactBest=query.get('space')==='r20';
const createScene=createBestScene,loadGardenAssets=loadBestAssets;
const HERO_SCALE=.66; // Approximately 1.06 m pot width and 1.5 m complete display height.
const canvas=document.querySelector('canvas'),reduced=matchMedia('(prefers-reduced-motion: reduce)');
const stats={ready:false,frames:0,mode:study,reduced:reduced.matches,firstFrameMs:null,framesMs:[],model:null};
window.__gardenStatus=stats;
let renderer,camera,garden,model,foliage,frame=0,lost=false,points=[],baseYaw=0,yaw=0,pitch=13,distance=5,zoom=1,target=new THREE.Vector3(),down,pinch;
const pointers=new Map();
const started=performance.now();
let loadDetailedFoliage;
async function loadCompressedGLB(loader,name){if(typeof DecompressionStream!=='function')return loader.loadAsync('/models/'+name+'.glb');const response=await fetch('/models/'+name+'.glb.gz');if(!response.ok)throw Error('Model fetch failed: '+response.status);let bytes=await response.arrayBuffer();if(new DataView(bytes).getUint32(0,true)!==0x46546c67)bytes=await new Response(new Blob([bytes]).stream().pipeThrough(new DecompressionStream('gzip'))).arrayBuffer();return loader.parseAsync(bytes,'/models/');}
function still(){document.documentElement.classList.remove('ready');stats.ready=false;cancelAnimationFrame(frame);frame=0;}
function scanPoints(){points=[];if(query.get('frame')==='shared'){for(const x of [-1.55,1.30])for(const y of [-.08,2.28])for(const z of [-.72,.68])points.push(new THREE.Vector3(x,y,z).multiplyScalar(HERO_SCALE));return;}garden.subject.updateMatrixWorld(true);garden.subject.traverse(o=>{if(!o.isMesh||!o.visible)return;if(o.isInstancedMesh){o.geometry.computeBoundingBox();const b=o.userData.foliageEnvelope||o.geometry.boundingBox,m=new THREE.Matrix4();for(let i=0;i<o.count;i++){o.getMatrixAt(i,m);m.premultiply(o.matrixWorld);for(const x of [b.min.x,b.max.x])for(const y of [b.min.y,b.max.y])for(const z of [b.min.z,b.max.z])points.push(new THREE.Vector3(x,y,z).applyMatrix4(m));}}else{const p=o.geometry.attributes.position;for(let i=0;i<p.count;i+=8)points.push(new THREE.Vector3().fromBufferAttribute(p,i).applyMatrix4(o.matrixWorld));}});}
function setCamera(fit=true){
 const a=THREE.MathUtils.degToRad(yaw),b=THREE.MathUtils.degToRad(pitch);const front=new THREE.Vector3(Math.sin(a)*Math.cos(b),Math.sin(b),Math.cos(a)*Math.cos(b));const right=new THREE.Vector3(Math.cos(a),0,-Math.sin(a));const up=new THREE.Vector3().crossVectors(front,right);
 if(fit){
  const box=new THREE.Box3().setFromPoints(points);box.getCenter(target);target.y+=innerHeight>innerWidth?.04:.025;
  const tan=Math.tan(THREE.MathUtils.degToRad(camera.fov/2)),portrait=innerHeight>innerWidth;distance=0;
  const fillX=portrait?.94:.84,fillY=portrait?.78:.80;
  const tx=tan*camera.aspect*fillX,ty=tan*fillY;let ax=-Infinity,bx=Infinity,ay=-Infinity,by=Infinity,zmax=-Infinity;
  const q=new THREE.Vector3();for(const p of points){q.copy(p).sub(target);const z=q.dot(front),x=q.dot(right),y=q.dot(up);ax=Math.max(ax,x+tx*z);bx=Math.min(bx,x-tx*z);ay=Math.max(ay,y+ty*z);by=Math.min(by,y-ty*z);zmax=Math.max(zmax,z);}
  distance=Math.max((ax-bx)/(2*tx),(ay-by)/(2*ty),zmax+.2);target.addScaledVector(right,(ax+bx)/2+(portrait?0:.095)).addScaledVector(up,(ay+by)/2+(portrait?distance*tan*.015:0));
 }
 if(fit&&innerWidth>=innerHeight&&study==='garden'&&!query.has('detail')){target.set(0,.78,0);const d=query.get('composition')==='baseline'?3.95:3.65;distance=Math.max(d,d*1.45/(innerWidth/innerHeight));}
 const detail=query.get('detail');if(detail==='wood'){target.set(-.03,1.03,.02).multiplyScalar(HERO_SCALE);distance=2.05*HERO_SCALE;}else if(detail==='leaf'){target.set(-.72,1.32,.04).multiplyScalar(HERO_SCALE);distance=1.4*HERO_SCALE;}else if(detail==='pot'){target.set(0,.31,0).multiplyScalar(HERO_SCALE);distance=2.65*HERO_SCALE;}
 if(!detail)distance*=zoom;
 camera.position.copy(target).addScaledVector(front,distance);camera.lookAt(target);camera.updateMatrixWorld();
 const bounds={left:1,right:0,top:1,bottom:0},q=new THREE.Vector3();for(const p of points){q.copy(p).project(camera);const x=(q.x+1)/2,y=(1-q.y)/2;bounds.left=Math.min(bounds.left,x);bounds.right=Math.max(bounds.right,x);bounds.top=Math.min(bounds.top,y);bounds.bottom=Math.max(bounds.bottom,y);}
 stats.framing=bounds;stats.camera={yaw,pitch,distance,zoom,position:camera.position.toArray(),target:target.toArray()};
}
function render(){if(lost||document.hidden)return;const t=performance.now();stats.foliageLOD=foliage.update(camera,innerHeight,distance,query.get("foliage-lod"));if(stats.foliageLOD.changed)renderer.shadowMap.needsUpdate=true;if(stats.foliageLOD.needsHigh)loadDetailedFoliage?.();renderer.info.reset();renderer.render(garden.scene,camera);stats.frames++;stats.framesMs.push(performance.now()-t);if(stats.framesMs.length>120)stats.framesMs.shift();stats.drawCalls=renderer.info.render.calls;stats.triangles=renderer.info.render.triangles;if(!stats.ready){stats.firstFrameMs=performance.now()-started;stats.navigationToFirstFrameMs=performance.now();stats.ready=true;document.documentElement.classList.add('ready');}}
function requestRender(){if(frame)return;frame=requestAnimationFrame(()=>{frame=0;render();});}
function resize(){const portrait=innerHeight>innerWidth,ratio=innerWidth/innerHeight;camera.aspect=ratio;camera.fov=portrait?Number(query.get("fov")||54):38;camera.updateProjectionMatrix();baseYaw=Number(query.get('yaw')??(portrait?(ratio<.40?-42:ratio<.52?-27:-23):0));if(portrait&&!query.has('yaw'))baseYaw=query.get('composition')==='baseline'?(innerWidth<350?-33:-30):(query.get('space')==='balanced'?(ratio<.42?-42:ratio<.52?-36:-34):(ratio<.42?-45:ratio<.52?-40:-30));if(!portrait&&!query.has('yaw'))baseYaw=query.get('space')==='balanced'?-7:query.get('space')==='offset'?-18:0;yaw=baseYaw;pitch=Number(query.get('pitch')??(portrait?6:10));zoom=1;setCamera();const pixel=Math.min(devicePixelRatio,1.6);renderer.setPixelRatio(pixel);renderer.setSize(innerWidth,innerHeight,false);renderer.shadowMap.needsUpdate=true;stats.viewport=[innerWidth,innerHeight];render();}
try{
 if(query.get("shadow-filter")!=="original")configureShadowFilter();
 const context=canvas.getContext('webgl2',{alpha:false,antialias:true,powerPreference:'high-performance'});if(!context)throw Error('WebGL2 unavailable');
 renderer=new THREE.WebGLRenderer({canvas,context,antialias:true});renderer.outputColorSpace=THREE.SRGBColorSpace;renderer.toneMapping=THREE.ACESFilmicToneMapping;renderer.toneMappingExposure=study==='clay'?1.05:1.0;renderer.shadowMap.enabled=true;renderer.shadowMap.type=query.get('shadow-type')==='vsm'?THREE.VSMShadowMap:query.get('shadow-type')==='soft'?THREE.PCFSoftShadowMap:THREE.PCFShadowMap;renderer.shadowMap.autoUpdate=false;
 const draco=new DRACOLoader().setDecoderPath('/draco/').setWorkerLimit(2),loader=new GLTFLoader().setDRACOLoader(draco),reference=query.has('reference'),candidate=query.get('candidate')||'landmark-v02';
 const [gltf,wood,mats,loadedAssets]=await Promise.all([reference?loader.loadAsync(query.get('reference')==='basis'?'/models/basis.glb':'/models/hero.glb'):loadCompressedGLB(loader,'hero-low'),['landmark-v01','landmark-v02'].includes(candidate)&&!reference?loader.loadAsync('/compare/r24/models/'+candidate+'.glb'):null,makeMaterials(),loadGardenAssets(loader,study)]);
 model=gltf.scene;foliage=prepareFoliageLOD(gltf);
 if(wood){const old=[];model.traverse(o=>{if(o.isMesh&&(/Continuous[_ ]aged/.test(o.name)||/Terminal[_ ]twig/.test(o.name)))old.push(o)});if(old.length!==2)throw Error('Expected original core and twig hierarchy');for(const o of old)o.removeFromParent();for(const o of [...wood.scene.children])model.add(o);}
 let detailedRequest;loadDetailedFoliage=()=>{if(detailedRequest)return;stats.detailLoading=true;detailedRequest=loadCompressedGLB(loader,'foliage-high').then(detail=>{foliage.installHigh(detail);stats.detailLoading=false;stats.detailReady=true;requestRender();}).catch(error=>{stats.detailLoading=false;stats.detailError=error.message;});};
 window.addEventListener('pagehide',()=>draco.dispose(),{once:true});
 model.scale.setScalar(HERO_SCALE);applyHeroMaterials(model,mats,study==='clay');stats.worldScale=HERO_SCALE;stats.loading={parallelAssets:true,sharedDraco:true,woodReplacement:Boolean(wood),decoderWorkerLimit:2,exactGeometrySplit:!reference,losslessModelGzip:!reference&&typeof DecompressionStream==='function'};
 // Failed shape gate: gray only. Material finish intentionally not started.
 if(true)model.traverse(o=>{if(o.isMesh&&(/Continuous[_ ]aged/.test(o.name)||/Terminal[_ ]twig/.test(o.name)))o.material=new THREE.MeshStandardMaterial({color:'#88847e',roughness:1,metalness:0});});
 if(study==='normals')model.traverse(o=>{if(o.isMesh)o.material=new THREE.MeshNormalMaterial();});
 if(query.get('shadow')==='0')model.traverse(o=>{if(o.isMesh)o.receiveShadow=false;});
 if(query.has('bare'))model.traverse(o=>{if(/Canopy|foliage|sprays|twig|shoots|particles|terminal[ _]branch/i.test(o.name))o.visible=false;});
 garden=await createScene(model,study,loadedAssets);const renderPartition=createRenderPartition(renderer,garden.scene,garden.subject,model,query.get('render')||'both');stats.renderPartition=renderPartition.stats;stats.garden=garden.metadata;stats.layout=garden.layout;camera=new THREE.PerspectiveCamera(38,1,.04,60);scanPoints();renderer.info.autoReset=false;
 stats.model={meshes:0,vertices:0,instances:0,hasWoodMasks:false};model.traverse(o=>{if(o.isMesh){stats.model.meshes++;stats.model.vertices+=o.geometry.attributes.position.count;if(o.isInstancedMesh)stats.model.instances+=o.count;if(/Continuous[_ ]aged/.test(o.name)){stats.model.authoringVersion=o.userData.authoring_version;stats.model.hasWoodMasks=Boolean(o.geometry.attributes.color);stats.model.woodAttributes=Object.keys(o.geometry.attributes);stats.model.woodUVRange=[Infinity,Infinity,-Infinity,-Infinity];const uv=o.geometry.attributes.uv;if(uv)for(let n=0;n<uv.count;n+=100){const r=stats.model.woodUVRange;r[0]=Math.min(r[0],uv.getX(n));r[1]=Math.min(r[1],uv.getY(n));r[2]=Math.max(r[2],uv.getX(n));r[3]=Math.max(r[3],uv.getY(n));}stats.model.woodMaterial=o.material.customProgramCacheKey();}}});
 window.__garden={stats,foliage,renderPartition,scene:garden.scene,subject:garden.subject,camera,renderer,render,model,setView:(azimuth,elevation=13)=>{yaw=azimuth;pitch=elevation;setCamera();render();},setKey:(p)=>{garden.key.position.set(...p);renderer.shadowMap.needsUpdate=true;render();}};
 window.addEventListener('resize',resize);reduced.addEventListener('change',()=>{stats.reduced=reduced.matches;render();});document.addEventListener('visibilitychange',()=>{if(!document.hidden)render();});
 canvas.addEventListener('pointerdown',e=>{if(reduced.matches)return;pointers.set(e.pointerId,new THREE.Vector2(e.clientX,e.clientY));down={x:e.clientX,y:e.clientY,yaw,pitch};if(pointers.size===2){const [a,b]=[...pointers.values()];pinch={distance:a.distanceTo(b),zoom};}canvas.setPointerCapture(e.pointerId);});
 canvas.addEventListener('pointermove',e=>{if(!pointers.has(e.pointerId)||reduced.matches)return;pointers.set(e.pointerId,new THREE.Vector2(e.clientX,e.clientY));if(pointers.size===2&&pinch){const [a,b]=[...pointers.values()];zoom=THREE.MathUtils.clamp(pinch.zoom*pinch.distance/Math.max(a.distanceTo(b),10),.60,1);setCamera();requestRender();return;}if(!down)return;const portrait=innerHeight>innerWidth,limit=portrait?6:8;yaw=THREE.MathUtils.clamp(down.yaw+(e.clientX-down.x)*.045,baseYaw-limit,baseYaw+limit);pitch=THREE.MathUtils.clamp(down.pitch+(e.clientY-down.y)*.035,portrait?6:8,portrait?10:12);setCamera();requestRender();});
 const release=e=>{pointers.delete(e.pointerId);pinch=undefined;const next=pointers.values().next().value;down=next?{x:next.x,y:next.y,yaw,pitch}:undefined;};
 canvas.addEventListener('pointerup',release);canvas.addEventListener('pointercancel',release);
 canvas.addEventListener('wheel',e=>{if(reduced.matches)return;e.preventDefault();zoom=THREE.MathUtils.clamp(zoom*Math.exp(e.deltaY*.0012),.60,1);setCamera();requestRender();},{passive:false});
 canvas.addEventListener('dblclick',()=>{if(!reduced.matches)resize();});
 canvas.addEventListener('webglcontextlost',e=>{e.preventDefault();lost=true;still();});canvas.addEventListener('webglcontextrestored',()=>{lost=false;renderer.shadowMap.needsUpdate=true;render();});
 resize();
}catch(error){stats.error=error?.message||error?.type||String(error);still();console.warn('Static garden retained:',error.message);}
