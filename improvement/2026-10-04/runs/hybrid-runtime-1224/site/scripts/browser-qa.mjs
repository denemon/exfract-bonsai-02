import { spawn } from 'node:child_process';
import { mkdtemp, readFile, writeFile, mkdir } from 'node:fs/promises';
import { join } from 'node:path';
import { tmpdir } from 'node:os';
import assert from 'node:assert/strict';

const mode = process.env.QA_MODE || 'normal';
const out = process.env.QA_OUT || `qa/${mode}`;
const url = process.env.QA_URL || 'http://127.0.0.1:5187/';
const dpr = Number(process.env.QA_DPR || 1);
await mkdir(out, { recursive: true });
const profile = await mkdtemp(join(tmpdir(), 'bonsai-hybrid-qa-'));
const chrome = spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', [
  '--headless', '--no-first-run', '--no-default-browser-check', `--user-data-dir=${profile}`,
  '--remote-debugging-address=127.0.0.1', '--remote-debugging-port=0',
  ...(mode === 'no-webgl' ? ['--disable-webgl'] : []), 'about:blank',
], { stdio: ['ignore', 'ignore', 'pipe'] });
let stderr = '', ws, nextId = 0, session;
chrome.stderr.on('data', data => stderr += data);
const requests = new Map(), logs = [], results = [];
const pause = ms => new Promise(resolve => setTimeout(resolve, ms));
function send(method, params = {}, sessionId) {
  return new Promise((resolve, reject) => {
    const id = ++nextId;
    const timer = setTimeout(() => { requests.delete(id); reject(new Error(`${method} timed out`)); }, 15000);
    requests.set(id, { resolve, reject, timer });
    ws.send(JSON.stringify({ id, method, params, ...(sessionId ? { sessionId } : {}) }));
  });
}
const call = (method, params = {}) => send(method, params, session);
async function evaluate(expression) {
  const r = await call('Runtime.evaluate', { expression, returnByValue: true, awaitPromise: true });
  if (r.exceptionDetails) throw new Error(JSON.stringify(r.exceptionDetails));
  return r.result.value;
}
const probe = `(() => {
  const i = document.querySelector('picture img'), c = document.querySelector('canvas');
  return { ready: !!(i?.complete && i.naturalWidth), location: location.href, viewport: [innerWidth, innerHeight], dpr: devicePixelRatio,
    source: i?.currentSrc, naturalSize: [i?.naturalWidth,i?.naturalHeight], text: document.body.innerText,
    scroll: document.documentElement.scrollWidth > innerWidth || document.documentElement.scrollHeight > innerHeight,
    canvasVisible: c && getComputedStyle(c).opacity !== '0' && getComputedStyle(c).visibility !== 'hidden',
    stats: window.__bonsai?.stats || null, userAgent: navigator.userAgent,
    resources: performance.getEntriesByType('resource').map(r=>({name:r.name.split('/').pop(),bytes:r.transferSize,duration:r.duration})),
    longTasks: window.__longTasks || [] };
})()`;
async function waitFor(predicate, name) {
  let value;
  for (let n = 0; n < 100; n++) {
    value = await evaluate(probe);
    if (predicate(value)) return value;
    await pause(100);
  }
  throw new Error(`${name}: ${JSON.stringify(value)}`);
}
async function screenshot(name, width, height) {
  const r = await call('Page.captureScreenshot', { format: 'png', captureBeyondViewport: false,
    clip: { x: 0, y: 0, width, height, scale: 1 } });
  await writeFile(join(out, `${name}.png`), Buffer.from(r.data, 'base64'));
}
const setMotion = value => call('Emulation.setEmulatedMedia', { features: [{ name: 'prefers-reduced-motion', value }] });
const point = (x,y) => call('Input.dispatchMouseEvent', { type: 'mouseMoved', x, y });
try {
  let portInfo;
  for (let n = 0; n < 140; n++) {
    try { portInfo = await readFile(join(profile, 'DevToolsActivePort'), 'utf8'); break; } catch { await pause(100); }
  }
  assert.ok(portInfo, 'Chrome started');
  const [port, path] = portInfo.trim().split('\n');
  ws = new WebSocket(`ws://127.0.0.1:${port}${path}`);
  await new Promise((resolve, reject) => { ws.onopen = resolve; ws.onerror = reject; });
  ws.onmessage = ({ data }) => {
    const msg = JSON.parse(data), request = requests.get(msg.id);
    if (request) {
      clearTimeout(request.timer); requests.delete(msg.id);
      msg.error ? request.reject(new Error(JSON.stringify(msg.error))) : request.resolve(msg.result);
    } else if (msg.method === 'Runtime.exceptionThrown' || msg.method === 'Log.entryAdded') logs.push(msg);
  };
  const { targetId } = await send('Target.createTarget', { url: 'about:blank' });
  ({ sessionId: session } = await send('Target.attachToTarget', { targetId, flatten: true }));
  for (const domain of ['Page', 'Runtime', 'Log', 'Network', 'Performance']) await call(`${domain}.enable`);
  await call('Page.addScriptToEvaluateOnNewDocument', { source: `window.__longTasks=[];new PerformanceObserver(l=>{window.__longTasks.push(...l.getEntries().map(e=>({start:e.startTime,duration:e.duration})));}).observe({type:'longtask',buffered:true});` });
  if (mode === 'blocked-js') await call('Network.setBlockedURLs', { urls: ['*/src/*.js', '*/assets/*.js', '*/node_modules/*.js'] });
  await setMotion('reduce');
  const basic = [['desktop',1440,900,'desktop'],['mobile-390',390,844,'portrait'],['mobile-320',320,932,'tall']];
  const extra = [['desktop-16-9',1920,1080,'wide'],['landscape',844,390,'wide'],['tablet',768,1024,'portrait'],
    ['square',1024,1024,'square'],['mobile-390-short',390,740,'portrait'],['mobile-320-short',320,568,'portrait'],
    ['ultrawide',2560,1080,'wide'],['desktop-5-4',1280,1024,'square']];
  const cases = mode === 'normal' && process.env.QA_BASIC !== '1' ? [...basic,...extra] : basic;
  for (const [name,width,height,source] of cases) {
    await call('Emulation.setDeviceMetricsOverride', { width, height, deviceScaleFactor: dpr, mobile: false });
    const viewURL=new URL(url);viewURL.searchParams.set('qa',name);
    await call('Page.navigate', { url: viewURL.href });
    const state = await waitFor(r=>r.location === viewURL.href && r.ready && r.source.endsWith(`/${source}.webp`) &&
      (mode === 'blocked-js' || r.stats?.imageReady),name);
    await pause(100); await screenshot(name,width,height);
    assert.equal(state.text,''); assert.equal(state.scroll,false); assert.equal(state.canvasVisible,false);
    if (mode !== 'blocked-js') { assert.equal(state.stats.reducedMotion,true); assert.equal(state.stats.frames,0); }
    results.push({ name,...state });
    console.log(`${name}: ${source}, full image ready, no text/scroll`);
  }
  if (mode !== 'blocked-js' && process.env.QA_BASIC !== '1') {
    await call('Emulation.setDeviceMetricsOverride', { width:1440,height:900,deviceScaleFactor:dpr,mobile:false });
    const motionURL=new URL(url);motionURL.searchParams.set('qa','motion');
    await setMotion('no-preference'); await call('Page.navigate',{url:motionURL.href});
    await waitFor(r=>r.location === motionURL.href && r.ready && r.stats,'motion image'); await point(1390,80);
    if (mode === 'no-webgl') {
      const state = await waitFor(r=>r.stats?.fallbackReason === 'webgl-unavailable','no WebGL');
      assert.equal(state.canvasVisible,false); assert.equal(state.ready,true);
      await screenshot('no-webgl',1440,900); results.push({name:'no-webgl',...state});
    } else {
      let state = await waitFor(r=>r.stats?.mode === 'relief','pointer relief');
      assert.equal(state.stats.pointerFine,true);
      await pause(1000); await screenshot('motion-right',1440,900);
      results.push({name:'motion-right',...(await evaluate(probe))});
      await point(40,820); await pause(1000); await screenshot('motion-left',1440,900);
      state = await evaluate(probe); assert.ok(state.stats.maxOffsetPixels < 2,'movement remains below two CSS pixels');
      const idleBefore=state.stats.frames; await pause(400); assert.equal((await evaluate(probe)).stats.frames,idleBefore,'idle loop stops');
      results.push({name:'motion-left-idle',...state,idleFramesOver400ms:0});
      const frameStart=state.stats.frames, started=Date.now();
      for(let i=0;i<24;i++){await point(180+i*45,300+Math.sin(i/4)*120);await pause(32);}
      state=await evaluate(probe);results.push({name:'moving-performance',durationMs:Date.now()-started,frames:state.stats.frames-frameStart,...state});
      await setMotion('reduce');
      state=await waitFor(r=>r.stats?.reducedMotion && !r.stats.engineReady,'reduced motion change');
      assert.equal(state.canvasVisible,false); assert.equal(state.stats.engineReady,false);
      const reducedBefore=state.stats.frames;await pause(300);assert.equal((await evaluate(probe)).stats.frames,reducedBefore);
      await screenshot('reduced-motion',1440,900);results.push({name:'reduced-motion',...state,framesOver300ms:0});
      await setMotion('no-preference');await point(1100,350);await waitFor(r=>r.stats?.mode==='relief','context setup');
      await evaluate(`window.__loss=window.__bonsai.renderer.getContext().getExtension('WEBGL_lose_context');window.__loss.loseContext()`);
      state=await waitFor(r=>r.stats?.contextLost,'context lost');assert.equal(state.canvasVisible,false);assert.ok(state.ready);
      await screenshot('context-lost',1440,900);results.push({name:'context-lost',...state});
      await pause(180);await evaluate('window.__loss.restoreContext()');await pause(700);await point(1150,380);
      state=await waitFor(r=>r.stats?.mode==='relief'&&!r.stats.contextLost,'context restored');results.push({name:'context-restored',...state});
      await setMotion('reduce');
      // Source switching after a live engine must return to the matching complete still.
      for(const [width,height,source]of [[390,844,'portrait'],[320,932,'tall'],[844,390,'wide'],[1024,1024,'square'],[1440,900,'desktop']]){
        await call('Emulation.setDeviceMetricsOverride',{width,height,deviceScaleFactor:dpr,mobile:false});
        state=await waitFor(r=>r.ready&&r.source.endsWith(`/${source}.webp`)&&r.viewport[0]===width,'resize');
        assert.equal(state.canvasVisible,false);results.push({name:`resize-${width}-${height}`,...state});
      }
      results.push({name:'heap',metrics:await call('Performance.getMetrics'),heap:await call('Runtime.getHeapUsage')});
    }
  }
  assert.equal(logs.filter(x=>x.method==='Runtime.exceptionThrown').length,0,'no uncaught runtime exceptions');
} finally {
  await writeFile(join(out,'results.json'),JSON.stringify({mode,dpr,url,results,logs},null,2));
  if(ws)ws.close();chrome.kill('SIGTERM');await writeFile(join(out,'chrome.log'),stderr);
}
