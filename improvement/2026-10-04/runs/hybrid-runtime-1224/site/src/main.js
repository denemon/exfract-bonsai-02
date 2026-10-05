const image = document.querySelector('#scene-image');
const canvas = document.querySelector('canvas');
const motion = matchMedia('(prefers-reduced-motion: reduce)');
const fine = matchMedia('(hover: hover) and (pointer: fine)');
const stats = {
  imageReady: false, engineReady: false, mode: 'loading-image',
  source: '', frames: 0, running: false, reducedMotion: motion.matches,
  pointerFine: fine.matches, contextLost: false, fallbackReason: null,
  offset: [0, 0], maxOffsetPixels: 0, frameTimes: [],
};
let engine, pending, epoch = 0, raf = 0, lastTime = 0, lastDraw = 0;
let target = [0, 0], offset = [0, 0];

function permitted() {
  return fine.matches && !motion.matches && !document.hidden && innerWidth >= 768 &&
    !navigator.connection?.saveData && stats.imageReady && !stats.contextLost;
}
function stop() {
  cancelAnimationFrame(raf); raf = 0; lastTime = 0; stats.running = false;
}
function showStill() {
  stop(); offset = [0, 0]; target = [0, 0]; stats.offset = [0, 0];
  canvas.style.opacity = '0';
  stats.mode = stats.imageReady ? 'still' : 'loading-image';
}
function dispose() {
  epoch++; showStill(); engine?.dispose(); engine = undefined;
  stats.engineReady = false; pending = undefined;
}
function imageChanged() {
  if (!image.complete || !image.naturalWidth) return;
  const changed = stats.source !== image.currentSrc;
  if (changed) dispose();
  stats.source = image.currentSrc; stats.imageReady = true;
  if (!engine) stats.mode = 'still';
}
image.addEventListener('load', imageChanged);
imageChanged();

async function getEngine() {
  if (engine) return engine;
  if (stats.fallbackReason === 'webgl-unavailable' || stats.fallbackReason === 'renderer-unavailable') return;
  if (pending) return pending;
  const version = epoch;
  pending = (async () => {
    try {
      const { createRelief } = await import('./relief.js');
      if (version !== epoch || !permitted()) return;
      const preparedAt = performance.now();
      const next = await createRelief(canvas, image);
      if (!next) { stats.fallbackReason = 'webgl-unavailable'; return; }
      if (version !== epoch || !permitted()) { next.dispose(); return; }
      engine = next; stats.engineReady = true;
      stats.enginePrepareMs = performance.now() - preparedAt;
      stats.geometryTriangles = next.triangles;
      stats.texturePixels = image.naturalWidth * image.naturalHeight;
      stats.fallbackReason = null;
      return next;
    } catch {
      stats.fallbackReason = 'renderer-unavailable';
      showStill();
    } finally { if (version === epoch) pending = undefined; }
  })();
  return pending;
}

function draw(now) {
  raf = 0;
  if (!engine || !permitted()) { showStill(); return; }
  const dt = lastTime ? Math.min(now - lastTime, 80) : 33;
  if (lastDraw && now - lastDraw < 31) { raf = requestAnimationFrame(draw); return; }
  lastTime = now; lastDraw = now;
  const mix = 1 - Math.exp(-dt / 105);
  offset = offset.map((value, index) => value + (target[index] - value) * mix);
  const settled = offset.every((value, index) => Math.abs(value - target[index]) < 0.00006);
  if (settled) offset = [...target];
  if (settled && target[0] === 0 && target[1] === 0) { showStill(); return; }
  const started = performance.now();
  engine.render(offset);
  stats.frameTimes.push(performance.now() - started);
  if (stats.frameTimes.length > 120) stats.frameTimes.shift();
  stats.frames++; stats.offset = [...offset];
  stats.maxOffsetPixels = engine.maxOffsetPixels(offset);
  stats.mode = 'relief'; canvas.style.opacity = '1';
  if (!settled) raf = requestAnimationFrame(draw);
  else { stats.running = false; lastTime = 0; }
}
function wake() {
  if (!raf && engine && permitted()) {
    stats.running = true; lastTime = 0; raf = requestAnimationFrame(draw);
  }
}
async function move(event) {
  if (event.pointerType !== 'mouse' || !permitted()) return;
  target = [Math.max(-1, Math.min(1, event.clientX / innerWidth * 2 - 1)) * 0.012,
    Math.max(-1, Math.min(1, 1 - event.clientY / innerHeight * 2)) * 0.009];
  await getEngine(); wake();
}
window.addEventListener('pointermove', move, { passive: true });
document.documentElement.addEventListener('pointerleave', () => { target = [0, 0]; wake(); });
window.addEventListener('blur', showStill);
document.addEventListener('visibilitychange', showStill);
function preferenceChanged() {
  stats.reducedMotion = motion.matches; stats.pointerFine = fine.matches;
  if (!permitted()) dispose();
}
motion.addEventListener('change', preferenceChanged);
fine.addEventListener('change', preferenceChanged);
window.addEventListener('resize', () => { dispose(); imageChanged(); }, { passive: true });
canvas.addEventListener('webglcontextlost', (event) => {
  event.preventDefault(); stats.contextLost = true; stats.fallbackReason = 'context-lost'; dispose();
});
canvas.addEventListener('webglcontextrestored', () => {
  stats.contextLost = false; stats.fallbackReason = null;
  showStill();
});

// Read-only diagnostics for the local browser verification; nothing is rendered as UI.
window.__bonsai = {
  stats,
  get renderer() { return engine?.renderer; },
  get image() { return image; },
};
