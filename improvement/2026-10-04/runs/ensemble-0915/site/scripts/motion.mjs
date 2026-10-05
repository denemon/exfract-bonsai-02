import {createHash} from 'node:crypto';
import {spawn} from 'node:child_process';
import {mkdir,mkdtemp,readFile,writeFile,rm,unlink} from 'node:fs/promises';
import {join} from 'node:path';import {tmpdir} from 'node:os';import assert from 'node:assert/strict';
const gpuSamples=Number(process.env.QA_GPU_SAMPLES||15);assert.ok(Number.isInteger(gpuSamples)&&gpuSamples>=15&&gpuSamples<=122);
const out=process.env.QA_OUT||'qa/core';await mkdir(out,{recursive:true});
const cases=process.env.QA_CASES?JSON.parse(process.env.QA_CASES):[
 ['pc',1440,900,''],['mobile-390',390,844,''],['mobile-320',320,568,''],
 ['clay-front',1440,900,'?study=clay&yaw=0&bare=1'],['clay-three-quarter',1440,900,'?study=clay&yaw=55&bare=1'],['wood-detail',1440,900,'?detail=wood']];
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
 await call('Emulation.setEmulatedMedia',{features:[{name:'prefers-reduced-motion',value:'no-preference'}]});
 const motionCases=[['pc',1440,900,''],['mobile-390',390,844,''],['leaf-detail',1440,900,'?detail=leaf']];
 for(const [name,w,h,query] of motionCases){
  await call('Emulation.setDeviceMetricsOverride',{width:w,height:h,deviceScaleFactor:name==='mobile-390'?3:1,mobile:false});
  const u=new URL((process.env.QA_URL||'http://127.0.0.1:5207/')+query);u.searchParams.set('qa','motion-'+name);await call('Page.navigate',{url:u.href});
  let state;for(let n=0;n<200;n++){state=await ev(probe);if(state.ready&&state.url===u.href)break;await pause(100);}assert.ok(state.ready,'Ready before drag');for(let n=0;n<200&&state.stats.detailLoading;n++){await pause(50);state=await ev(probe)}assert.ok(!state.stats.detailError);await pause(150);
  const idleA=await call('Page.captureScreenshot',{format:'png',captureBeyondViewport:false});await pause(350);const idleB=await call('Page.captureScreenshot',{format:'png',captureBeyondViewport:false});const digest=b=>createHash('sha256').update(Buffer.from(b,'base64')).digest('hex');assert.equal(digest(idleA.data),digest(idleB.data),'Idle pixels stable');
  const x=Math.floor(w*.44),y=Math.floor(h*.52),offsets=[0,32,64,96,64,32,0],frames=[];await call('Input.dispatchMouseEvent',{type:'mousePressed',x,y,button:'left',buttons:1,clickCount:1});
  for(let k=0;k<offsets.length;k++){
   await call('Input.dispatchMouseEvent',{type:'mouseMoved',x:x+offsets[k],y,button:'left',buttons:1});await ev('new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))');
   const state=await ev(probe),shot=await call('Page.captureScreenshot',{format:'png',captureBeyondViewport:false});const f={index:k,offsetPx:offsets[k],sha256:digest(shot.data),camera:state.stats.camera,lod:state.stats.foliageLOD,triangles:state.stats.triangles,renderCpuMs:state.stats.framesMs.at(-1)};frames.push(f);if(process.env.QA_SAVE_MOTION_PNG!=='0')await writeFile(join(out,name+'-frame-'+k+'.png'),Buffer.from(shot.data,'base64'));
  }
  await call('Input.dispatchMouseEvent',{type:'mouseReleased',x,y,button:'left',buttons:0,clickCount:1});
  const pairs=[[0,6],[1,5],[2,4]].map(([a,b])=>({a,b,sameCamera:JSON.stringify(frames[a].camera)===JSON.stringify(frames[b].camera),samePixels:frames[a].sha256===frames[b].sha256,sameLOD:frames[a].lod.level===frames[b].lod.level,highGroups:[frames[a].lod.highGroups,frames[b].lod.highGroups]}));assert.ok(pairs.every(p=>p.sameCamera),'Forward reverse same exact camera');assert.ok(pairs.every(p=>p.samePixels),'Forward reverse same pixels, no hysteretic shadow or LOD flicker in sampled poses');
  assert.ok(Math.abs(frames[3].camera.yaw-frames[0].camera.yaw)>3.9,'Actual pointer drag changes camera');assert.equal(state.text,'');assert.equal(state.scroll,false);results.push({name,method:'Actual Mac Chrome pointer drag, forward and reverse, sequential PNG after two RAF; finite sampled poses, not continuous video',idlePixelStable:true,frames,pairs});console.log(JSON.stringify({name,idlePixelStable:true,pairs,levels:frames.map(f=>f.lod.level)}));
 }
 assert.equal(logs.length,0,'Ordinary capture must not contain shader errors, exceptions, or warnings');
}finally{await writeFile(join(out,'results.json'),JSON.stringify({results,logs},null,2));if(ws)ws.close();chrome.kill('SIGTERM');await writeFile(join(out,'chrome.log'),stderr);if(chrome.exitCode===null)await Promise.race([new Promise(resolve=>chrome.once('exit',resolve)),pause(2000)]);if(chrome.exitCode!==null){if(process.env.QA_PROFILE)await rm(profileLock,{recursive:true});else await rm(profile,{recursive:true,force:true});}}
