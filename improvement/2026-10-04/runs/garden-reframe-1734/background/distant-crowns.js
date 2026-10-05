import * as THREE from 'three';
import {branch,random} from './garden-geometry.js';
// Each unequal crown is composed of multiple woody axes with irregular fan
// branches filling front and back. Nothing fills a sphere or uses a billboard.
const specimens=[{"name":"Layered garden tree in middle distance","origin":[-3.55,-3.80],"spine":[[0,0.0,0],[0.12,0.4366,0.03],[0.02,0.9176,0.06],[0.15,1.3912,-0.1],[0.23,1.9165999999999999,-0.03],[0.15,2.3236,0.04]],"regions":[{"t":0.25,"spine":[[-0.27,0.6808000000000001,0.15],[-0.65,0.8361999999999999,0.29],[-0.99,0.9916,0.3]],"reach":[0.8141999999999999,0.39442,0.6030000000000001],"lean":-0.18},{"t":0.34,"spine":[[0.31,0.888,0.06],[0.68,1.0508,-0.05],[0.92,1.1322,0.09]],"reach":[0.8417999999999999,0.43290000000000006,0.6834],"lean":0.14},{"t":0.47,"spine":[[-0.18,1.2062,0.21],[-0.44,1.3985999999999998,0.54],[-0.67,1.48,0.58]],"reach":[0.8694,0.47137999999999997,0.67],"lean":-0.09},{"t":0.55,"spine":[[0.36,1.3912,-0.07],[0.57,1.5244,-0.36],[0.87,1.6132000000000002,-0.39]],"reach":[0.8003999999999999,0.49062000000000006,0.6566000000000001],"lean":0.19},{"t":0.66,"spine":[[-0.1,1.6132000000000002,-0.16],[-0.34,1.8055999999999999,-0.45],[-0.63,1.8869999999999998,-0.49]],"reach":[0.828,0.42328,0.5896],"lean":-0.16},{"t":0.75,"spine":[[0.29,1.8278,0.19],[0.45,1.9832,0.4],[0.46,2.1238,0.34]],"reach":[0.6761999999999999,0.46175999999999995,0.6432],"lean":0.13},{"t":0.87,"spine":[[0.09,2.1386000000000003,0.11],[-0.07,2.294,0.2],[-0.07,2.3828,0.07]],"reach":[0.5658,0.34631999999999996,0.5762],"lean":-0.11}]},{"name":"Rear inclined tree above boundary","origin":[1.40,-6.80],"spine":[[0,0.0,0],[-0.09,0.5852,0.03],[0.1,1.2008,0.12],[0.04,1.6720000000000002,0.04],[0.16,2.2192,-0.12],[0.09,2.6296,-0.06]],"regions":[{"t":0.39,"spine":[[-0.25,1.1932,0.1],[-0.53,1.3528,0.24],[-0.82,1.5124,0.3]],"reach":[0.6528,0.42484,0.5762],"lean":-0.16},{"t":0.49,"spine":[[0.32,1.4896,-0.06],[0.58,1.5808,-0.28],[0.78,1.6872000000000003,-0.27]],"reach":[0.7424,0.38532,0.6566000000000001],"lean":0.17},{"t":0.6,"spine":[[-0.12,1.71,-0.13],[-0.44,1.9,-0.27],[-0.57,2.0672,-0.45]],"reach":[0.6784,0.49400000000000005,0.5762],"lean":-0.12},{"t":0.68,"spine":[[0.35,1.9760000000000002,0.19],[0.64,2.1431999999999998,0.33],[0.85,2.2572,0.36]],"reach":[0.5760000000000001,0.38532,0.5896],"lean":0.16},{"t":0.77,"spine":[[-0.08,2.1508000000000003,0.19],[-0.3,2.2952,0.41],[-0.36,2.4624,0.35]],"reach":[0.5504,0.40508,0.6164000000000001],"lean":-0.1},{"t":0.87,"spine":[[0.16,2.3788,-0.05],[0.39,2.584,-0.19],[0.46,2.6448,-0.16]],"reach":[0.5504,0.35568000000000005,0.5092],"lean":0.16}]}];
export function distantCrowns(groundHeight){
 const rng=random(881327),wood=[],shoots=[],roots=[],rows=[],up=new THREE.Vector3(0,1,0);
 const add=(ps,r0,r1,steps=5,radial=5)=>{const b=branch(ps.map(p=>p.toArray()),r0,r1,steps,radial);wood.push(b.g);return b;};
 for(const [si,s]of specimens.entries()){
  const [x,z]=s.origin,base=new THREE.Vector3(x,groundHeight(x,z)-.005,z),at=p=>new THREE.Vector3(...p).add(base),begin=shoots.length;
  const trunk=add(s.spine.map(at),.045,.0035,20,7);roots.push({name:s.name,position:base.toArray()});const regions=[];
  s.regions.forEach((r,k)=>{
   const support=add([trunk.path.getPoint(r.t),...r.spine.map(at)],.016-k*.002,.0021,10,6),centre=support.path.getPoint(1),beginRegion=shoots.length;
   const radius=new THREE.Vector3(r.reach[0],r.reach[1],r.reach[2]),targets=[];
   for(let q=0;q<190+(k%3)*24;q++){
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
    const count=node.children?5:8;
    for(let bud=0;bud<count;bud++){
     const t=.14+(bud+.1)/(count+.2)*.80,origin=twig.path.getPoint(t),hand=(n+bud+k)%2?-1:1;
     const dir=axis.clone().multiplyScalar(.29+.20*rng()).addScaledVector(side,hand*(.54+.29*rng())).addScaledVector(up,.12+.35*rng()).normalize(),size=(node.children?.052:.064)*(.84+.29*rng());
     shoots.push({p:origin,direction:dir,length:size,width:.82+.30*rng(),roll:(rng()-.5)*1.44,shade:.85+.19*rng()});
    }
   }
   regions.push({centre:centre.toArray(),halfExtents:radius.toArray(),supportingAxis:r.spine,attractionEndpoints:targets.length,unreachedEndpoints:remaining.length,growingNodes:nodes.length,closedLeaves:shoots.length-beginRegion});
  });
  rows.push({name:s.name,origin:s.origin,primaryAxes:s.regions.length,regions,closedLeaves:shoots.length-begin});
 }
 return {wood,shoots,roots,metadata:{version:'pavilion-layered-v01',strategy:'Unequal overlapping crown regions contain physical endpoint-guided branching and attached closed leaves throughout their depth; no mirrored fans, spheres or cards',specimens:rows,instances:shoots.length}};
}
