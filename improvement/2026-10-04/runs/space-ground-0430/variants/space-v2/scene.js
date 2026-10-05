import {loadGardenRocks,placeGardenRocks} from './garden-rocks.js';
import * as THREE from 'three';
import {gardenMaterials} from './garden-materials.js';
import {batches,groundGeometry,groundHeight,setGroundField,planting,random} from './garden-geometry.js';

function sky(scene){
 const material=new THREE.ShaderMaterial({side:THREE.BackSide,depthWrite:false,toneMapped:false,
 vertexShader:'varying vec3 direction;void main(){direction=position;gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.);}',
 fragmentShader:`varying vec3 direction;void main(){vec3 d=normalize(direction);float t=smoothstep(-.03,.72,d.y);vec3 c=mix(vec3(.016,.040,.085),vec3(.0025,.008,.024),pow(t,.67));float veil=sin(d.x*7.+d.y*10.)*sin(d.z*9.-d.y*7.);c+=vec3(.001,.0018,.003)*veil*(1.-t);gl_FragColor=vec4(c,1.);#include <colorspace_fragment>}`.replace(';#include',';\n#include')});
 const dome=new THREE.Mesh(new THREE.SphereGeometry(45,36,18),material);dome.name='Deep blue night sky';dome.renderOrder=-100;scene.add(dome);
 const rng=random(19721),p=[];for(let i=0;i<70;i++){const a=rng()*Math.PI*2,h=.17+rng()*.72,r=Math.sqrt(1-h*h);p.push(44*r*Math.cos(a),44*h,44*r*Math.sin(a));}
 const geometry=new THREE.BufferGeometry();geometry.setAttribute('position',new THREE.Float32BufferAttribute(p,3));const stars=new THREE.Points(geometry,new THREE.PointsMaterial({color:'#b9c7dc',size:.022,transparent:true,opacity:.4,depthWrite:false,toneMapped:false}));stars.name='Sparse faint stars';scene.add(stars);
}

function architecture(scene,m,layout){
 const batch=batches(scene,m),{box}=batch,rng=random(93011),yaw=-.21;
 const housePoint=p=>new THREE.Vector3(p[0]-2.46,p[1],p[2]-.60).applyAxisAngle(new THREE.Vector3(0,1,0),yaw).add(new THREE.Vector3(2.08,0,.15));
 const B=(p,s,key,angle=0)=>box(housePoint(p).toArray(),s,key,angle,yaw);
 const supportContacts=[];
 // A raised room and an open underside beneath the narrow veranda.
 // Floor boards bear on two continuous beams, then short posts and stone feet.
 B([3.77,.076,-1.91],[2.33,.21,5.05],'foundation');
 for(const z of [-4.22,-2.64,-1.05,.32]){
  const p=housePoint([1.98,0,z]),floor=groundHeight(p.x,p.z),stoneTop=.027;
  B([1.98,(floor-.020+stoneTop)/2,z],[.25,stoneTop-floor+.020,.28],'foundation');
  B([1.98,.125,z],[.102,.200,.11],'vertical');
  supportContacts.push({position:[p.x,p.z],groundY:floor,stoneBottom:floor-.020,stoneTop,woodBottom:.025,woodTop:.225});
 }
 B([1.98,.223,-1.91],[.136,.125,5.30],'lengthwise');
 B([2.43,.229,-1.91],[.15,.137,5.38],'lengthwise');
 for(let i=0;i<37;i++)B([2.10,.288,-4.49+i*.141],[.87,.044,.135],'horizontal');
 // Thin front end-board overlaps the supporting beam; no huge solid slab.
 B([2.10,.281,.682],[.87,.058,.034],'horizontal');
 B([1.663,.280,-1.91],[.035,.059,5.35],'lengthwise');
 // Interior floor is a little higher, with a continuous wooden perimeter.
 B([3.76,.311,-1.91],[2.46,.05,5.18],'horizontal');
 for(const x of [2.61,4.80])B([x,.344,-1.92],[.16,.052,4.99],'lengthwise');
 for(const z of [-4.40,.51])B([3.72,.344,z],[2.07,.052,.13],'horizontal');
 for(let row=0;row<3;row++)for(let col=0;col<2;col++){
  const x=3.185+col*1.015,z=-3.58+row*1.60;
  B([x,.348,z],[1.001,.056,1.576],'tatami');
  for(const dx of [-.477,.477])B([x+dx,.377,z],[.025,.004,1.574],'matBorder');
 }
 // Sill and paired shallow track rebates have actual depth.
 for(const [x,w]of [[2.39,.073],[2.476,.091],[2.558,.058]])B([x,.369,-1.91],[w,.066,5.20],'lengthwise');
 for(const z of [-4.20,-2.80,-.40,.66]){
  B([2.46,1.498,z],[.145,2.255,.158],'vertical');
  B([2.46,2.552,z],[.225,.13,.222],'lengthwise');
 }
 B([2.46,2.573,-1.78],[.23,.158,5.26],'lengthwise');
 B([2.461,2.468,-1.78],[.168,.040,5.18],'lengthwise');
 // Wall returns enclose the room instead of a flat rectangle across the view.
 B([4.96,1.489,-1.91],[.20,2.24,5.31],'plaster');
 B([3.73,1.489,-4.53],[2.67,2.24,.18],'plaster');
 B([4.89,1.498,.66],[.16,2.255,.16],'vertical');
 B([3.66,2.57,.66],[2.61,.17,.18],'horizontal');
 B([4.67,1.485,.64],[.29,2.22,.18],'plaster');
 B([4.455,1.49,.627],[.09,2.25,.23],'vertical');
 B([3.43,2.435,.645],[2.03,.09,.095],'horizontal');
 // The rear alcove has near cheeks, a raised floor and a deeper back plane.
 B([3.88,.416,-4.10],[1.78,.103,.64],'horizontal');
 B([3.88,1.44,-4.48],[1.67,1.99,.045],'alcove');
 B([2.998,1.447,-4.12],[.086,2.0,.65],'vertical');
 B([4.752,1.447,-4.12],[.085,2.0,.65],'vertical');
 B([3.875,2.423,-4.12],[1.84,.102,.66],'horizontal');
 B([3.875,2.362,-3.794],[1.81,.040,.035],'horizontal');
 // A deep secondary screen crosses only the rear bay, so the garden sees
 // the near posts, inner floor and back alcove at different distances.
 for(const z of [-3.91,-3.35]){
  B([2.52,1.464,z],[.042,2.045,.525],'paper');
  for(const zz of [z-.272,z+.272])B([2.486,1.464,zz],[.036,2.145,.030],'vertical');
  for(const yy of [.44,.93,1.53,2.485])B([2.483,yy,z],[.037,.020,.548],'lengthwise');
 }
 // Ceiling, joists and layered eaves. Each visible edge has its own thickness.
 B([3.72,2.676,-1.91],[2.69,.055,5.4],'horizontal');
 for(const z of [-4.35,-3.1,-1.85,-.60,.57])B([3.73,2.601,z],[2.69,.108,.105],'horizontal');
 B([3.23,2.824,-1.88],[3.96,.043,5.70],'horizontal',.092);
 B([3.29,2.918,-1.88],[4.21,.074,5.86],'roof',.092);
 B([1.18,2.719,-1.88],[.130,.154,5.90],'lengthwise');
 B([1.106,2.762,-1.88],[.039,.061,5.91],'lengthwise');
 for(let j=0;j<28;j++){
  const z=-4.72+j*.211;
  B([1.78,2.740,z],[1.19,.076,.061],'horizontal',.092);
  B([2.32,2.662,z],[.26,.118,.07],'horizontal');
 }
 for(let j=0;j<47;j++){
  const g=new THREE.CylinderGeometry(.042,.042,4.23,8,1,true,0,Math.PI);g.rotateZ(Math.PI/2+.092);g.rotateY(yaw);g.translate(...housePoint([3.28,2.969,-4.77+j*.127]).toArray());batch.add(g,'roof');
 }
 // Concealed cove lighting has a real lip above the front room opening.
 B([3.86,2.552,-.15],[1.28,.050,.155],'horizontal');
 B([3.86,2.513,-.092],[1.28,.07,.036],'lengthwise');
 const rearZ=layout==='b'?-5.15:-4.92;
 box([-2.20,.10,rearZ],[11.72,.22,.25],'foundation');
 box([-2.20,.69,rearZ-.07],[11.72,1.13,.078],'rearWood');
 for(let i=-30;i<67;i++){
  const boardRng=i<0?random(93011+i*377):rng,x=-4.45+i*.119,height=1.10+(boardRng()-.5)*.018;
  box([x,.12+height/2,rearZ],[.111,height,.068+boardRng()*.020],'rearWood');
 }
 for(const y of [.32,.91,1.245])box([-2.20,y,rearZ+.055],[11.72,.059,.083],'lengthwise');
 for(const x of [-8.06,-6.3,-4.55,-2.6,-.55,1.0,2.45,3.65])box([x,.69,rearZ+.015],[.115,1.4,.13],'vertical');
 box([-2.20,1.38,rearZ-.015],[11.89,.063,.62],'roof',0);
 box([-2.20,1.34,rearZ+.306],[11.93,.11,.065],'lengthwise');
 box([-2.20,1.29,rearZ+.01],[11.72,.09,.095],'lengthwise');
 return {...batch.done(),version:'space-v2',houseYaw:yaw,frontEdge:housePoint([1.75,.3,.6]).toArray(),deckTop:.31,interiorFloorTop:.376,verandaSupportContacts:supportContacts,roomOpening:{front:housePoint([2.46,1.5,-.4]).toArray(),rear:housePoint([2.46,1.5,-2.8]).toArray(),yMin:.402,yMax:2.448},layers:['floorboards 44mm','support beams125mm','short posts200mm','buried foundation feet','grooved66mm threshold','158mm-deep posts','recessed room and alcove','separate joists/rafters/roof'],rearBoundaryZ:rearZ};
}

export async function createScene(hero,study){
 const scene=new THREE.Scene(),subject=new THREE.Group();subject.name='bonsai';subject.add(hero);scene.add(subject);
 const clay=['clay','material','normals'].includes(study),layout=new URLSearchParams(location.search).get('layout')||'b';
 if(clay){
  scene.background=new THREE.Color('#dedcd6');
  const ground=new THREE.Mesh(new THREE.PlaneGeometry(30,30),new THREE.MeshStandardMaterial({color:'#d1cec6',roughness:1}));ground.rotation.x=-Math.PI/2;ground.position.y=-.035;ground.receiveShadow=true;scene.add(ground);
  scene.add(new THREE.HemisphereLight('#ffffff','#9a9387',1.1));const key=new THREE.DirectionalLight('#fffaf0',3.4);key.position.set(-3.8,4.5,2.8);key.target.position.set(0,.9,0);key.castShadow=true;key.shadow.mapSize.set(2048,2048);Object.assign(key.shadow.camera,{left:-3,right:3,top:3,bottom:-3,near:.1,far:12});key.shadow.bias=-.0001;key.shadow.normalBias=.003;key.shadow.radius=5;scene.add(key,key.target);const fill=new THREE.DirectionalLight('#edf0f4',.55);fill.position.set(3,3,-2);scene.add(fill);return {scene,subject,key,ground,layout:'diagnostic'};
 }
 scene.background=new THREE.Color('#101e32');sky(scene);scene.fog=new THREE.FogExp2('#142337',.020);
 const [m,rockAssets]=await Promise.all([gardenMaterials(),loadGardenRocks()]);setGroundField(m.terrain.image);const ground=new THREE.Mesh(groundGeometry(),m.ground);ground.name='Continuous mineral gravel and growing moss';ground.receiveShadow=true;scene.add(ground);
 const farGeometry=new THREE.PlaneGeometry(100,100);farGeometry.rotateX(-Math.PI/2);farGeometry.translate(0,-.029,0);const distantGround=new THREE.Mesh(farGeometry,m.ground);distantGround.name='Continuous distant mineral ground';distantGround.receiveShadow=true;scene.add(distantGround);
 const built=architecture(scene,m,layout);
 const rocks=placeGardenRocks(scene,rockAssets,m);
 const plants=planting(scene,m,layout);
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
 plants.mossTufts=0;plants.mossTuftTriangles=0;plants.mossDetail='Authored shore and soil hollows share one relief field with geometry; no moss sheet or scattered tetrahedra';
 
 scene.updateMatrixWorld(true);let bed;const feet=[];hero.traverse(o=>{if(!o.isMesh)return;if(/bedding[_ ]stone/i.test(o.name))bed=o;if(/ceramic[_ ]foot/i.test(o.name))feet.push(o);});
 const ray=new THREE.Raycaster(),contacts=[];if(bed)for(const foot of feet){const bounds=new THREE.Box3().setFromObject(foot),centre=bounds.getCenter(new THREE.Vector3());ray.set(new THREE.Vector3(centre.x,bounds.min.y+.035,centre.z),new THREE.Vector3(0,-1,0));const hit=ray.intersectObject(bed,false)[0];contacts.push({foot:foot.name,footBottomY:bounds.min.y,stoneTopY:hit?.point.y,gapMetres:hit?bounds.min.y-hit.point.y:null});}
 scene.add(new THREE.HemisphereLight('#a3bddb','#29251d',.58));
 const moon=new THREE.DirectionalLight('#a9c6e9',.58);moon.position.set(-3.2,7.0,-2.5);moon.castShadow=true;moon.shadow.mapSize.set(1024,1024);Object.assign(moon.shadow.camera,{left:-7,right:7,top:6,bottom:-5,near:.3,far:18});moon.shadow.normalBias=.009;moon.shadow.bias=-.00012;moon.shadow.radius=5;scene.add(moon);
 // A concealed, broad warm garden wash and cool sky illuminate one place.
 const key=new THREE.SpotLight('#ffe0b5',70,14,.78,1,2);key.position.set(-2.2,3.4,3.2);key.target.position.set(0,.72,-.4);key.castShadow=true;key.shadow.mapSize.set(2048,2048);key.shadow.camera.near=.15;key.shadow.camera.far=14;key.shadow.bias=-.00012;key.shadow.normalBias=.0023;key.shadow.radius=7;scene.add(key,key.target);
 const roomPoint=p=>new THREE.Vector3(p[0]-2.46,p[1],p[2]-.60).applyAxisAngle(new THREE.Vector3(0,1,0),-.21).add(new THREE.Vector3(2.08,0,.15));
 const room=new THREE.SpotLight('#ffd4a0',18,7,.82,1,2);room.position.copy(roomPoint([3.96,2.49,-.88]));room.target.position.copy(roomPoint([3.84,1.05,-4.38]));room.castShadow=true;room.shadow.mapSize.set(1024,1024);room.shadow.camera.near=.12;room.shadow.camera.far=7;room.shadow.bias=-.00015;room.shadow.normalBias=.003;room.shadow.radius=4;scene.add(room,room.target);
 const roomBounce=new THREE.PointLight('#ecd0a4',2.5,3.6,2);roomBounce.position.copy(roomPoint([2.88,1.74,-1.72]));scene.add(roomBounce);
 const rearGlow=new THREE.SpotLight('#ddc5a0',8.4,5.5,.67,1,2);rearGlow.position.set(-3.70,.20,-3.1);rearGlow.target.position.set(-2.80,1.50,-3.7);scene.add(rearGlow,rearGlow.target);
 return {scene,subject,key,ground,layout:'night-'+layout,metadata:{terrain:{version:'space-v2',rootContacts,heightSource:'The same lossless512px linear data field used by the ground material',triangles:ground.geometry.index.count/3,samples:[[-2.11,-1.60],[-2.78,-.25],[-3.10,.81],[0,0]].map(([x,z])=>({x,z,y:groundHeight(x,z)}))},phase:'Space v2: supported veranda, layered room, real weathered stone volume and one-sided growing ground; fixed hero and cameras',materialMaps:m.maps,roomLight:{position:room.position.toArray(),target:room.target.position.toArray(),shadowMap:1024,porchFillPosition:roomBounce.position.toArray(),porchFill:'Weak room bounce approximation within the deep room; no emissive visible object'},contacts,reference:'hybrid-1132/desktop-candidate01.png',architecture:built,planting:plants,largeGardenStones:rocks,scatteredSmallStoneObjects:0,groundBaseY:-.022,stoneMinimumY:-.0497234085,stoneBurialAtNominalGround:.0277234085,lightDesign:'Same cool sky/moon and hero key; moon now occluded by real architecture, warm concealed room lighting, no visible glow surface'}};
}
