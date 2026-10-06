import {defineConfig} from '/Users/kazuki.tanaka/dev0/exfract-bonsai-02/node_modules/vite/dist/node/index.js';
import {createReadStream,statSync,readFileSync} from 'node:fs';import {createGzip,gzipSync} from 'node:zlib';import {fileURLToPath} from 'node:url';import {resolve,extname} from 'node:path';
const here=fileURLToPath(new URL('.',import.meta.url)),formal='/Users/kazuki.tanaka/dev0/exfract-bonsai-02',shared=resolve(here,'../../ancient-volume-0810/site/public'),best=resolve(here,'../../depth-balance-1905/candidate'),r21=resolve(here,'../../layer-balance-2055/candidate');
function isfile(p){try{return statSync(p).isFile()}catch{return false}}
function serve(server,preview=false){server.middlewares.use((req,res,next)=>{let path;try{path=decodeURIComponent(req.url.split('?')[0]);}catch{return next();}let folder,file,htmlPrefix='';const compare=path.match(/^\/compare\/(r20|r21|r22)(\/.*)?$/);
if(compare){const key=compare[1],tail=compare[2]&&compare[2]!=='/'?compare[2]:'/index.html',base=key==='r20'?best:key==='r21'?r21:here;
 if(tail.startsWith('/stills/')){folder=resolve(base,'public');file=resolve(folder,'.'+tail);if(key==='r22'&&!isfile(file)){folder=resolve(r21,'public');file=resolve(folder,'.'+tail);}}
 else if(key==='r22'&&!preview)return next();
 else{folder=resolve(base,'dist');file=resolve(folder,'.'+tail);if(key!=='r22')htmlPrefix='/compare/'+key;}
}
else if(path==='/'||path==='/index.html'||path.startsWith('/assets/')){folder=resolve(best,'dist');file=resolve(folder,path==='/'?'index.html':'.'+path);}
else if(path.startsWith('/stills/')||path.startsWith('/materials/')){folder=resolve(best,'public');file=resolve(folder,'.'+path);}
else if(/^\/(models|garden|rocks|draco|bark)\//.test(path)){folder=shared;file=resolve(folder,'.'+path);}
else if(path.startsWith('/qa/r22/')){folder=resolve(here,'../qa');file=resolve(folder,'.'+path.slice(7));}
else return next();
if(!file.startsWith(folder+'/'))return next();if(!isfile(file))return next();const info=statSync(file),type={'.html':'text/html; charset=utf-8','.js':'text/javascript','.css':'text/css','.wasm':'application/wasm','.jpg':'image/jpeg','.webp':'image/webp','.png':'image/png','.glb':'model/gltf-binary','.gz':'application/octet-stream','.json':'application/json'}[extname(file)]||'application/octet-stream';res.setHeader('Content-Type',type);res.setHeader('Cache-Control',/\.(js|css|html)$/.test(file)?'no-store':'public,max-age=3600');
if(htmlPrefix&&extname(file)==='.html'){const body=readFileSync(file,'utf8').replaceAll('="/assets/','="'+htmlPrefix+'/assets/').replaceAll('/stills/',htmlPrefix+'/stills/'),data=gzipSync(body);res.setHeader('Content-Encoding','gzip');res.setHeader('Content-Length',data.length);return res.end(req.method==='HEAD'?undefined:data);}
const compress=/\bgzip\b/.test(req.headers['accept-encoding']||'')&&/\.(js|css|html|wasm)$/.test(file);if(compress)res.setHeader('Content-Encoding','gzip');else res.setHeader('Content-Length',info.size);if(req.method==='HEAD')return res.end();compress?createReadStream(file).pipe(createGzip({level:6})).pipe(res):createReadStream(file).pipe(res);
});}
export default defineConfig({root:here,base:'/compare/r22/',publicDir:false,cacheDir:resolve(here,'../../hand-junction-1029/qa/vite-cache'),build:{copyPublicDir:false,emptyOutDir:false,chunkSizeWarningLimit:1100},server:{host:'127.0.0.1',port:5214,strictPort:true,headers:{'Cache-Control':'no-store'},fs:{allow:[formal]}},preview:{host:'127.0.0.1',port:5214,strictPort:true},plugins:[{name:'stable-best-root-separated-trials',configureServer:s=>serve(s,false),configurePreviewServer:s=>serve(s,true)}]});
