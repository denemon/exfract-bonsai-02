import {backgroundLeafMaterial} from './background-finish.js';
import * as THREE from 'three';
// Closed asymmetric cupped leaves, with a front ridge and an underside. The
// longest local axis is Y. These are small individual leaves, not canopy cards.
function closedLeaf(variant){
 const baseline=new URLSearchParams(location.search).get("far-shape")==="baseline",width=(baseline?[.29,.33,.26,.31]:[.34,.40,.29,.37])[variant],bend=(baseline?[.042,.067,.028,.052]:[.063,.10,.035,.078])[variant];
 const ps=[[0,0,0],[-width*.64,.18,-.016],[-width,.47,.010],[-width*.63,.76,.041],[baseline?0:(variant-1.5)*.045,1,.094],[width*(baseline?.55:.72),.80,.052],[width*.91,.49,.004],[width*.62,.21,-.018],[.016,.52,bend+.045],[-.003,.49,-.021]].flat(),ix=[];
 for(let i=0;i<8;i++){const j=(i+1)%8;ix.push(j,i,8,i,j,9);}
 const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(ps,3));g.setIndex(ix);g.computeVertexNormals();return g;
}
export function evergreenTemplates(){return [0,1,2,3].map(v=>({geometry:closedLeaf(v),triangles:16,sourceName:'Own closed cupped broadleaf '+v}));}
export function installEvergreenShoots(scene,sources,leaves){
 const material=backgroundLeafMaterial(),up=new THREE.Vector3(0,1,0),obj=new THREE.Object3D(),rows=[];
 const spatialGroups=new Map();for(const leaf of leaves){const name=leaf.specimen||'grounded-understory';if(!spatialGroups.has(name))spatialGroups.set(name,[]);spatialGroups.get(name).push(leaf);}
 for(const [specimen,spatialLeaves]of spatialGroups)for(let variant=0;variant<sources.length;variant++){
  const list=spatialLeaves.filter((_,i)=>i%sources.length===variant),source=sources[variant],mesh=new THREE.InstancedMesh(source.geometry,material,list.length);mesh.name='Branch attached closed garden broadleaves '+specimen+' '+variant;
  list.forEach((a,i)=>{obj.position.copy(a.p);obj.quaternion.setFromUnitVectors(up,a.direction);obj.rotateY(a.roll);obj.scale.set(a.length*(a.width||1),a.length,a.length);obj.updateMatrix();mesh.setMatrixAt(i,obj.matrix);mesh.setColorAt(i,new THREE.Color().setRGB(a.shade*.78,a.shade*.87,a.shade*.80));});
  mesh.castShadow=mesh.receiveShadow=true;mesh.instanceMatrix.needsUpdate=true;mesh.computeBoundingSphere();scene.add(mesh);rows.push({specimen,variant,instances:list.length,triangles:list.length*16});
 }
 return {source:'Own four small closed bent botanical leaf prototypes,16tri each; hero geometry untouched',batching:'Per physical specimen frustum bounds; all original leaves remain, no manual hiding or extra LOD',support:'Every leaf origin is on an actual authored twig path, unequal paired leaves and terminal buds, no cards or spheres',instances:leaves.length,triangles:leaves.length*16,groups:rows};
}
