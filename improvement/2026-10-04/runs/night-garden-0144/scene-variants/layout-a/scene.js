import * as THREE from 'three';
import {gardenMaterials} from './garden-materials.js';
import {batches,groundGeometry,stoneGeometry,planting,random} from './garden-geometry.js';

function sky(scene){
 const material=new THREE.ShaderMaterial({side:THREE.BackSide,depthWrite:false,toneMapped:false,
 vertexShader:'varying vec3 direction;void main(){direction=position;gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.);}',
 fragmentShader:`varying vec3 direction;void main(){vec3 d=normalize(direction);float t=clamp(d.y*1.65,0.,1.);vec3 c=mix(vec3(.013,.038,.081),vec3(.0025,.008,.022),pow(t,.67));float veil=sin(d.x*7.+d.y*10.)*sin(d.z*9.-d.y*7.);c+=vec3(.001,.0018,.003)*veil*(1.-t);gl_FragColor=vec4(c,1.);#include <colorspace_fragment>}`.replace(';#include',';\n#include')});
 const dome=new THREE.Mesh(new THREE.SphereGeometry(45,36,18),material);dome.name='Deep blue night sky';dome.renderOrder=-100;scene.add(dome);
 const rng=random(19721),p=[];for(let i=0;i<70;i++){const a=rng()*Math.PI*2,h=.17+rng()*.72,r=Math.sqrt(1-h*h);p.push(44*r*Math.cos(a),44*h,44*r*Math.sin(a));}
 const geometry=new THREE.BufferGeometry();geometry.setAttribute('position',new THREE.Float32BufferAttribute(p,3));const stars=new THREE.Points(geometry,new THREE.PointsMaterial({color:'#b9c7dc',size:.022,transparent:true,opacity:.4,depthWrite:false,toneMapped:false}));stars.name='Sparse faint stars';scene.add(stars);
}

function architecture(scene,m,layout){
 const batch=batches(scene,m),{box}=batch;const rng=random(93011);
 const shift=layout==='b'?-.55:0;
 const B=(p,s,key,angle=0)=>box([p[0],p[1],p[2]+shift],s,key,angle);
 // Foundation, separate deck and interior floor. The underside and joints read
 // through the open bay, rather than a flat facade placed behind the tree.
 B([3.60,.068,-1.87],[3.48,.18,5.40],'foundation');
 for(const z of [-4.26,-2.50,-.72,.60])for(const x of [1.91,2.56,4.78])B([x,.072,z],[.20,.21,.20],'foundation');
 B([1.75,.18,-1.88],[.13,.21,5.45],'lengthwise');
 for(let i=0;i<37;i++)B([3.45,.27,-4.42+i*.143],[3.54,.060,.135],'horizontal');
 B([3.77,.32,-1.96],[2.43,.055,4.99],'horizontal');
 // Thick framing of the left-facing facade, with a deep open room.
 for(const z of [-4.18,-2.80,-.40,.66])B([2.46,1.47,z],[.16,2.43,.18],'vertical');
 B([2.46,2.66,-1.76],[.21,.25,5.24],'lengthwise');
 B([2.46,.39,-1.76],[.16,.15,5.24],'lengthwise');
 B([4.91,1.54,-1.88],[.19,2.51,5.39],'plaster');
 B([3.63,1.54,-4.50],[2.54,2.51,.18],'plaster');
 B([3.69,1.54,.77],[2.61,2.51,.18],'plaster');
 B([3.72,2.68,-1.89],[2.68,.13,5.4],'horizontal');
 // A recess beyond the opening has separate side, back and raised floor planes.
 B([4.20,.40,-2.92],[1.24,.105,1.22],'horizontal');
 B([4.79,1.45,-2.92],[.045,2.02,1.16],'plaster');
 B([4.26,1.46,-3.53],[1.22,2.04,.10],'vertical');
 // Restrained paper screens occupy only one rear bay, not a full backdrop grid.
 for(const z of [-3.84,-3.33]){
  B([2.49,1.47,z],[.046,2.02,.48],'paper');
  for(const zz of [z-.246,z+.246])B([2.453,1.47,zz],[.035,2.12,.027],'vertical');
  for(const yy of [.51,1.02,1.63,2.44])B([2.451,yy,z],[.036,.021,.49],'lengthwise');
 }
 // Framed right-front return prevents an infinite dark interior.
 B([4.43,1.40,-.0],[.85,2.0,.05],'paper');
 for(const x of [4.01,4.44,4.87])B([x,1.40,.035],[.029,2.08,.037],'vertical');
 for(const y of [.40,1.03,1.68,2.4])B([4.44,y,.035],[.88,.027,.04],'horizontal');
 // Layered eaves: visible beam thickness, irregular weathered end grain,
 // shaded underside and a shallow pitched ceramic cap.
 B([3.23,2.86,-1.88],[3.96,.13,5.70],'horizontal',.092);
 B([3.29,2.98,-1.88],[4.21,.084,5.86],'roof',.092);
 B([1.18,2.72,-1.88],[.12,.15,5.90],'lengthwise');
 for(let j=0;j<31;j++)B([1.73,2.77,-4.76+j*.187],[1.10,.073,.054],'horizontal',.092);
 for(let j=0;j<47;j++){
  const g=new THREE.CylinderGeometry(.042,.042,4.23,6,1,true,0,Math.PI);g.rotateZ(Math.PI/2+.092);g.translate(3.28,3.031,-4.77+j*.127+shift);batch.add(g,'roof');
 }
 // The garden boundary is a low, deep timber structure with varied boards.
 const rearZ=layout==='b'?-5.15:-4.92;
 box([-1.03,.10,rearZ],[6.98,.22,.25],'foundation');
 for(let i=0;i<57;i++){
  const x=-4.45+i*.119,height=1.10+(rng()-.5)*.018;
  box([x,.12+height/2,rearZ],[.111,height,.068+rng()*.020],'rearWood');
 }
 for(const y of [.32,.91,1.245])box([-1.03,y,rearZ+.055],[6.98,.059,.083],'lengthwise');
 for(const x of [-4.55,-2.6,-.55,1.0,2.45])box([x,.69,rearZ+.015],[.115,1.4,.13],'vertical');
 box([-1.03,1.38,rearZ-.015],[7.15,.063,.62],'roof',0);
 box([-1.03,1.34,rearZ+.306],[7.19,.11,.065],'lengthwise');
 return {...batch.done(),frontEdgeX:1.75,deckTop:.30,roomOpening:{x:2.46,zMin:-2.80+shift,zMax:-.40+shift,yMin:.47,yMax:2.53},rearBoundaryZ:rearZ};
}

export function createScene(hero,study){
 const scene=new THREE.Scene(),subject=new THREE.Group();subject.name='bonsai';subject.add(hero);scene.add(subject);
 const clay=['clay','material','normals'].includes(study),layout=new URLSearchParams(location.search).get('layout')||'a';
 if(clay){
  scene.background=new THREE.Color('#dedcd6');
  const ground=new THREE.Mesh(new THREE.PlaneGeometry(30,30),new THREE.MeshStandardMaterial({color:'#d1cec6',roughness:1}));ground.rotation.x=-Math.PI/2;ground.position.y=-.035;ground.receiveShadow=true;scene.add(ground);
  scene.add(new THREE.HemisphereLight('#ffffff','#9a9387',1.1));const key=new THREE.DirectionalLight('#fffaf0',3.4);key.position.set(-3.8,4.5,2.8);key.target.position.set(0,.9,0);key.castShadow=true;key.shadow.mapSize.set(2048,2048);Object.assign(key.shadow.camera,{left:-3,right:3,top:3,bottom:-3,near:.1,far:12});key.shadow.bias=-.0001;key.shadow.normalBias=.003;key.shadow.radius=5;scene.add(key,key.target);const fill=new THREE.DirectionalLight('#edf0f4',.55);fill.position.set(3,3,-2);scene.add(fill);return {scene,subject,key,ground,layout:'diagnostic'};
 }
 scene.background=new THREE.Color('#101e32');sky(scene);scene.fog=new THREE.FogExp2('#142337',.020);
 const m=gardenMaterials(),ground=new THREE.Mesh(groundGeometry(),m.ground);ground.name='Continuous mineral gravel and growing moss';ground.receiveShadow=true;scene.add(ground);
 const built=architecture(scene,m,layout);
 const rocks=[{center:[-1.87,.065,-1.54],scale:[.57,.50,.42],seed:3},{center:[-2.80,.055,-2.70],scale:[.42,.40,.37],seed:14}];
 for(const r of rocks){const rock=new THREE.Mesh(stoneGeometry(r.center,r.scale,r.seed),m.stone);rock.name='Partly buried natural garden stone';rock.castShadow=rock.receiveShadow=true;scene.add(rock);}
 const plants=planting(scene,m,layout);
 scene.add(new THREE.HemisphereLight('#a3bddb','#29251d',.46));
 const moon=new THREE.DirectionalLight('#a9c6e9',.44);moon.position.set(-3.2,7.0,-2.5);scene.add(moon);
 // A concealed, broad warm garden wash and cool sky illuminate one place.
 const key=new THREE.SpotLight('#ffe0b5',44,14,.78,1,2);key.position.set(-2.2,3.4,3.2);key.target.position.set(0,.72,-.4);key.castShadow=true;key.shadow.mapSize.set(2048,2048);key.shadow.camera.near=.15;key.shadow.camera.far=14;key.shadow.bias=-.00012;key.shadow.normalBias=.0023;key.shadow.radius=7;scene.add(key,key.target);
 const room=new THREE.PointLight('#ffcb8b',10.5,7,2);room.position.set(3.69,1.40,layout==='b'?-2.07:-1.52);scene.add(room);
 const rearGlow=new THREE.PointLight('#d5ae74',1.45,3.5,2);rearGlow.position.set(-2.9,.42,-3.50);scene.add(rearGlow);
 return {scene,subject,key,ground,layout:'night-'+layout,metadata:{phase:'Night layout study; hero geometry unchanged',reference:'hybrid-1132/desktop-candidate01.png',architecture:built,planting:plants,largeGardenStones:rocks,scatteredSmallStoneObjects:0,groundBaseY:-.022,stoneMinimumY:-.0497234085,stoneBurialAtNominalGround:.0277234085,lightDesign:'Soft cool sky/moon, restrained broad warm garden wash, warm room opening; no daylight or visible moon glow'}};
}
