import {selectedSettings} from './selected-settings.js';
import {backgroundShadowFilter} from './m17-procedural-detail.js';
import {distantCrowns} from './m21-distant-crowns.js';
import {evergreenTemplates,installEvergreenShoots} from './m22-broadleaf-support.js';
import * as THREE from 'three';
import terrainDesign from './m23-terrain-design.json';
import {RoundedBoxGeometry} from 'three/addons/geometries/RoundedBoxGeometry.js';
import {mergeGeometries,mergeVertices} from 'three/addons/utils/BufferGeometryUtils.js';

export function random(seed=7241){let s=seed;return ()=>{s=(Math.imul(s,1664525)+1013904223)>>>0;return s/4294967296;};}
export function batches(scene,materials){
 const groups=new Map();
 const add=(geometry,material)=>{
  if(!geometry.getAttribute('grainPosition'))geometry.setAttribute('grainPosition',geometry.attributes.position.clone());
  if(!geometry.getAttribute('grainNormal'))geometry.setAttribute('grainNormal',geometry.attributes.normal.clone());
  if(!geometry.getAttribute('boardSeed'))geometry.setAttribute('boardSeed',new THREE.Float32BufferAttribute(new Float32Array(geometry.attributes.position.count).fill(.5),1));
  if(!groups.has(material))groups.set(material,[]);groups.get(material).push(geometry.index?geometry.toNonIndexed():geometry);
 };
 const box=(p,size,key,angle=0,yaw=0)=>{
  const g=new RoundedBoxGeometry(...size,1,Math.min(.002,...size.map(v=>v*.055)));
  g.setAttribute('grainPosition',g.attributes.position.clone());g.setAttribute('grainNormal',g.attributes.normal.clone());
  const seed=((Math.sin(p[0]*23.71+p[1]*17.17+p[2]*39.03)*43758.5)%1+1)%1;
  g.setAttribute('boardSeed',new THREE.Float32BufferAttribute(new Float32Array(g.attributes.position.count).fill(seed),1));
  g.rotateZ(angle);g.rotateY(yaw);g.translate(...p);add(g,key);
 };
 const done=()=>{let triangles=0;for(const [key,gs]of groups){const g=mergeGeometries(gs,false);const mesh=new THREE.Mesh(g,materials[key]);mesh.name='Garden architecture '+key;mesh.castShadow=mesh.receiveShadow=true;scene.add(mesh);triangles+=g.attributes.position.count/3;gs.forEach(x=>x.dispose());}return {drawCalls:groups.size,triangles};};
 return {add,box,done};
}
let terrainPixels=null,terrainWidth=0,terrainHeight=0,dataFromBuffer=false;
export function setGroundField(image){
 if(image.data){dataFromBuffer=true;terrainPixels=image.data;terrainWidth=image.width;terrainHeight=image.height;if(terrainWidth!==terrainDesign.size||terrainHeight!==terrainDesign.size)throw Error('Spatial terrain dimensions changed');return;}
 const canvas=document.createElement('canvas');canvas.width=image.width;canvas.height=image.height;
 const ctx=canvas.getContext('2d',{willReadFrequently:true});ctx.drawImage(image,0,0);
 const data=ctx.getImageData(0,0,canvas.width,canvas.height);terrainPixels=data.data;terrainWidth=canvas.width;terrainHeight=canvas.height;
 if(terrainWidth!==terrainDesign.size||terrainHeight!==terrainDesign.size)throw Error('Ground field dimensions changed');
}
function fieldHeight(x,z){
 if(!terrainPixels)return terrainDesign.baseY;
 const [xmin,zmin,xmax,zmax]=terrainDesign.domain;
 const u=THREE.MathUtils.clamp((x-xmin)/(xmax-xmin)*terrainWidth-.5,0,terrainWidth-1),v=THREE.MathUtils.clamp((dataFromBuffer?z-zmin:zmax-z)/(zmax-zmin)*terrainHeight-.5,0,terrainHeight-1);
 const i=Math.floor(u),j=Math.floor(v),a=u-i,b=v-j;
 const h=(i,j)=>terrainPixels[(Math.min(j,terrainHeight-1)*terrainWidth+Math.min(i,terrainWidth-1))*4+2]/255;
 const rise=(1-b)*THREE.MathUtils.lerp(h(i,j),h(i+1,j),a)+b*THREE.MathUtils.lerp(h(i,j+1),h(i+1,j+1),a);
 return terrainDesign.baseY+rise*terrainDesign.heightScale;
}
function gridSegments(parts){
 const values=[];for(const [start,end,step]of parts){const n=Math.ceil((end-start)/step);for(let i=0;i<n;i++)values.push(start+(end-start)*i/n);}values.push(parts.at(-1)[1]);return values;
}
const groundX=gridSegments([[-6,-4,.20],[-4,-.62,.035],[-.62,6,.18]]),groundZ=gridSegments([[-7,-3.7,.20],[-3.7,3,.035],[3,7,.20]]);
function groundCell(values,x){let lo=0,hi=values.length-1;while(hi-lo>1){const mid=(lo+hi)>>1;if(values[mid]>x)hi=mid;else lo=mid;}return Math.min(lo,values.length-2);}
export function groundHeight(x,z){
 if(x<groundX[0]||x>groundX.at(-1)||z<groundZ[0]||z>groundZ.at(-1))return -.029;
 const i=groundCell(groundX,x),j=groundCell(groundZ,z),x0=groundX[i],x1=groundX[i+1],z0=groundZ[j],z1=groundZ[j+1],u=(x-x0)/(x1-x0),v=(z-z0)/(z1-z0);
 const a=fieldHeight(x0,z0),b=fieldHeight(x1,z0),c=fieldHeight(x0,z1),d=fieldHeight(x1,z1);
 return u+v<=1?a+u*(b-a)+v*(c-a):d+(1-u)*(c-d)+(1-v)*(b-d);
}
export function groundGeometry(){
 const positions=[],uv=[],indices=[],nx=groundX.length-1,nz=groundZ.length-1;
 for(let j=0;j<=nz;j++)for(let i=0;i<=nx;i++){const x=groundX[i],z=groundZ[j];positions.push(x,fieldHeight(x,z),z);uv.push((x+6)/12,(z+7)/14);}
 for(let j=0;j<nz;j++)for(let i=0;i<nx;i++){const a=j*(nx+1)+i,b=a+1,c=a+nx+1,d=c+1;indices.push(a,c,b,b,c,d);}
 const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(positions,3));g.setAttribute('uv',new THREE.Float32BufferAttribute(uv,2));g.setIndex(indices);g.computeVertexNormals();return g;
}
export function stoneGeometry(center,scale,seed){
 const g=new THREE.IcosahedronGeometry(1,6);const p=g.attributes.position;
 for(let i=0;i<p.count;i++){
  let x=p.getX(i),y=p.getY(i),z=p.getZ(i);
  const f=1+.085*Math.sin(x*6.4+z*4.7+seed)+.065*Math.cos(y*7.1-z*3.7+seed*.7)+.045*Math.sin(z*10.4+x*4.);
  x*=f;y*=1+.065*Math.sin(x*4+z*8+seed);z*=f;
  // A few broad weathered fracture faces, retaining the existing buried footprint.
  for(const [nx,ny,nz,limit]of [[.14,1.,.18,.67],[.68,.16,.72,.92],[-.77,.22,.31,.94],[.12,.09,-1.,.92],[-.29,.13,.94,.90]]){
   const dot=nx*x+ny*y+nz*z;if(dot>limit){const clip=limit/dot;x*=clip;y*=clip;z*=clip;}
  }
  p.setXYZ(i,x*scale[0]+center[0]+y*.07,y*scale[1]+center[1],z*scale[2]+center[2]);
 }
 g.deleteAttribute('normal');g.deleteAttribute('uv');const welded=mergeVertices(g,1e-5);welded.computeVertexNormals();return welded;
}
export function branch(points,r0,r1,steps=13,radial=7){
 const path=new THREE.CatmullRomCurve3(points.map(p=>new THREE.Vector3(...p))),frames=path.computeFrenetFrames(steps,false);const ps=[],indices=[];
 for(let j=0;j<=steps;j++){
  const t=j/steps,c=path.getPoint(t),radius=THREE.MathUtils.lerp(r0,r1,Math.pow(t,.82));
  for(let i=0;i<radial;i++){const a=i/radial*Math.PI*2,variation=1+.11*Math.cos(a*3+j*.29)+.05*Math.sin(a*5-j*.4);const q=c.clone().addScaledVector(frames.normals[j],Math.cos(a)*radius*variation).addScaledVector(frames.binormals[j],Math.sin(a)*radius*variation*.91);ps.push(...q);}
 }
 for(let j=0;j<steps;j++)for(let i=0;i<radial;i++){const a=j*radial+i,b=j*radial+(i+1)%radial,c=a+radial,d=b+radial;indices.push(a,b,c,b,d,c);}
 const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(ps,3));g.setIndex(indices);g.computeVertexNormals();g.setAttribute('uv',new THREE.Float32BufferAttribute(new Float32Array(ps.length/3*2),2));return {g,path};
}
export function planting(scene,materials,hero){
 const evergreens=evergreenTemplates(hero),evergreenShoots=[],thickerCanopy=selectedSettings().get("canopy")==="mass-v04";
 const rng=random(90812),wood=[],rootCenters=[],leafGroups={maple:[],distant:[],shrub:[]},UP=new THREE.Vector3(0,1,0);
 const addBranch=(points,r0,r1,steps=7,radial=5)=>{const b=branch(points.map(p=>p.toArray()),r0,r1,steps,radial);wood.push(b.g);return b;};
 const leaf=(p,direction,length,kind,roll,shade)=>leafGroups[kind].push({p,direction,roll,length,color:new THREE.Color().setRGB(.75*shade,.84*shade,.64*shade)});
 function shortShoot(a,b,kind,exposure=1,leafSize=.052){
  const middle=a.clone().lerp(b,.55).addScaledVector(UP,.016),twig=addBranch([a,middle,b],kind==='shrub'?.0015:.0017,.00045,3,3);
  const axis=b.clone().sub(a).normalize(),across=new THREE.Vector3().crossVectors(axis,UP);if(across.lengthSq()<.01)across.set(1,0,0);across.normalize();
  if(kind==='distant'){
   for(let j=0;j<(exposure<.65?1:2);j++){const p=twig.path.getPoint(j?.64:.14),dir=axis.clone().addScaledVector(across,j?.34:-.24).addScaledVector(UP,.30+(j%2)*.12).normalize();evergreenShoots.push({p,direction:dir,length:(leafSize/.09)*(thickerCanopy?.38+.095*rng():.20+.055*rng())*(exposure<.65?.72:1.08),roll:rng()*Math.PI*2,shade:.85+.14*rng()});}
   return;
  }
  // Bud clusters are deliberately short and unequal. Some inner nodes stay bare,
  // while outward terminal buds carry a little more leaf area toward open sky.
  const nodes=exposure<.65?[.18,.36,.54,.72,.90]:[.15,.32,.48,.62,.75,.88,.98];
  nodes.forEach((t,j)=>{
   const p=twig.path.getPoint(t),sign=j%2?1:-1;
   const direction=axis.clone().multiplyScalar(.28+.34*rng()).addScaledVector(across,sign*(.53+.24*rng())).addScaledVector(UP,.12+.34*rng()).normalize();
   const l=leafSize*(.74+.26*rng())*(j===nodes.length-1?.77:1);
   leaf(p,direction,l,kind,(rng()-.5)*1.13,.88+rng()*.18);
   if(j===1||j===3){const mate=direction.clone().addScaledVector(across,-sign*1.25).addScaledVector(axis,.38).normalize();leaf(p.clone().addScaledVector(axis,.003),mate,l*.82,kind,(rng()-.5)*.85,.88+rng()*.12);}
  });
 }
 // Physical, individually authored branch axes; the trees are not scale/seed
 // variants of one recursively repeated skeleton.
 const specimens=[]; // Middle/rear trees are fully authored in distant-crowns.js.
 const growthPlans=[
  [[.22,-1,.23,.62],[.40,1,.30,1],[.65,-1,.28,.9],[.81,1,.29,1],[.95,-1,.22,.9]],
  [[.29,1,.31,1],[.45,-1,.23,.55],[.69,1,.28,1],[.90,-1,.26,1]],
  [[.18,-1,.23,.5],[.46,1,.31,.9],[.57,-1,.27,1],[.80,1,.26,.8],[.95,-1,.19,1]],
  [[.34,1,.28,1],[.55,-1,.30,.8],[.75,1,.23,1],[.93,-1,.21,.9]],
  [[.27,-1,.29,.75],[.48,1,.33,1],[.74,-1,.28,.85],[.90,1,.25,1]]
 ];
 for(const [si,s]of specimens.entries()){
  const base=new THREE.Vector3(s.origin[0],groundHeight(s.origin[0],s.origin[2])-.004,s.origin[2]),at=p=>new THREE.Vector3(...p).add(base);
  const trunk=addBranch(s.spine.map(at),si===0?.040:.040,.0037,20,8);rootCenters.push({name:s.name,position:base.toArray()});
  const limbs=s.arms.map(([t,points],k)=>addBranch([trunk.path.getPoint(t),...points.map(at)],.0135-k*.0013,.0017,9,6));
  limbs.push({path:new THREE.CatmullRomCurve3([trunk.path.getPoint(.82),trunk.path.getPoint(.93),trunk.path.getPoint(1)])});
  limbs.forEach((limb,k)=>{
   const layerLeafSize=s.size*(si===1?[.80,1.20,1.0,.92,.73,.76][k]:si===2?[1.10,.85,1.08,.88,.76,.70][k]:1);
   const plan=growthPlans[(k+si)%growthPlans.length];
   plan.forEach(([t,handed,span,exposure],j)=>{
    const a=limb.path.getPoint(t),axis=limb.path.getTangent(t),side=new THREE.Vector3().crossVectors(axis,UP).normalize();span*=si===0?.68:.83;
    const b=a.clone().addScaledVector(axis,span*.68).addScaledVector(side,handed*span).addScaledVector(UP,.055+(j%3)*.035);
    const fork=addBranch([a,a.clone().lerp(b,.43).addScaledVector(UP,-.016),b],.0034,.0009,5,4);
    // Leaves along the middle forks interrupt exposed wood, not only its tips.
    const shootNodes=exposure<.65?[.45,.87]:[.14,.32,.49,.67,.84,.99];
    shootNodes.forEach((u,ii)=>{
     const p=fork.path.getPoint(u),advance=fork.path.getTangent(u),sign=(ii+j)%2?1:-1;
     const end=p.clone().addScaledVector(advance,.071+(ii%2)*.032).addScaledVector(axis,sign*.058).addScaledVector(UP,.039);
     shortShoot(p,end,s.kind,exposure,layerLeafSize);
    });
    if(j===1||j===3){const p=limb.path.getPoint(Math.max(.10,t-.12));shortShoot(p,p.clone().addScaledVector(axis,.14).addScaledVector(side,-handed*.07).addScaledVector(UP,.07),s.kind,.7,layerLeafSize*.92);}
   });
   if(si===0){
    const innerGroups=[[[.14,-1,.18],[.54,1,.17]],[[.10,1,.20],[.35,-1,.18],[.62,1,.15]],[[.19,-1,.15],[.49,1,.21]],[[.27,1,.17],[.56,-1,.18]],[[.12,-1,.18],[.43,1,.19]],[[.15,1,.15],[.59,-1,.13]]][k];
    for(const [t,handed,reach]of innerGroups){
     for(let arm=0;arm<2;arm++){
      const a=limb.path.getPoint(t+arm*.027),axis=limb.path.getTangent(t),side=new THREE.Vector3().crossVectors(axis,UP).normalize();
      const tip=a.clone().addScaledVector(axis,reach*(arm?.55:.87)).addScaledVector(side,handed*reach*(arm?-.45:.49)).addScaledVector(UP,arm?.105:.052);
      const fork=addBranch([a,a.clone().lerp(tip,.48).addScaledVector(UP,.02),tip],.0025,.00055,4,4);
      for(const [j,u]of [.16,.56,.94].entries()){
       const q=fork.path.getPoint(u),end=q.clone().addScaledVector(axis,.06).addScaledVector(side,(j%2?-1:1)*.043).addScaledVector(UP,.036);
       shortShoot(q,end,'maple',1,.061);
      }
     }
    }
   }
  });
 }
 // Low multi-axial shrubs: sprawling old wood supports unequal little crowns.
 // The three shrubs have different forks and heights; none radiates from one dot.
 const baselineShrubGrowth=selectedSettings().get('near-growth')==='baseline',organicNear=selectedSettings().get('near-shape')!=='baseline';
 const shrubs=[
  {origin:[-1.50,.52],scale:.86,axes:[
   [[-.17,0,-.08],[-.11,.10,-.03],[.10,.17,.02],[.32,.23,-.01]],
   [[.01,0,.01],[-.12,.12,.08],[-.31,.25,.14],[-.43,.27,.10]],
   [[-.07,0,-.02],[-.02,.18,-.12],[.10,.31,-.25],[.21,.30,-.32]],
   [[.04,0,.02],[.02,.14,.13],[.17,.20,.28],[.24,.19,.35]]]},
  {origin:[-1.66,-1.60],scale:.95,axes:[
   [[-.06,0,-.03],[-.17,.15,-.10],[-.32,.29,-.15],[-.48,.26,-.09]],
   [[.01,0,.05],[.13,.11,.14],[.28,.21,.18],[.44,.28,.11]],
   [[.06,0,-.02],[.05,.16,-.13],[-.07,.35,-.28],[-.19,.38,-.33]],
   [[-.03,0,.03],[-.12,.11,.19],[-.05,.18,.32],[.12,.20,.39]]]},
  {origin:[-3.08,-2.12],scale:1.15,axes:[
   [[-.08,0,-.01],[-.22,.11,.04],[-.39,.26,.18],[-.52,.25,.27]],
   [[.03,0,-.06],[.18,.15,-.16],[.39,.28,-.20],[.53,.31,-.15]],
   [[-.01,0,.03],[.02,.18,.12],[.16,.32,.27],[.34,.36,.34]],
   [[.02,0,-.02],[-.05,.19,-.13],[-.20,.41,-.29],[-.37,.43,-.30]],
   [[.04,0,.01],[.14,.11,.06],[.33,.18,.03],[.51,.17,-.02]]]}
 ];
 const occupiedAxes=[[[[-0.17,0,-0.08],[-0.08,0.055,-0.06],[0.14,0.1,-0.04],[0.34,0.15,-0.01]],[[0.01,0,0.01],[-0.08,0.065,0.03],[-0.26,0.13,0.04],[-0.38,0.17,0.065]],[[-0.07,0,-0.02],[-0.035,0.06,-0.025],[0.04,0.16,-0.1],[0.14,0.22,-0.15]],[[0.04,0,0.02],[0.08,0.06,0.04],[0.2,0.11,0.085],[0.27,0.14,0.12]]],[[[-0.06,0,-0.03],[-0.11,0.055,-0.055],[-0.25,0.11,-0.07],[-0.38,0.15,-0.055]],[[0.01,0,0.05],[0.09,0.06,0.07],[0.25,0.12,0.08],[0.35,0.17,0.065]],[[0.06,0,-0.02],[0.055,0.075,-0.055],[-0.015,0.16,-0.13],[-0.14,0.23,-0.19]],[[-0.03,0,0.03],[-0.08,0.05,0.075],[-0.025,0.095,0.14],[0.095,0.135,0.19]]],[[[-0.08,0,-0.01],[-0.15,0.05,0.025],[-0.31,0.1,0.08],[-0.4,0.135,0.15]],[[0.03,0,-0.06],[0.12,0.06,-0.09],[0.29,0.12,-0.13],[0.42,0.175,-0.105]],[[-0.01,0,0.03],[0.03,0.075,0.075],[0.13,0.145,0.15],[0.23,0.19,0.2]],[[0.02,0,-0.02],[-0.02,0.08,-0.07],[-0.13,0.2,-0.16],[-0.25,0.255,-0.2]],[[0.04,0,0.01],[0.12,0.05,0.035],[0.27,0.095,0.035],[0.4,0.13,0.01]]]];
 if(!baselineShrubGrowth)shrubs.forEach((s,i)=>s.axes=occupiedAxes[i]);
 if(organicNear){shrubs[0].origin=[-1.25,.36];for(const [si,s]of shrubs.entries())s.axes=s.axes.map((axis,k)=>axis.map((p,i)=>i===0?p:[p[0]*(1+(.11*Math.sin(k*2.1+si))),p[1]*(1+(.15*Math.cos(k+si*2.4))),p[2]+.047*Math.sin(k*1.8+si+.7)*i/3]));}
 // Unequal alternate short shoots on the existing old multiaxial skeleton.
 // Local RNG leaves every already-authored rear specimen untouched.
 const shrubRng=random(304618),forkRng=random(308032),shrubShootRecords=[],terminalForkRecords=[];
 function smallShrubShoot(a,b,exposure,specimen){
  const axis=b.clone().sub(a).normalize(),side=new THREE.Vector3().crossVectors(axis,UP).normalize();
  const mid=a.clone().lerp(b,.53).addScaledVector(UP,.004+shrubRng()*.008);
  const twig=addBranch([a,mid,b],.0009,.00025,3,3),length=twig.path.getLength();
  const count=exposure<.65?2+Math.floor(shrubRng()*2):3+Math.floor(shrubRng()*3);
  const gaps=Array.from({length:count-1},()=>.010+shrubRng()*.012),used=gaps.reduce((n,x)=>n+x,0);
  const lastT=exposure<.65?.86:.90+forkRng()*.06;let t=Math.max(.035,lastT-used/Math.max(length,used*1.18));const positions=[];
  for(let i=0;i<count;i++){
   if(i)t+=gaps[i-1]/Math.max(length,used*1.18);
   t=Math.min(t,.98);positions.push(t);
   const q=twig.path.getPoint(t),sign=(i+specimen)%2?1:-1;
   const direction=axis.clone().multiplyScalar(.30+shrubRng()*.34).addScaledVector(side,sign*(.48+shrubRng()*.20)).addScaledVector(UP,.10+shrubRng()*.26).normalize();
   const l=(.022+(.010+shrubRng()*.008)*exposure)*(organicNear?1.14:1),shade=.91+shrubRng()*.15;
   leafGroups.shrub.push({p:q,direction,length:l,roll:(shrubRng()-.5)*(organicNear?1.54:.92),color:new THREE.Color().setRGB(shade*.92,shade,shade*.87),variant:Math.floor(shrubRng()*4)});
   if(i===count-1&&exposure>.76&&shrubRng()>.28){
    const tipDir=axis.clone().addScaledVector(side,-sign*.27).addScaledVector(UP,.16).normalize();
    leafGroups.shrub.push({p:q,direction:tipDir,length:l*.74,roll:(shrubRng()-.5)*(organicNear?1.16:.53),color:new THREE.Color().setRGB(shade*.95,shade,shade*.88),variant:(i+specimen)%4});
   }
  }
  if(exposure>.76&&forkRng()<.65){
   const source=twig.path.getPoint(.66),depth=(forkRng()<.5?-1:1)*(.020+forkRng()*.015);
   const end=source.clone().addScaledVector(axis,.012+forkRng()*.009).add(new THREE.Vector3(0,.005+forkRng()*.007,depth));
   const mid=source.clone().lerp(end,.53).addScaledVector(UP,.003),fork=addBranch([source,mid,end],.00045,.00018,3,3);
   const direction=end.clone().sub(source).normalize(),across=new THREE.Vector3().crossVectors(direction,UP).normalize(),leaves=2+Math.floor(forkRng()*3),nodes=[];
   for(let i=0;i<leaves;i++){
    const u=.48+i*(.49/Math.max(1,leaves-1)),q=fork.path.getPoint(u),dir=direction.clone().multiplyScalar(.52).addScaledVector(across,(i%2?1:-1)*(.39+forkRng()*.22)).addScaledVector(UP,.14+forkRng()*.20).normalize(),l=(.022+forkRng()*.011)*(organicNear?1.14:1),shade=.93+forkRng()*.12;
    leafGroups.shrub.push({p:q,direction:dir,length:l,roll:(forkRng()-.5)*(organicNear?1.38:.80),color:new THREE.Color().setRGB(shade*.92,shade,shade*.87),variant:Math.floor(forkRng()*4)});nodes.push(q.toArray());
   }
   terminalForkRecords.push({specimen,source:source.toArray(),end:end.toArray(),depthOffsetMetres:depth,leaves,nodes,actualTwigSupported:true});
  }
  shrubShootRecords.push({specimen,length,nodes:count,positions,actualNodePositions:positions.map(t=>twig.path.getPoint(t).toArray()),desiredInternodes:gaps});
 }
 for(const [si,s]of shrubs.entries()){
  const [x,z]=s.origin;
  for(const [k,points]of s.axes.entries()){
   const rootX=x+points[0][0]*.63*s.scale,rootZ=z+points[0][2]*.64*s.scale,rootY=groundHeight(rootX,rootZ)-.007;
   const stem=addBranch(points.map(p=>new THREE.Vector3(x+p[0]*.63*s.scale,rootY+p[1]*.78*s.scale,z+p[2]*.64*s.scale)),.007,.0015,7,5);
   rootCenters.push({name:'Low shrub '+si+' axis '+k,position:[rootX,rootY,rootZ]});
   const count=3+Math.floor(shrubRng()*3),nodes=[];let t=(baselineShrubGrowth?.17:.11)+shrubRng()*.045;
   for(let j=0;j<count;j++){nodes.push(Math.min(t,.96));t+=(baselineShrubGrowth?.13:.14)+shrubRng()*.14;}
   nodes.forEach((t,j)=>{
    const a=stem.path.getPoint(t),axis=stem.path.getTangent(t),side=new THREE.Vector3().crossVectors(axis,UP).normalize(),sign=(j+k+si)%2?1:-1;
    const end=a.clone().addScaledVector(axis,(baselineShrubGrowth?.08:.05)+shrubRng()*(baselineShrubGrowth?.10:.07)).addScaledVector(side,sign*((baselineShrubGrowth?.08:.045)+shrubRng()*(baselineShrubGrowth?.09:.065))).addScaledVector(UP,.018+shrubRng()*.035);
    const twig=addBranch([a,a.clone().lerp(end,.54).addScaledVector(UP,.010+shrubRng()*.010),end],.0024,.0007,5,4);
    const n=6+Math.floor(shrubRng()*4),gaps=Array.from({length:n-1},()=>.010+shrubRng()*.012),sum=gaps.reduce((s,x)=>s+x,0);let u=.07;
    for(let ii=0;ii<n;ii++){
     if(ii)u+=gaps[ii-1]/Math.max(twig.path.getLength(),sum*1.12);u=Math.min(u,.96);
     const p=twig.path.getPoint(u),localAxis=twig.path.getTangent(u),localSide=new THREE.Vector3().crossVectors(localAxis,UP).normalize();
     const sweep=(ii%2?1:-1)*((baselineShrubGrowth?.035:.023)+shrubRng()*(baselineShrubGrowth?.035:.026)),exposure=j===0?.52+.12*shrubRng():.76+.24*shrubRng();
     const tip=p.clone().addScaledVector(localAxis,.025+shrubRng()*(baselineShrubGrowth?.048:.036)).addScaledVector(localSide,sweep).addScaledVector(UP,.010+shrubRng()*.027);
     smallShrubShoot(p,tip,exposure,si);
    }
   });
  }
 }
 const crowns=distantCrowns(groundHeight);wood.push(...crowns.wood);evergreenShoots.push(...crowns.shoots);rootCenters.push(...crowns.roots);
 const woodMesh=new THREE.Mesh(mergeGeometries(wood.map(g=>g.toNonIndexed()),false),materials.treeBark);woodMesh.name='Individually authored garden branching';woodMesh.castShadow=woodMesh.receiveShadow=true;scene.add(woodMesh);
 function leafGeometry(kind){
  const outline=kind==='maple'?[[0,0,0],[-.18,.006,.24],[-.46,-.002,.24],[-.27,.013,.41],[-.54,.004,.68],[-.20,.021,.58],[0,.006,1.04],[.22,.018,.57],[.51,-.005,.72],[.28,.014,.40],[.44,-.005,.24],[.16,.007,.22]]:[[0,0,0],[-.19,.015,.23],[-.32,.03,.56],[0,.005,1.08],[.31,.015,.63],[.18,.01,.26]];
  const ps=outline.flat(),n=outline.length;ps.push(0,.072,.48,0,-.022,.46);const ix=[];for(let j=0;j<n;j++){const k=(j+1)%n;ix.push(j,k,n,k,j,n+1);}const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(ps,3));g.setIndex(ix);g.computeVertexNormals();return g;
 }
 function thinShrubLeaf(variant){
  const width=(organicNear?[.23,.27,.255,.29]:[.20,.23,.25,.27])[variant],bend=(organicNear?[.045,.032,.060,.048]:[.037,.055,.046,.059])[variant];
  const ps=[[0,0,0],[-width*(organicNear?.48:.62),bend*.23,.19],[-width,bend*.65,.46],[-width*.62,bend*.88,.76],[(variant-1.5)*(organicNear?.036:.008),bend*.90,1],[width*(organicNear?.72:.58),bend*.86,.80],[width*(organicNear?.84:.92),bend*.54,.48],[width*.55,bend*.08,.20],[.012,bend+.006,.48],[-.005,bend-.008,.49]].flat(),ix=[];
  for(let i=0;i<8;i++){const j=(i+1)%8;ix.push(i,j,8,j,i,9);}
  const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(ps,3));g.setIndex(ix);g.computeVertexNormals();return g;
 }
 const groupStats=[],transform=new THREE.Object3D(),forward=new THREE.Vector3(0,0,1),shrubMaterial=materials.leaves.clone();
 shrubMaterial.vertexColors=false;shrubMaterial.roughness=.96;shrubMaterial.metalness=0;shrubMaterial.userData.backgroundPcfTaps=0;backgroundShadowFilter(shrubMaterial);
 for(const [kind,all]of Object.entries(leafGroups)){
  if(!all.length)continue;
  for(let variant=0;variant<(kind==='shrub'?4:1);variant++){
   const leaves=kind==='shrub'?all.filter(l=>l.variant===variant):all,geo=kind==='shrub'?thinShrubLeaf(variant):leafGeometry(kind);
   const mesh=new THREE.InstancedMesh(geo,kind==='shrub'?shrubMaterial:materials.leaves,leaves.length);mesh.name=kind==='maple'?'Branch attached garden leaves':'Branch attached '+kind+' garden leaves '+variant;
   leaves.forEach((l,i)=>{transform.position.copy(l.p);transform.quaternion.setFromUnitVectors(forward,l.direction);transform.rotateZ(l.roll);transform.scale.set(l.length,l.length,l.length);transform.updateMatrix();mesh.setMatrixAt(i,transform.matrix);mesh.setColorAt(i,l.color);});
   mesh.castShadow=mesh.receiveShadow=true;mesh.instanceMatrix.needsUpdate=true;mesh.computeBoundingSphere();scene.add(mesh);groupStats.push({kind,variant,instances:leaves.length,trianglesPerLeaf:geo.index.count/3,triangles:geo.index.count/3*leaves.length});
  }
 }
 const evergreenStats=installEvergreenShoots(scene,evergreens,evergreenShoots);
 return {terminalForkRecords,shrubShootRecords,shrubLeafDesign:{version:organicNear?'unequal-occupied-v02':baselineShrubGrowth?'thin-grown-v02':'low-occupied-v01',bladeThicknessMM:[.308,.560],bladeLengthMM:organicNear?[25,45]:[22,40],bendMM:[.814,2.36],variants:4,primaryAxesUnchanged:baselineShrubGrowth,rootPositionsUnchanged:!organicNear,frontRootMovedMetres:organicNear?[.25,-.16]:[0,0],existingLeavesAndForksOnly:true,density:'Unequal2-5nodes,10-22mm desired internodes, bareinner nodes and denserouter buds; every leaf attaches to a twig'},distantCrownDesign:crowns.metadata,evergreenStats,rootCenters,design:'Three distinct layered trees at middle/rear and beyond the pavilion, each rooted and physically branch-attached; low multiaxial shrubs and continuous moss cushions return to natural stones',specimens:specimens.map(({name,origin,kind,arms})=>({name,origin,kind,primaryArms:arms.length})),shrubOrigins:shrubs.map(s=>s.origin),branchTriangles:woodMesh.geometry.attributes.position.count/3,leafInstances:groupStats.reduce((s,g)=>s+g.instances,0),leafTriangles:groupStats.reduce((s,g)=>s+g.triangles,0),leafGroups:groupStats,rootGroundHeightSamples:[...specimens.map(s=>[s.origin[0],s.origin[2]]),...shrubs.map(s=>s.origin)].map(([x,z])=>({x,z,groundY:groundHeight(x,z)}))};
}
