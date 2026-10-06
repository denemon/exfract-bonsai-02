import {defineConfig} from '/Users/kazuki.tanaka/dev0/exfract-bonsai-02/node_modules/vite/dist/node/index.js';
import {createReadStream,statSync,readFileSync} from 'node:fs';import {createGzip,gzipSync} from 'node:zlib';import {fileURLToPath} from 'node:url';import {resolve,extname} from 'node:path';
const here=fileURLToPath(new URL('.',import.meta.url)),formal='/Users/kazuki.tanaka/dev0/exfract-bonsai-02',shared=resolve(here,'../../ancient-volume-0810/site/public'),best=resolve(here,'../../depth-balance-1905/candidate'),r21=resolve(here,'../../layer-balance-2055/candidate'),r22=resolve(here,'../../steady-render-2225/candidate'),r23=resolve(here,'../../native-grip-0017/candidate'),r24=resolve(here,'../../landmark-volume-0055/candidate'),r25=resolve(here,'../../root-flow-0206/candidate');
// Unadopted trials never replace the user TOP. Only an explicit completed
// local gate record can select this unchanged-R20 performance derivative.
function selectedRoot(){const choice=JSON.parse(readFileSync(resolve(here,'../routing.json'),'utf8'));return choice.adopted&&choice.relatedQAComplete?here:r25;}
function isfile(p){try{return statSync(p).isFile()}catch{return false}}
function serve(server,preview=false){server.middlewares.use((req,res,next)=>{let path;try{path=decodeURIComponent(req.url.split('?')[0]);}catch{return next();}let folder,file,htmlPrefix='';const compare=path.match(/^\/compare\/(r20|r21|r22|r23|r24|r25|r26)(\/.*)?$/);
if(compare){const key=compare[1],tail=compare[2]&&compare[2]!=='/'?compare[2]:'/index.html',base=key==='r20'?best:key==='r21'?r21:key==='r22'?r22:key==='r23'?r23:key==='r24'?r24:key==='r25'?r25:here;
 if((key==='r23'||key==='r24'||key==='r25'||key==='r26')&&tail.startsWith('/models/')){folder=resolve(base,'../models');file=resolve(folder,tail.slice(8));}
 else if((key==='r25'||key==='r26')&&tail.startsWith('/materials/')){folder=resolve(base,'../materials');file=resolve(folder,tail.slice(11));}
 else if(tail.startsWith('/stills/')){folder=resolve(base,'public');file=resolve(folder,'.'+tail);if(key==='r22'&&!isfile(file)){folder=resolve(r21,'public');file=resolve(folder,'.'+tail);}}
 else if(key==='r26'&&!preview)return next();
 else{folder=resolve(base,'dist');file=resolve(folder,'.'+tail);if(key==='r20'||key==='r21')htmlPrefix='/compare/'+key;}
}
else if(path==='/'||path==='/index.html'){folder=resolve(selectedRoot(),'dist');file=resolve(folder,'index.html');}
else if(path.startsWith('/assets/')){folder=resolve(best,'dist');file=resolve(folder,'.'+path);}
else if(path.startsWith('/stills/')||path.startsWith('/materials/')){folder=resolve(best,'public');file=resolve(folder,'.'+path);}
else if(/^\/(models|garden|rocks|draco|bark)\//.test(path)){folder=shared;file=resolve(folder,'.'+path);}
else if(path.startsWith('/qa/r26/')){folder=resolve(here,'../qa');file=resolve(folder,'.'+path.slice(7));}
else return next();
if(!file.startsWith(folder+'/'))return next();if(!isfile(file))return next();const info=statSync(file),type={'.html':'text/html; charset=utf-8','.js':'text/javascript','.css':'text/css','.wasm':'application/wasm','.jpg':'image/jpeg','.webp':'image/webp','.png':'image/png','.glb':'model/gltf-binary','.gz':'application/octet-stream','.json':'application/json'}[extname(file)]||'application/octet-stream';res.setHeader('Content-Type',/hero-(?:root-v02|age-v01)\.glb\.gz$/.test(file)?'model/gltf-binary':type);if(/hero-(?:root-v02|age-v01)\.glb\.gz$/.test(file))res.setHeader('Content-Encoding','gzip');res.setHeader('Cache-Control',/\.(js|css|html)$/.test(file)?'no-store':'public,max-age=3600');
if(htmlPrefix&&extname(file)==='.html'){const body=readFileSync(file,'utf8').replaceAll('="/assets/','="'+htmlPrefix+'/assets/').replaceAll('/stills/',htmlPrefix+'/stills/'),data=gzipSync(body);res.setHeader('Content-Encoding','gzip');res.setHeader('Content-Length',data.length);return res.end(req.method==='HEAD'?undefined:data);}
const compress=/\bgzip\b/.test(req.headers['accept-encoding']||'')&&/\.(js|css|html|wasm)$/.test(file);if(compress)res.setHeader('Content-Encoding','gzip');else res.setHeader('Content-Length',info.size);if(req.method==='HEAD')return res.end();compress?createReadStream(file).pipe(createGzip({level:6})).pipe(res):createReadStream(file).pipe(res);
});}
export default defineConfig({root:here,base:'/compare/r26/',publicDir:false,cacheDir:resolve(here,'../../hand-junction-1029/qa/vite-cache'),build:{copyPublicDir:false,emptyOutDir:false,chunkSizeWarningLimit:1100},server:{host:'127.0.0.1',port:5214,strictPort:true,headers:{'Cache-Control':'no-store'},fs:{allow:[formal]}},preview:{host:'127.0.0.1',port:5214,strictPort:true},plugins:[{name:'stable-best-root-separated-trials',configureServer:s=>serve(s,false),configurePreviewServer:s=>serve(s,true)}]});
