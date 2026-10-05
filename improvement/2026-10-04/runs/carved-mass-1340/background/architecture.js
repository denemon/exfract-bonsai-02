import * as THREE from 'three';
import {batches,groundHeight,random} from './garden-geometry.js';

export function architecture(scene,m,layout){
 const batch=batches(scene,m),{box}=batch,rng=random(93011),yaw=-.21;
 const housePoint=p=>new THREE.Vector3(p[0]-2.46,p[1],p[2]-.60).applyAxisAngle(new THREE.Vector3(0,1,0),yaw).add(new THREE.Vector3(1.72,0,-1.35));
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
 B([3.83,.624,-2.62],[1.15,.085,.53],'horizontal');
 for(const x of [3.36,4.30])for(const z of [-2.82,-2.42])B([x,.484,z],[.056,.225,.056],'vertical');
 B([3.54,.475,-1.85],[.42,.044,.39],'horizontal');
 B([3.55,.424,-1.85],[.37,.053,.34],'tatami');
 B([3.83,.696,-2.62],[.125,.06,.125],'vertical');
 B([3.83,.844,-2.62],[.177,.238,.177],'lampShade');
 for(const x of [3.736,3.924])B([x,.844,-2.62],[.014,.252,.197],'vertical');
 B([3.83,.971,-2.62],[.196,.016,.197],'horizontal');
 const rearZ=-6.20;
 box([-2.20,.10,rearZ],[11.72,.22,.25],'foundation');
 box([-2.20,.81,rearZ-.07],[11.72,1.37,.078],'rearWood');
 for(let i=-30;i<67;i++){
  const boardRng=i<0?random(93011+i*377):rng,x=-4.45+i*.119,height=1.34+(boardRng()-.5)*.018;
  box([x,.12+height/2,rearZ],[.111,height,.068+boardRng()*.020],'rearWood');
 }
 for(const y of [.32,1.02,1.46])box([-2.20,y,rearZ+.055],[11.72,.059,.083],'lengthwise');
 for(const x of [-8.06,-6.3,-4.55,-2.6,-.55,1.0,2.45,3.65])box([x,.81,rearZ+.015],[.115,1.62,.13],'vertical');
 // A real shallow pitched tiled roof, two sides and a raised ridge.
 for(const hand of [-1,1]){
  const roof=new THREE.BoxGeometry(11.90,.045,.49);roof.rotateX(hand*.29);roof.translate(-2.20,1.68,rearZ+hand*.23);batch.add(roof,'roof');
  for(let k=0;k<81;k++){const tile=new THREE.CylinderGeometry(.037,.037,.52,8,1,true,0,Math.PI);tile.rotateX(Math.PI/2-hand*.29);tile.translate(-8.05+k*.147,1.718,rearZ+hand*.235);batch.add(tile,'roof');}
 }
 const ridge=new THREE.CylinderGeometry(.066,.066,11.94,10);ridge.rotateZ(Math.PI/2);ridge.translate(-2.20,1.81,rearZ);batch.add(ridge,'roof');
 box([-2.20,1.59,rearZ+.467],[11.93,.11,.065],'lengthwise');
 box([-2.20,1.54,rearZ+.01],[11.72,.09,.095],'lengthwise');
 return {...batch.done(),version:'spatial-v03',houseYaw:yaw,frontEdge:housePoint([1.75,.3,.6]).toArray(),deckTop:.31,interiorFloorTop:.376,verandaSupportContacts:supportContacts,roomOpening:{front:housePoint([2.46,1.5,-.4]).toArray(),rear:housePoint([2.46,1.5,-2.8]).toArray(),yMin:.402,yMax:2.448},layers:['floorboards 44mm','support beams125mm','short posts200mm','buried foundation feet','grooved66mm threshold','158mm-deep posts','recessed room and alcove','separate joists/rafters/roof'],rearBoundaryZ:rearZ};
}

