import * as THREE from 'three';
export function applyStudyLighting(scene,mode){
 if(mode!=='neutral')return {mode:'night',diagnostic:false};
 scene.background=new THREE.Color('#8e9da6');
 let index=0;const rows=[];scene.traverse(o=>{if(!o.isLight)return;
  if(o.isHemisphereLight){o.intensity=1.2;o.color.set('#e0e4e7');o.groundColor.set('#74766c');}
  else if(o.isDirectionalLight){o.intensity=1.1;o.color.set('#e7ebee');o.shadow.radius=3;}
  else if(o.isSpotLight&&o.intensity===70){o.intensity=14;o.color.set('#f4f3ef');o.shadow.radius=4;}
  else o.intensity=0;
  rows.push({order:index++,type:o.type,intensity:o.intensity,color:o.color.getHexString()});
 });return {mode:'neutral',diagnostic:true,description:'Broad neutral sky fill with restrained neutral key; fixed physical garden/camera, artificial auxiliary sources off',lights:rows};
}
