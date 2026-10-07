import * as THREE from 'three';
// Existing free, locally stored Cedar001 maps are a provisional wood texture,
// not an identification of the reference tree or a scan of that bonsai.
export async function makeNativeWoodFinish(mode='gray',surface='aged-v01'){
 mode='normal';surface='living-v01';
 const refined=surface==='bearing-v01';
 const loader=new THREE.TextureLoader(),required=['color',...(mode==='color'?[]:['roughness']),...(mode==='normal'?['normal']:[])];
 const loaded=await Promise.all(required.map(n=>loader.loadAsync('bark/'+n+'.webp'))),textures=Object.fromEntries(required.map((n,i)=>[n,loaded[i]]));
 const fissure=await loader.loadAsync('materials/aged-growth-v01.webp');fissure.colorSpace=THREE.NoColorSpace;fissure.flipY=false;fissure.wrapS=THREE.RepeatWrapping;fissure.wrapT=THREE.ClampToEdgeWrapping;fissure.anisotropy=4;
 textures.color.colorSpace=THREE.SRGBColorSpace;for(const name of ['roughness','normal'])if(textures[name])textures[name].colorSpace=THREE.NoColorSpace;for(const t of loaded){t.wrapS=t.wrapT=THREE.RepeatWrapping;t.anisotropy=4;}
 const wood=new THREE.MeshStandardMaterial({color:'#ffffff',roughness:.96,metalness:0});wood.defines={USE_UV1:'',USE_UV2:''};
 wood.onBeforeCompile=s=>{
  s.uniforms.nativeWoodNeutrality={value:refined?.68:.60};s.uniforms.nativeGrowthAmplitude={value:refined?.0021:.0019};s.uniforms.nativeWoodColor={value:textures.color};s.uniforms.nativeFissure={value:fissure};if(textures.roughness)s.uniforms.nativeWoodRough={value:textures.roughness};if(textures.normal)s.uniforms.nativeWoodNormal={value:textures.normal};
  s.vertexShader='varying vec2 vNativeMain;varying vec2 vNativeBranch;varying float vNativeBlend;varying vec2 vGrowthMain;varying vec2 vGrowthBranch;varying float vCalibre;\n'+s.vertexShader;
  s.vertexShader=s.vertexShader.replace('#include <begin_vertex>','#include <begin_vertex>\nvNativeMain=vec2(uv.x,(1.-uv.y)/.72)+vec2(.07,.11);vNativeBranch=vec2(uv1.x,(1.-uv1.y)/.72)+vec2(.38,.11);vNativeBlend=clamp(uv2.x,0.,1.);vGrowthMain=vec2(uv.x,(1.-uv.y)/2.8*1.10+.08);vGrowthBranch=vec2(uv1.x,(1.-uv1.y)/2.8*1.10+.08);vCalibre=clamp(1.-uv2.y,.08,1.);');
  s.fragmentShader='varying vec2 vNativeMain;varying vec2 vNativeBranch;varying float vNativeBlend;varying vec2 vGrowthMain;varying vec2 vGrowthBranch;varying float vCalibre;uniform sampler2D nativeWoodColor;uniform sampler2D nativeFissure;uniform float nativeWoodNeutrality;uniform float nativeGrowthAmplitude;\n'+(textures.roughness?'uniform sampler2D nativeWoodRough;\n':'')+(textures.normal?`uniform sampler2D nativeWoodNormal;
vec3 nativeWoodBump(vec3 geometric,vec3 surfacePosition,vec2 uv,vec3 value){vec3 a=dFdx(surfacePosition),b=dFdy(surfacePosition);vec2 ta=dFdx(uv),tb=dFdy(uv);vec3 bp=cross(b,geometric),ap=cross(geometric,a);vec3 tangent=bp*ta.x+ap*tb.x,bitangent=bp*ta.y+ap*tb.y;float scale=inversesqrt(max(max(dot(tangent,tangent),dot(bitangent,bitangent)),1e-12));vec3 n=value*2.-1.;n.xy*=.12+.05*vCalibre;return normalize(mat3(tangent*scale,bitangent*scale,geometric)*n);}
`:'')+s.fragmentShader;
  s.fragmentShader=s.fragmentShader.replace('#include <color_fragment>',`#include <color_fragment>
vec3 woodSample=mix(texture2D(nativeWoodColor,vNativeMain).rgb,texture2D(nativeWoodColor,vNativeBranch).rgb,vNativeBlend);float woodLuma=dot(woodSample,vec3(.2126,.7152,.0722));vec4 grownSurface=mix(texture2D(nativeFissure,vGrowthMain),texture2D(nativeFissure,vGrowthBranch),vNativeBlend);float fractureHeight=grownSurface.r;
// Warm low-saturation brown; no white deadwood or emissive silver accent.
diffuseColor.rgb=clamp(mix(woodSample,vec3(woodLuma),.76)*.86+vec3(.087,.078,.064),vec3(.074,.065,.052),vec3(.295,.268,.224))*(.97+.055*grownSurface.a);diffuseColor.a=1.;`);
  let maps='';if(textures.roughness)maps+='float woodRough=mix(texture2D(nativeWoodRough,vNativeMain).r,texture2D(nativeWoodRough,vNativeBranch).r,vNativeBlend);roughnessFactor=clamp(.916+.042*grownSurface.b+.022*woodRough,.916,.985);\n';
  if(textures.normal)maps+='vec3 woodMainNormal=nativeWoodBump(normal,-vViewPosition,vNativeMain,texture2D(nativeWoodNormal,vNativeMain).rgb),woodBranchNormal=nativeWoodBump(normal,-vViewPosition,vNativeBranch,texture2D(nativeWoodNormal,vNativeBranch).rgb);normal=normalize(mix(woodMainNormal,woodBranchNormal,vNativeBlend));float footprint=length(fwidth(vGrowthMain)*vec2(.912*max(vCalibre,.08),1.848));float smallFilter=1.-smoothstep(.0015,.004,footprint);float mediumHeight=(nativeGrowthAmplitude*(fractureHeight*2.-1.)+.00028*(grownSurface.g*2.-1.)*smallFilter)*(.25+.75*vCalibre);vec3 sigmaX=dFdx(-vViewPosition),sigmaY=dFdy(-vViewPosition),R1=cross(sigmaY,normal),R2=cross(normal,sigmaX);float det=dot(sigmaX,R1);vec3 heightGradient=sign(det)*(dFdx(mediumHeight)*R1+dFdy(mediumHeight)*R2);normal=normalize(abs(det)*normal-heightGradient);\n';
  s.fragmentShader=s.fragmentShader.replace('#include <normal_fragment_maps>','#include <normal_fragment_maps>\n'+maps);
 };
 wood.customProgramCacheKey=()=>`native-independent-wood-${mode}-${refined?'v6-bearing-return':'moon-measured-growth-domain-v03'}`;return {wood,twig:new THREE.MeshStandardMaterial({color:'#796c5a',roughness:.97,metalness:0})};
}
