import * as THREE from 'three';
import {RoundedBoxGeometry} from 'three/addons/geometries/RoundedBoxGeometry.js';
export function createScene(hero,study){
 const scene=new THREE.Scene();const subject=new THREE.Group();subject.name='bonsai';subject.add(hero);scene.add(subject);
 const clay=['clay','material','normals'].includes(study);scene.background=new THREE.Color(clay?'#dedcd6':'#17263b');
 const ground=new THREE.Mesh(new THREE.PlaneGeometry(30,30),new THREE.MeshStandardMaterial({color:clay?'#d1cec6':'#757e86',roughness:1}));ground.rotation.x=-Math.PI/2;ground.position.y=-.035;ground.receiveShadow=true;scene.add(ground);
 scene.add(new THREE.HemisphereLight(clay?'#ffffff':'#adc3e0',clay?'#9a9387':'#34352f',clay?1.1:.80));
 const key=clay?new THREE.DirectionalLight('#fffaf0',3.4):new THREE.SpotLight('#ffe6c8',58,12,.56,.70,2);key.position.set(...(clay?[-3.8,4.5,2.8]:[-2.2,2.8,3.4]));key.target.position.set(0,.9,0);key.castShadow=true;key.shadow.mapSize.set(2048,2048);if(clay)Object.assign(key.shadow.camera,{left:-3,right:3,top:3,bottom:-3});Object.assign(key.shadow.camera,{near:.1,far:12});key.shadow.bias=Number(new URLSearchParams(location.search).get('shadow-bias')??-.0001);key.shadow.normalBias=.003;key.shadow.radius=5;scene.add(key,key.target);
 const fill=new THREE.DirectionalLight(clay?'#edf0f4':'#91acd5',clay?.55:.75);fill.position.set(3,3,-2);scene.add(fill);
 if(!clay){
  scene.fog=new THREE.Fog('#17263b',15,32);
  const timber=new THREE.MeshStandardMaterial({color:'#44342a',roughness:.88});const plaster=new THREE.MeshStandardMaterial({color:'#b4a68e',roughness:1});const warm=new THREE.MeshStandardMaterial({color:'#b59d75',roughness:1});const stone=new THREE.MeshStandardMaterial({color:'#62665d',roughness:1});
  const box=(p,s,m)=>{const o=new THREE.Mesh(new RoundedBoxGeometry(...s,1,.005),m);o.position.set(...p);o.castShadow=o.receiveShadow=true;scene.add(o);return o;};
  // Stage-one spatial scaffold: solid veranda, deep room, timber thickness and boundary.
  box([3.4,.18,-2.9],[3.6,.36,5.6],stone);
  for(let n=0;n<34;n++)box([3.4,.40,-5.5+n*.157],[3.6,.07,.149],timber);
  for(const z of [-5.4,-3.35,-1.3]){box([1.68,1.67,z],[.16,2.55,.17],timber);box([4.95,1.67,z],[.18,2.55,.17],timber);}
  box([3.32,3.08,-3.3],[3.8,.20,5.3],timber);box([3.5,3.43,-3.3],[4.2,.13,5.8],timber);
  for(let n=0;n<24;n++)box([1.6,3.3,-5.9+n*.235],[.72,.10,.052],timber);
  box([5.03,1.7,-3.45],[.18,2.5,5.3],plaster);box([3.4,1.75,-5.63],[3.3,2.5,.20],plaster);
  box([3.45,1.72,-4.94],[2.45,2.36,.12],warm);
  for(let n=0;n<7;n++)box([2.35+n*.35,1.72,-4.85],[.025,2.34,.035],timber);
  for(let n=0;n<3;n++)box([3.39,.82+n*.77,-4.85],[2.13,.024,.035],timber);
  const room=new THREE.PointLight('#ffd59b',8,8,2);room.position.set(3.0,2.2,-3.8);scene.add(room);
  box([-2.0,.77,-5.5],[8,.1,.21],timber);box([-2.0,.41,-5.55],[8,.82,.2],plaster);
 }
 return {scene,subject,key,ground};
}
