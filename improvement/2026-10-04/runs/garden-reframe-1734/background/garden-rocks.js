import * as THREE from 'three';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';
import {DRACOLoader} from 'three/addons/loaders/DRACOLoader.js';

export async function loadGardenRocks(sharedLoader){
 const draco=sharedLoader?null:new DRACOLoader().setDecoderPath('/draco/'),loader=sharedLoader||new GLTFLoader().setDRACOLoader(draco),textures=new THREE.TextureLoader();
 try{return await Promise.all(['boulder_01','rock_09'].map(async id=>{
  const [gltf,...maps]=await Promise.all([loader.loadAsync('/rocks/'+id+'.glb'),...['diff','nor_gl','arm'].map(n=>textures.loadAsync('/rocks/'+id+'_'+n+'.webp'))]);
  gltf.scene.updateMatrixWorld(true);let geometry;gltf.scene.traverse(o=>{if(o.isMesh){if(geometry)throw Error('Garden stone must be one mesh');geometry=o.geometry.clone().applyMatrix4(o.matrixWorld);}});
  if(!geometry?.attributes.uv)throw Error('Garden stone UVs missing');
  maps[0].colorSpace=THREE.SRGBColorSpace;for(const t of maps){t.flipY=false;t.anisotropy=4;}
  return {id,geometry,maps};
 }));}finally{draco?.dispose();}
}

export function placeGardenRocks(scene,assets,gardenMaterials){
 const finish=new URLSearchParams(location.search).get("finish")==="material-v01";
 const placements=[{id:'boulder_01',center:[-1.08,.72],horizontalExtent:.58,yaw:1.20,burial:.19},{id:'rock_09',center:[-1.10,-1.10],horizontalExtent:.80,yaw:.85,burial:.06}],rows=[];
 for(const [i,asset]of assets.entries()){
  const p=placements[i],g=asset.geometry;g.rotateY(p.yaw);g.computeBoundingBox();let b=g.boundingBox,size=b.getSize(new THREE.Vector3()),centre=b.getCenter(new THREE.Vector3());
  const scale=p.horizontalExtent/Math.max(size.x,size.z);g.translate(-centre.x,-b.min.y,-centre.z);g.scale(scale,scale,scale);g.translate(p.center[0],-.022-p.burial,p.center[1]);g.computeBoundingBox();
  const [color,normal,arm]=asset.maps,m=new THREE.MeshStandardMaterial({color:'#bdc5bc',map:color,normalMap:normal,normalScale:new THREE.Vector2(.67,.67),aoMap:arm,aoMapIntensity:.70,roughnessMap:arm,roughness:1,metalness:0});
  m.onBeforeCompile=s=>{
   s.uniforms.rockTerrain={value:gardenMaterials.terrain};s.uniforms.rockMoss={value:gardenMaterials.ground.userData.mossTexture};
   s.vertexShader='varying vec3 vRockWorld;\n'+s.vertexShader;s.vertexShader=s.vertexShader.replace('#include <begin_vertex>','#include <begin_vertex>\nvRockWorld=(modelMatrix*vec4(transformed,1.)).xyz;');
   s.fragmentShader='varying vec3 vRockWorld;uniform sampler2D rockTerrain;uniform sampler2D rockMoss;\n'+s.fragmentShader;
   s.fragmentShader=s.fragmentShader.replace('#include <color_fragment>',`#include <color_fragment>
    ${finish?'float mineralLuma=dot(diffuseColor.rgb,vec3(.2126,.7152,.0722));diffuseColor.rgb=mix(diffuseColor.rgb,vec3(mineralLuma)*vec3(.97,1.01,1.035),.78);':''}
    vec3 field=texture2D(rockTerrain,(vRockWorld.xz-vec2(-6.,-7.))/vec2(12.,14.)).rgb;
    float ground=-.022+field.b*.30;
    float rooted=1.-smoothstep(.009,.073,vRockWorld.y-ground);
    vec3 growing=texture2D(rockMoss,vRockWorld.xz/.42).rgb;
    diffuseColor.rgb=mix(diffuseColor.rgb,growing*.88,rooted*field.r*.74);
   `);
   s.fragmentShader=s.fragmentShader.replace('#include <roughnessmap_fragment>','#include <roughnessmap_fragment>\nroughnessFactor=max(roughnessFactor,.90);');
  };
  m.customProgramCacheKey=()=>asset.id+'-grounded-scan-v1-'+finish;
  const rock=new THREE.Mesh(g,m);rock.name='Partly buried scanned garden stone '+asset.id;rock.castShadow=rock.receiveShadow=true;scene.add(rock);
  const triangles=g.index?g.index.count/3:g.attributes.position.count/3;
  rows.push({...p,triangles,bounds:{min:g.boundingBox.min.toArray(),max:g.boundingBox.max.toArray()},material:'Local CC0 PBR, matte roughness lower bound .90, ground-field root transition',source:'https://polyhaven.com/a/'+asset.id,textures:asset.maps.map(t=>({url:t.image.src,width:t.image.width,height:t.image.height}))});
 }
 return rows;
}
