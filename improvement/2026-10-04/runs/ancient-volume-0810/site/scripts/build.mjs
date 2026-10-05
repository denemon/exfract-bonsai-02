import {build} from 'vite';
import {symlink,readlink} from 'node:fs/promises';
import {fileURLToPath} from 'node:url';
import {resolve} from 'node:path';
const root=fileURLToPath(new URL('../',import.meta.url));
await build({root,configFile:false,build:{copyPublicDir:false}});
// The local review build shares immutable model/decoder/stills instead of copying them.
for(const name of ['models','draco','stills','still-manifest.json','bark','garden','rocks']){
  const path=resolve(root,'dist',name),target='../public/'+name;
  try{await symlink(target,path);}catch(e){if(e.code!=='EEXIST'||await readlink(path)!==target)throw e;}
}
