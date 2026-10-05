import {spawn} from 'node:child_process';
import {mkdtemp,readFile,writeFile,mkdir} from 'node:fs/promises';
import {join} from 'node:path';
import {tmpdir} from 'node:os';
import assert from 'node:assert/strict';
const out=process.env.QA_OUT||'qa/final';await mkdir(out,{recursive:true});
const profile=await mkdtemp(join(tmpdir(),'bonsai-02-qa-'));
const disabled=process.env.QA_DISABLE==='1',blocked=process.env.QA_BLOCK_APP==='1',stillOnly=disabled||blocked,prefix=blocked?'loading-':disabled?'fallback-':'';
const chrome=spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',['--headless','--no-first-run','--no-default-browser-check',`--user-data-dir=${profile}`,'--remote-debugging-address=127.0.0.1','--remote-debugging-port=0',...(disabled?['--disable-webgl']:[]),'about:blank'],{stdio:['ignore','ignore','pipe']});
const pause=ms=>new Promise(r=>setTimeout(r,ms));let errorLog='';chrome.stderr.on('data',x=>errorLog+=x);
let ws,id=0;const pending=new Map(),logs=[];
function send(method,params={},sessionId){return new Promise((resolve,reject)=>{const n=++id,timer=setTimeout(()=>{pending.delete(n);reject(new Error(method+' timeout'))},15000);pending.set(n,{resolve,reject,timer});ws.send(JSON.stringify({id:n,method,params,...(sessionId?{sessionId}:{})}))})}
async function ev(s,expression){const r=await send('Runtime.evaluate',{expression,returnByValue:true,awaitPromise:true},s);if(r.exceptionDetails)throw new Error(JSON.stringify(r.exceptionDetails));return r.result.value;}
const probe=`(()=>{const g=window.__garden,css=getComputedStyle(document.querySelector('#scene')),gl=g?.renderer.getContext(),debug=gl&&!gl.isContextLost()?gl.getExtension('WEBGL_debug_renderer_info'):null;return {devicePixelRatio,gpu:debug?{renderer:gl.getParameter(debug.UNMASKED_RENDERER_WEBGL),vendor:gl.getParameter(debug.UNMASKED_VENDOR_WEBGL)}:null,jsHeapBytes:performance.memory?.usedJSHeapSize,ready:document.documentElement.classList.contains('ready'),canvasVisible:css.visibility!=='hidden'&&Number(css.opacity)>0,stats:g?.stats,viewport:[innerWidth,innerHeight],still:{complete:document.querySelector('.still img').complete,width:document.querySelector('.still img').naturalWidth,src:document.querySelector('.still img').currentSrc},text:document.body.innerText,version:navigator.userAgent};})()`;
async function shot(s,name,w,h){const r=await send('Page.captureScreenshot',{format:'png',captureBeyondViewport:false,clip:{x:0,y:0,width:w,height:h,scale:1}},s);await writeFile(join(out,name+'.png'),Buffer.from(r.data,'base64'));}
const results=[];
try{
 let info;for(let n=0;n<140;n++){try{info=await readFile(join(profile,'DevToolsActivePort'),'utf8');break}catch{}await pause(100)}if(!info)throw new Error('Chrome unavailable');
 const [port,path]=info.trim().split('\n');ws=new WebSocket(`ws://127.0.0.1:${port}${path}`);await new Promise((r,j)=>{ws.onopen=r;ws.onerror=j});
 ws.onmessage=({data})=>{const msg=JSON.parse(data),p=pending.get(msg.id);if(p){clearTimeout(p.timer);pending.delete(msg.id);msg.error?p.reject(new Error(JSON.stringify(msg.error))):p.resolve(msg.result)}else if(msg.method==='Runtime.exceptionThrown'||msg.method==='Log.entryAdded')logs.push(msg)};
 const {targetId}=await send('Target.createTarget',{url:'about:blank'}),{sessionId:s}=await send('Target.attachToTarget',{targetId,flatten:true});await send('Runtime.enable',{},s);await send('Page.enable',{},s);await send('Log.enable',{},s);
 if(blocked){await send('Network.enable',{},s);await send('Network.setBlockedURLs',{urls:['*/assets/*.js']},s);}
 await send('Emulation.setEmulatedMedia',{features:[{name:'prefers-reduced-motion',value:'reduce'}]},s);
 const cases=[['desktop',1440,900],['mobile-390',390,844],['mobile-320',320,932],['landscape',844,390]];
 if(process.env.QA_EXTRA==='1')cases.push(['mobile-390-short',390,740],['mobile-320-short',320,568],['portrait-wide',768,1024]);
 if(process.env.QA_CASES)cases.splice(0,cases.length,...JSON.parse(process.env.QA_CASES));
 for(const [name,w,h]of cases){
  await send('Emulation.setDeviceMetricsOverride',{width:w,height:h,deviceScaleFactor:Number(process.env.QA_DPR||1),mobile:false},s);await send('Page.navigate',{url:process.env.QA_URL||'http://127.0.0.1:5182/'},s);
  let r;for(let n=0;n<120;n++){try{r=await ev(s,probe);if((stillOnly?r.still.width>0:r.ready)&&r.viewport[0]===w)break}catch{}await pause(150)}
  await pause(350);r=await ev(s,probe);await shot(s,prefix+name,w,h);assert.equal(r.text,'');assert.deepEqual(r.viewport,[w,h]);
  if(!stillOnly){assert.equal(r.ready,true);const b=r.stats.framing;assert.ok(b.left>.02&&b.right<.98&&b.top>.02&&b.bottom<.98,'subject fits with margin '+JSON.stringify(b));}
  else{assert.equal(r.ready,false);assert.equal(r.canvasVisible,false);assert.ok(r.still.width>0);}
  results.push({name,...r});console.log(JSON.stringify({name,ready:r.ready,stats:r.stats}));
  if(!stillOnly&&process.env.QA_MOTION_VIEWS==='1'){
   await send('Emulation.setEmulatedMedia',{features:[{name:'prefers-reduced-motion',value:'no-preference'}]},s);await pause(200);const sampleStart=await ev(s,'({frames:window.__garden.stats.frames,now:performance.now()})');await pause(1400);const sampleEnd=await ev(s,'({frames:window.__garden.stats.frames,now:performance.now()})');results.push({name:name+'-motion',sample:{durationMs:sampleEnd.now-sampleStart.now,frames:sampleEnd.frames-sampleStart.frames,fps:(sampleEnd.frames-sampleStart.frames)*1000/(sampleEnd.now-sampleStart.now)},...(await ev(s,probe))});
   await send('Emulation.setEmulatedMedia',{features:[{name:'prefers-reduced-motion',value:'reduce'}]},s);await pause(150);
  }
 }
 if(!stillOnly&&process.env.QA_FULL==='1'){
  for(const [w,h]of [[390,844],[320,568],[1440,900],[844,390]]){
   await send('Emulation.setDeviceMetricsOverride',{width:w,height:h,deviceScaleFactor:Number(process.env.QA_DPR||1),mobile:false},s);await pause(250);
   const resized=await ev(s,probe),b=resized.stats.framing;assert.deepEqual(resized.viewport,[w,h]);assert.equal(resized.ready,true);assert.ok(b.left>.02&&b.right<.98&&b.top>.02&&b.bottom<.98);results.push({name:`resize-${w}-${h}`,...resized});
  }
  const before=await ev(s,'window.__garden.stats.frames');await pause(400);const after=await ev(s,'window.__garden.stats.frames');assert.equal(before,after,'reduced motion stops loop');results.push({name:'reduced-motion',before,after});
  await send('Emulation.setEmulatedMedia',{features:[{name:'prefers-reduced-motion',value:'no-preference'}]},s);await pause(2500);results.push({name:'motion-performance',...(await ev(s,probe))});
  await ev(s,`window.__qaLose=window.__garden.renderer.getContext().getExtension('WEBGL_lose_context');window.__qaLose.loseContext()`);await pause(300);const lost=await ev(s,probe);assert.equal(lost.ready,false);assert.equal(lost.canvasVisible,false);assert.ok(lost.still.width>0);await shot(s,'context-lost',844,390);results.push({name:'context-lost',...lost});
  await ev(s,`window.__qaLose.restoreContext()`);await pause(2500);assert.equal((await ev(s,probe)).ready,true);results.push({name:'context-restored',...(await ev(s,probe))});
 }
 await writeFile(join(out,prefix+'results.json'),JSON.stringify({results,logs},null,2));assert.ok(!logs.some(x=>x.method==='Runtime.exceptionThrown'),'no browser exceptions');
}finally{if(ws)ws.close();chrome.kill('SIGTERM');await writeFile(join(out,disabled?'fallback-chrome.log':'chrome.log'),errorLog);}
