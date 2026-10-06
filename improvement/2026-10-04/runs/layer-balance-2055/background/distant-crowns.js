import * as THREE from 'three';
import {branch,random} from './garden-geometry.js';
// Each unequal crown is composed of multiple woody axes with irregular fan
// branches filling front and back. Nothing fills a sphere or uses a billboard.
const specimens=[{"name":"Layered garden tree in middle distance","origin":[-3.35,-5.65],"spine":[[0,0.0,0],[0.12,0.624338,0.03],[0.02,1.312168,0.06],[0.15,1.9894159999999999,-0.1],[0.23,2.740738,-0.03],[0.15,3.322748,0.04]],"regions":[{"t":0.25,"spine":[[-0.27,0.9735440000000001,0.15],[-0.65,1.1957659999999999,0.29],[-0.99,1.417988,0.3]],"reach":[0.8304839999999999,0.5285228000000001,0.6210900000000001],"lean":-0.18},{"t":0.34,"spine":[[0.31,1.2698399999999999,0.06],[0.68,1.5026439999999999,-0.05],[0.92,1.619046,0.09]],"reach":[0.8586359999999998,0.5800860000000001,0.703902],"lean":0.14},{"t":0.47,"spine":[[-0.18,1.7248659999999998,0.21],[-0.44,1.9999979999999997,0.54],[-0.67,2.1164,0.58]],"reach":[0.8867879999999999,0.6316492,0.6901],"lean":-0.09},{"t":0.55,"spine":[[0.36,1.9894159999999999,-0.07],[0.57,2.1798919999999997,-0.36],[0.87,2.3068760000000004,-0.39]],"reach":[0.8164079999999999,0.6574308000000001,0.6762980000000001],"lean":0.19},{"t":0.66,"spine":[[-0.1,2.3068760000000004,-0.16],[-0.34,2.5820079999999996,-0.45],[-0.63,2.6984099999999995,-0.49]],"reach":[0.84456,0.5671952,0.607288],"lean":-0.16},{"t":0.75,"spine":[[0.29,2.613754,0.19],[0.45,2.835976,0.4],[0.46,3.0370340000000002,0.34]],"reach":[0.6897239999999999,0.6187583999999999,0.662496],"lean":0.13},{"t":0.87,"spine":[[0.09,3.0581980000000004,0.11],[-0.07,3.28042,0.2],[-0.07,3.407404,0.07]],"reach":[0.577116,0.46406879999999995,0.5934860000000001],"lean":-0.11}]},{"name":"Rear inclined tree above boundary","origin":[0.55,-7.25],"spine":[[0,0.0,0],[-0.09,0.9070600000000001,0.03],[0.1,1.8612400000000002,0.12],[0.04,2.5916,0.04],[0.16,3.4397599999999997,-0.12],[0.09,4.07588,-0.06]],"regions":[{"t":0.39,"spine":[[-0.25,1.84946,0.1],[-0.53,2.0968400000000003,0.24],[-0.82,2.34422,0.3]],"reach":[0.6658560000000001,0.5692856000000001,0.5934860000000001],"lean":-0.16},{"t":0.49,"spine":[[0.32,2.3088800000000003,-0.06],[0.58,2.45024,-0.28],[0.78,2.6151600000000004,-0.27]],"reach":[0.7572479999999999,0.5163288,0.6762980000000001],"lean":0.17},{"t":0.6,"spine":[[-0.12,2.6505,-0.13],[-0.44,2.945,-0.27],[-0.57,3.2041600000000003,-0.45]],"reach":[0.691968,0.6619600000000001,0.5934860000000001],"lean":-0.12},{"t":0.68,"spine":[[0.35,3.0628,0.19],[0.64,3.32196,0.33],[0.85,3.49866,0.36]],"reach":[0.58752,0.5163288,0.607288],"lean":0.16},{"t":0.77,"spine":[[-0.08,3.3337400000000006,0.19],[-0.3,3.55756,0.41],[-0.36,3.81672,0.35]],"reach":[0.561408,0.5428072,0.6348920000000001],"lean":-0.1},{"t":0.87,"spine":[[0.16,3.6871400000000003,-0.05],[0.39,4.0052,-0.19],[0.46,4.09944,-0.16]],"reach":[0.561408,0.4766112000000001,0.524476],"lean":0.16}]},{"name":"Quiet distant tree behind the far pavilion","origin":[5.8,-5.9],"spine":[[0.0,0.0,0.0],[0.1008,1.0431190000000001,0.0348],[-0.11200000000000002,2.140426,0.1392],[-0.044800000000000006,2.98034,0.0464],[-0.17920000000000003,3.9557239999999996,-0.1392],[-0.1008,4.687262,-0.0696]],"regions":[{"t":0.39,"spine":[[0.28,2.1268789999999997,0.11599999999999999],[0.5936000000000001,2.411366,0.2784],[0.9184,2.6958529999999996,0.348]],"reach":[0.5792947200000002,0.5294356080000001,0.6350300200000001],"lean":0.16},{"t":0.6,"spine":[[0.13440000000000002,3.048075,-0.1508],[0.49280000000000007,3.3867499999999997,-0.3132],[0.6384,3.684784,-0.522]],"reach":[0.60201216,0.6156228000000001,0.6350300200000001],"lean":0.12},{"t":0.68,"spine":[[-0.392,3.52222,0.22039999999999998],[-0.7168000000000001,3.8202539999999994,0.3828],[-0.9520000000000001,4.023459,0.41759999999999997]],"reach":[0.5992704000000001,0.48018578400000006,0.6497981600000001],"lean":-0.16},{"t":0.77,"spine":[[0.08960000000000001,3.8338010000000002,0.22039999999999998],[0.336,4.091194,0.4755999999999999],[0.4032,4.389228,0.40599999999999997]],"reach":[0.48842496,0.5048106960000001,0.6793344400000002],"lean":0.1},{"t":0.87,"spine":[[-0.17920000000000003,4.240211,-0.057999999999999996],[-0.4368000000000001,4.60598,-0.22039999999999998],[-0.5152000000000001,4.714356,-0.1856]],"reach":[0.5726361600000001,0.44324841600000014,0.5611893200000001],"lean":-0.16}]}];
export function distantCrowns(groundHeight){
 const rng=random(881327),wood=[],shoots=[],roots=[],rows=[],up=new THREE.Vector3(0,1,0);
 const add=(ps,r0,r1,steps=5,radial=5)=>{const b=branch(ps.map(p=>p.toArray()),r0,r1,steps,radial);wood.push(b.g);return b;};
 for(const [si,s]of specimens.entries()){
  const [x,z]=s.origin,base=new THREE.Vector3(x,groundHeight(x,z)-.005,z),at=p=>new THREE.Vector3(...p).add(base),begin=shoots.length;
  const trunk=add(s.spine.map(at),si===2?.070:.045,si===2?.005:.0035,20,7);roots.push({name:s.name,position:base.toArray()});const regions=[];
  s.regions.forEach((r,k)=>{
   const support=add([trunk.path.getPoint(r.t),...r.spine.map(at)],.016-k*.002,.0021,10,6),centre=support.path.getPoint(1),beginRegion=shoots.length;
   const radius=new THREE.Vector3(r.reach[0],r.reach[1],r.reach[2]),targets=[];
   for(let q=0;q<[158,203,174,224,147,180,139][(k+si*2)%7];q++){
    const theta=rng()*Math.PI*2,zeta=rng()*2-1,flat=Math.sqrt(1-zeta*zeta),radial=Math.pow(rng(),.39),lobe=1+.11*Math.sin(theta*3+si*.9)+.09*Math.cos(theta*5+zeta*3+k);
    const v=new THREE.Vector3(Math.cos(theta)*flat, zeta,Math.sin(theta)*flat).multiply(radius).multiplyScalar(radial*lobe);
    v.x+=v.y*r.lean;v.z+=.055*Math.sin(v.y*9+theta);targets.push(centre.clone().add(v));
   }
   const nodes=[.25,.45,.65,.82,1].map(t=>({p:support.path.getPoint(t),parent:-1,children:0})),remaining=targets.slice();
   // Each endpoint guides the nearest existing twig. Growth divides naturally
   // toward different endpoints instead of repeating a mirrored fan or shelf.
   for(let pass=0;pass<76&&remaining.length;pass++){
    const directions=new Map();
    for(let t=remaining.length-1;t>=0;t--){
     const target=remaining[t];let nearest=-1,best=.65*.65;
     for(let n=0;n<nodes.length;n++){const d=nodes[n].p.distanceToSquared(target);if(d<best){best=d;nearest=n;}}
     if(nearest<0)continue;
     if(best<.044*.044){remaining.splice(t,1);continue;}
     const row=directions.get(nearest)||{sum:new THREE.Vector3(),count:0};row.sum.add(target.clone().sub(nodes[nearest].p).normalize());row.count++;directions.set(nearest,row);
    }
    if(!directions.size)break;
    let added=0;
    for(const [parent,{sum}]of directions){
     const dir=sum.normalize(),length=.050+.015*rng(),pos=nodes[parent].p.clone().addScaledVector(dir,length);
     if(nodes.some(n=>n.p.distanceToSquared(pos)<.017*.017))continue;
     nodes[parent].children++;nodes.push({p:pos,parent,children:0});added++;
    }
    if(!added)break;
   }
   for(let n=0;n<nodes.length;n++){
    if(nodes[n].parent<0)continue;
    const node=nodes[n],a=nodes[node.parent].p,b=node.p,axis=b.clone().sub(a).normalize(),side=new THREE.Vector3().crossVectors(axis,up);if(side.lengthSq()<.02)side.set(1,0,0);side.normalize();
    const twig=add([a,a.clone().lerp(b,.50).addScaledVector(up,.003),b],node.children?.0012:.00075,.00030,2,3);
    // Leaves occupy the growing interior as well as the outer tips. Leaf bases
    // are exact points on this twig; no detached floating leaf cloud.
    const count=node.children?(n%4===0?2:3):(n%5===0?5:6);
    for(let bud=0;bud<count;bud++){
     const t=.14+(bud+.1)/(count+.2)*.80,origin=twig.path.getPoint(t),hand=(n+bud+k)%2?-1:1;
     const dir=axis.clone().multiplyScalar(.29+.20*rng()).addScaledVector(side,hand*(.54+.29*rng())).addScaledVector(up,.12+.35*rng()).normalize(),size=(node.children?.090:.106)*(.79+.35*rng());
     shoots.push({p:origin,direction:dir,length:size,width:.82+.30*rng(),roll:(rng()-.5)*1.44,shade:.85+.19*rng()});
    }
   }
   // Short, physical secondary twigs fill the supporting axis interior.
   // Their paired leaves stay on these twigs; outer tips remain unequal.
   for(const [j,t]of [.13,.24,.33,.43,.56,.62,.73,.86,.94].entries()){
    const a=support.path.getPoint(t),axis=support.path.getTangent(t),side=new THREE.Vector3().crossVectors(axis,up).normalize(),hand=(j+k)%2?1:-1;
    const tip=a.clone().addScaledVector(axis,.13).addScaledVector(side,hand*(.13+.035*rng())).addScaledVector(up,.05);
    const twig=add([a,a.clone().lerp(tip,.49).addScaledVector(up,.013),tip],.0015,.0004,3,4);
    for(let leaf=0;leaf<8;leaf++){
     const base=twig.path.getPoint(.12+leaf*.11),sign=leaf%2?1:-1,dir=axis.clone().multiplyScalar(.38).addScaledVector(side,sign*.65).addScaledVector(up,.29).normalize();
     shoots.push({p:base,direction:dir,length:.072*(.86+.20*rng()),width:.90+.22*rng(),roll:(rng()-.5)*1.22,shade:.86+.16*rng()});
    }
   }
   regions.push({centre:centre.toArray(),halfExtents:radius.toArray(),supportingAxis:r.spine,attractionEndpoints:targets.length,unreachedEndpoints:remaining.length,growingNodes:nodes.length,closedLeaves:shoots.length-beginRegion});
  });
  for(let n=begin;n<shoots.length;n++)shoots[n].specimen='distant-tree-'+si;
  rows.push({name:s.name,origin:s.origin,primaryAxes:s.regions.length,regions,closedLeaves:shoots.length-begin});
 }
 return {wood,shoots,roots,metadata:{version:'unequal-twig-leaf-distribution-v21',strategy:'Unequal overlapping crown regions contain physical endpoint-guided branching and attached closed leaves throughout their depth; no mirrored fans, spheres or cards',specimens:rows,instances:shoots.length}};
}
