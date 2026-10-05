import * as THREE from 'three';

// Six spatial crowns share twelve botanical prototypes. Each representation
// contains closed scale leaves; distance never substitutes a card or billboard.
export function prepareFoliageLOD(gltf){
 const templates=new Map(),remove=[],items=[];
 gltf.scene.traverse(o=>{if(o.isMesh&&o.userData.foliage_lod_template){templates.set(Number(o.userData.foliage_variant),o.geometry);remove.push(o);}});
 for(const o of remove)o.removeFromParent();
 const definitions=new Map(gltf.parser.json.nodes.filter(n=>n.mesh!==undefined).map(n=>[n.name,gltf.parser.json.meshes[n.mesh].name]));
 gltf.scene.traverse(o=>{
  if(!o.isInstancedMesh)return;
  const match=/^Volumetric scale shoot (\d+)(?:\.\d+)?$/.exec(definitions.get(o.userData.name)||'');
  if(!match)return;
  const low=templates.get(Number(match[1]));if(!low)throw Error('Missing volumetric foliage LOD');
  const high=o.geometry;high.computeBoundingBox();low.computeBoundingBox();
  o.userData.foliageEnvelope=high.boundingBox.clone().union(low.boundingBox);
  o.computeBoundingSphere();const envelope=o.boundingSphere.clone();
  o.geometry=low;o.computeBoundingSphere();envelope.union(o.boundingSphere);o.geometry=high;o.boundingSphere=envelope;
  items.push({mesh:o,high,low,level:'high',sphere:new THREE.Sphere(),lowTriangles:low.index.count/3*o.count,extraTriangles:(high.index.count-low.index.count)/3*o.count});
 });
 const frustum=new THREE.Frustum(),projection=new THREE.Matrix4(),viewPoint=new THREE.Vector3();
 const leafBudget=2400000;
 const isVisible=mesh=>{for(let p=mesh;p;p=p.parent)if(!p.visible)return false;return true;};
 return {
  count:items.length,
  update(camera,height,distance,forced){
   projection.multiplyMatrices(camera.projectionMatrix,camera.matrixWorldInverse);frustum.setFromProjectionMatrix(projection);
   const eligible=[];let visibleLeafTriangles=0,visibleGroups=0;
   for(const item of items){
    item.sphere.copy(item.mesh.boundingSphere).applyMatrix4(item.mesh.matrixWorld);
    item.visible=isVisible(item.mesh)&&frustum.intersectsSphere(item.sphere);item.next='low';
    const depth=Math.max(.1,item.sphere.center.distanceTo(camera.position));
    item.pixels=.07*height/(2*depth*Math.tan(THREE.MathUtils.degToRad(camera.fov/2)));
    if(item.visible){
     visibleLeafTriangles+=item.lowTriangles;visibleGroups++;
     viewPoint.copy(item.sphere.center).project(camera);
     item.priority=item.pixels/(1+.2*(viewPoint.x**2+viewPoint.y**2))*(item.level==='high'?1.03:1);
     if(item.pixels>(item.level==='high'?38:42))eligible.push(item);
    }
   }
   eligible.sort((a,b)=>b.priority-a.priority);
   for(const item of eligible)if(visibleLeafTriangles+item.extraTriangles<=leafBudget){item.next='high';visibleLeafTriangles+=item.extraTriangles;}
   if(forced==='high'||forced==='low'){
    visibleLeafTriangles=0;
    for(const item of items){item.next=forced;if(item.visible)visibleLeafTriangles+=item.lowTriangles+(forced==='high'?item.extraTriangles:0);}
   }
   let changed=false,highGroups=0;
   for(const item of items){if(item.next==='high')highGroups++;if(item.level!==item.next){item.mesh.geometry=item[item.next];item.level=item.next;changed=true;}}
   const level=highGroups===0?'low':highGroups===items.length?'high':'mixed';
   return {level,changed,highGroups,visibleGroups,groups:items.length,visibleLeafTriangles,leafBudget,closedScaleLeaves:true};
  }
 };
}
