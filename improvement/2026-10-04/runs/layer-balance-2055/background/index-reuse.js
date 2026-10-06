import * as THREE from 'three';
// Reuse exactly identical vertex attributes. No welding, tolerance, changing
// normals, silhouette simplification or triangle removal is involved.
export function indexExactAttributes(g){
 if(g.index||new URLSearchParams(location.search).get('index')==='original')return g;
 const names=Object.keys(g.attributes).sort(),attrs=names.map(n=>g.attributes[n]);
 if(attrs.some(a=>a.isInterleavedBufferAttribute||!(a.array instanceof Float32Array)))return g;
 const bits=attrs.map(a=>new Uint32Array(a.array.buffer,a.array.byteOffset,a.array.length)),ids=new Map(),first=[],indices=new Uint32Array(g.attributes.position.count);
 for(let v=0;v<indices.length;v++){
  let key='';for(let a=0;a<attrs.length;a++)for(let c=0;c<attrs[a].itemSize;c++)key+=bits[a][v*attrs[a].itemSize+c]+',';
  let id=ids.get(key);if(id===undefined){id=first.length;ids.set(key,id);first.push(v);}indices[v]=id;
 }
 const result=new THREE.BufferGeometry();
 for(let a=0;a<names.length;a++){const old=attrs[a],values=new Float32Array(first.length*old.itemSize),word=new Uint32Array(values.buffer);for(let v=0;v<first.length;v++)for(let c=0;c<old.itemSize;c++)word[v*old.itemSize+c]=bits[a][first[v]*old.itemSize+c];result.setAttribute(names[a],new THREE.BufferAttribute(values,old.itemSize,old.normalized));}
 result.setIndex(new THREE.BufferAttribute(indices,1));result.userData.exactIndexReuse={originalVertices:indices.length,storedVertices:first.length,triangles:indices.length/3,attributeNames:names,allFloat32BitsPreserved:true,noTrianglesRemoved:true};
 g.dispose();return result;
}
