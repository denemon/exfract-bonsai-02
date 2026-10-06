import * as THREE from 'three';
export function configureShadowFilter(){
 const original=THREE.ShaderChunk.shadowmap_pars_fragment,start=original.indexOf('\t\t\t\tshadow = ('),end=original.indexOf(') * 0.2;',start);if(start<0||end<0)throw Error('Pinned Three PCF contract changed');
 const count=new URLSearchParams(location.search).get('perf')==='original'?16:8;
 const replacement=`shadow=0.0;for(int sampleIndex=0;sampleIndex<${count};sampleIndex++){shadow+=texture(shadowMap,vec3(shadowCoord.xy+vogelDiskSample(sampleIndex,${count},0.0)*radius,shadowCoord.z));}shadow*=${1/count};`;
 THREE.ShaderChunk.shadowmap_pars_fragment=original.slice(0,start)+replacement+original.slice(end+') * 0.2;'.length);
}
