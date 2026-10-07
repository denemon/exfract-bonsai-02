import * as THREE from 'three';
import {applyUserGroundFinish} from './ground-finish.js';
import {createMoonScene as selected,loadMoonAssets as loadSelected} from './modules/m01-moon-court-whole-final-v01.js';
async function loadGround(){const started=performance.now(),r=await fetch(new URL('./garden/shore-ground.bin.gz',document.baseURI));if(!r.ok)throw Error('Terrain fetch '+r.status);let b=await r.arrayBuffer();if(new Uint8Array(b)[0]===31){if(typeof DecompressionStream!=='function')throw Error('Terrain gzip unavailable');b=await new Response(new Blob([b]).stream().pipeThrough(new DecompressionStream('gzip'))).arrayBuffer();}const h=new DataView(b);if(h.getUint32(0,true)!==0x53485231||h.getUint32(4,true)!==68252||h.getUint32(8,true)!==406626||h.getUint32(12,true)!==4||b.byteLength!==4356600)throw Error('Terrain binding mismatch');return {bytes:b,fetchAndDecodeMs:performance.now()-started};}
export async function loadMoonAssets(loader,study){const [assets,shore]=await Promise.all([loadSelected(loader,study),loadGround()]);assets.shore=shore;return assets;}
function shoreMaterial(original){
 const m=original.clone(),previous=original.onBeforeCompile;
 m.onBeforeCompile=s=>{
  previous.call(m,s);s.vertexShader='attribute vec4 shoreFacies;varying vec4 vShoreFacies;\n'+s.vertexShader;s.vertexShader=s.vertexShader.replace('vCourtGround=(modelMatrix*vec4(transformed,1.)).xyz;','vCourtGround=(modelMatrix*vec4(transformed,1.)).xyz;vShoreFacies=shoreFacies;');
  s.fragmentShader='varying vec4 vShoreFacies;\n'+s.fragmentShader;
  const replace=(a,b)=>{if(!s.fragmentShader.includes(a))throw Error('Selected shore shader binding missing: '+a.slice(0,40));s.fragmentShader=s.fragmentShader.replace(a,b);};
  replace('float cd=cgIsland(cp)+.010*(en(vCourtGround*47.)-.5)+.005*(en(vCourtGround*101.)-.5),cm=1.-smoothstep(-.024,.017,cd);','float cd=vShoreFacies.w,cm=clamp(vShoreFacies.x,0.,1.)*mix(.38,1.,clamp(vShoreFacies.y,0.,1.));');
  replace('cWave=cos(cPhase*6.2831853),cLong=smoothstep(.07,.24,cd);','cWave=cos(cPhase*6.2831853),cLong=smoothstep(.028,.105,cd);');
  replace('cLocal=smoothstep(.025,.05,cd)*(1.-smoothstep(.11,.21,cd));','cLocal=0.;');
  replace('float cSoil=(1.-smoothstep(.008,.027,abs(cd+.023)))*(.18+.24*en(vCourtGround*27.));','float cSoil=clamp(vShoreFacies.z,0.,1.);');
  replace('diffuseColor.rgb=mix(cSand,vec3(.058,.046,.029),cSoil);','diffuseColor.rgb=mix(cSand,vec3(.080,.067,.043),cSoil);');
 };m.customProgramCacheKey=()=> 'continuous-shore-static-corrected-profile-v01';return m;
}
export async function createMoonScene(hero,study,assets){const g=await selected(hero,study,assets),started=performance.now(),b=assets.shore.bytes,n=68252;let at=16;const geom=new THREE.BufferGeometry();for(const [name,size]of [['position',3],['normal',3],['shoreFacies',4]]){geom.setAttribute(name,new THREE.BufferAttribute(new Float32Array(b,at,n*size),size));at+=n*size*4;}geom.setIndex(new THREE.BufferAttribute(new Uint32Array(b,at,406626),1));geom.computeBoundingBox();geom.computeBoundingSphere();const old=g.ground.geometry;g.ground.geometry=geom;g.ground.material=shoreMaterial(g.ground.material);g.ground.castShadow=true;old.dispose();g.metadata={...g.metadata,continuousShore:{version:'continuous-shore-static-corrected-profile-v01',lossless:true,vertices:n,triangles:135542,runtimeRefinement0:true,fetchAndDecodeMs:assets.shore.fetchAndDecodeMs,bindMs:performance.now()-started,rootStoneHeroCameraLightHeld:true,awardLevelQualityCertified:false}};return applyUserGroundFinish(g);}
