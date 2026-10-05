import * as THREE from 'three';
const refined=()=>new URLSearchParams(location.search).get('background-finish')==='refined';
export function backgroundLeafMaterial(){return new THREE.MeshStandardMaterial({color:refined()?'#66755c':'#3b5443',roughness:.96,metalness:0});}
export function backgroundLightScale(){return new URLSearchParams(location.search).get('background-light')==='refined'?1.32:1;}
