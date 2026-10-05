import {readFile} from 'node:fs/promises';import {createHash} from 'node:crypto';const source=new URL('../../irregular-volume-1200/qa/capture-comparison.mjs',import.meta.url);let code=await readFile(source,'utf8');if(createHash('sha256').update(code).digest('hex')!=="140ae482d9b09d822f55bfbd65e847e7d9642e05f0535d3f6b9715143a320095")throw Error('Protected comparison template changed');const a="assert.equal(state.stats.model.authoringVersion,'primary-structure-v01')";if(code.split(a).length!==2)throw Error('Template version anchor changed');code=code.replace(a,"assert.equal(state.stats.model.authoringVersion,"+JSON.stringify(process.env.QA_EXPECT_VERSION||'carved-v01')+")");code=code.replace("'--headless',","'--headless','--disable-gpu-shader-disk-cache',");code=code.replace('if(state.ready&&state.url===u.href)break;','if(state.ready&&new URL(state.url).searchParams.get(\'qa\')===name)break;');
if(process.env.QA_GPU_INFO==='1'){
const marker="if(process.env.QA_FOLIAGE_BOUNDS==='1')state.foliageTemplateBounds";
code=code.replace(marker,"state.graphics=await ev(\"(()=>{const g=window.__garden,gl=g.renderer.getContext(),d=gl.getExtension('WEBGL_debug_renderer_info');return {renderer:d?gl.getParameter(d.UNMASKED_RENDERER_WEBGL):gl.getParameter(gl.RENDERER),vendor:d?gl.getParameter(d.UNMASKED_VENDOR_WEBGL):gl.getParameter(gl.VENDOR),version:gl.getParameter(gl.VERSION),devicePixelRatio,renderPixelRatio:g.renderer.getPixelRatio(),canvasPixels:[g.renderer.domElement.width,g.renderer.domElement.height],gpuTimerSupported:!!gl.getExtension('EXT_disjoint_timer_query_webgl2')}})()\");\n"+marker);
}
if(process.env.QA_FIXED_CAMERA_GPU==='1'){
code=code.replace('g.setView(origin.yaw+Math.sin(n*.31)*4,origin.pitch);','g.render();');
code=code.replaceAll('g.setView(origin.yaw,origin.pitch);','g.render();');
code=code.replace('actual same Mac GPU for both viewports','fixed actual screenshot camera, same Mac GPU for all viewports');
}
try{await import('data:text/javascript;base64,'+Buffer.from(code).toString('base64'));}catch(error){process.stderr.write(error.name+': '+error.message+'\n');process.exitCode=1;}
