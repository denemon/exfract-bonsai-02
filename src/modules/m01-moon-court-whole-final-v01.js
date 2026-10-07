import * as THREE from 'three';
import {mergeGeometries} from 'three/addons/utils/BufferGeometryUtils.js';
import {createMoonScene as selected,loadMoonAssets} from './m10-moon-star-garden-final-v01.js';
import {noise} from './m11-garden-materials.js';
import {random} from './m12-garden-geometry.js';
import {islandDistance,moonGroundHeight} from './m13-moon-wall-ground-layered-v10.js';
export {loadMoonAssets};

// Packing boundaries are the actual stone contours; they do not merely set
// bounds around rescaled copies of one rock. Front, bevel, side and rear faces
// enclose each thick piece. All joints recede behind the projecting faces.
function clip(poly,nx,ny,c){const out=[];for(let i=0;i<poly.length;i++){const a=poly[i],b=poly[(i+1)%poly.length],da=a[0]*nx+a[1]*ny-c,db=b[0]*nx+b[1]*ny-c;if(da<=0)out.push(a);if((da<=0)!==(db<=0)){const t=da/(da-db);out.push([a[0]+t*(b[0]-a[0]),a[1]+t*(b[1]-a[1])]);}}return out;}
function inset(poly,d){let p=poly.map(a=>a.slice());for(let i=0;i<poly.length;i++){const a=poly[i],b=poly[(i+1)%poly.length],dx=b[0]-a[0],dy=b[1]-a[1],l=Math.hypot(dx,dy);p=clip(p,dy/l,-dx/l,(dy*a[0]-dx*a[1])/l-d);}return p;}
function piece(poly,z,rng,id){
 const cx=poly.reduce((s,p)=>s+p[0],0)/poly.length,cy=poly.reduce((s,p)=>s+p[1],0)/poly.length;
 // Unequal side break points and limited corner breaks replace alternating
 // Voronoi diamonds. The same contours bound neighbouring receiving stones.
 const outer=[];
 for(let i=0;i<poly.length;i++){const p=poly[i],prev=poly[(i+poly.length-1)%poly.length],next=poly[(i+1)%poly.length],cut=.006+rng()*.017;const la=Math.hypot(prev[0]-p[0],prev[1]-p[1]),lb=Math.hypot(next[0]-p[0],next[1]-p[1]);outer.push([p[0]+(prev[0]-p[0])*Math.min(.13,cut/la),p[1]+(prev[1]-p[1])*Math.min(.13,cut/la)],[p[0]+(next[0]-p[0])*Math.min(.13,cut/lb),p[1]+(next[1]-p[1])*Math.min(.13,cut/lb)]);}
 for(const p of outer){const l=Math.hypot(p[0]-cx,p[1]-cy),k=1-(.0017+rng()*.0013)/l;p[0]=cx+(p[0]-cx)*k;p[1]=cy+(p[1]-cy)*k;}
 const front=z+.276+rng()*.025,back=z-.235,tx=(rng()-.5)*.13,ty=(rng()-.5)*.12;
 const inner=outer.map(([x,y])=>{const l=Math.hypot(x-cx,y-cy),k=Math.max(.77,1-(.010+rng()*.014)/l);return [cx+(x-cx)*k,cy+(y-cy)*k];});
 const ps=[],ix=[],cache=new Map(),shade=.89+rng()*.23;
 const add=(x,y,zz)=>{const key=[x,y,zz].map(v=>v.toFixed(7)).join(',');if(cache.has(key))return cache.get(key);const i=ps.length/3;ps.push(x,y,zz);cache.set(key,i);return i;};
 const face=(a,b,c)=>ix.push(add(...a),add(...b),add(...c));
 const rough=(x,y)=>.0058*Math.sin(x*28.3+y*11.7+id*1.3)*Math.sin(y*31.1-x*7.7+id)+.0027*Math.sin(x*67.1-y*49.7+id*5);
 const depth=(x,y)=>front+tx*(x-cx)+ty*(y-cy)+rough(x,y);
 const surface=(a,b,c,n)=>{if(n){const ab=[(a[0]+b[0])/2,(a[1]+b[1])/2],bc=[(b[0]+c[0])/2,(b[1]+c[1])/2],ca=[(c[0]+a[0])/2,(c[1]+a[1])/2];surface(a,ab,ca,n-1);surface(ab,b,bc,n-1);surface(ca,bc,c,n-1);surface(ab,bc,ca,n-1);}else face([a[0],a[1],depth(...a)],[b[0],b[1],depth(...b)],[c[0],c[1],depth(...c)]);};
 for(let i=0;i<outer.length;i++){const j=(i+1)%outer.length,a=outer[i],b=outer[j],u=inner[i],v=inner[j];surface([cx,cy],u,v,3);const oa=[a[0],a[1],front-.024+rough(...a)],ob=[b[0],b[1],front-.024+rough(...b)],ia=[u[0],u[1],depth(...u)],ib=[v[0],v[1],depth(...v)],ba=[a[0],a[1],back],bb=[b[0],b[1],back];face(oa,ob,ia);face(ob,ib,ia);face(oa,ba,ob);face(ob,ba,bb);face([cx,cy,back],bb,ba);}
 const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(ps,3));g.setIndex(ix);g.computeVertexNormals();const colors=new Float32Array(ps.length);for(let i=0;i<colors.length;i+=3){colors[i]=shade;colors[i+1]=shade*(.992+.012*Math.sin(id));colors[i+2]=shade*(.956+.026*Math.cos(id));}g.setAttribute('color',new THREE.Float32BufferAttribute(colors,3));const ng=g.toNonIndexed();g.dispose();return ng;
}

function mineralMaterial(map){
 const m=new THREE.MeshStandardMaterial({color:'#ffffff',roughness:1,metalness:0,vertexColors:true});
 m.onBeforeCompile=s=>{s.uniforms.courtRock={value:map};s.vertexShader='varying vec3 vCourt;\n'+s.vertexShader;s.vertexShader=s.vertexShader.replace('#include <begin_vertex>','#include <begin_vertex>\nvCourt=(modelMatrix*vec4(transformed,1.)).xyz;');s.fragmentShader='varying vec3 vCourt;uniform sampler2D courtRock;\n'+noise+s.fragmentShader;
 s.fragmentShader=s.fragmentShader.replace('#include <color_fragment>',`#include <color_fragment>
 vec3 cStone=texture2D(courtRock,fract(vec2(vCourt.x+vCourt.z*.17,vCourt.y)*1.9)).rgb;float cLuma=dot(cStone,vec3(.2126,.7152,.0722));
 float cBroad=en(vCourt*3.7),cFine=en(vCourt*vec3(173.,151.,137.));
 vec3 cMineral=vec3(.283,.294,.270)*(.83+.23*cBroad)+vec3(.094,.099,.084)*cLuma;
 float cVein=smoothstep(.48,.55,en(vCourt*vec3(6.,19.,8.)))*(.75+.25*cBroad);
 cMineral*=.955+.067*cFine-.030*cVein;
 float cSoil=1.-smoothstep(-.020,.045,vCourt.y);diffuseColor.rgb*=mix(cMineral,cMineral*vec3(.76,.75,.69),cSoil);
 `);s.fragmentShader=s.fragmentShader.replace('#include <normal_fragment_maps>','#include <normal_fragment_maps>\nnormal=envBump(normal,(cFine-.5)*.0011+(en(vCourt*32.)-.5)*.0026,-vViewPosition);');};
 m.customProgramCacheKey=()=> 'court-packed-weathered-granite-v02';return m;
}
function replaceFoundation(g,assets){
 const scene=g.scene,earth=scene.getObjectByName('Garden architecture rearWood'),p=earth.geometry.attributes.position,t=earth.geometry.attributes.boardSeed;
 let start=Infinity,end=-Infinity,z=0,count=0;for(let i=0;i<p.count;i++)if(t.getX(i)<.5){start=Math.min(start,p.getX(i));end=Math.max(end,p.getX(i));z+=p.getZ(i);count++;}z/=count;
 // The actual earth front is above the broad bearing stones. Its lower lip
 // extends into their top course; a recessed mineral core closes the joints.
 for(let i=0;i<p.count;i++)if(t.getX(i)<.5){const x=p.getX(i),y=p.getY(i),v=(y-.345)/(1.99-.345);p.setY(i,.327+.016*Math.sin(x*2.43)+v*(1.99-.327-.016*Math.sin(x*2.43)));}p.needsUpdate=true;earth.geometry.computeVertexNormals();
 const old=earth.material.onBeforeCompile;earth.material.onBeforeCompile=s=>{old.call(earth.material,s);s.fragmentShader=s.fragmentShader.replace('clay*=.955+.075*en(vEnv*vec3(.52,.81,.66));','clay*=.94+.11*en(vEnv*vec3(.52,.81,.66));clay*=1.-.07*(1.-smoothstep(.33,.51,vEnv.y))*en(vEnv*vec3(4.2,.7,2.1));');};earth.material.customProgramCacheKey=()=> 'court-earth-bearing-lip-v01';
 for(const name of ['Garden architecture masonry','Garden architecture masonryJoint']){const o=scene.getObjectByName(name);if(o){o.removeFromParent();o.geometry.dispose();o.material.dispose();}}
 const rng=random(818249),joints=[[start,start,start,start]],heights=[-.105,.071,.237,.392];let x=start;
 while(x<end){x=Math.min(end,x+.53+rng()*.58);joints.push(x===end?[x,x,x,x]:[x+(rng()-.5)*.018,x+(rng()-.5)*.053,x+(rng()-.5)*.073,x+(rng()-.5)*.072]);}
 const geometries=[],rows=[];let id=0;
 for(let i=0;i<joints.length-1;i++){const l=joints[i],r=joints[i+1],top=.362+rng()*.034;let poly=[[l[0],-.105],[r[0],-.105],[r[1],.071],[r[2],.237],[r[3],top],[l[3],top],[l[2],.237],[l[1],.071]],pieces=[poly];
  if(i%5===3){const width=.09+rng()*.10,y=.22+rng()*.07,corner=[r[3],top],a=[r[3]-width,top],b=[r[2],y];poly=[[l[0],-.105],[r[0],-.105],[r[1],.071],b,a,[l[3],top],[l[2],.237],[l[1],.071]];pieces=[poly,[b,corner,a]];}
  for(const p of pieces){const q=piece(p,z,rng,id);geometries.push(q);rows.push({id:id++,actualPackingOutline:p,triangles:q.attributes.position.count/3});}
 }
 const joint=new THREE.BoxGeometry(end-start,.482,.370);joint.translate((start+end)/2,.136,z-.079);const backing=new THREE.Mesh(joint,new THREE.MeshStandardMaterial({color:'#77766b',roughness:1}));backing.name='Garden architecture masonryJoint';backing.castShadow=backing.receiveShadow=true;scene.add(backing);
 const combined=mergeGeometries(geometries,false);geometries.forEach(a=>a.dispose());const stones=new THREE.Mesh(combined,mineralMaterial(assets[1][1].maps[0]));stones.name='Garden architecture masonry';stones.castShadow=stones.receiveShadow=true;scene.add(stones);
 return {version:'unequal-broad-bearing-stone-breaks-v02',rows,stoneDepthMetres:[.5025,.5445],frontSetbackOfJointBackingMetres:[.170,.212],buriedBottomY:-.105,nominalStoneTopRange:[.362,.396],earthLipYRange:[.311,.343],nominalEarthLipOverlapRange:[.019,.085],shape:'Actual unequal clipped solid outlines; broad irregular planar front, irregular weathered bevel, thick side and rear. No distorted shared scan and no equal sphere forms.',notNativeOrStructuralStressCertified:true};
}
function courtGround(m){
 const a=new THREE.MeshStandardMaterial({color:'#ffffff',roughness:1,metalness:0});
 a.onBeforeCompile=s=>{s.uniforms.courtMoss={value:m.ground.userData.mossTexture};s.vertexShader='varying vec3 vCourtGround;\n'+s.vertexShader;s.vertexShader=s.vertexShader.replace('#include <begin_vertex>','#include <begin_vertex>\nvCourtGround=(modelMatrix*vec4(transformed,1.)).xyz;');
 s.fragmentShader='varying vec3 vCourtGround;uniform sampler2D courtMoss;\n'+noise+`
 float cgEllipse(vec2 p,vec2 c,vec2 r){return (length((p-c)/r)-1.)*min(r.x,r.y);}
 float cgSmooth(float a,float b,float k){float h=clamp(.5+.5*(b-a)/k,0.,1.);return mix(b,a,h)-k*h*(1.-h);}
 float cgIsland(vec2 p){float d=cgSmooth(cgEllipse(p,vec2(.65,-.43),vec2(1.04,.69)),cgEllipse(p,vec2(-.10,-.21),vec2(.79,.40)),.26);d=min(d,cgEllipse(p,vec2(-.95,.63),vec2(.45,.27)));return d+.020*sin(p.x*13.+p.y*8.)+.014*sin(p.y*22.-p.x*7.);}
 `+s.fragmentShader;
 s.fragmentShader=s.fragmentShader.replace('#include <color_fragment>',`#include <color_fragment>
 vec2 cp=vCourtGround.xz;float cd=cgIsland(cp)+.010*(en(vCourtGround*47.)-.5)+.005*(en(vCourtGround*101.)-.5),cm=1.-smoothstep(-.024,.017,cd);
 float cb=en(vCourtGround*3.7),cf=en(vCourtGround*vec3(811.,151.,773.)),cPatch=en(vCourtGround*vec3(8.,2.,11.));
 float cGrainAA=1.-smoothstep(.007,.019,length(fwidth(vCourtGround)));
 float cPath=cp.y+.09*cp.x+.085*sin(cp.x*.35)+.12*exp(-pow((cp.x-.40)/1.32,2.))*tanh((cp.y+.40)/.48)+.045*exp(-pow((cp.x+.95)/.48,2.))*tanh((cp.y-.63)/.22);
 float cPhase=(cPath+.0009*sin(cp.x*14.+cp.y*3.))/.09,cAA=1.-smoothstep(.22,.64,fwidth(cPhase)),cWave=cos(cPhase*6.2831853),cLong=smoothstep(.07,.24,cd);
 float cRing=cd/.09,cRingAA=1.-smoothstep(.22,.64,fwidth(cRing)),cRingW=cos(cRing*6.2831853),cLocal=smoothstep(.025,.05,cd)*(1.-smoothstep(.11,.21,cd));
 vec3 cSand=vec3(.240,.234,.220)*(.96+.045*cb+.10*(cf-.5)*cGrainAA);cSand*=1.-.008*(.5-.5*cWave)*cAA*cLong-.005*(.5-.5*cRingW)*cRingAA*cLocal;
 vec3 cMoss=texture2D(courtMoss,cp/.38).rgb*vec3(.73,.82,.68)*(.75+.20*cPatch+.14*en(vCourtGround*31.));
 float cDry=smoothstep(.54,.75,en(vCourtGround*vec3(17.,2.,19.)))*.19;cMoss=mix(cMoss,vec3(.081,.075,.041),cDry);
 float cSoil=(1.-smoothstep(.008,.027,abs(cd+.023)))*(.18+.24*en(vCourtGround*27.));
 diffuseColor.rgb=mix(cSand,vec3(.058,.046,.029),cSoil);diffuseColor.rgb=mix(diffuseColor.rgb,cMoss,cm);
 `);s.fragmentShader=s.fragmentShader.replace('#include <normal_fragment_maps>',`#include <normal_fragment_maps>
 float cRelief=mix(.00032*cWave*cAA*cLong+.00022*cRingW*cRingAA*cLocal+(cf-.5)*.00055*cGrainAA,(en(vCourtGround*113.)-.5)*.0021+(cPatch-.5)*.0026,cm);normal=envBump(normal,cRelief,-vViewPosition);
 `);};a.customProgramCacheKey=()=> 'court-quiet-mineral-grain-moss-relief-v01';return a;
}
function groundRelief(x,z){const d=islandDistance(x,z),inside=Math.max(0,Math.min(1,(-d-.01)/.18)),anchor=1-Math.exp(-((x-.65)**2+(z+.45)**2)/.044);return .009*inside*anchor*(Math.sin(x*6.1+z*4.3)+.6*Math.sin(z*13.7-x*3.2));}
function refineStones(scene){for(const role of ['main','companion','discarded']){const o=scene.getObjectByName('Moon garden '+role+' buried natural stone');const m=o.material.clone();m.onBeforeCompile=s=>{s.fragmentShader=s.fragmentShader.replace('#include <color_fragment>',`#include <color_fragment>
 float cLuma=dot(diffuseColor.rgb,vec3(.2126,.7152,.0722));diffuseColor.rgb=mix(diffuseColor.rgb,vec3(cLuma)*vec3(1.018,1.,.945),.60)*${role==='companion'?'1.04':'.94'}+vec3(${role==='companion'?'.077,.075,.067':'.057,.055,.048'});
 `);s.fragmentShader=s.fragmentShader.replace('#include <roughnessmap_fragment>','#include <roughnessmap_fragment>\nroughnessFactor=max(.93,roughnessFactor);');};m.customProgramCacheKey=()=> 'court-scanned-slate-mineral-'+role+'-v01';m.normalScale.set(.45,.45);o.material=m;}}
export async function createMoonScene(hero,study,assets){
 const g=await selected(hero,study,assets),foundation=replaceFoundation(g,assets),gp=g.ground.geometry.attributes.position;
 for(let i=0;i<gp.count;i++){const x=gp.getX(i),z=gp.getZ(i);gp.setY(i,moonGroundHeight(x,z)+groundRelief(x,z));}gp.needsUpdate=true;g.ground.geometry.computeVertexNormals();g.ground.material.dispose();g.ground.material=courtGround(assets[0]);refineStones(g.scene);g.scene.updateMatrixWorld(true);
 g.layout='moon-court-whole-v02';g.metadata={...g.metadata,version:g.layout,foundation,selectedTrunkRootCameraMoonAllHeld:true,mainStonesPositionsHeld:true,noAdditionalProps:true,groundRefinement:{sharedOriginalIslandOutline:true,broadMossReliefMaximumMeters:.0144,rootGroundAnchorHeldAtCentreOnly:true,rakeGeometryAndPeriodHeld:true,rakeReliefMeters:[.00032,.00022],notAllFootprintContactCertificate:true},previousFallbackUnsynchronized:false,fallbackSceneVersion:"moon-court-v02",visualStudyOnly:false,allMaterialsAndPerformanceFinal:false};return g;
}
