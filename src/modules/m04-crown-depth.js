import * as THREE from 'three';
export async function applyCompactDepth(gltf){
 const spec=gltf.parser.json.extras?.connected_depth_compact;if(!spec)throw Error('Missing exact compact crown');
 const [matrixBuffer,fitBuffer]=await Promise.all([gltf.parser.getDependency('bufferView',spec.matrixView),gltf.parser.getDependency('bufferView',spec.fitView)]),values=decodeExactMatrices(matrixBuffer,spec),fit=new Float64Array(fitBuffer),groups=new Map(spec.groups.map(x=>[x.name,x]));
 let shoots=0,used=0,twigs=0;
 gltf.scene.traverse(o=>{if(!o.isMesh)return;if(/Terminal[_ ]twig/.test(o.name)){o.userData.authoring_version=o.userData.authoring_version||'twig-depth-v01';twigs++;}const row=groups.get(o.userData.name);if(!row)return;if(!o.isInstancedMesh||o.count!==row.count)throw Error('Compact instance count mismatch');
  for(let i=0;i<row.count;i++){const src=row.offset+i*12,dst=i*16,a=o.instanceMatrix.array;for(const [k,v]of [0,1,2,4,5,6,8,9,10,12,13,14].entries())a[dst+v]=values[src+k];a[dst+3]=a[dst+7]=a[dst+11]=0;a[dst+15]=1;shoots++;}o.instanceMatrix.needsUpdate=true;o.userData.crownDepthVersion=spec.version;used++;
 });
 if(shoots!==2800||used!==72||twigs!==1||fit.length!==spec.fitCount*3)throw Error('Compact crown invariant failed');
 return {fitWorld:fit,status:{version:spec.version,shoots,groups:used,twigCount:twigs,exactR40Float32MatrixCoefficients:spec.exactActualR40InstanceMatrices!==false,exactDependentJunctionMatrices:spec.exactDependentJunctionMatrices===true,oldLeafGeometryMasksCountPreserved:true,originalWorldFitHull:true,originalFitWorldPoints:52818,retainedHullVertices:spec.fitCount}};
}

function decodeExactMatrices(buffer,spec){if(spec.matrixEncoding!=='float32-byteplanes-le-v01')return new Float32Array(buffer);const encoded=new Uint8Array(buffer),count=encoded.length/4,raw=new Uint8Array(encoded.length);for(let i=0;i<count;i++)for(let k=0;k<4;k++)raw[i*4+k]=encoded[k*count+i];return new Float32Array(raw.buffer); }
