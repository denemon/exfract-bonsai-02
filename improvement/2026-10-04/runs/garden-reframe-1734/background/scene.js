import {backgroundLightScale} from './background-finish.js';
import {housePoint} from './layout.js';
import {architecture} from './architecture.js';
import {backgroundGeometrySignature} from './geometry-signature.js';
import {loadGardenRocks,placeGardenRocks} from './garden-rocks.js';
import * as THREE from 'three';
import {gardenMaterials} from './garden-materials.js';
import {batches,groundGeometry,groundHeight,setGroundField,planting,random} from './garden-geometry.js';

function sky(scene){
 const finish=new URLSearchParams(location.search).get("finish")==="material-v01";
 const material=new THREE.ShaderMaterial({side:THREE.BackSide,depthWrite:false,toneMapped:false,
 vertexShader:'varying vec3 direction;void main(){direction=position;gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.);}',
 fragmentShader:`varying vec3 direction;void main(){vec3 d=normalize(direction);float t=smoothstep(-.03,.72,d.y);vec3 c=mix(${finish?"vec3(.022,.055,.130),vec3(.004,.015,.052)":"vec3(.016,.040,.085),vec3(.0025,.008,.024)"},pow(t,.67));float veil=sin(d.x*7.+d.y*10.)*sin(d.z*9.-d.y*7.);c+=vec3(.001,.0018,.003)*veil*(1.-t);gl_FragColor=vec4(c,1.);#include <colorspace_fragment>}`.replace(';#include',';\n#include')});
 const dome=new THREE.Mesh(new THREE.SphereGeometry(45,36,18),material);dome.name='Deep blue night sky';dome.renderOrder=-100;scene.add(dome);
 const rng=random(19721),p=[];for(let i=0;i<70;i++){const a=rng()*Math.PI*2,h=.17+rng()*.72,r=Math.sqrt(1-h*h);p.push(44*r*Math.cos(a),44*h,44*r*Math.sin(a));}
 const geometry=new THREE.BufferGeometry();geometry.setAttribute('position',new THREE.Float32BufferAttribute(p,3));const stars=new THREE.Points(geometry,new THREE.PointsMaterial({color:'#b9c7dc',size:.022,transparent:true,opacity:.4,depthWrite:false,toneMapped:false}));stars.name='Sparse faint stars';scene.add(stars);
}


export async function loadGardenAssets(loader,study){if(['clay','material','normals'].includes(study))return null;return Promise.all([gardenMaterials(),loadGardenRocks(loader)]);}

export async function createScene(hero,study,loadedAssets){
 const scene=new THREE.Scene(),subject=new THREE.Group();subject.name='bonsai';subject.add(hero);scene.add(subject);
 const clay=['clay','material','normals'].includes(study),layout=new URLSearchParams(location.search).get('layout')||'b';
 if(clay){
  scene.background=new THREE.Color('#dedcd6');
  const ground=new THREE.Mesh(new THREE.PlaneGeometry(30,30),new THREE.MeshStandardMaterial({color:'#d1cec6',roughness:1}));ground.rotation.x=-Math.PI/2;ground.position.y=-.035;ground.receiveShadow=true;scene.add(ground);
  scene.add(new THREE.HemisphereLight('#ffffff','#9a9387',1.1));const key=new THREE.DirectionalLight('#fffaf0',3.4);key.position.set(-3.8,4.5,2.8);key.target.position.set(0,.9,0);key.castShadow=true;key.shadow.mapSize.set(2048,2048);Object.assign(key.shadow.camera,{left:-3,right:3,top:3,bottom:-3,near:.1,far:12});key.shadow.bias=-.0001;key.shadow.normalBias=.003;key.shadow.radius=5;scene.add(key,key.target);const fill=new THREE.DirectionalLight('#edf0f4',.55);fill.position.set(3,3,-2);scene.add(fill);return {scene,subject,key,ground,layout:'diagnostic'};
 }
 scene.background=new THREE.Color('#101e32');sky(scene);scene.fog=new THREE.FogExp2('#142337',.020);
 const [m,rockAssets]=loadedAssets||await Promise.all([gardenMaterials(),loadGardenRocks()]);m.lampShade=new THREE.MeshStandardMaterial({color:'#d0c3a4',roughness:.96,metalness:0,emissive:'#d9a665',emissiveIntensity:new URLSearchParams(location.search).get('room-light')==='proposed'?.12:0});setGroundField(m.terrain.image);const ground=new THREE.Mesh(groundGeometry(),m.ground);ground.name='Continuous mineral gravel and growing moss';ground.receiveShadow=true;scene.add(ground);
 const farGeometry=new THREE.PlaneGeometry(100,100);farGeometry.rotateX(-Math.PI/2);farGeometry.translate(0,-.029,0);const distantGround=new THREE.Mesh(farGeometry,m.ground);distantGround.name='Continuous distant mineral ground';distantGround.receiveShadow=true;scene.add(distantGround);
 const built=architecture(scene,m,layout);
 const rocks=placeGardenRocks(scene,rockAssets,m);
 const plants=planting(scene,m,hero);
 scene.updateMatrixWorld(true);const rootRay=new THREE.Raycaster();
 const foundation=scene.getObjectByName('Garden architecture foundation');
 for(const row of built.verandaSupportContacts){
  const [x,z]=row.position;
  rootRay.set(new THREE.Vector3(x,row.woodBottom+.02,z),new THREE.Vector3(0,-1,0));
  const foot=rootRay.intersectObject(foundation,false)[0];
  rootRay.set(new THREE.Vector3(x,.15,z),new THREE.Vector3(0,-1,0));
  const terrain=rootRay.intersectObjects([ground,distantGround],false)[0];
  Object.assign(row,{actualStoneTopY:foot?.point.y,woodToStoneGap:foot?row.woodBottom-foot.point.y:null,actualGroundY:terrain?.point.y,stoneBottomToGround:terrain?row.stoneBottom-terrain.point.y:null});
 }

 const rootContacts=plants.rootCenters.map(root=>{const [x,y,z]=root.position;rootRay.set(new THREE.Vector3(x,y+.30,z),new THREE.Vector3(0,-1,0));const hit=rootRay.intersectObjects([ground,distantGround],false)[0];return {name:root.name,rootCenter:root.position,surfaceY:hit?.point.y,signedBurial:hit?y-hit.point.y:null};});
 plants.mossTufts=0;plants.mossTuftTriangles=0;plants.rejectedMossFronds='Diagnostic objects omitted: isolated chip/dot silhouettes; source/patches/evidence retained';plants.mossDetail='Connected unequal low cushions, density patches and soil seams share one height/material field; no scattered tuft objects';plants.terrainFieldDesign=m.terrain.userData;
 
 scene.updateMatrixWorld(true);let bed;const feet=[];hero.traverse(o=>{if(!o.isMesh)return;if(/bedding[_ ]stone/i.test(o.name))bed=o;if(/ceramic[_ ]foot/i.test(o.name))feet.push(o);});
 const ray=new THREE.Raycaster(),contacts=[];if(bed)for(const foot of feet){const bounds=new THREE.Box3().setFromObject(foot),centre=bounds.getCenter(new THREE.Vector3());ray.set(new THREE.Vector3(centre.x,bounds.min.y+.035,centre.z),new THREE.Vector3(0,-1,0));const hit=ray.intersectObject(bed,false)[0];contacts.push({foot:foot.name,footBottomY:bounds.min.y,stoneTopY:hit?.point.y,gapMetres:hit?bounds.min.y-hit.point.y:null});}
 scene.add(new THREE.HemisphereLight('#a3bddb','#29251d',.58));
 const moon=new THREE.DirectionalLight('#a9c6e9',.58);moon.position.set(-3.2,7.0,-2.5);moon.castShadow=true;moon.shadow.mapSize.set(1024,1024);Object.assign(moon.shadow.camera,{left:-7,right:7,top:6,bottom:-5,near:.3,far:18});moon.shadow.normalBias=.009;moon.shadow.bias=-.00012;moon.shadow.radius=5;scene.add(moon);
 // A concealed, broad warm garden wash and cool sky illuminate one place.
 const key=new THREE.SpotLight('#ffe0b5',70,14,.78,1,2);key.position.set(-2.2,3.4,3.2);key.target.position.set(0,.72,-.4);key.castShadow=true;key.shadow.mapSize.set(2048,2048);key.shadow.camera.near=.15;key.shadow.camera.far=14;key.shadow.bias=-.00012;key.shadow.normalBias=.0023;key.shadow.radius=7;scene.add(key,key.target);
 const proposedRoom=new URLSearchParams(location.search).get('room-light')==='proposed';
 const roomPoint=p=>housePoint(p);
 const room=new THREE.SpotLight('#ffd4a0',18,7,.82,1,2);room.position.copy(roomPoint([4.80,2.35,-4.86]));room.target.position.copy(roomPoint([4.72,1.10,-6.23]));room.castShadow=true;room.shadow.mapSize.set(1024,1024);room.shadow.camera.near=.12;room.shadow.camera.far=7;room.shadow.bias=-.00015;room.shadow.normalBias=.003;room.shadow.radius=4;scene.add(room,room.target);
 const roomBounce=new THREE.PointLight('#ecd0a4',proposedRoom?3.5:2.5,3.6,2);roomBounce.position.copy(roomPoint([3.45,1.43,-5.10]));scene.add(roomBounce);
 if(proposedRoom){const lamp=new THREE.PointLight('#ffd4a0',1.1,3.1,2);lamp.position.copy(roomPoint([5.08,.904,-5.84]));lamp.name='Small room console lantern source';scene.add(lamp);}
 const rearGlow=new THREE.SpotLight('#ddc5a0',20*backgroundLightScale(),5.5,.67,1,2);rearGlow.position.set(-3.45,.15,-4.50);rearGlow.target.position.set(-3.55,1.65,-3.80);rearGlow.castShadow=true;rearGlow.shadow.mapSize.set(1024,1024);rearGlow.shadow.bias=-.00012;rearGlow.shadow.normalBias=.004;scene.add(rearGlow,rearGlow.target);
 const rearTreeWash=new THREE.SpotLight('#ddc5a0',14*backgroundLightScale(),5.9,.81,1,2);rearTreeWash.position.set(1.60,.12,-7.50);rearTreeWash.target.position.set(1.40,2.30,-6.80);rearTreeWash.castShadow=true;rearTreeWash.shadow.mapSize.set(1024,1024);rearTreeWash.shadow.bias=-.00012;rearTreeWash.shadow.normalBias=.004;scene.add(rearTreeWash,rearTreeWash.target);
 const geometrySignature=await backgroundGeometrySignature(scene,subject,m.terrain);
 return {scene,subject,key,ground,layout:'night-'+layout,metadata:{geometrySignature,backgroundFinish:new URLSearchParams(location.search).get('finish')||'baseline',canopyMass:new URLSearchParams(location.search).get('canopy')||'baseline',terrain:{version:'pavilion-terrain-v01',rootContacts,heightSource:'One authored512px linear data field used by both geometry and material, generated in memory',triangles:ground.geometry.index.count/3,samples:[[-2.11,-1.60],[-2.78,-.25],[-3.10,.81],[0,0]].map(([x,z])=>({x,z,y:groundHeight(x,z)}))},phase:'Pavilion wide opening, layered trees at middle/rear, connected unequal moss cushions; hero gray-brown/brown geometry/material unchanged',materialMaps:m.maps,roomLight:{position:room.position.toArray(),target:room.target.position.toArray(),shadowMap:1024,porchFillPosition:roomBounce.position.toArray(),porchFill:'Weak room bounce approximation within the deep room; proposed mode includes a weakly emissive paper lamp shade (.12), plus its finite point source'},contacts,reference:'hybrid-1132/desktop-candidate01.png',architecture:built,planting:plants,largeGardenStones:rocks,scatteredSmallStoneObjects:0,groundBaseY:-.022,stoneMinimumY:-.0497234085,stoneBurialAtNominalGround:.0277234085,lightComparison:proposedRoom?'Room sources follow new architecture; hero key/exposure fixed':'All original world light positions and powers fixed for structure comparison',lightDesign:'Same cool sky/moon and hero key; moon occluded by real architecture, warm room lighting; small dry paper lamp shade has weak emission in proposed mode, not a luminous wall'}};
}
