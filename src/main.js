import * as THREE from 'three';
import {EffectComposer} from 'three/addons/postprocessing/EffectComposer.js';
import {RenderPass} from 'three/addons/postprocessing/RenderPass.js';
import {GTAOPass} from 'three/addons/postprocessing/GTAOPass.js';
import {OutputPass} from 'three/addons/postprocessing/OutputPass.js';
import {SMAAPass} from 'three/addons/postprocessing/SMAAPass.js';
import {createGarden} from './scene.js';
import {viewFor} from './framing.js';

const canvas=document.querySelector('#scene');
const reduced=matchMedia('(prefers-reduced-motion: reduce)');
const started=performance.now();
let renderer,composer,garden,camera,frame=0,frames=0,previous=0,lost=false;
let targetOffset=new THREE.Vector2(),offset=new THREE.Vector2(),view;
const stats={frames:0,ready:false,reduced:reduced.matches,firstFrameMs:null,frameMs:[],drawCalls:0,triangles:0};
function fallback(){canvas.style.visibility='hidden';document.documentElement.classList.remove('ready');stats.ready=false;}
function boundsOnScreen(){
 const result={left:1,right:0,top:1,bottom:0};
 garden.subject.traverse(o=>{if(!o.isMesh)return;const p=o.geometry.attributes.position;const m=new THREE.Matrix4().multiplyMatrices(camera.projectionMatrix,camera.matrixWorldInverse).multiply(o.matrixWorld).elements;
  for(let i=0;i<p.count;i++){const x=p.getX(i),y=p.getY(i),z=p.getZ(i),w=m[3]*x+m[7]*y+m[11]*z+m[15],sx=((m[0]*x+m[4]*y+m[8]*z+m[12])/w+1)/2,sy=(1-(m[1]*x+m[5]*y+m[9]*z+m[13])/w)/2;result.left=Math.min(result.left,sx);result.right=Math.max(result.right,sx);result.top=Math.min(result.top,sy);result.bottom=Math.max(result.bottom,sy);}
 });return result;
}
function resize(){
 const width=innerWidth,height=innerHeight;view=viewFor(width,height);camera.fov=view.fov;camera.aspect=width/height;camera.position.set(...view.position);camera.lookAt(...view.target);camera.updateProjectionMatrix();
 const dpr=Math.min(devicePixelRatio,view.portrait?1.6:1.5);renderer.setPixelRatio(dpr);renderer.setSize(width,height);composer.setPixelRatio(dpr);composer.setSize(width,height);
 camera.updateMatrixWorld(true);offset.set(0,0);targetOffset.set(0,0);stats.framing=boundsOnScreen();stats.viewport=[width,height];stats.buffer=[canvas.width,canvas.height];stats.camera=view;
 renderer.shadowMap.needsUpdate=true;previous=0;render(performance.now(),true);
}
function render(now,forced=false){
 if(lost||document.hidden)return;
 if(!forced&&now-previous<32)return;
 const a=performance.now();
 if(!reduced.matches){
  offset.lerp(targetOffset,.06);camera.position.set(view.position[0]+offset.x*.025,view.position[1]+offset.y*.012,view.position[2]);camera.lookAt(...view.target);
  // Each shoot bends less than a millimetre: the canopy does not rotate.
  const f=garden.foliageGroups[0];f.position.x=Math.sin(now*.0006)*.0012;f.position.z=Math.sin(now*.00048)*.0006;
 }
 renderer.info.reset();composer.render();stats.intervals=stats.intervals||[];if(previous)stats.intervals.push(now-previous);if(stats.intervals.length>120)stats.intervals.shift();previous=now;frames++;stats.frames=frames;stats.drawCalls=renderer.info.render.calls;stats.triangles=renderer.info.render.triangles;
 stats.frameMs.push(performance.now()-a);if(stats.frameMs.length>120)stats.frameMs.shift();
 if(!stats.ready){stats.firstFrameMs=performance.now()-started;stats.ready=true;canvas.style.visibility='visible';document.documentElement.classList.add('ready');}
}
function loop(now){frame=0;render(now);if(!reduced.matches&&!document.hidden&&!lost)frame=requestAnimationFrame(loop);}
function resume(){if(frame)cancelAnimationFrame(frame);frame=0;stats.reduced=reduced.matches;if(!lost&&!document.hidden){render(performance.now(),true);if(!reduced.matches)frame=requestAnimationFrame(loop);}}

try{
 const gl=canvas.getContext('webgl2',{alpha:false,antialias:false,powerPreference:'high-performance'});if(!gl)throw new Error('WebGL2 unavailable');
 renderer=new THREE.WebGLRenderer({canvas,context:gl,antialias:false,alpha:false});renderer.outputColorSpace=THREE.SRGBColorSpace;renderer.toneMapping=THREE.ACESFilmicToneMapping;renderer.toneMappingExposure=.90;
 renderer.info.autoReset=false;renderer.shadowMap.enabled=true;renderer.shadowMap.type=THREE.PCFSoftShadowMap;renderer.shadowMap.autoUpdate=false;
 garden=createGarden();camera=new THREE.PerspectiveCamera(42,1,.1,50);
 composer=new EffectComposer(renderer);composer.addPass(new RenderPass(garden.scene,camera));
 const ao=new GTAOPass(garden.scene,camera,innerWidth,innerHeight);ao.blendIntensity=.62;ao.updateGtaoMaterial({radius:.23,distanceExponent:1.8,thickness:.6});composer.addPass(ao);composer.addPass(new OutputPass());composer.addPass(new SMAAPass());
 window.__garden={stats,scene:garden.scene,camera,renderer,composer,bounds:garden.bounds,render:()=>render(performance.now(),true)};
 canvas.addEventListener('webglcontextlost',e=>{e.preventDefault();lost=true;if(frame)cancelAnimationFrame(frame);frame=0;fallback();});
 canvas.addEventListener('webglcontextrestored',()=>{lost=false;renderer.shadowMap.needsUpdate=true;resume();});
 window.addEventListener('resize',resize);reduced.addEventListener('change',resume);document.addEventListener('visibilitychange',resume);
 window.addEventListener('pointermove',e=>{if(!reduced.matches&&e.pointerType==='mouse')targetOffset.set(e.clientX/innerWidth*2-1,e.clientY/innerHeight*2-1);},{passive:true});
 window.addEventListener('pointerleave',()=>targetOffset.set(0,0));resize();resume();
}catch(error){fallback();stats.error=error.message;console.warn('Garden still displayed:',error.message);}
