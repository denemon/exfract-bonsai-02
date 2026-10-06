import * as THREE from 'three';
// Existing free, locally stored Cedar001 maps are a provisional wood texture,
// not an identification of the reference tree or a scan of that bonsai.
export async function makeNativeWoodFinish(mode='gray'){
 if(mode==='gray')return {wood:new THREE.MeshStandardMaterial({color:'#88847e',roughness:1,metalness:0}),twig:new THREE.MeshStandardMaterial({color:'#88847e',roughness:1,metalness:0})};
 if(mode==='checker'){
 const wood=new THREE.MeshStandardMaterial({color:'#ffffff',roughness:.96,metalness:0});wood.defines={USE_UV1:'',USE_UV2:''};wood.onBeforeCompile=s=>{
 s.vertexShader='varying vec2 vCheckMain;varying vec2 vCheckBranch;varying float vCheckBlend;\n'+s.vertexShader;
 s.vertexShader=s.vertexShader.replace('#include <begin_vertex>','#include <begin_vertex>\nvCheckMain=vec2(uv.x,(1.-uv.y)/.72);vCheckBranch=vec2(uv1.x,(1.-uv1.y)/.72);vCheckBlend=uv2.x;');
 s.fragmentShader='varying vec2 vCheckMain;varying vec2 vCheckBranch;varying float vCheckBlend;\n'+s.fragmentShader;
 s.fragmentShader=s.fragmentShader.replace('#include <color_fragment>',`#include <color_fragment>
 float mainGrid=mod(floor(vCheckMain.x*12.)+floor(vCheckMain.y*12.),2.),branchGrid=mod(floor(vCheckBranch.x*12.)+floor(vCheckBranch.y*12.),2.);float grid=mix(mainGrid,branchGrid,vCheckBlend);diffuseColor.rgb=mix(vec3(.055,.038,.024),vec3(.21,.15,.09),grid);`);
 };wood.customProgramCacheKey=()=> 'periodic-growth-checker-v1';return {wood,twig:new THREE.MeshStandardMaterial({color:'#514236',roughness:.97,metalness:0})};
 }
 if(mode==='base'){const wood=new THREE.MeshStandardMaterial({color:'#66584b',roughness:.96,metalness:0});wood.customProgramCacheKey=()=> 'native-independent-wood-base-v2-aligned';return {wood,twig:new THREE.MeshStandardMaterial({color:'#514236',roughness:.97,metalness:0})};}
 if(!['color','roughness','normal'].includes(mode))throw Error('Unknown native wood finish');
 const loader=new THREE.TextureLoader(),required=['color',...(mode==='color'?[]:['roughness']),...(mode==='normal'?['normal']:[])];
 const loaded=await Promise.all(required.map(n=>loader.loadAsync('/bark/'+n+'.webp'))),textures=Object.fromEntries(required.map((n,i)=>[n,loaded[i]]));
 const fissure=await loader.loadAsync('/compare/r28/materials/growth-fissures.webp');fissure.colorSpace=THREE.NoColorSpace;fissure.flipY=false;fissure.wrapS=THREE.RepeatWrapping;fissure.wrapT=THREE.ClampToEdgeWrapping;fissure.anisotropy=4;
 textures.color.colorSpace=THREE.SRGBColorSpace;for(const name of ['roughness','normal'])if(textures[name])textures[name].colorSpace=THREE.NoColorSpace;for(const t of loaded){t.wrapS=t.wrapT=THREE.RepeatWrapping;t.anisotropy=4;}
 const wood=new THREE.MeshStandardMaterial({color:'#ffffff',roughness:.96,metalness:0});wood.defines={USE_UV1:'',USE_UV2:''};
 wood.onBeforeCompile=s=>{
  s.uniforms.nativeWoodColor={value:textures.color};s.uniforms.nativeFissure={value:fissure};if(textures.roughness)s.uniforms.nativeWoodRough={value:textures.roughness};if(textures.normal)s.uniforms.nativeWoodNormal={value:textures.normal};
  s.vertexShader='varying vec2 vNativeMain;varying vec2 vNativeBranch;varying float vNativeBlend;varying vec2 vGrowthMain;varying vec2 vGrowthBranch;varying float vCalibre;\n'+s.vertexShader;
  s.vertexShader=s.vertexShader.replace('#include <begin_vertex>','#include <begin_vertex>\nvNativeMain=vec2(uv.x,(1.-uv.y)/.72)+vec2(.07,.11);vNativeBranch=vec2(uv1.x,(1.-uv1.y)/.72)+vec2(.38,.11);vNativeBlend=clamp(uv2.x,0.,1.);vGrowthMain=vec2(uv.x,(1.-uv.y)/2.8);vGrowthBranch=vec2(uv1.x,(1.-uv1.y)/2.8);vCalibre=clamp(1.-uv2.y,.08,1.);');
  s.fragmentShader='varying vec2 vNativeMain;varying vec2 vNativeBranch;varying float vNativeBlend;varying vec2 vGrowthMain;varying vec2 vGrowthBranch;varying float vCalibre;uniform sampler2D nativeWoodColor;uniform sampler2D nativeFissure;\n'+(textures.roughness?'uniform sampler2D nativeWoodRough;\n':'')+(textures.normal?`uniform sampler2D nativeWoodNormal;
vec3 nativeWoodBump(vec3 geometric,vec3 surfacePosition,vec2 uv,vec3 value){vec3 a=dFdx(surfacePosition),b=dFdy(surfacePosition);vec2 ta=dFdx(uv),tb=dFdy(uv);vec3 bp=cross(b,geometric),ap=cross(geometric,a);vec3 tangent=bp*ta.x+ap*tb.x,bitangent=bp*ta.y+ap*tb.y;float scale=inversesqrt(max(max(dot(tangent,tangent),dot(bitangent,bitangent)),1e-12));vec3 n=value*2.-1.;n.xy*=.12+.05*vCalibre;return normalize(mat3(tangent*scale,bitangent*scale,geometric)*n);}
`:'')+s.fragmentShader;
  s.fragmentShader=s.fragmentShader.replace('#include <color_fragment>',`#include <color_fragment>
vec3 woodSample=mix(texture2D(nativeWoodColor,vNativeMain).rgb,texture2D(nativeWoodColor,vNativeBranch).rgb,vNativeBlend);float woodLuma=dot(woodSample,vec3(.2126,.7152,.0722));float fractureHeight=mix(texture2D(nativeFissure,vGrowthMain).r,texture2D(nativeFissure,vGrowthBranch).r,vNativeBlend);
// Warm low-saturation brown; no white deadwood or emissive silver accent.
diffuseColor.rgb=clamp(mix(woodSample,vec3(woodLuma),.60)*1.20*(.92+.08*fractureHeight),vec3(.024,.022,.018),vec3(.215,.192,.165));diffuseColor.a=1.;`);
  let maps='';if(textures.roughness)maps+='float woodRough=mix(texture2D(nativeWoodRough,vNativeMain).r,texture2D(nativeWoodRough,vNativeBranch).r,vNativeBlend);roughnessFactor=clamp(.90+.075*woodRough+.02*(1.-fractureHeight),.90,.995);\n';
  if(textures.normal)maps+='vec3 woodMainNormal=nativeWoodBump(normal,-vViewPosition,vNativeMain,texture2D(nativeWoodNormal,vNativeMain).rgb),woodBranchNormal=nativeWoodBump(normal,-vViewPosition,vNativeBranch,texture2D(nativeWoodNormal,vNativeBranch).rgb);normal=normalize(mix(woodMainNormal,woodBranchNormal,vNativeBlend));float mediumHeight=.0008*(.25+.75*vCalibre)*fractureHeight;vec3 sigmaX=dFdx(-vViewPosition),sigmaY=dFdy(-vViewPosition),R1=cross(sigmaY,normal),R2=cross(normal,sigmaX);float det=dot(sigmaX,R1);vec3 heightGradient=sign(det)*(dFdx(mediumHeight)*R1+dFdy(mediumHeight)*R2);normal=normalize(abs(det)*normal-heightGradient);\n';
  s.fragmentShader=s.fragmentShader.replace('#include <normal_fragment_maps>','#include <normal_fragment_maps>\n'+maps);
 };
 wood.customProgramCacheKey=()=>`native-independent-wood-${mode}-v4-fissure-flow`;return {wood,twig:new THREE.MeshStandardMaterial({color:'#514236',roughness:.97,metalness:0})};
}
