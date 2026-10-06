import * as THREE from 'three';
// Closed scale leaves retain all original vertices, normal directions, crowns
// and shadow sampling. Weak subsurface approximation uses only each physical
// direct light after its existing occlusion and attenuation.
export function applyLeafFinish(m,finish='original'){
 if(!['original','botanical'].includes(finish))throw Error('Unknown leaf finish');
 if(finish==='original')return {name:finish,closedGeometryUnchanged:true,roughness:.78,backScatter:0};
 for(const leaf of [m.leaf,m.leafLow]){
  leaf.roughness=.86;const prior=leaf.onBeforeCompile,key=leaf.customProgramCacheKey();
  leaf.onBeforeCompile=shader=>{prior(shader);let physical=THREE.ShaderChunk.lights_physical_pars_fragment;const direct='reflectedLight.directDiffuse += irradiance * BRDF_Lambert( material.diffuseContribution );';
   if(!physical.includes(direct))throw Error('Physical leaf direct-light hook changed');
   physical=physical.replace(direct,`float backFacing = saturate( -dot( geometryNormal, directLight.direction ) );
    vec3 transmitted = directLight.color * backFacing * 0.055;
    reflectedLight.directDiffuse += (irradiance * 0.945 + transmitted) * BRDF_Lambert( material.diffuseContribution );`);
   shader.fragmentShader=shader.fragmentShader.replace('#include <lights_physical_pars_fragment>',physical);
  };
  leaf.customProgramCacheKey=()=>key+'-closed-scale-botanical-v1';
 }
 return {name:finish,closedGeometryUnchanged:true,roughness:.86,backScatter:.055,frontEnergy:.945,usesOccludedPhysicalDirectLights:true,emissive:0,alpha:1};
}
