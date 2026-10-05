import * as THREE from 'three';
export const HOUSE_ORIGIN=new THREE.Vector3(2.37,0,-2.86);
export const HOUSE_YAW=-.14;
export function housePoint(p){return new THREE.Vector3(p[0]-2.46,p[1],p[2]-.60).applyAxisAngle(new THREE.Vector3(0,1,0),HOUSE_YAW).add(HOUSE_ORIGIN);}
