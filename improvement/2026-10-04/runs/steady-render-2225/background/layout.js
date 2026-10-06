import * as THREE from 'three';
export const spatialTrial=new URLSearchParams(location.search).get('space')||'offset';
const placements={baseline:[1.85,0,-3.8,-18],slide:[1.85,0,-3.8,-18],separate:[2.25,0,-3.70,-14],terrace:[2.55,.06,-3.05,-10],balanced:[1.65,0,-4.30,-18],offset:[2.45,.02,-3.25,-14]};
const at=placements[spatialTrial]||placements.offset;
export const HOUSE_YAW=at[3]*Math.PI/180,HOUSE_X_SCALE=.76,HOUSE_FRONT=new THREE.Vector3(...at.slice(0,3));
export const HOUSE_MATRIX=new THREE.Matrix4().makeTranslation(...HOUSE_FRONT.toArray()).multiply(new THREE.Matrix4().makeRotationY(HOUSE_YAW)).multiply(new THREE.Matrix4().makeScale(HOUSE_X_SCALE,1,1)).multiply(new THREE.Matrix4().makeTranslation(-1.28,0,4.10));
export function housePoint(p){return new THREE.Vector3(...p).applyMatrix4(HOUSE_MATRIX);}
