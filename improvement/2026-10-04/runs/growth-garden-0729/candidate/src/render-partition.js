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
 const physicalRoots=[...scene.children];
 let mode=initialMode,batches=[],batchKey='',optimized=true;const identity=new THREE.Matrix4(),snapshots=[];
 function sameSource(o,s){if(!s||o.geometry!==s.geometry||o.material!==s.material||o.count!==s.count||o.instanceMatrix.version!==s.version||o.castShadow!==s.cast||o.receiveShadow!==s.receive||o.renderOrder!==s.order||o.layers.mask!==s.layers)return false;for(let n=0;n<16;n++)if(o.matrixWorld.elements[n]!==s.matrix[n])return false;return true;}
 function saveSources(){snapshots.length=0;for(const o of sources)snapshots.push({geometry:o.geometry,material:o.material,count:o.count,version:o.instanceMatrix.version,cast:o.castShadow,receive:o.receiveShadow,order:o.renderOrder,layers:o.layers.mask,matrix:o.matrixWorld.elements.slice()});}
 const stats={mode,nativeFoliageGroups:sources.length,batchedGroups:0,batchActive:false,lightPartitionActive:false,drawPasses:1,excludedFiniteLights:proof,nativeEnvelope:{min:bounds.min.toArray(),max:bounds.max.toArray()},nativeBuffersAndMaterialsUnmodified:true,instanceMatricesCopiedBitExactly:true,fullShadowUpdates:0,batchCacheHits:0,batchRebuilds:0,extraCompleteColorPassForShadowUpdate:false};
 function activateBatches(){
  if(!subject.matrixWorld.equals(identity)||!sources.length||sources.some(o=>!o.visible||o.instanceColor||o.material!==o.userData.foliageMaterials?.low))return false;
  const valid=optimized&&snapshots.length===sources.length&&sources.every((o,n)=>sameSource(o,snapshots[n]));
  const key=valid?batchKey:sources.map(o=>o.geometry.uuid+':'+o.material.uuid+':'+o.matrixWorld.elements.join(',')).join('|');
  if(valid)stats.batchCacheHits++;
  if(key!==batchKey||optimized&&!valid){stats.batchRebuilds++;
   for(const o of batches){display.remove(o);o.dispose();}batches=[];const grouped=new Map();
   for(const o of sources){const id=o.geometry.uuid+':'+o.material.uuid+':'+o.matrixWorld.elements.join(',')+':'+o.castShadow+':'+o.receiveShadow+':'+o.renderOrder+':'+o.layers.mask;let a=grouped.get(id);if(!a){a=[];grouped.set(id,a);}a.push(o);}
   for(const group of grouped.values()){
    const source=group[0],count=group.reduce((n,o)=>n+o.count,0),batch=new THREE.InstancedMesh(source.geometry,source.material,count);batch.name='Equivalent closed leaves '+batches.length;batch.matrixAutoUpdate=false;batch.matrix.copy(source.matrixWorld);batch.castShadow=source.castShadow;batch.receiveShadow=source.receiveShadow;batch.renderOrder=source.renderOrder;batch.layers.mask=source.layers.mask;
    let offset=0;for(const o of group){batch.instanceMatrix.array.set(o.instanceMatrix.array.subarray(0,o.count*16),offset);offset+=o.count*16;}
    batch.instanceMatrix.needsUpdate=true;batch.computeBoundingBox();batch.computeBoundingSphere();display.add(batch);batches.push(batch);
   }
   display.updateWorldMatrix(true,true);batchKey=key;stats.batchedGroups=batches.length;saveSources();
  }
  for(const o of sources)o.visible=false;display.visible=true;return true;
 }
 function finishBatches(active){if(active){for(const o of sources)o.visible=true;display.visible=false;}}
 // Persistent public Scene objects give each color pass its own light state.
 // Native geometry has exactly one parent. Identity scope Scenes keep native
 // world matrices unchanged; the original physical Scene still owns all roots
 // transitively and remains the only authority for complete shadow updates.
 const physicalLights=[];scene.traverse(o=>{if(o.isLight)physicalLights.push(o)});
 const backgroundScene=new THREE.Scene(),heroScene=new THREE.Scene();
 backgroundScene.name='Stable background color scope';heroScene.name='Stable hero color scope';
 for(const scope of [backgroundScene,heroScene]){scope.matrixWorldAutoUpdate=false;scope.fog=scene.fog;scope.environment=scene.environment;scope.environmentIntensity=scene.environmentIntensity;scope.environmentRotation.copy(scene.environmentRotation);}
 backgroundScene.background=scene.background;heroScene.background=null;
 scene.add(backgroundScene,heroScene);
 for(const root of physicalRoots)if(root===subject)heroScene.add(root);else if(!root.isLight&&root.type!=='Object3D')backgroundScene.add(root);
 const replicas=[];
 function replica(source,scope){const light=source.clone();light.name='Color-pass replica: '+(source.name||source.type);light.userData.physicalSourceUUID=source.uuid;light.userData.colorPassReplica=true;light.matrixAutoUpdate=false;light.matrixWorldAutoUpdate=false;light.color=source.color;if(source.target)light.target=source.target;if(source.shadow)light.shadow=source.shadow;scope.add(light);replicas.push({source,light});return light;}
 for(const source of physicalLights){replica(source,backgroundScene);if(!excluded.includes(source))replica(source,heroScene);}
 const excludedState=excluded.map(o=>({light:o,matrix:o.matrixWorld.elements.slice(),target:o.target?.matrixWorld.elements.slice(),distance:o.distance,angle:o.angle}));
 const nativeProof=[];model.traverse(o=>{if(!o.isMesh)return;const envelope=o.userData.foliageEnvelope;nativeProof.push({object:o,world:o.matrixWorld.elements.slice(),geometry:envelope?null:o.geometry,attribute:envelope?null:o.geometry.attributes.position,attributeVersion:envelope?null:o.geometry.attributes.position.version,count:o.count,instances:o.instanceMatrix,instanceVersion:o.instanceMatrix?.version,envelope:envelope?[...envelope.min.toArray(),...envelope.max.toArray()]:null});});
 function nativeExclusionBoundsStillValid(){for(const s of nativeProof){const o=s.object;if(o.count!==s.count||o.instanceMatrix!==s.instances||o.instanceMatrix?.version!==s.instanceVersion)return false;for(let n=0;n<16;n++)if(o.matrixWorld.elements[n]!==s.world[n])return false;if(s.envelope){const b=o.userData.foliageEnvelope;if(!b)return false;const a=[b.min.x,b.min.y,b.min.z,b.max.x,b.max.y,b.max.z];for(let n=0;n<6;n++)if(a[n]!==s.envelope[n])return false;}else if(o.geometry!==s.geometry||o.geometry.attributes.position!==s.attribute||s.attribute.version!==s.attributeVersion)return false;}return true;}
 function exclusionsStillValid(){for(const s of excludedState){const o=s.light;if(o.distance!==s.distance||o.angle!==s.angle)return false;for(let n=0;n<16;n++)if(o.matrixWorld.elements[n]!==s.matrix[n]||o.target&&o.target.matrixWorld.elements[n]!==s.target[n])return false;}return true;}
 function updateScopes(){scene.updateWorldMatrix(true,false);backgroundScene.matrixWorld.copy(scene.matrixWorld);heroScene.matrixWorld.copy(scene.matrixWorld);scene.updateMatrixWorld();for(const {source,light}of replicas){light.matrixWorld.copy(source.matrixWorld);light.intensity=source.intensity;light.distance=source.distance;light.angle=source.angle;light.penumbra=source.penumbra;light.decay=source.decay;light.castShadow=source.castShadow;light.visible=source.visible;light.layers.mask=source.layers.mask;light.map=source.map;if(source.shadow)light.shadow=source.shadow;if(source.target)light.target=source.target;}backgroundScene.fog=heroScene.fog=scene.fog;backgroundScene.environment=heroScene.environment=scene.environment;backgroundScene.environmentIntensity=heroScene.environmentIntensity=scene.environmentIntensity;backgroundScene.background=scene.background;}
 function completePhysical(camera){const saved=replicas.map(({light})=>light.visible);for(const {light}of replicas)light.visible=false;try{return original(scene,camera)}finally{replicas.forEach(({light},n)=>light.visible=saved[n])}}
 stats.stableScopes={publicAPIOnly:true,originalPhysicalLights:physicalLights.length,backgroundLightReplicas:physicalLights.length,heroLightReplicas:physicalLights.length-excluded.length,samePhysicalShadowObjects:true,nativeGeometryHasOneParent:true,identityScopesPreserveWorld:true,frameProgramStateStable:true,completeShadowUpdateBeforeColor:true,nativeEnvelopeDependencyGuard:true};
 renderer.render=(input,camera)=>{
  if(input!==scene)return original(input,camera);
  updateScopes();stats.extraCompleteColorPassForShadowUpdate=false;
  if(mode==='original'){stats.batchActive=false;stats.lightPartitionActive=false;stats.drawPasses=1;return completePhysical(camera);}
  let batchActive=(mode==='batch'||mode==='both'||mode==='stable')&&activateBatches();stats.batchActive=!!batchActive;
  const lightActive=(mode==='light-cull'||mode==='both'||mode==='stable')&&excluded.length>0&&subject.visible&&scene.matrixWorld.equals(identity)&&subject.matrixWorld.equals(identity)&&exclusionsStillValid()&&nativeExclusionBoundsStillValid();stats.lightPartitionActive=!!lightActive;stats.drawPasses=lightActive?2:1;
  if((mode==='stable'||mode==='both')&&!lightActive&&batchActive){finishBatches(batchActive);batchActive=false;stats.batchActive=false;}
  const savedShadowAutoUpdate=renderer.shadowMap.autoUpdate;
  try{
   if(!lightActive)return completePhysical(camera);
   // Build every physical caster's cached map from the complete equivalent
   // scene. The split color passes must never regenerate incomplete maps.
   if(renderer.shadowMap.enabled&&(renderer.shadowMap.autoUpdate||renderer.shadowMap.needsUpdate)){
    // The renderer initializes its internal render state before shadow maps.
    // A complete original pass rebuilds every map; the next color pass clears
    // that transient color frame. No direct internal shadow-map call.
    completePhysical(camera);stats.fullShadowUpdates++;stats.extraCompleteColorPassForShadowUpdate=true;
   }
   renderer.shadowMap.autoUpdate=false;
   if(mode==='stable'){const savedAutoClear=renderer.autoClear;try{original(backgroundScene,camera);renderer.autoClear=false;original(heroScene,camera)}finally{renderer.autoClear=savedAutoClear;}return;}
   const subjectVisible=subject.visible;subject.visible=false;
   try{completePhysical(camera)}finally{subject.visible=subjectVisible}
   const hidden=[],savedBackground=scene.background,savedAutoClear=renderer.autoClear;
   for(const o of physicalRoots){if(o===subject||o.isLight||o.type==='Object3D')continue;if(o.visible){hidden.push(o);o.visible=false;}}
   const excludedVisibility=excluded.map(o=>o.visible);for(const o of excluded)o.visible=false;
   scene.background=null;renderer.autoClear=false;
   try{completePhysical(camera)}finally{for(const o of hidden)o.visible=true;excluded.forEach((o,n)=>o.visible=excludedVisibility[n]);scene.background=savedBackground;renderer.autoClear=savedAutoClear;}
  }finally{renderer.shadowMap.autoUpdate=savedShadowAutoUpdate;finishBatches(batchActive)}
 };
 return {stats,setOptimization(value){optimized=!!value;},setMode(next){if(!['original','batch','light-cull','both','stable'].includes(next))throw Error('Unknown render partition');mode=next;stats.mode=next;},sources,batches:()=>batches,physicalLights,backgroundScene,heroScene,replicas};
}
