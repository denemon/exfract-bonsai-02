import {selectedSettings} from './selected-settings.js';
import {backgroundShadowFilter} from './m28-procedural-detail.js';
import * as THREE from 'three';
const refined=()=>selectedSettings().get('background-finish')==='refined';
export function backgroundLeafMaterial(){
 const m=new THREE.MeshStandardMaterial({color:refined()?'#82906b':'#3b5443',roughness:.94,metalness:0});
 if(refined()){
  m.onBeforeCompile=s=>{
   // Thin botanical tissue passes a small fraction of backside irradiance.
   // It remains shadowed/attenuated by the same real finite world sources.
   const chunk=THREE.ShaderChunk.lights_physical_pars_fragment;
   const old='reflectedLight.directDiffuse += irradiance * BRDF_Lambert( material.diffuseContribution );';
   if(!chunk.includes(old))throw Error('Physical diffuse shader contract changed');
   const next=old+'\n float leafBack=saturate(-dot(geometryNormal,directLight.direction));\n reflectedLight.directDiffuse += leafBack*.24*directLight.color*vec3(.80,1.,.54)*BRDF_Lambert(material.diffuseContribution);';
   s.fragmentShader=s.fragmentShader.replace('#include <lights_physical_pars_fragment>',chunk.replace(old,next));
  };
  m.customProgramCacheKey=()=> 'garden-thin-tissue-refined-v01';
 }
 return backgroundShadowFilter(m);
}
export function backgroundLightScale(){return selectedSettings().get('background-light')==='refined'?1.32:1;}
