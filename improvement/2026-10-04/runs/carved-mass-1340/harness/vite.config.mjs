import {defineConfig} from '/Users/kazuki.tanaka/dev0/exfract-bonsai-02/node_modules/vite/dist/node/index.js';
import {readFileSync,createReadStream,statSync} from 'node:fs';
import {fileURLToPath} from 'node:url';
import {resolve} from 'node:path';
const here=fileURLToPath(new URL('.',import.meta.url)),run=resolve(here,'..'),formal='/Users/kazuki.tanaka/dev0/exfract-bonsai-02',base=resolve(run,'../ancient-volume-0810/site'),entry=resolve(base,'src/main.js');
const edits=[
 ["yaw=baseYaw;pitch=Number(query.get('pitch')??(portrait?9:10));","if(query.get('composition')==='designed'&&portrait)baseYaw=ratio<.52?-30:-33;yaw=baseYaw;pitch=Number(query.get('pitch')??(portrait?(query.get('composition')==='designed'?8:9):10));"],
 ["import {createScene,loadGardenAssets} from './scene.js';","import {createScene,loadGardenAssets} from '/background-scene.js';"],
 ["if(query.get('frame')==='shared'){for(const x of [-1.55,1.30])for(const y of [-.08,2.28])for(const z of [-.72,.68])","if(query.get('frame')==='shared'){for(const x of [-1.48,1.42])for(const y of [-.08,2.50])for(const z of [-.72,.68])"],
 ["import './style.css';","import './style.css';\nimport {applyStructure,structuralMaterial} from '/carved-preview.js';"],
 ["const query=new URLSearchParams(location.search),study=query.get('study')||'garden';","const query=new URLSearchParams(location.search),study=query.get('study')||'garden',structure=['carved-v01','carved-v02'].includes(query.get('irregular'))&&!query.has('reference')?query.get('irregular'):null;"],
 ["['ancient-v01','ancient-v02'].includes(candidate)&&!reference?loader.loadAsync('/models/'+candidate+'.glb'):null","structure?loader.loadAsync('/models/'+structure+'.glb'):['ancient-v01','ancient-v02'].includes(candidate)&&!reference?loader.loadAsync('/models/'+candidate+'.glb'):null"],
 ["model=gltf.scene;foliage=prepareFoliageLOD(gltf);","model=gltf.scene;if(structure&&wood)applyStructure(model,wood);foliage=prepareFoliageLOD(gltf);"],
 ["if(wood){const old=[];","if(wood&&!structure){const old=[];"],
 ["applyHeroMaterials(model,mats,study==='clay');stats.worldScale","applyHeroMaterials(model,mats,study==='clay');if(structure||query.has('comparison'))structuralMaterial(model,study==='clay');stats.structure=model.userData.structure;stats.worldScale"]
];
export default defineConfig({root:here,publicDir:resolve(base,'public'),cacheDir:resolve(run,'../hand-junction-1029/qa/vite-cache'),server:{host:'127.0.0.1',port:5209,strictPort:true,fs:{allow:[formal]}},plugins:[{name:'readonly-stage12-carved-harness',enforce:'pre',transform(code,id){if(id.split('?')[0]!==entry)return;let adapted=code;for(const [a,b]of edits){if(adapted.split(a).length!==2)throw Error('Protected entry anchor changed: '+a);adapted=adapted.replace(a,b);}return {code:adapted,map:null};},configureServer(server){server.middlewares.use((req,res,next)=>{const path=req.url?.split('?')[0];if(!['/models/carved-v01.glb','/models/carved-v02.glb'].includes(path))return next();const file=resolve(run,'models',path.split('/').pop());res.setHeader('Content-Type','model/gltf-binary');res.setHeader('Content-Length',statSync(file).size);res.setHeader('Cache-Control','no-store');if(req.method==='HEAD')return res.end();createReadStream(file).pipe(res);});}}]});
