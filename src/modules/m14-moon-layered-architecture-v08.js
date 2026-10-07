import {tsuijiBoundary} from './m18-moon-layered-boundary-v08.js';
import {housePoint,HOUSE_YAW,HOUSE_X_SCALE,HOUSE_MATRIX} from './m15-layout.js';
import {RoundedBoxGeometry} from 'three/addons/geometries/RoundedBoxGeometry.js';
import * as THREE from 'three';import {batches,groundHeight,random} from './m12-garden-geometry.js';
// A wide unsupported opening is carried by an actual deep perimeter beam and
// two corner columns. Interior planes recede from that front plane by 2.45m.
export function architecture(scene,m){
 const batch=batches(scene,m),{box}=batch,contacts=[],rng=random(93011),left=1.28,right=6.08,front=-4.10,back=-6.64,cx=(left+right)/2;
 let housePhase=true;const B=(p,s,key,angle=0)=>box(housePhase?housePoint(p).toArray():p,housePhase?[s[0]*HOUSE_X_SCALE,s[1],s[2]]:s,key,angle,housePhase?HOUSE_YAW:0);
 // Named receivers retain bounds measured from the produced Float32 vertices.
 const parts=[],inverseHouse=HOUSE_MATRIX.clone().invert(),v=new THREE.Vector3();
 const A=(p,size,key,name,pitch=0)=>{
  const at=housePoint(p),dims=[size[0]*HOUSE_X_SCALE,size[1],size[2]],g=new RoundedBoxGeometry(...dims,1,Math.min(.002,...dims.map(n=>n*.055)));
  g.setAttribute('grainPosition',g.attributes.position.clone());g.setAttribute('grainNormal',g.attributes.normal.clone());
  const seed=((Math.sin(at.x*23.71+at.y*17.17+at.z*39.03)*43758.5)%1+1)%1;
  g.setAttribute('boardSeed',new THREE.Float32BufferAttribute(new Float32Array(g.attributes.position.count).fill(seed),1));
  g.rotateX(pitch);g.rotateY(HOUSE_YAW);g.translate(at.x,at.y,at.z);
  const local=new THREE.Box3(),world=new THREE.Box3(),a=g.attributes.position;
  for(let i=0;i<a.count;i++){v.fromBufferAttribute(a,i);world.expandByPoint(v);v.applyMatrix4(inverseHouse);local.expandByPoint(v);}
  parts.push({name,key,vertices:a.count,localBounds:{min:local.min.toArray(),max:local.max.toArray()},worldBounds:{min:world.min.toArray(),max:world.max.toArray()},pitchRadians:pitch});batch.add(g,key);
 };
 B([cx,.077,-5.42],[4.88,.22,2.52],'foundation');
 for(const [i,x] of [1.42,2.61,3.80,4.99,6.05].entries()){
  const z=-3.72,at=housePoint([x,0,z]),floor=groundHeight(at.x,at.z),top=.023;
  A([x,(floor-.021+top)/2,z],[.25,top-floor+.021,.28],'foundation','stone-foot-'+i);A([x,.1025,z],[.097,.159,.106],'vertical','short-post-'+i);
  contacts.push({position:[at.x,at.z],groundY:floor,stoneBottom:floor-.021,stoneTop:top,woodBottom:.023,woodTop:.182});
 }
 A([cx,.216,-3.72],[5.02,.068,.14],'horizontal','front-crossbeam');A([cx,.216,-4.30],[5.03,.068,.14],'horizontal','rear-crossbeam');
 for(const [i,x]of [1.42,2.61,3.80,4.99,6.08].entries())A([x,.282,-4.01],[.086,.064,.85],'lengthwise','longitudinal-joist-'+i);
 for(let i=0;i<28;i++)A([1.1735+i*.185,.328,-3.99],[.181,.028,.99],'lengthwise','deck-board-'+i);
 A([cx,.318,-3.49],[5.23,.048,.035],'horizontal','veranda-front-fascia');
 B([cx,.313,-5.38],[4.92,.048,2.39],'horizontal');
 for(const z of [-6.48,-4.22])B([cx,.349,z],[4.86,.05,.14],'horizontal');
 for(const x of [1.34,6.03])B([x,.349,-5.35],[.16,.05,2.41],'lengthwise');
 for(let col=0;col<3;col++)for(let row=0;row<2;row++){
  const x=2.10+col*1.57,z=-5.91+row*1.07;B([x,.348,z],[1.546,.057,1.047],'tatami');
  for(const dz of [-.49,.49])B([x,.378,z+dz],[1.548,.004,.025],'matBorder');
 }
 // Grooved sill and narrow upright corner supports stay out of the open bay.
 for(const [i,[z,w]]of [[-4.408,.07],[-4.342,.064],[-4.276,.066]].entries())A([cx,.369,z],[4.82,.064,w],'horizontal','grooved-sill-'+i);
 for(const [i,x]of [1.42,6.08].entries()){
  A([x,1.439,-4.13],[.178,2.102,.188],'vertical','outer-column-'+i);
  A([x,.365,-4.13],[.216,.046,.224],'horizontal','column-seat-'+i);
 }
 A([cx,2.570,front],[5.05,.160,.220],'horizontal','front-bearing-beam');
 // Thick side returns, back wall and a recessed alcove make a room, not a card.
 A([1.31,1.487,-5.56],[.19,2.236,2.45],'vertical','left-return');A([6.13,1.487,-5.56],[.19,2.236,2.45],'plaster','right-return');
 for(const [i,x]of [1.33,6.10].entries())A([x,1.487,-4.25],[.10,2.236,.18],'vertical','column-return-'+i);
 // The wall crowns carry one continuous perimeter frame. Its modest embedded
 // lap closes the wall/ceiling section and joins the actual front/rear beams.
 A([1.31,2.622,-5.410],[.190,.104,2.750],'lengthwise','room-head-left');
 A([6.13,2.622,-5.410],[.190,.104,2.750],'lengthwise','room-head-right');
 A([cx,2.622,-6.640],[4.990,.104,.190],'horizontal','room-head-back');
 B([1.42,1.487,back],[.20,2.236,.19],'plaster');B([2.955,1.487,back],[.27,2.236,.19],'plaster');B([4.59,1.487,back],[3.00,2.236,.19],'plaster');B([2.17,2.53,back],[1.50,.27,.19],'plaster');
 B([2.17,.418,-6.32],[1.35,.108,.59],'horizontal');B([2.17,1.43,-6.67],[1.31,1.95,.044],'alcove');
 for(const x of [1.45,2.89])B([x,1.46,-6.30],[.088,2.02,.64],'vertical');B([2.17,2.425,-6.30],[1.59,.11,.67],'horizontal');
 // A second, narrow screen behind the open bay has actual rails and divisions.
 B([5.12,1.47,-6.48575],[1.29,2.08,.0005],'paper');
 for(const x of [4.43,5.81])B([x,1.46,-6.48],[.057,2.15,.052],'vertical');
 for(let i=0;i<5;i++)B([4.52+i*.30,1.47,-6.474],[.020,2.04,.023],'vertical');
 for(const y of [.44,1.10,1.77,2.49])B([5.12,y,-6.4725],[1.43,.025,.026],'horizontal');
 // The front roof load returns to the corner columns and four real ceiling beams.
 A([cx,2.687,-5.42],[5.07,.046,2.46],'horizontal','ceiling-panel');
 for(const [i,x]of [1.46,2.97,4.48,5.98].entries())A([x,2.612,-5.42],[.105,.104,2.46],'lengthwise','ceiling-beam-'+i);
 A([cx,2.750,-3.42],[5.72,.090,.110],'horizontal','eave-fascia');B([cx,2.797,-3.409],[5.77,.052,.037],'horizontal');
 A([cx,2.668,-4.160],[5.05,.036,.236],'horizontal','rafter-bearing-purlin');
 for(let i=0;i<25;i++)A([.87+i*.236,2.710,-4.06],[.063,.058,1.16],'lengthwise','main-rafter-'+i,.040);
 for(let i=0;i<13;i++)A([.87+i*.472,2.744,-3.69],[.056,.046,.54],'lengthwise','short-rafter-'+i,.040);
 // Continuous boarding closes the exposed roof section, without flattening the
 // two received rafter courses. Each underside sits on its actual pitched top.
 const slope=.040,mainBoardZ=-4.303,flyBoardZ=-3.686;
 const mainTopAt=z=>2.710+.058/(2*Math.cos(slope))-Math.tan(slope)*(z+4.06);
 const flyTopAt=z=>2.744+.046/(2*Math.cos(slope))-Math.tan(slope)*(z+3.69);
 A([cx,mainTopAt(mainBoardZ)+.014/(2*Math.cos(slope)),mainBoardZ],[5.72,.014,.710],'horizontal','soffit-main-boarding',slope);
 A([cx,flyTopAt(flyBoardZ)+.014/(2*Math.cos(slope)),flyBoardZ],[5.72,.014,.568],'horizontal','soffit-flying-boarding',slope);
 const seamZ=-3.958,seamBottom=mainTopAt(seamZ)+.012,seamTop=flyTopAt(seamZ)+.002;
 A([cx,(seamBottom+seamTop)/2,seamZ],[5.72,seamTop-seamBottom,.018],'horizontal','soffit-course-return');
 A([cx,2.731,-4.215],[5.07,.042,.064],'horizontal','soffit-inner-return');
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
 for(const [panelIndex,centre]of [3.25,4.37,5.49].entries()){
  const panelZ=panelIndex===1?-4.386:-4.320,width=1.146,bottom=.390,top=2.452,frame=.052,innerW=width-frame*2;
  const left=centre-width/2,right=centre+width/2;
  B([centre,bottom+.044,panelZ],[width,.088,.050],'horizontal');
  B([centre,top-.033,panelZ],[width,.066,.050],'horizontal');
  for(const x of [left+frame/2,right-frame/2])B([x,(bottom+top)/2+.011,panelZ],[frame,top-bottom-.132,.050],'vertical');
  const paperBottom=bottom+.088,paperTop=top-.066,height=paperTop-paperBottom,cy=(paperBottom+paperTop)/2;
  B([centre,cy,panelZ-.01225],[innerW+.005,height+.006,.0005],'paper');
  for(let col=1;col<3;col++)B([left+frame+innerW*col/3,cy,panelZ-.002],[.00845,height,.013],'vertical');
  for(let row=1;row<7;row++){
   const y=paperBottom+height*row/7;
   for(let col=0;col<3;col++)B([left+frame+innerW*(col+.5)/3,y,panelZ-.007],[innerW/3-.00585,.0078,.0065],'horizontal');
  }
  // Shallow recessed pull: timber recess and a dark, matte insert, no ornament.
  B([left+.053,1.27,panelZ+.029],[.028,.069,.004],'matBorder');
  shojiRows.push({centre:housePoint([centre,cy,panelZ]).toArray(),authoredPanelZ:panelZ,facadeRecessMetres:-4.085-panelZ,outerWidthMetres:width*HOUSE_X_SCALE,outerHeightMetres:top-bottom,paperThicknessMetres:.0005,frameThicknessMetres:.050,kumikoWidthMetres:.00845*HOUSE_X_SCALE,kumikoDepthMetres:.013,joinery:'Stopped rails with1mm joints; half-depth stepped kumiko crossing; paper meets rear face, not a glowing card'});
 }
 A([cx,.385,-4.345],[4.82,.040,.248],'horizontal','track-bottom-base');A([cx,2.459,-4.345],[4.83,.055,.248],'horizontal','track-top-base');
 // Low left boundary joins the pavilion return; it does not cross the room.
 housePhase=false;const rearZ=-4.96,boundaryStart=-13.16,leftFront=housePoint([1.31,0,-4.10]),leftBack=housePoint([1.31,0,-6.64]),boundaryEnd=leftFront.clone().lerp(leftBack,(rearZ-leftFront.z)/(leftBack.z-leftFront.z)).x-.084,length=boundaryEnd-boundaryStart,centre=(boundaryEnd+boundaryStart)/2;
 const tsuiji=tsuijiBoundary(batch,boundaryStart,boundaryEnd,rearZ,m.wallSurface);
 const part=name=>parts.find(p=>p.name===name),joins=[];
 const receive=(lower,upper)=>{const a=part(lower).localBounds,b=part(upper).localBounds;joins.push({lower,upper,verticalGapMetres:b.min[1]-a.max[1],xzOverlapMetres:[Math.min(a.max[0],b.max[0])-Math.max(a.min[0],b.min[0]),Math.min(a.max[2],b.max[2])-Math.max(a.min[2],b.min[2])]});};
 for(let i=0;i<5;i++){receive('stone-foot-'+i,'short-post-'+i);receive('short-post-'+i,'front-crossbeam');receive('front-crossbeam','longitudinal-joist-'+i);receive('rear-crossbeam','longitudinal-joist-'+i);}
 for(const [i,joistIndex]of [0,4].entries()){
  const seat=part('column-seat-'+i).localBounds;
  const board=parts.find(p=>p.name.startsWith('deck-board-')&&p.localBounds.min[0]<seat.min[0]&&p.localBounds.max[0]>seat.min[0]);
  receive('longitudinal-joist-'+joistIndex,board.name);receive(board.name,'column-seat-'+i);receive('column-seat-'+i,'outer-column-'+i);receive('outer-column-'+i,'front-bearing-beam');
 }
 receive('front-bearing-beam','rafter-bearing-purlin');for(let i=0;i<4;i++)receive('ceiling-beam-'+i,'ceiling-panel');
 const bearingSystem={parts,joins,loadPaths:[{column:'outer-column-0',sameXJoist:'longitudinal-joist-0',crossbeams:['front-crossbeam','rear-crossbeam'],frontPost:'short-post-0',frontStone:'stone-foot-0',authoredColumnZ:-4.13,frontPostZ:-3.72,frontPostXOffsetMetres:0},{column:'outer-column-1',sameXJoist:'longitudinal-joist-4',crossbeams:['front-crossbeam','rear-crossbeam'],frontPost:'short-post-4',frontStone:'stone-foot-4',authoredColumnZ:-4.13,frontPostZ:-3.72,frontPostXOffsetMetres:-.030*HOUSE_X_SCALE}],measurement:'Bounds measured from actual produced Float32 geometry after world transform and inverse house matrix; unpitched seating gap and XZ footprint intersections only. Bevels, pitched rafter faces and Boolean joint cuts are not certified by these bounds. This is not a structural stress analysis.',plannedDeckToTatamiStepMetres:.034,mainRafterCount:25,shortRafterCount:13,deckBoardCount:28,soffitAssembly:{cause:'Continuous stepped boarding closes eave section exposed by ceiling setback',mainBoardZRange:[-4.658,-3.948],flyingBoardZRange:[-3.970,-3.402],boardingThicknessMetres:.014,support:'Lower faces match actual tilted top planes of25 main and13 short rafters;18mm course return connects the stepped sheets; inner return reaches the ceiling panel',angledContactsQualification:'Analytic produced-box face planes with bevel allowance, not Boolean cuts or stress analysis'}};
 const actual=name=>part(name).localBounds;
 const closurePieces=['left-return','right-return','room-head-left','room-head-right','room-head-back','front-bearing-beam','rafter-bearing-purlin','ceiling-panel','soffit-main-boarding','soffit-flying-boarding','soffit-course-return','soffit-inner-return'];
 bearingSystem.enclosure={version:'continuous-perimeter-frame-v02',localToWorld:HOUSE_MATRIX.toArray(),parts:closurePieces.map(name=>({name,bounds:actual(name)})),support:'104mm continuous side/back timber frame embeds35mm into the real wall crowns, meets front beam and receives ceiling with10mm lap.36mm existing front purlin deepens inward to receive the ceiling front edge; no detached invisible occluder.',qualification:'Measured actual produced Float32 bounds. Pixel/room triangle closure rays are recorded separately; Boolean mortises and stress analysis are not certified.',nominalWallTop:2.605,nominalWallBottom:.369,wallToFloorBorderLapMetres:.005,nominalCeilingUnderside:2.664,nominalWallHeadEmbed:.035,nominalCeilingHeadLap:.010};
 return {...batch.done(),bearingSystem,version:'pavilion-enclosure-v02',tsuiji,houseYaw:HOUSE_YAW,frontEdge:housePoint([cx,.30,-3.49]).toArray(),deckTop:.342,interiorFloorTop:.376,verandaSupportContacts:contacts,roomOpening:{front:housePoint([1.42,1.50,-4.10]).toArray(),rear:housePoint([6.0,1.50,-4.10]).toArray(),yMin:.402,yMax:2.448},layers:['235/301mm recessed front shoji with two staggered tracks','160mm front bearing beam on two actual178mm authored columns','continuous28mm veranda boards on same-X longitudinal joists and two crossbeams','2.54m recessed room with side returns/alcove/screen','34mm rise from veranda to tatami','buried stone feet and159mm short posts','25 pitched main rafters and13 short flying rafters received on36mm purlin; tiled roof outline held'],rearBoundaryZ:rearZ,rearBoundaryEndX:boundaryEnd,roomIntersectionAvoided:true,rearBoundaryHeightMetres:2.321,frontShoji:shojiRows,nearOpenBayWidthMetres:(2.69-1.42)*HOUSE_X_SCALE,boundaryContactSamples:[-10.64,-8.28,-5.92,-3.56,-1.20,1.16,boundaryEnd-.02].map(x=>({x,z:rearZ,groundY:groundHeight(x,rearZ),foundationBottom:-.045,foundationBurial:groundHeight(x,rearZ)+.045}))};
}
