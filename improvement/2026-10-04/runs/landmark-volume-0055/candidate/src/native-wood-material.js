import * as THREE from 'three';
// Existing free, locally stored Cedar001 maps are a provisional wood texture,
// not an identification of the reference tree or a scan of that bonsai.
export async function makeNativeWoodFinish(mode='gray'){
 if(mode==='gray')return {wood:new THREE.MeshStandardMaterial({color:'#88847e',roughness:1,metalness:0}),twig:new THREE.MeshStandardMaterial({color:'#88847e',roughness:1,metalness:0})};
 if(mode==='base'){const wood=new THREE.MeshStandardMaterial({color:'#66584b',roughness:.96,metalness:0});wood.customProgramCacheKey=()=> 'native-independent-wood-base-v2-aligned';return {wood,twig:new THREE.MeshStandardMaterial({color:'#514236',roughness:.97,metalness:0})};}
 if(!['color','roughness','normal'].includes(mode))throw Error('Unknown native wood finish');
 const loader=new THREE.TextureLoader(),required=['color',...(mode==='color'?[]:['roughness']),...(mode==='normal'?['normal']:[])];
 const loaded=await Promise.all(required.map(n=>loader.loadAsync('/bark/'+n+'.webp'))),textures=Object.fromEntries(required.map((n,i)=>[n,loaded[i]]));
 textures.color.colorSpace=THREE.SRGBColorSpace;for(const t of loaded){t.wrapS=t.wrapT=THREE.RepeatWrapping;t.anisotropy=4;}
 const wood=new THREE.MeshStandardMaterial({color:'#ffffff',roughness:.96,metalness:0});wood.defines={USE_UV1:'',USE_UV2:''};
 wood.onBeforeCompile=s=>{
  s.uniforms.nativeWoodColor={value:textures.color};if(textures.roughness)s.uniforms.nativeWoodRough={value:textures.roughness};if(textures.normal)s.uniforms.nativeWoodNormal={value:textures.normal};
  s.vertexShader='varying vec2 vNativeMain;varying vec2 vNativeBranch;varying float vNativeBlend;\n'+s.vertexShader;
  s.vertexShader=s.vertexShader.replace('#include <begin_vertex>','#include <begin_vertex>\nvNativeMain=vec2(uv.x,1.-uv.y)/.72+vec2(.07,.11);vNativeBranch=vec2(uv1.x,1.-uv1.y)/.72+vec2(.38,.11);vNativeBlend=clamp(uv2.x,0.,1.);');
  s.fragmentShader='varying vec2 vNativeMain;varying vec2 vNativeBranch;varying float vNativeBlend;uniform sampler2D nativeWoodColor;\n'+(textures.roughness?'uniform sampler2D nativeWoodRough;\n':'')+(textures.normal?`uniform sampler2D nativeWoodNormal;
vec3 nativeWoodBump(vec3 geometric,vec3 surfacePosition,vec2 uv,vec3 value){vec3 a=dFdx(surfacePosition),b=dFdy(surfacePosition);vec2 ta=dFdx(uv),tb=dFdy(uv);vec3 bp=cross(b,geometric),ap=cross(geometric,a);vec3 tangent=bp*ta.x+ap*tb.x,bitangent=bp*ta.y+ap*tb.y;float scale=inversesqrt(max(max(dot(tangent,tangent),dot(bitangent,bitangent)),1e-12));vec3 n=value*2.-1.;n.xy*=.20;return normalize(mat3(tangent*scale,bitangent*scale,geometric)*n);}
`:'')+s.fragmentShader;
  s.fragmentShader=s.fragmentShader.replace('#include <color_fragment>',`#include <color_fragment>
vec3 woodSample=mix(texture2D(nativeWoodColor,vNativeMain).rgb,texture2D(nativeWoodColor,vNativeBranch).rgb,vNativeBlend);float woodLuma=dot(woodSample,vec3(.2126,.7152,.0722));
// Warm low-saturation brown; no white deadwood or emissive silver accent.
diffuseColor.rgb=clamp(mix(woodSample,vec3(woodLuma),.45)*1.20,vec3(.024,.019,.014),vec3(.23,.185,.14));diffuseColor.a=1.;`);
  let maps='';if(textures.roughness)maps+='float woodRough=mix(texture2D(nativeWoodRough,vNativeMain).r,texture2D(nativeWoodRough,vNativeBranch).r,vNativeBlend);roughnessFactor=clamp(.94+.055*woodRough,.94,.995);\n';
  if(textures.normal)maps+='vec3 woodMainNormal=nativeWoodBump(normal,-vViewPosition,vNativeMain,texture2D(nativeWoodNormal,vNativeMain).rgb),woodBranchNormal=nativeWoodBump(normal,-vViewPosition,vNativeBranch,texture2D(nativeWoodNormal,vNativeBranch).rgb);normal=normalize(mix(woodMainNormal,woodBranchNormal,vNativeBlend));\n';
  s.fragmentShader=s.fragmentShader.replace('#include <normal_fragment_maps>','#include <normal_fragment_maps>\n'+maps);
 };
 wood.customProgramCacheKey=()=>`native-independent-wood-${mode}-v2-aligned`;return {wood,twig:new THREE.MeshStandardMaterial({color:'#514236',roughness:.97,metalness:0})};
}
