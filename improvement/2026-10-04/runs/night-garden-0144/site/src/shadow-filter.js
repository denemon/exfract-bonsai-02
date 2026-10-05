import * as THREE from 'three';

// Three r185's default five rotated PCF samples leave visible sampling grain
// on the broad pale trunk. Use a stable 16-sample disk for this static scene.
export function configureShadowFilter(){
 const original=THREE.ShaderChunk.shadowmap_pars_fragment;
 const start=original.indexOf('\t\t\t\tshadow = (');
 const end=original.indexOf(') * 0.2;',start);
 if(start<0||end<0)throw Error('Pinned Three PCF implementation changed');
 const replacement=`\t\t\t\tshadow = 0.0;
                for (int sampleIndex=0;sampleIndex<16;sampleIndex++) {
                    shadow += texture(shadowMap,vec3(shadowCoord.xy+vogelDiskSample(sampleIndex,16,0.0)*radius,shadowCoord.z));
                }
                shadow *= 0.0625;`;
 THREE.ShaderChunk.shadowmap_pars_fragment=original.slice(0,start)+replacement+original.slice(end+') * 0.2;'.length);
}
