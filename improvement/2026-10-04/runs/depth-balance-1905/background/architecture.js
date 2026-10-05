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
 B([1.42,1.49,back],[.20,2.23,.19],'plaster');B([2.955,1.49,back],[.27,2.23,.19],'plaster');B([4.59,1.49,back],[3.00,2.23,.19],'plaster');B([2.17,2.53,back],[1.50,.27,.19],'plaster');
 B([2.17,.418,-6.32],[1.35,.108,.59],'horizontal');B([2.17,1.43,-6.67],[1.31,1.95,.044],'alcove');
 for(const x of [1.45,2.89])B([x,1.46,-6.30],[.088,2.02,.64],'vertical');B([2.17,2.425,-6.30],[1.59,.11,.67],'horizontal');
 // A second, narrow screen behind the open bay has actual rails and divisions.
 B([5.12,1.47,-6.48575],[1.29,2.08,.0005],'paper');
 for(const x of [4.43,5.81])B([x,1.46,-6.48],[.057,2.15,.052],'vertical');
 for(let i=0;i<5;i++)B([4.52+i*.30,1.47,-6.474],[.020,2.04,.023],'vertical');
 for(const y of [.44,1.10,1.77,2.49])B([5.12,y,-6.4725],[1.43,.025,.026],'horizontal');
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
 B([2.31,2.525,-4.91],[1.3,.052,.145],'horizontal');B([2.31,2.484,-4.853],[1.3,.070,.036],'lengthwise');
 B([2.31,.689,-5.84],[1.36,.085,.51],'horizontal');
 for(const x of [1.72,2.90])for(const z of [-6.02,-5.67])B([x,.524,z],[.057,.25,.056],'vertical');
 B([1.77,.445,-5.03],[.40,.046,.38],'horizontal');B([1.77,.394,-5.03],[.36,.056,.34],'tatami');
 B([2.53,.766,-5.84],[.13,.06,.13],'vertical');B([2.53,.904,-5.84],[.177,.216,.177],'lampShade');
 for(const x of [2.436,2.624])B([x,.904,-5.84],[.014,.23,.197],'vertical');B([2.53,1.020,-5.84],[.196,.016,.197],'horizontal');
 // Three real front shoji panels leave a generous near opening into the room.
 // Stiles, stopped rails, stepped half-lap kumiko and paper meet at real depths.
 const shojiRows=[];
 for(const centre of [3.25,4.37,5.49]){
  const width=1.12,bottom=.390,top=2.452,frame=.052,innerW=width-frame*2;
  const left=centre-width/2,right=centre+width/2;
  B([centre,bottom+.044,-4.085],[width,.088,.050],'horizontal');
  B([centre,top-.033,-4.085],[width,.066,.050],'horizontal');
  for(const x of [left+frame/2,right-frame/2])B([x,(bottom+top)/2+.011,-4.085],[frame,top-bottom-.132,.050],'vertical');
  const paperBottom=bottom+.088,paperTop=top-.066,height=paperTop-paperBottom,cy=(paperBottom+paperTop)/2;
  B([centre,cy,-4.09725],[innerW+.005,height+.006,.0005],'paper');
  for(let col=1;col<3;col++)B([left+frame+innerW*col/3,cy,-4.087],[.013,height,.020],'vertical');
  for(let row=1;row<7;row++){
   const y=paperBottom+height*row/7;
   for(let col=0;col<3;col++)B([left+frame+innerW*(col+.5)/3,y,-4.092],[innerW/3-.009,.012,.010],'horizontal');
  }
  // Shallow recessed pull: timber recess and a dark, matte insert, no ornament.
  B([left+.053,1.27,-4.056],[.028,.069,.004],'matBorder');
  shojiRows.push({centre:housePoint([centre,cy,-4.085]).toArray(),outerWidthMetres:width*HOUSE_X_SCALE,outerHeightMetres:top-bottom,paperThicknessMetres:.0005,frameThicknessMetres:.050,kumikoWidthMetres:.013*HOUSE_X_SCALE,kumikoDepthMetres:.020,joinery:'Stopped rails with1mm joints; half-depth stepped kumiko crossing; paper meets rear face, not a glowing card'});
 }
 B([cx,.385,-4.095],[4.82,.040,.194],'horizontal');B([cx,2.459,-4.095],[4.83,.055,.191],'horizontal');
 // Low left boundary joins the pavilion return; it does not cross the room.
 housePhase=false;const rearZ=-4.96,boundaryStart=-13.16,leftFront=housePoint([1.31,0,-4.10]),leftBack=housePoint([1.31,0,-6.64]),boundaryEnd=leftFront.clone().lerp(leftBack,(rearZ-leftFront.z)/(leftBack.z-leftFront.z)).x-.084,length=boundaryEnd-boundaryStart,centre=(boundaryEnd+boundaryStart)/2;
 B([centre,.066,rearZ],[length,.222,.25],'foundation');B([centre,1.044,rearZ-.058],[length,1.85,.078],'rearWood');
 for(let i=0;i<Math.floor(length/.119);i++){const x=boundaryStart+.06+i*.119,h=1.87+(rng()-.5)*.018;B([x,.115+h/2,rearZ],[.112,h,.069+rng()*.018],'rearWood');}
 B([centre,2.054,rearZ],[length,.110,.150],'horizontal');
 for(const y of [.29,1.07,1.92])B([centre,y,rearZ+.048],[length,.055,.080],'horizontal');
 for(const x of [-13,-10.64,-8.28,-5.92,-3.56,-1.20,1.16,boundaryEnd-.02])B([x,1.04,rearZ+.004],[.110,2.10,.132],'vertical');
 for(const hand of [-1,1]){
  const g=new THREE.BoxGeometry(length+.14,.04,.40);g.rotateX(hand*.29);g.translate(centre,2.15,rearZ+hand*.185);batch.add(g,'roof');
  for(let i=0;i<Math.floor(length/.148);i++){const tile=new THREE.CylinderGeometry(.035,.035,.426,7,1,true,Math.PI/2,Math.PI);tile.rotateX(Math.PI/2+hand*.29);tile.translate(boundaryStart+.06+i*.148,2.174,rearZ+hand*.186);batch.add(tile,'roof');}
 }
 const r=new THREE.CylinderGeometry(.058,.058,length+.22,9);r.rotateZ(Math.PI/2);r.translate(centre,2.263,rearZ);batch.add(r,'roof');
 return {...batch.done(),version:'solemn-front-shoji-v01',houseYaw:HOUSE_YAW,frontEdge:housePoint([cx,.30,-3.49]).toArray(),deckTop:.31,interiorFloorTop:.376,verandaSupportContacts:contacts,roomOpening:{front:housePoint([1.42,1.50,-4.10]).toArray(),rear:housePoint([6.0,1.50,-4.10]).toArray(),yMin:.402,yMax:2.448},layers:['3.65m real front bay,0.965m near opening and three851mm front shoji','246mm bearing perimeter beam','120mm far corner column; near load carried by cedar return','2.54m recessed room','actual side returns/alcove/screen','44mm deck boards/support beams/short posts/buried feet','two roof planes/rafters/hollow tiles/ridge'],rearBoundaryZ:rearZ,rearBoundaryEndX:boundaryEnd,roomIntersectionAvoided:true,rearBoundaryHeightMetres:2.321,frontShoji:shojiRows,nearOpenBayWidthMetres:(2.69-1.42)*HOUSE_X_SCALE,boundaryContactSamples:[-10.64,-8.28,-5.92,-3.56,-1.20,1.16,boundaryEnd-.02].map(x=>({x,z:rearZ,groundY:groundHeight(x,rearZ),foundationBottom:-.045,foundationBurial:groundHeight(x,rearZ)+.045}))};
}
