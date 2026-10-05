import {
  WebGLRenderer, Scene, PerspectiveCamera, PlaneGeometry, MeshBasicMaterial,
  Mesh, Texture, SRGBColorSpace, NoToneMapping, LinearFilter,
} from 'three';

// Gentle continuous relief, not segmentation, hidden geometry or free camera control.
// These source-relative regions describe the same tree/pot/plinth in each composition.
const profiles = {
  desktop: [[.53,.28,.24,.18,.38],[.26,.46,.18,.12,.36],[.49,.54,.14,.24,.40],[.49,.73,.20,.075,.43],[.46,.87,.31,.07,.45]],
  wide: [[.55,.31,.16,.18,.38],[.38,.48,.15,.12,.36],[.50,.56,.105,.24,.40],[.51,.76,.125,.075,.43],[.5,.88,.21,.065,.45]],
  square: [[.53,.37,.21,.15,.38],[.28,.5,.18,.1,.36],[.49,.56,.13,.2,.40],[.51,.68,.19,.07,.43],[.50,.77,.29,.07,.45]],
  portrait: [[.55,.37,.29,.13,.38],[.28,.46,.22,.09,.36],[.51,.51,.17,.16,.40],[.53,.63,.30,.06,.43],[.52,.70,.42,.07,.45]],
  tall: [[.52,.36,.29,.12,.38],[.25,.44,.20,.09,.36],[.47,.51,.19,.16,.40],[.5,.62,.32,.055,.43],[.50,.71,.44,.07,.45]],
};
const smooth = (a, b, x) => { const t = Math.max(0, Math.min(1, (x-a)/(b-a))); return t*t*(3-2*t); };

export async function createRelief(canvas, image) {
  const context = canvas.getContext('webgl2', { alpha: true, antialias: false, powerPreference: 'low-power', preserveDrawingBuffer: false });
  if (!context) return null;
  context.pixelStorei(context.UNPACK_FLIP_Y_WEBGL, false);
  context.pixelStorei(context.UNPACK_PREMULTIPLY_ALPHA_WEBGL, false);
  const renderer = new WebGLRenderer({ canvas, context, alpha: true, antialias: false });
  renderer.outputColorSpace = SRGBColorSpace; renderer.toneMapping = NoToneMapping;
  renderer.setClearColor(0x000000, 0);
  renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
  renderer.setSize(innerWidth, innerHeight, false);
  const aspect = innerWidth / innerHeight;
  const camera = new PerspectiveCamera(2 * Math.atan(1 / 3) * 180 / Math.PI, aspect, .1, 8);
  camera.position.z = 3;
  const scene = new Scene();
  const texture = new Texture(image);
  texture.colorSpace = SRGBColorSpace; texture.generateMipmaps = false;
  texture.minFilter = LinearFilter; texture.magFilter = LinearFilter; texture.needsUpdate = true;
  const geometry = new PlaneGeometry(2 * aspect, 2, 160, 100);
  const sourceAspect = image.naturalWidth / image.naturalHeight;
  const sx = Math.min(1, aspect / sourceAspect), sy = Math.min(1, sourceAspect / aspect);
  const name = new URL(image.currentSrc).pathname.split('/').pop().split('.')[0];
  const regions = profiles[name] || profiles.desktop;
  const positions = geometry.attributes.position, uvs = geometry.attributes.uv;
  let maxDepth = 0;
  for (let i = 0; i < positions.count; i++) {
    const screenU = uvs.getX(i), screenV = uvs.getY(i);
    const u = .5 + (screenU-.5)*sx, v = .5 + (screenV-.5)*sy, y = 1-v;
    let z = .035 + .50 * smooth(.55, 1, y);
    for (const [cx,cy,rx,ry,depth] of regions) {
      const d = ((u-cx)/rx)**2 + ((y-cy)/ry)**2;
      z = Math.max(z, .035 + depth * Math.exp(-d * 1.4));
    }
    z *= smooth(0, .04, Math.min(screenU, 1-screenU, screenV, 1-screenV));
    maxDepth = Math.max(maxDepth, z);
    positions.setXYZ(i, positions.getX(i)*(3-z)/3, positions.getY(i)*(3-z)/3, z);
    uvs.setXY(i, u, v);
  }
  const material = new MeshBasicMaterial({ map: texture, depthTest: false, depthWrite: false, toneMapped: false });
  scene.add(new Mesh(geometry, material));
  await renderer.compileAsync(scene, camera);
  renderer.initTexture(texture);
  return {
    renderer, triangles: geometry.index.count / 3,
    render([x,y]) {
      camera.position.set(x,y,3);
      // Off-axis projection holds the distant reference plane still.
      camera.projectionMatrix.elements[8] = -x / aspect;
      camera.projectionMatrix.elements[9] = -y;
      camera.projectionMatrixInverse.copy(camera.projectionMatrix).invert();
      renderer.render(scene,camera);
    },
    maxOffsetPixels([x,y]) { return Math.hypot(x,y) * maxDepth / (3-maxDepth) * innerHeight / 2; },
    dispose() { geometry.dispose(); material.dispose(); texture.dispose(); renderer.dispose(); },
  };
}
