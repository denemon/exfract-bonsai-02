import * as THREE from 'three';

export function prepareFoliageLOD(gltf){
 const templates=new Map(),remove=[],items=[];
 gltf.scene.traverse(o=>{if(o.isMesh&&o.userData.foliage_lod_template){templates.set(Number(o.userData.foliage_variant),o.geometry);remove.push(o);}});
 for(const o of remove)o.removeFromParent();
 const definitions=new Map(gltf.parser.json.nodes.filter(n=>n.mesh!==undefined).map(n=>[n.name,gltf.parser.json.meshes[n.mesh].name]));
 gltf.scene.traverse(o=>{
  if(!o.isInstancedMesh)return;
  const match=/^Volumetric scale shoot (\d+)$/.exec(definitions.get(o.userData.name)||'');
  if(!match)return;
  const low=templates.get(Number(match[1]));if(!low)throw Error('Missing volumetric foliage LOD');
  o.geometry.computeBoundingBox();low.computeBoundingBox();
  o.userData.foliageEnvelope=o.geometry.boundingBox.clone().union(low.boundingBox);
  items.push({mesh:o,high:o.geometry,low});
 });
 let current='high';
 return {
  count:items.length,
  update(camera,height,distance,forced){
   const shootPixels=.07*height/(2*Math.max(distance,.1)*Math.tan(THREE.MathUtils.degToRad(camera.fov/2)));
   const level=forced==='high'||forced==='low'?forced:shootPixels>(current==='high'?34:38)?'high':'low';
   const changed=level!==current;
   if(changed)for(const item of items){item.mesh.geometry=item[level];item.mesh.computeBoundingSphere();}
   current=level;
   return {level,changed,shootPixels,groups:items.length,closedScaleLeaves:true};
  }
 };
}
