import {build} from '/Users/kazuki.tanaka/dev0/exfract-bonsai-02/node_modules/vite/dist/node/index.js';
import {fileURLToPath} from 'node:url';
const root=fileURLToPath(new URL('../site/',import.meta.url));
const result=await build({root,configFile:false,build:{write:false,copyPublicDir:false}});
console.log(JSON.stringify({diagnosticSourceBuild:true,wroteBundle:false,copiedAssets:false,outputs:(Array.isArray(result)?result:[result]).flatMap(r=>r.output.map(x=>({fileName:x.fileName,bytes:typeof x.code==='string'?Buffer.byteLength(x.code):Buffer.byteLength(x.source)})))}));
