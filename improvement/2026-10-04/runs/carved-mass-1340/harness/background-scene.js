import * as before from '../../ancient-volume-0810/site/src/scene.js';
import * as after from '../background/scene.js';
const selected=['spatial-v01','spatial-v02','spatial-v03'].includes(new URLSearchParams(location.search).get('space'))?after:before;
export const createScene=selected.createScene,loadGardenAssets=selected.loadGardenAssets;
