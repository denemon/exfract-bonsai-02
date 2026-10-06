from pathlib import Path
import json,hashlib
R=Path('/Users/kazuki.tanaka/dev0/exfract-bonsai-02/improvement/2026-10-04/runs/organic-ensemble-1017');P=R.parent/'idle-causality-0935';H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
t=(R/'qa/cohort.mjs').read_text();old=hashlib.sha256(t.encode()).hexdigest();assert 'gzipSync'not in t
t=t.replace("import {readFile,mkdir}","import {gzipSync} from 'node:zlib';\nimport {readFile,mkdir}").replace("function save(path,data){const part=path+'.partial'","function save(path,data){const compressed=mode!=='factor';if(compressed)path+='.gz';const part=path+'.partial'").replace('writeFileSync(fd,JSON.stringify(data));','writeFileSync(fd,compressed?gzipSync(JSON.stringify(data),{level:9,mtime:0}):JSON.stringify(data));').replace("console.log('CHECKPOINT '+JSON.stringify({id,samples:data.cpuSubmitMs?.length,CPU:data.cpuSubmitMs,GPU:data.gpuElapsedMs,first3D:data.navigationToFirst3DMs}))","console.log('CHECKPOINT '+JSON.stringify({id,samples:data.cpuSubmitMs?.length,first3D:data.navigationToFirst3DMs,rawSavedCompressed:true}))")
(R/'qa/cohort.mjs').write_text(t)
with(R/'qa/checkpoint-compression-before-qualification.json').open('x')as f:json.dump({'componentRunnerSHA256':old,'qualificationRunnerSHA256':hashlib.sha256(t.encode()).hexdigest(),'compressedNumericRawFromFirstCohort':True,'losslessFullRaw':True,'exclusivePartFsyncHardlinkFinalUnlinkOwnPartialDirFsync':True,'noTimedExpressionChange':True,'thresholdChangeCount':0,'beforeFirstQualifiedCohort':True,'oldRawOverwriteCount':0},f,indent=2)
freeze=json.loads((R/'selected-scene-freeze.json').read_text())
for n,h in(freeze['sourceSHA256']|freeze['fixedNativeSevenSHA256']).items():assert H(R/n)==h
with(R/'qa/selected-before-qualification.json').open('x')as f:json.dump({'stage':34,'scene':'living-v01/v5/planting-v02/stable','nativeAndSourceFixedExact':True,'R32AndR33FailuresUnresolved':True,'finiteComponent14RawPresent':True,'componentCPU390RegressedUnqualified':True,'thresholdChangeCount':0,'qualificationRepeatCountAllowed':0,'activeSamplesEachVariantWidth':236,'idleSamplesEachVariantWidth':28,'coldSamplesEachVariantWidth':2,'ChromePID':61609,'budgetTemporaryOverrun':True,'old42NotPooled':True,'runCandidateAdopted':False},f,indent=2)
with(R/'qa/qualified-batch.py').open('x')as f:f.write("""from pathlib import Path
import subprocess,os
R=Path(__file__).resolve().parents[1]
with(R/'qa/qualified-console.log').open('x')as log:
 for mode,count in [('idle',8),('frame',8),('cold',4)]:
  for view in ['pc','mobile-390','mobile-320']:
   for c in range(count):
    p=subprocess.run(['node','qa/cohort.mjs',mode,view,str(c)],cwd=R,capture_output=True,text=True);log.write(p.stdout+p.stderr);log.flush();os.fsync(log.fileno());print(p.stdout.strip(),flush=True);assert p.returncode==0,p.stderr
print('QUALIFIED60_RAW_EXCLUSIVE_COMPLETE',flush=True)
""")
t=(P/'qa/idle-causality-summarize.py').read_text().replace('runs/idle-causality-0935','runs/organic-ensemble-1017').replace('import json,statistics','import gzip,json,statistics').replace("J=lambda p:json.loads(p.read_text())","J=lambda p:json.loads(gzip.decompress(p.read_bytes())if p.suffix=='.gz'else p.read_text())").replace("glob(m+'-*.json')","glob(m+'-*.json.gz')").replace("glob('*.json')if p.name.startswith(('frame-','idle-','cold-'))","glob('*.json.gz')if p.name.startswith(('frame-','idle-','cold-'))").replace("else'aged-v01'","else'living-v01'").replace("'stage':33","'stage':34").replace('R32 unchanged aged-v01/aged-growth-v01/low-occupied-rootshade-v01/stable','R34 living-v01/aged-growth-v01/organic-occupied-v02/stable').replace("'sourceChanged':False,'sameActualCameraDPR'","'sourceChanged':True,'budgetTemporaryExceeded':True,'R32AndR33FailuresUnresolved':True,'sameActualCameraDPR'")
with(R/'qa/summarize.py').open('x')as f:f.write(t)
print('Native/source freeze exact; existing60cohort and51fixedtolgates, compressedraw prepared before first sample. No repeats authorized.')
