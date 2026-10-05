import {defineConfig} from '/Users/kazuki.tanaka/dev0/exfract-bonsai-02/node_modules/vite/dist/node/index.js';
import {readFileSync,createReadStream,statSync} from 'node:fs';
import {fileURLToPath} from 'node:url';
import {resolve} from 'node:path';
const here=fileURLToPath(new URL('.',import.meta.url)),run=resolve(here,'..'),formal='/Users/kazuki.tanaka/dev0/exfract-bonsai-02',base=resolve(run,'../ancient-volume-0810/site'),entry=resolve(base,'src/main.js');
const edits=[
 ["import './style.css';","import './style.css';\nimport {applyCompact,structuralMaterial} from '/compact-preview.js';"],
 ["const query=new URLSearchParams(location.search),study=query.get('study')||'garden';","const query=new URLSearchParams(location.search),study=query.get('study')||'garden',compact=query.get('compact')==='compact-v01'&&!query.has('reference')?'compact-v01':null;"],
 ["['ancient-v01','ancient-v02'].includes(candidate)&&!reference?loader.loadAsync('/models/'+candidate+'.glb'):null","compact?loader.loadAsync('/models/compact-v01.glb'):['ancient-v01','ancient-v02'].includes(candidate)&&!reference?loader.loadAsync('/models/'+candidate+'.glb'):null"],
 ["model=gltf.scene;foliage=prepareFoliageLOD(gltf);","model=gltf.scene;if(compact&&wood)applyCompact(model,wood);foliage=prepareFoliageLOD(gltf);"],
 ["if(wood){const old=[];","if(wood&&!compact){const old=[];"],
 ["applyHeroMaterials(model,mats,study==='clay');stats.worldScale","applyHeroMaterials(model,mats,study==='clay');if(compact)structuralMaterial(model,study==='clay');stats.compact=model.userData.compact;stats.worldScale"]
];
export default defineConfig({root:here,publicDir:resolve(base,'public'),cacheDir:resolve(run,'../hand-junction-1029/qa/vite-cache'),server:{host:'127.0.0.1',port:5209,strictPort:true,fs:{allow:[formal]}},plugins:[{name:'readonly-stage12-harness',enforce:'pre',transform(code,id){if(id.split('?')[0]!==entry)return;let adapted=code;for(const [a,b]of edits){if(adapted.split(a).length!==2)throw Error('Protected entry anchor changed: '+a);adapted=adapted.replace(a,b);}return {code:adapted,map:null};},configureServer(server){server.middlewares.use((req,res,next)=>{if(req.url?.split('?')[0]!=='/models/compact-v01.glb')return next();const file=resolve(run,'models/compact-v01.glb');res.setHeader('Content-Type','model/gltf-binary');res.setHeader('Content-Length',statSync(file).size);res.setHeader('Cache-Control','no-store');if(req.method==='HEAD')return res.end();createReadStream(file).pipe(res);});}}]});
