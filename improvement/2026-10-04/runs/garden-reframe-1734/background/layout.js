import * as THREE from 'three';
export const HOUSE_YAW=-28*Math.PI/180,HOUSE_X_SCALE=.68,HOUSE_FRONT=new THREE.Vector3(2.10,0,-2.65);
export const HOUSE_MATRIX=new THREE.Matrix4().makeTranslation(...HOUSE_FRONT.toArray()).multiply(new THREE.Matrix4().makeRotationY(HOUSE_YAW)).multiply(new THREE.Matrix4().makeScale(HOUSE_X_SCALE,1,1)).multiply(new THREE.Matrix4().makeTranslation(-1.28,0,4.10));
export function housePoint(p){return new THREE.Vector3(...p).applyMatrix4(HOUSE_MATRIX);}
