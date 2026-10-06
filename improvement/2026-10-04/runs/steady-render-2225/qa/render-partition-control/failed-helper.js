import * as THREE from 'three';
// Draw organization only. Native mesh attributes, matrices, materials, LOD,
// physical lights and cached shadows remain the authoritative scene.
export function createRenderPartition(renderer,scene,subject,model,initialMode='original'){
 const original=renderer.render.bind(renderer),sources=[];
 model.traverse(o=>{if(o.isInstancedMesh&&o.userData.foliageEnvelope)sources.push(o)});
 const display=new THREE.Group();display.name='Equivalent closed-leaf display batches';display.visible=false;subject.add(display);
 const bounds=new THREE.Box3(),corner=new THREE.Vector3(),matrix=new THREE.Matrix4();
 model.updateWorldMatrix(true,true);
 model.traverse(o=>{if(!o.isMesh)return;const b=o.userData.foliageEnvelope||(o.geometry.computeBoundingBox(),o.geometry.boundingBox);if(o.isInstancedMesh){for(let n=0;n<o.count;n++){o.getMatrixAt(n,matrix);matrix.premultiply(o.matrixWorld);for(const x of [b.min.x,b.max.x])for(const y of [b.min.y,b.max.y])for(const z of [b.min.z,b.max.z])bounds.expandByPoint(corner.set(x,y,z).applyMatrix4(matrix))}}else bounds.union(b.clone().applyMatrix4(o.matrixWorld));});
 const sphere=bounds.getBoundingSphere(new THREE.Sphere()),excluded=[],proof=[],casters=[];
 scene.traverse(o=>{if(!o.isLight)return;if(o.castShadow)casters.push(o);if(!(o.isPointLight||o.isSpotLight)||!o.distance)return;const position=o.getWorldPosition(new THREE.Vector3()),nearest=bounds.distanceToPoint(position);let reason;
 if(nearest>o.distance+1e-5)reason={method:'Entire native + deferred-high envelope outside finite cutoff',minimumDistance:nearest,cutoff:o.distance};
 else if(o.isSpotLight){const axis=o.target.getWorldPosition(new THREE.Vector3()).sub(position).normalize(),to=sphere.center.clone().sub(position),distance=to.length();if(distance>sphere.radius){const separation=Math.acos(THREE.MathUtils.clamp(axis.dot(to.normalize()),-1,1)),minimumAngle=separation-Math.asin(sphere.radius/distance);if(minimumAngle>o.angle+1e-5)reason={method:'Entire native + deferred-high sphere outside spot cone',minimumAngleRadians:minimumAngle,coneHalfAngleRadians:o.angle,sphereRadius:sphere.radius};}}
 if(reason){excluded.push(o);proof.push({type:o.type,name:o.name,position:position.toArray(),...reason})}
 });
 let mode=initialMode,batches=[],batchKey='';
 const stats={mode,nativeFoliageGroups:sources.length,batchedGroups:0,batchActive:false,lightPartitionActive:false,drawPasses:1,excludedFiniteLights:proof,nativeEnvelope:{min:bounds.min.toArray(),max:bounds.max.toArray()},nativeBuffersAndMaterialsUnmodified:true,instanceMatricesCopiedBitExactly:true,fullShadowUpdates:0};
 function activateBatches(){
  if(!sources.length||sources.some(o=>!o.visible||o.material!==o.userData.foliageMaterials?.low))return false;
  const key=sources.map(o=>o.geometry.uuid+':'+o.material.uuid+':'+o.matrixWorld.elements.join(',')).join('|');
  if(key!==batchKey){
   for(const o of batches){display.remove(o);o.dispose();}batches=[];const grouped=new Map();
   for(const o of sources){const id=o.geometry.uuid+':'+o.material.uuid+':'+o.matrixWorld.elements.join(',')+':'+o.castShadow+':'+o.receiveShadow;let a=grouped.get(id);if(!a){a=[];grouped.set(id,a);}a.push(o);}
   for(const group of grouped.values()){
    const source=group[0],count=group.reduce((n,o)=>n+o.count,0),batch=new THREE.InstancedMesh(source.geometry,source.material,count);batch.name='Equivalent closed leaves '+batches.length;batch.matrixAutoUpdate=false;batch.matrix.copy(source.matrixWorld);batch.castShadow=source.castShadow;batch.receiveShadow=source.receiveShadow;batch.renderOrder=source.renderOrder;batch.layers.mask=source.layers.mask;
    let offset=0;for(const o of group){batch.instanceMatrix.array.set(o.instanceMatrix.array.subarray(0,o.count*16),offset);offset+=o.count*16;}
    batch.instanceMatrix.needsUpdate=true;batch.computeBoundingBox();batch.computeBoundingSphere();display.add(batch);batches.push(batch);
   }
   display.updateWorldMatrix(true,true);batchKey=key;stats.batchedGroups=batches.length;
  }
  for(const o of sources)o.visible=false;display.visible=true;return true;
 }
 function finishBatches(active){if(active){for(const o of sources)o.visible=true;display.visible=false;}}
 renderer.render=(input,camera)=>{
  if(input!==scene||mode==='original')return original(input,camera);
  const batchActive=(mode==='batch'||mode==='both')&&activateBatches();stats.batchActive=!!batchActive;
  const lightActive=(mode==='light-cull'||mode==='both')&&excluded.length>0&&subject.visible;stats.lightPartitionActive=!!lightActive;stats.drawPasses=lightActive?2:1;
  try{
   if(!lightActive)return original(scene,camera);
   // Build every physical caster's cached map from the complete equivalent
   // scene. The split color passes must never regenerate incomplete maps.
   if(renderer.shadowMap.enabled&&(renderer.shadowMap.autoUpdate||renderer.shadowMap.needsUpdate)){
    scene.updateMatrixWorld(true);camera.updateMatrixWorld(true);const target=renderer.getRenderTarget(),face=renderer.getActiveCubeFace(),level=renderer.getActiveMipmapLevel();renderer.shadowMap.render(casters,scene,camera);renderer.setRenderTarget(target,face,level);stats.fullShadowUpdates++;
   }
   const subjectVisible=subject.visible;subject.visible=false;
   try{original(scene,camera)}finally{subject.visible=subjectVisible}
   const hidden=[],savedBackground=scene.background,savedAutoClear=renderer.autoClear;
   for(const o of scene.children){if(o===subject||o.isLight||o.type==='Object3D')continue;if(o.visible){hidden.push(o);o.visible=false;}}
   const excludedVisibility=excluded.map(o=>o.visible);for(const o of excluded)o.visible=false;
   scene.background=null;renderer.autoClear=false;
   try{original(scene,camera)}finally{for(const o of hidden)o.visible=true;excluded.forEach((o,n)=>o.visible=excludedVisibility[n]);scene.background=savedBackground;renderer.autoClear=savedAutoClear;}
  }finally{finishBatches(batchActive)}
 };
 return {stats,setMode(next){if(!['original','batch','light-cull','both'].includes(next))throw Error('Unknown render partition');mode=next;stats.mode=next;},sources,batches:()=>batches};
}
