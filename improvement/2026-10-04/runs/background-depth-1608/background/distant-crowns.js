import * as THREE from 'three';
import {branch,random} from './garden-geometry.js';
// Each unequal crown is composed of multiple woody axes with irregular fan
// branches filling front and back. Nothing fills a sphere or uses a billboard.
const specimens=[
 {name:'Near cedar compound crown',origin:[-3.42,-8.3],spine:[[0,0,0],[.09,.76,0],[.10,1.42,.04],[.04,2.07,.08],[.17,2.65,.11],[.11,2.99,.03]],regions:[
  {t:.45,spine:[[-.29,1.62,.16],[-.57,1.91,.18],[-.81,2.08,.20]],reach:[.49,.34,.39],sides:11,lean:-.24},
  {t:.62,spine:[[.26,2.05,-.05],[.52,2.37,-.20],[.76,2.44,-.14]],reach:[.55,.45,.42],sides:13,lean:.17},
  {t:.81,spine:[[-.05,2.58,.15],[-.07,2.88,.23],[.02,3.03,.12]],reach:[.45,.38,.38],sides:12,lean:-.12}]},
 {name:'Far cedar inclined crown',origin:[-.15,-11.15],spine:[[0,0,0],[-.03,.94,.04],[.04,1.68,.12],[-.07,2.33,.03],[.03,2.95,-.08],[-.06,3.33,-.01]],regions:[
  {t:.53,spine:[[-.22,2.00,.13],[-.52,2.44,.31],[-.76,2.61,.27]],reach:[.48,.35,.43],sides:10,lean:.18},
  {t:.66,spine:[[.25,2.40,-.15],[.58,2.63,-.27],[.85,2.77,-.21]],reach:[.57,.44,.38],sides:12,lean:-.20},
  {t:.77,spine:[[-.21,2.81,-.13],[-.48,3.04,-.36],[-.54,3.16,-.42]],reach:[.32,.30,.37],sides:9,lean:-.10},
  {t:.87,spine:[[-.06,3.02,.06],[-.10,3.30,.24],[-.02,3.40,.17]],reach:[.44,.37,.42],sides:11,lean:.22}]}
];
export function distantCrowns(groundHeight){
 const rng=random(881327),wood=[],shoots=[],roots=[],rows=[],up=new THREE.Vector3(0,1,0);
 const add=(ps,r0,r1,steps=5,radial=5)=>{const b=branch(ps.map(p=>p.toArray()),r0,r1,steps,radial);wood.push(b.g);return b;};
 for(const [si,s]of specimens.entries()){
  const [x,z]=s.origin,base=new THREE.Vector3(x,groundHeight(x,z)-.005,z),at=p=>new THREE.Vector3(...p).add(base),begin=shoots.length;
  const trunk=add(s.spine.map(at),.045,.0035,20,7);roots.push({name:s.name,position:base.toArray()});const regions=[];
  s.regions.forEach((r,k)=>{
   const support=add([trunk.path.getPoint(r.t),...r.spine.map(at)],.016-k*.002,.0021,10,6),centre=support.path.getPoint(1),beginRegion=shoots.length;
   const radius=new THREE.Vector3(r.reach[0]*1.18,r.reach[1]*1.33,r.reach[2]*1.25),targets=[];
   for(let q=0;q<118+(k%2)*24;q++){
    const theta=rng()*Math.PI*2,zeta=rng()*2-1,flat=Math.sqrt(1-zeta*zeta),radial=Math.pow(rng(),.39),lobe=1+.11*Math.sin(theta*3+si*.9)+.09*Math.cos(theta*5+zeta*3+k);
    const v=new THREE.Vector3(Math.cos(theta)*flat, zeta,Math.sin(theta)*flat).multiply(radius).multiplyScalar(radial*lobe);
    v.x+=v.y*r.lean;v.z+=.055*Math.sin(v.y*9+theta);targets.push(centre.clone().add(v));
   }
   const seed=centre.clone().add(new THREE.Vector3(-r.lean*.13,-.13,.018)),root=add([support.path.getPoint(.73),support.path.getPoint(.90),seed],.0026,.0016,4,4);
   const nodes=[{p:seed,parent:-1,children:0}],remaining=targets.slice();
   // Each endpoint guides the nearest existing twig. Growth divides naturally
   // toward different endpoints instead of repeating a mirrored fan or shelf.
   for(let pass=0;pass<76&&remaining.length;pass++){
    const directions=new Map();
    for(let t=remaining.length-1;t>=0;t--){
     const target=remaining[t];let nearest=-1,best=.53*.53;
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
   for(let n=1;n<nodes.length;n++){
    const node=nodes[n],a=nodes[node.parent].p,b=node.p,axis=b.clone().sub(a).normalize(),side=new THREE.Vector3().crossVectors(axis,up);if(side.lengthSq()<.02)side.set(1,0,0);side.normalize();
    const twig=add([a,a.clone().lerp(b,.50).addScaledVector(up,.003),b],node.children?.0012:.00075,.00030,2,3);
    // Leaves occupy the growing interior as well as the outer tips. Leaf bases
    // are exact points on this twig; no detached floating leaf cloud.
    const count=node.children?3:5;
    for(let bud=0;bud<count;bud++){
     const t=.14+(bud+.1)/(count+.2)*.80,origin=twig.path.getPoint(t),hand=(n+bud+k)%2?-1:1;
     const dir=axis.clone().multiplyScalar(.29+.20*rng()).addScaledVector(side,hand*(.54+.29*rng())).addScaledVector(up,.12+.35*rng()).normalize(),size=(node.children?.073:.087)*(.84+.29*rng());
     shoots.push({p:origin,direction:dir,length:size,width:.82+.30*rng(),roll:(rng()-.5)*1.44,shade:.85+.19*rng()});
    }
   }
   regions.push({centre:centre.toArray(),halfExtents:radius.toArray(),supportingAxis:r.spine,attractionEndpoints:targets.length,unreachedEndpoints:remaining.length,growingNodes:nodes.length,closedLeaves:shoots.length-beginRegion});
  });
  rows.push({name:s.name,origin:s.origin,primaryAxes:s.regions.length,regions,closedLeaves:shoots.length-begin});
 }
 return {wood,shoots,roots,metadata:{version:'depth-v04',strategy:'Unequal overlapping crown regions contain physical endpoint-guided branching and attached closed leaves throughout their depth; no mirrored fans, spheres or cards',specimens:rows,instances:shoots.length}};
}
