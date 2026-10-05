import {spawn} from 'node:child_process';
import {mkdir,mkdtemp,readFile,writeFile,rm,unlink} from 'node:fs/promises';
import {join,resolve} from 'node:path';import {pathToFileURL} from 'node:url';import {tmpdir} from 'node:os';import assert from 'node:assert/strict';
const out=process.env.QA_OUT||'../qa';await mkdir(out,{recursive:true});
const version=process.env.QA_VERSION||'edge-v01';const cases=[[version+'-sections',1290,570],[version+'-control-net',1290,680]];
assert.ok(process.env.QA_PROFILE,'Set the one reusable dedicated QA_PROFILE');const profile=process.env.QA_PROFILE;
const profileLock=profile+'.active';
if(process.env.QA_PROFILE){await mkdir(profileLock);await mkdir(profile,{recursive:true});try{await unlink(join(profile,'DevToolsActivePort'));}catch(e){if(e.code!=='ENOENT')throw e;}}
const chrome=spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',['--headless','--disable-background-networking','--disable-component-update','--disable-features=OptimizationHints,OptimizationHintsFetching,OptimizationTargetPrediction','--disable-sync','--disable-default-apps','--no-first-run','--no-default-browser-check',`--user-data-dir=${profile}`,'--remote-debugging-address=127.0.0.1','--remote-debugging-port=0','about:blank'],{stdio:['ignore','ignore','pipe']});
let stderr='',ws,next=0,session;chrome.stderr.on('data',v=>stderr+=v);
const pending=new Map(),logs=[],results=[];const pause=ms=>new Promise(r=>setTimeout(r,ms));
function send(method,params={},s){return new Promise((resolve,reject)=>{const id=++next;const timer=setTimeout(()=>{pending.delete(id);reject(Error(method+' timed out'));},25000);pending.set(id,{resolve,reject,timer});ws.send(JSON.stringify({id,method,params,...(s?{sessionId:s}:{})}));});}
const call=(m,p={})=>send(m,p,session);
async function ev(expression){const r=await call('Runtime.evaluate',{expression,returnByValue:true,awaitPromise:true});if(r.exceptionDetails)throw Error(JSON.stringify(r.exceptionDetails));return r.result.value;}
const probe=`(()=>{const g=window.__garden;return {url:location.href,ready:g?.stats.ready||false,stats:g?.stats,text:document.body.innerText,viewport:[innerWidth,innerHeight],scroll:document.documentElement.scrollWidth>innerWidth||document.documentElement.scrollHeight>innerHeight,programs:g?.renderer.info.programs?.map(p=>p.diagnostics?{runnable:p.diagnostics.runnable,log:p.diagnostics.programLog}:null),userAgent:navigator.userAgent}})()`;
try{
 let info;for(let n=0;n<120;n++){try{info=await readFile(join(profile,'DevToolsActivePort'),'utf8');break;}catch{await pause(100);}}assert.ok(info,'Chrome started');
 const [port,path]=info.trim().split('\n');ws=new WebSocket(`ws://127.0.0.1:${port}${path}`);await new Promise((r,j)=>{ws.onopen=r;ws.onerror=j;});
 ws.onmessage=({data})=>{const m=JSON.parse(data),p=pending.get(m.id);if(p){clearTimeout(p.timer);pending.delete(m.id);m.error?p.reject(Error(JSON.stringify(m.error))):p.resolve(m.result);}else if(m.method==='Runtime.exceptionThrown'||m.method==='Log.entryAdded'||(m.method==='Runtime.consoleAPICalled'&&['error','warning'].includes(m.params.type)))logs.push(m);};
 const {targetId}=await send('Target.createTarget',{url:'about:blank'});({sessionId:session}=await send('Target.attachToTarget',{targetId,flatten:true}));for(const x of ['Runtime','Page','Log'])await call(x+'.enable');
 await call('Emulation.setEmulatedMedia',{features:[{name:'prefers-reduced-motion',value:'reduce'}]});
 for(const [name,w,h]of cases){
  await call('Emulation.setDeviceMetricsOverride',{width:w,height:h,deviceScaleFactor:1,mobile:false});
  const url=pathToFileURL(resolve(out,name+'.svg')).href;await call('Page.navigate',{url});
  let ready=false;for(let n=0;n<100;n++){try{ready=await ev(`location.href===${JSON.stringify(url)}&&document.readyState==='complete'&&document.documentElement.tagName.toLowerCase()==='svg'`);if(ready)break;}catch{}await pause(100);}
  assert.ok(ready,'Local SVG is loaded');await pause(100);
  const shot=await call('Page.captureScreenshot',{format:'png',captureBeyondViewport:false,clip:{x:0,y:0,width:w,height:h,scale:1}});
  await writeFile(join(out,name+'.png'),Buffer.from(shot.data,'base64'));results.push({name,url,viewport:[w,h],ready,browser:'Actual Mac Chrome CDP; same dedicated QA profile'});
 }
 assert.equal(logs.filter(x=>x.method==='Runtime.exceptionThrown').length,0);
}finally{await writeFile(join(out,version+'-diagram-captures.json'),JSON.stringify({results,logs},null,2));if(ws)ws.close();chrome.kill('SIGTERM');await writeFile(join(out,version+'-diagram-chrome.log'),stderr);if(chrome.exitCode===null)await Promise.race([new Promise(resolve=>chrome.once('exit',resolve)),pause(2000)]);if(chrome.exitCode!==null){if(process.env.QA_PROFILE)await rm(profileLock,{recursive:true});else await rm(profile,{recursive:true,force:true});}}
