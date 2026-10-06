import {housePoint,HOUSE_YAW,HOUSE_X_SCALE,HOUSE_MATRIX} from './layout.js';
import * as THREE from 'three';import {batches,groundHeight,random} from './garden-geometry.js';
// A wide unsupported opening is carried by an actual deep perimeter beam and
// two corner columns. Interior planes recede from that front plane by 2.45m.
export function architecture(scene,m){
 const batch=batches(scene,m),{box}=batch,contacts=[],rng=random(93011),left=1.28,right=6.08,front=-4.10,back=-6.64,cx=(left+right)/2;
 let housePhase=true;const B=(p,s,key,angle=0)=>box(housePhase?housePoint(p).toArray():p,housePhase?[s[0]*HOUSE_X_SCALE,s[1],s[2]]:s,key,angle,housePhase?HOUSE_YAW:0);
 B([cx,.077,-5.42],[4.88,.22,2.52],'foundation');
 for(const x of [1.42,2.61,3.80,4.99,6.05]){
  const z=-3.72,at=housePoint([x,0,z]),floor=groundHeight(at.x,at.z),top=.023;
  B([x,(floor-.021+top)/2,z],[.25,top-floor+.021,.28],'foundation');B([x,.130,z],[.097,.214,.106],'vertical');
  contacts.push({position:[at.x,at.z],groundY:floor,stoneBottom:floor-.021,stoneTop:top,woodBottom:.023,woodTop:.237});
 }
 B([cx,.220,-3.73],[5.02,.13,.14],'horizontal');B([cx,.219,-4.30],[5.03,.13,.14],'horizontal');
 for(let i=0;i<37;i++)B([1.17+i*.139,.288,-3.92],[.135,.044,.83],'lengthwise');
 B([cx,.280,-3.49],[5.23,.060,.035],'horizontal');
 B([cx,.313,-5.38],[4.92,.048,2.39],'horizontal');
 for(const z of [-6.48,-4.22])B([cx,.349,z],[4.86,.05,.14],'horizontal');
 for(const x of [1.34,6.03])B([x,.349,-5.35],[.16,.05,2.41],'lengthwise');
 for(let col=0;col<3;col++)for(let row=0;row<2;row++){
  const x=2.10+col*1.57,z=-5.91+row*1.07;B([x,.348,z],[1.546,.057,1.047],'tatami');
  for(const dz of [-.49,.49])B([x,.378,z+dz],[1.548,.004,.025],'matBorder');
 }
 // Grooved sill and narrow upright corner supports stay out of the open bay.
 for(const [z,w]of [[-4.173,.07],[-4.100,.064],[-4.028,.066]])B([cx,.369,z],[4.82,.064,w],'horizontal');
 for(const x of [right]){
  B([x,1.49,front],[.158,2.24,.172],'vertical');B([x,2.553,front],[.231,.125,.252],'horizontal');
  B([x,.397,front],[.246,.063,.254],'horizontal');
 }
 B([cx,2.568,front],[5.05,.246,.225],'horizontal');B([cx,2.418,front],[4.83,.047,.078],'horizontal');
 // Thick side returns, back wall and a recessed alcove make a room, not a card.
 B([1.31,1.49,-5.44],[.19,2.23,2.61],'vertical');B([6.13,1.49,-5.44],[.19,2.23,2.61],'plaster');
 B([2.80,1.49,back],[3.00,2.23,.19],'plaster');B([5.67,1.49,back],[1.06,2.23,.19],'plaster');
 B([4.72,.418,-6.32],[1.71,.108,.59],'horizontal');B([4.72,1.43,-6.67],[1.67,1.95,.044],'alcove');
 for(const x of [3.84,5.60])B([x,1.46,-6.30],[.088,2.02,.64],'vertical');B([4.72,2.425,-6.30],[1.88,.11,.67],'horizontal');
 // A second, narrow screen behind the open bay has actual rails and divisions.
 B([2.12,1.47,-6.50],[1.29,2.08,.041],'paper');
 for(const x of [1.43,2.81])B([x,1.46,-6.48],[.057,2.15,.052],'vertical');
 for(let i=0;i<5;i++)B([1.52+i*.30,1.47,-6.474],[.020,2.04,.023],'vertical');
 for(const y of [.44,1.10,1.77,2.49])B([2.12,y,-6.47],[1.43,.025,.026],'horizontal');
 // The front roof load returns to the corner columns and four real ceiling beams.
 B([cx,2.663,-5.32],[5.07,.06,2.69],'horizontal');
 for(const x of [1.46,2.97,4.48,5.98])B([x,2.602,-5.33],[.105,.105,2.62],'lengthwise');
 B([cx,2.749,-3.42],[5.72,.152,.138],'horizontal');B([cx,2.797,-3.409],[5.77,.052,.037],'horizontal');
 for(let i=0;i<33;i++)B([.87+i*.177,2.701,-3.85],[.063,.075,1.10],'lengthwise');
 // Two shallow tiled planes with a raised ridge and individually hollow tiles.
 for(const hand of [-1,1]){
  const roof=new THREE.BoxGeometry(5.80,.052,1.82);roof.rotateX(hand*.23);roof.translate(cx,2.984,-5.20+hand*.82);roof.applyMatrix4(HOUSE_MATRIX);batch.add(roof,'roof');
  for(let i=0;i<42;i++){const tile=new THREE.CylinderGeometry(.043,.043,1.83,8,1,true,Math.PI/2,Math.PI);tile.rotateX(Math.PI/2+hand*.23);tile.translate(.825+i*.139,3.012,-5.20+hand*.82);tile.applyMatrix4(HOUSE_MATRIX);batch.add(tile,'roof');}
 }
 const ridge=new THREE.CylinderGeometry(.07,.07,5.92,10);ridge.rotateZ(Math.PI/2);ridge.translate(cx,3.20,-5.2);ridge.applyMatrix4(HOUSE_MATRIX);batch.add(ridge,'roof');
 B([4.86,2.525,-4.91],[1.3,.052,.145],'horizontal');B([4.86,2.484,-4.853],[1.3,.070,.036],'lengthwise');
 B([4.86,.689,-5.84],[1.36,.085,.51],'horizontal');
 for(const x of [4.27,5.45])for(const z of [-6.02,-5.67])B([x,.524,z],[.057,.25,.056],'vertical');
 B([4.32,.445,-5.03],[.40,.046,.38],'horizontal');B([4.32,.394,-5.03],[.36,.056,.34],'tatami');
 B([5.08,.766,-5.84],[.13,.06,.13],'vertical');B([5.08,.904,-5.84],[.177,.216,.177],'lampShade');
 for(const x of [4.986,5.174])B([x,.904,-5.84],[.014,.23,.197],'vertical');B([5.08,1.020,-5.84],[.196,.016,.197],'horizontal');
 // Low left boundary joins the pavilion return; it does not cross the room.
 housePhase=false;const rearZ=-4.96,length=16.34,centre=-4.97;
 B([centre,.077,rearZ],[length,.20,.25],'foundation');B([centre,.659,rearZ-.058],[length,1.12,.078],'rearWood');
 for(let i=0;i<138;i++){const x=-13.10+i*.119,h=1.09+(rng()-.5)*.022;B([x,.115+h/2,rearZ],[.112,h,.069+rng()*.018],'rearWood');}
 B([centre,1.271,rearZ],[length,.118,.118],'horizontal');
 for(const y of [.29,.93,1.20])B([centre,y,rearZ+.048],[length,.055,.080],'horizontal');
 for(const x of [-13,-10.64,-8.28,-5.92,-3.56,-1.20,1.16,2.73])B([x,.66,rearZ+.004],[.103,1.34,.124],'vertical');
 for(const hand of [-1,1]){
  const g=new THREE.BoxGeometry(length+.14,.04,.40);g.rotateX(hand*.29);g.translate(centre,1.37,rearZ+hand*.185);batch.add(g,'roof');
  for(let i=0;i<112;i++){const tile=new THREE.CylinderGeometry(.035,.035,.426,7,1,true,Math.PI/2,Math.PI);tile.rotateX(Math.PI/2+hand*.29);tile.translate(-13.1+i*.148,1.394,rearZ+hand*.186);batch.add(tile,'roof');}
 }
 const r=new THREE.CylinderGeometry(.058,.058,length+.22,9);r.rotateZ(Math.PI/2);r.translate(centre,1.483,rearZ);batch.add(r,'roof');
 return {...batch.done(),version:'pavilion-wide-opening-v01',houseYaw:HOUSE_YAW,frontEdge:housePoint([cx,.30,-3.49]).toArray(),deckTop:.31,interiorFloorTop:.376,verandaSupportContacts:contacts,roomOpening:{front:housePoint([1.42,1.50,-4.10]).toArray(),rear:housePoint([6.0,1.50,-4.10]).toArray(),yMin:.402,yMax:2.448},layers:['3.15m diagonal uninterrupted front opening','246mm bearing perimeter beam','108mm far corner column; close load carried by thick cedar return','2.54m recessed room','actual side returns/alcove/screen','44mm deck boards/support beams/short posts/buried feet','two roof planes/rafters/hollow tiles/ridge'],rearBoundaryZ:rearZ};
}
