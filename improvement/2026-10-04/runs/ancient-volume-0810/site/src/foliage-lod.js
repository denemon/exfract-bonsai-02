import * as THREE from 'three';

// Six spatial crowns share twelve botanical prototypes. Each representation
// contains closed scale leaves; distance never substitutes a card or billboard.
export function prepareFoliageLOD(gltf){
 const templates=new Map(),remove=[],items=[];
 gltf.scene.traverse(o=>{if(o.isMesh&&o.userData.foliage_lod_template){templates.set(Number(o.userData.foliage_variant),o.geometry);remove.push(o);}});
 for(const o of remove)o.removeFromParent();
 const definitions=new Map(gltf.parser.json.nodes.filter(n=>n.mesh!==undefined).map(n=>[n.name,gltf.parser.json.meshes[n.mesh]]));
 let highAvailable=true;
 gltf.scene.traverse(o=>{
  if(!o.isInstancedMesh)return;
  const match=/^Volumetric scale shoot (\d+)(?:\.\d+)?$/.exec(definitions.get(o.userData.name)?.name||'');
  if(!match)return;
  const low=templates.get(Number(match[1]));if(!low)throw Error('Missing volumetric foliage LOD');
  let high=o.geometry;const saved=definitions.get(o.userData.name)?.extras?.deferred_high_bounds;
  if(saved){highAvailable=false;high=high.clone();high.boundingBox=new THREE.Box3(new THREE.Vector3(...saved.min),new THREE.Vector3(...saved.max));high.boundingSphere=new THREE.Sphere(new THREE.Vector3(...saved.sphere.center),saved.sphere.radius);o.geometry=high;}else high.computeBoundingBox();low.computeBoundingBox();
  o.userData.foliageEnvelope=high.boundingBox.clone().union(low.boundingBox);
  o.computeBoundingSphere();const envelope=o.boundingSphere.clone();
  o.geometry=low;o.computeBoundingSphere();envelope.union(o.boundingSphere);o.geometry=high;o.boundingSphere=envelope;
  items.push({variant:Number(match[1]),mesh:o,high,low,level:'high',crown:(o.userData.name||o.name).match(/Canopy[ _]spatial[ _]group[ _](\d+)/)?.[1]||'legacy',sphere:new THREE.Sphere(),lowTriangles:low.index.count/3*o.count,extraTriangles:(high.index.count-low.index.count)/3*o.count});
 });
 const frustum=new THREE.Frustum(),projection=new THREE.Matrix4(),viewPoint=new THREE.Vector3();
 const crowns=[...new Set(items.map(item=>item.crown))].map(key=>({key,items:items.filter(item=>item.crown===key),level:'high'}));
 const leafBudget=2600000,baseTriangles=items.reduce((sum,item)=>sum+item.lowTriangles,0);
 const isVisible=mesh=>{for(let p=mesh;p;p=p.parent)if(!p.visible)return false;return true;};
 return {
  count:items.length,
  installHigh(detail){const templates=new Map();detail.scene.traverse(o=>{if(o.isMesh){o.geometry.computeBoundingBox();templates.set(Number(o.userData.high_template_variant),o.geometry)}});if(templates.size!==12)throw Error('Expected twelve exact detailed foliage prototypes');for(const item of items){const high=templates.get(item.variant);if(!high)throw Error('Missing detailed leaf variant');item.high=high;item.extraTriangles=(high.index.count-item.low.index.count)/3*item.mesh.count;}highAvailable=true;},
  templateBounds(){const found=new Map();for(const i of items)if(!found.has(i.variant)){i.high.computeBoundingSphere();found.set(i.variant,{variant:i.variant,min:i.high.boundingBox.min.toArray(),max:i.high.boundingBox.max.toArray(),sphere:{center:i.high.boundingSphere.center.toArray(),radius:i.high.boundingSphere.radius}})}return [...found.values()]},
  update(camera,height,distance,forced){
   projection.multiplyMatrices(camera.projectionMatrix,camera.matrixWorldInverse);frustum.setFromProjectionMatrix(projection);
   const eligible=[];let allocatedLeafTriangles=baseTriangles;
   for(const crown of crowns){
    let visible=false,priority=0,pixels=0;const centre=new THREE.Vector3();
    for(const item of crown.items){
     item.sphere.copy(item.mesh.boundingSphere).applyMatrix4(item.mesh.matrixWorld);
     item.visible=isVisible(item.mesh)&&frustum.intersectsSphere(item.sphere);visible ||= item.visible;
     centre.add(item.sphere.center);
    }
    centre.divideScalar(crown.items.length);
    const depth=Math.max(.1,centre.distanceTo(camera.position));
    pixels=.07*height/(2*depth*Math.tan(THREE.MathUtils.degToRad(camera.fov/2)));
    viewPoint.copy(centre).project(camera);
    priority=pixels/(1+.45*(viewPoint.x**2+viewPoint.y**2))*(crown.level==='high'?1.25:1);
    crown.next='low';crown.priority=priority;crown.extraTriangles=crown.items.reduce((sum,item)=>sum+item.extraTriangles,0);
    if(visible&&pixels>(crown.level==='high'?38:42))eligible.push(crown);
   }
   const needsHigh=!highAvailable&&eligible.length>0;
   eligible.sort((a,b)=>b.priority-a.priority);
   for(const crown of eligible)if(highAvailable&&allocatedLeafTriangles+crown.extraTriangles<=leafBudget){crown.next='high';allocatedLeafTriangles+=crown.extraTriangles;}
   if(forced==='high'||forced==='low'){
    allocatedLeafTriangles=baseTriangles;
    for(const crown of crowns){crown.next=highAvailable?forced:'low';if(crown.next==='high')allocatedLeafTriangles+=crown.extraTriangles;}
   }
   let changed=false,highGroups=0,visibleGroups=0,visibleLeafTriangles=0;
   for(const crown of crowns){
    crown.level=crown.next;
    for(const item of crown.items){
     if(crown.next==='high')highGroups++;
     if(item.mesh.userData.foliageMaterials)item.mesh.material=item.mesh.userData.foliageMaterials[crown.next];
     if(item.level!==crown.next){item.mesh.geometry=item[crown.next];item.level=crown.next;changed=true;}
     if(item.visible){visibleGroups++;visibleLeafTriangles+=item.lowTriangles+(item.level==='high'?item.extraTriangles:0);}
    }
   }
   const level=highGroups===0?'low':highGroups===items.length?'high':'mixed';
   return {level,changed,highAvailable,needsHigh:needsHigh||(forced==='high'&&!highAvailable),highGroups,visibleGroups,groups:items.length,crowns:crowns.length,visibleLeafTriangles,allocatedLeafTriangles,leafBudget,closedScaleLeaves:true};
  }
 };
}
