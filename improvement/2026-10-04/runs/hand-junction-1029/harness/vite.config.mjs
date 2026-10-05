import {defineConfig} from '/Users/kazuki.tanaka/dev0/exfract-bonsai-02/node_modules/vite/dist/node/index.js';
import {readFileSync,createReadStream,statSync} from 'node:fs';
import {fileURLToPath} from 'node:url';
import {resolve} from 'node:path';
const here=fileURLToPath(new URL('.',import.meta.url)),run=resolve(here,'..'),formal='/Users/kazuki.tanaka/dev0/exfract-bonsai-02',base=resolve(run,'../ancient-volume-0810/site'),entry=resolve(base,'src/main.js');
const edits=[
 ["import './style.css';","import './style.css';\nimport {applyManual,structuralMaterial} from '/manual-preview.js';"],
 ["const query=new URLSearchParams(location.search),study=query.get('study')||'garden';","const query=new URLSearchParams(location.search),study=query.get('study')||'garden',manual=query.get('manual')==='junction-v01'&&!query.has('reference')?'junction-v01':null;"],
 ["['ancient-v01','ancient-v02'].includes(candidate)&&!reference?loader.loadAsync('/models/'+candidate+'.glb'):null","manual?loader.loadAsync('/models/junction-v01.glb'):['ancient-v01','ancient-v02'].includes(candidate)&&!reference?loader.loadAsync('/models/'+candidate+'.glb'):null"],
 ["model=gltf.scene;foliage=prepareFoliageLOD(gltf);","model=gltf.scene;if(manual&&wood)applyManual(model,wood);foliage=prepareFoliageLOD(gltf);"],
 ["if(wood){const old=[];","if(wood&&!manual){const old=[];"],
 ["applyHeroMaterials(model,mats,study==='clay');stats.worldScale","applyHeroMaterials(model,mats,study==='clay');if(manual)structuralMaterial(model,study==='clay');stats.manual=model.userData.manual;stats.worldScale"]
];
export default defineConfig({root:here,publicDir:resolve(base,'public'),cacheDir:resolve(run,'qa/vite-cache'),server:{host:'127.0.0.1',port:5209,strictPort:true,fs:{allow:[formal]}},plugins:[{name:'readonly-stage12-harness',enforce:'pre',transform(code,id){if(id.split('?')[0]!==entry)return;let adapted=code;for(const [a,b]of edits){if(adapted.split(a).length!==2)throw Error('Protected entry anchor changed: '+a);adapted=adapted.replace(a,b);}return {code:adapted,map:null};},configureServer(server){server.middlewares.use((req,res,next)=>{if(req.url?.split('?')[0]!=='/models/junction-v01.glb')return next();const file=resolve(run,'models/junction-v01.glb');res.setHeader('Content-Type','model/gltf-binary');res.setHeader('Content-Length',statSync(file).size);res.setHeader('Cache-Control','no-store');if(req.method==='HEAD')return res.end();createReadStream(file).pipe(res);});}}]});
