import * as THREE from 'three';
// A closed, slightly tapered earthen body. The two tile shells have real inner
// faces and eave rims; charcoal timber is restricted to bearing fascia / ends.
export function tsuijiBoundary(batch,start,end,z){
 const length=end-start,cx=(start+end)/2,base=.145,top=1.99,parts=[];
 const add=(g,tag,key='rearWood')=>{if(key==='rearWood')g.setAttribute('boardSeed',new THREE.Float32BufferAttribute(new Float32Array(g.attributes.position.count).fill(tag),1));batch.add(g,key);parts.push({tag,key,vertices:g.attributes.position.count,triangles:(g.index?.count||g.attributes.position.count)/3});};
 const block=(p,s,tag)=>{const g=new THREE.BoxGeometry(...s);g.translate(...p);add(g,tag);};
 const body=new THREE.BoxGeometry(length,top-base,.40,64,12,1),a=body.attributes.position;
 for(let i=0;i<a.count;i++){const x=a.getX(i)+cx,y=a.getY(i)+(top+base)/2,t=(y-base)/(top-base),side=a.getZ(i)/.20;const strata=.0025*Math.sin(y*26.+.12*Math.sin(x*1.9))+.0014*Math.sin(x*2.4+y*7.1);a.setXYZ(i,x,y,z+side*(.20-.05*t)+Math.abs(side)*strata);}
 body.computeVertexNormals();add(body,0);
 // Unequal broad stone footing joints, mostly seated beneath the earth.
 const widths=[.79,.95,.86,1.04,.73,.91,.84,1.02,.89,.78,.99,.85,.96,.82,.90,.94],scale=length/widths.reduce((a,b)=>a+b,0);let x=start;
 for(let i=0;i<widths.length;i++){const w=widths[i]*scale,bottom=-.045,upper=.171+.007*Math.sin(i*2.13);block([x+w/2,(bottom+upper)/2,z+.009],[w-.0025,upper-bottom,.443+(i%3)*.006],2);x+=w;}
 block([cx,2.045,z],[length+.09,.089,.429],1);
 for(const x of[start+.045,end-.045])block([x,1.073,z],[.094,1.936,.425],1);
 for(const hand of[-1,1]){
  const deck=new THREE.BoxGeometry(length+.14,.036,.403);deck.rotateX(hand*.29);deck.translate(cx,2.145,z+hand*.185);add(deck,null,'roof');
  const count=Math.floor(length/.192),pitch=length/count;
  for(let i=0;i<count;i++){const p=[],ix=[],r=[.041,.036],n=5,l=.424;for(let layer=0;layer<2;layer++)for(let end=0;end<2;end++)for(let k=0;k<=n;k++){const t=k/n*Math.PI;p.push(r[layer]*Math.cos(t),r[layer]*Math.sin(t),(end?1:-1)*l/2);}const id=(layer,end,k)=>layer*(n+1)*2+end*(n+1)+k,quad=(a,b,c,d)=>ix.push(a,b,c,b,d,c);for(let k=0;k<n;k++){quad(id(0,0,k),id(0,0,k+1),id(0,1,k),id(0,1,k+1));quad(id(1,0,k+1),id(1,0,k),id(1,1,k+1),id(1,1,k));for(const end of[0,1])quad(id(0,end,k),id(1,end,k),id(0,end,k+1),id(1,end,k+1));}for(const k of[0,n])quad(id(0,0,k),id(1,0,k),id(0,1,k),id(1,1,k));const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(p,3));g.setIndex(ix);g.setAttribute('uv',new THREE.Float32BufferAttribute(new Float32Array(p.length/3*2),2));g.computeVertexNormals();g.rotateX(hand*.29);g.translate(start+(i+.5)*pitch,2.166,z+hand*.185);add(g,null,'roof');}
 }
 const ridge=new THREE.CylinderGeometry(.058,.058,length+.22,9);ridge.rotateZ(Math.PI/2);ridge.translate(cx,2.263,z);add(ridge,null,'roof');
 return {version:'tapered-tsuiji-body-shell-v01',wallBodyThicknessMetres:[.40,.30],bodyY:[base,top],roofRidgeY:2.321,baseBottomY:-.045,tileShellThicknessMetres:.005,closedBody:true,tileInnerFacesAndEaveRims:true,blackTimberBearingFasciaAndTwoEndsOnly:true,originalWallBoundaryAndHouseJunctionPreserved:true,parts,triangles:parts.reduce((s,a)=>s+a.triangles,0)};
}
