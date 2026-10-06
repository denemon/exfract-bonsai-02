from pathlib import Path
import json,statistics,math,hashlib,collections,sys
R=Path('/Users/kazuki.tanaka/dev0/exfract-bonsai-02/improvement/2026-10-04/runs/idle-causality-0935');Q=R/'qa';J=lambda p:json.loads(p.read_text());H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def stat(a):
 a=sorted(a);return {'n':len(a),'median':statistics.median(a),'p95':a[math.ceil(.95*len(a))-1],'min':a[0],'max':a[-1]}
mode=sys.argv[1]
def new(p,d):
 with p.open('x')as f:json.dump(d,f,ensure_ascii=False,indent=2)
if mode=='diagnostic':
 ds=[J(p) for p in sorted((Q/'checkpoints').glob('diagnostic-*.json')) if 'cpuprofile' not in p.name and 'failure' not in p.name];assert len(ds)==16 and all(d['passed']and d['diagnostic']for d in ds)
 rows=[]
 for v in ['r31','candidate','oldwood','oldgarden','oldboth','content','warmr31','warmcandidate']:
  a=[d for d in ds if d['variant']==v];assert len(a)==2
  parts={k:stat([n[k]for d in a for n in d['parts']])for k in['foliage','renderer','other']}
  profiles=[]
  for d in a:
   p=J(Q/'checkpoints'/f'{d["id"]}.cpuprofile.json')['profile'];nodes={n['id']:n for n in p['nodes']};c=collections.Counter(p.get('samples',[]));tops=[{'function':nodes[k]['callFrame']['functionName'],'url':nodes[k]['callFrame']['url'],'selfSamples':n}for k,n in c.most_common(15)];profiles.append({'id':d['id'],'profileSampleCount':sum(c.values()),'topSelfSampleFunctions':tops,'samplingUs':500,'driverBlockingCannotBeSeparatedByJSProfiler':True})
  rows.append({'variant':v,'CPU':stat([x for d in a for x in d['cpuSubmitMs']]),'GPU':stat([x for d in a for x in d['gpuElapsedMs']]),'parts':parts,'cohorts':[{'id':d['id'],'CPU':stat(d['cpuSubmitMs']),'GPU':stat(d['gpuElapsedMs']),'CPUordered':d['cpuSubmitMs'],'actualIdleWait':stat(d['actualIdleWaitMs'])}for d in a],'profiles':profiles})
 d={'stage':33,'diagnosticOnly':True,'qualificationSamples':0,'rows':rows,'rawCohorts':len(ds),'rawSamples':112,'rawSHA256':{p.name:H(p)for p in sorted((Q/'checkpoints').glob('diagnostic-*.json'))},'limitations':['Instrumented profile500us and functionwrappers; not qualification','Two7sample cohorts percondition, actual temperature/frequency unavailable','Woodbundle changes shaderandatlas together','CPUrender submitincludes possible driverwait andJSinterruptions','Cause must be inferred cautiously; thresholds unchanged'],'sourceChanged':False,'oldPrimaryFailuresPreserved':True,'interrupted42NeverQualified':True};new(Q/'diagnostic-summary.json',d);print(json.dumps([{'variant':r['variant'],'CPU':r['CPU']['median'],'GPU':r['GPU']['median'],'parts':{k:x['median']for k,x in r['parts'].items()},'cohortCPU':[a['CPU']['median']for a in r['cohorts']]}for r in rows],indent=2))
elif mode=='qualified':
 raw={m:[J(p)for p in sorted((Q/'checkpoints').glob(m+'-*.json'))if 'failure'not in p.name]for m in['frame','idle','cold']};assert len(raw['frame'])==len(raw['idle'])==24 and len(raw['cold'])==12;assert all(d['passed']for a in raw.values()for d in a);rows=[];gates=[];blockGates=[]
 definitions=[('CPU_submit_ms','median',.5,.15),('CPU_submit_ms','p95',1.5,.2),('GPU_active_elapsed_ms','median',1,.15),('GPU_active_elapsed_ms','p95',2,.15),('GPU_idle_elapsed_ms','p95',3,.15),('cold_first3D_ms','median',800,.1),('CPU_idle_submit_ms','median',.75,.2),('CPU_idle_submit_ms','p95',1.5,.2),('GPU_idle_elapsed_ms','median',3,.2)]
 for width in['pc','mobile-390','mobile-320']:
  vs={};blocks={}
  for variant in['r31','candidate']:
   f=[d for d in raw['frame']if d['view']['name']==width and d['variant']==variant];i=[d for d in raw['idle']if d['view']['name']==width and d['variant']==variant];c=[d for d in raw['cold']if d['view']['name']==width and d['variant']==variant];assert len(f)==len(i)==4 and len(c)==2
   assert all(d['state']['version']==('grown-v02'if variant=='r31'else'aged-v01')and d['pixelRatio']==1 for d in f+i)
   vs[variant]={'CPU_submit_ms':stat([x for d in f for x in d['cpuSubmitMs'][2:]]),'GPU_active_elapsed_ms':stat([x for d in f for x in d['gpuElapsedMs'][2:]]),'CPU_idle_submit_ms':stat([x for d in i for x in d['cpuSubmitMs']]),'GPU_idle_elapsed_ms':stat([x for d in i for x in d['gpuElapsedMs']]),'actual_idle_wait_ms':stat([x for d in i for x in d['actualIdleWaitMs']]),'cold_first3D_ms':stat([d['navigationToFirst3DMs']for d in c]),'cold_completed_still_ms':stat([d['timing']['completedStillMs']for d in c]),'cold_FCP_ms':stat([next(p['startTime']for p in d['actualPaintEntries']if p['name']=='first-contentful-paint')for d in c]),'cold_encoded_body_bytes':stat([sum(p['encodedBodySize']for p in d['resources'])for d in c]),'draw_calls':f[0]['drawCalls'],'triangles':f[0]['triangles'],'actual_camera':f[0]['state']['camera']}
   blocks[variant]={b:{'CPU_idle_submit_ms':stat([x for d in i if d['orderBlock']==b for x in d['cpuSubmitMs']]),'GPU_idle_elapsed_ms':stat([x for d in i if d['orderBlock']==b for x in d['gpuElapsedMs']])}for b in['ABBA','BAAB']}
  assert vs['r31']['actual_camera']==vs['candidate']['actual_camera'];assert all(d['state']['camera']==vs['r31']['actual_camera']for m in raw.values()for d in m if d['view']['name']==width)
  def gate(metric,q,fixed,ratio,b,c,block=None):
   tol=max(fixed,b*ratio);return{'width':width,'metric':metric,'quantile':q,'baseline':b,'candidate':c,'delta':c-b,'predeclared_allowed_delta':tol,'passed':c-b<=tol,**({'block':block}if block else{})}
  for metric,q,fixed,ratio in definitions:gates.append(gate(metric,q,fixed,ratio,vs['r31'][metric][q],vs['candidate'][metric][q]))
  for b in['ABBA','BAAB']:
   for metric,q,fixed,ratio in definitions:
    if metric in['CPU_idle_submit_ms','GPU_idle_elapsed_ms']:blockGates.append(gate(metric,q,fixed,ratio,blocks['r31'][b][metric][q],blocks['candidate'][b][metric][q],b))
  rows.append({'width':width,'variants':vs,'idleOrderBlocks':blocks})
 d={'stage':33,'selectedCandidate':'R32 unchanged aged-v01/aged-growth-v01/low-occupied-rootshade-v01/stable','rawValid':True,'poolConditions':27,'poolPassedCount':sum(g['passed']for g in gates),'allPredeclaredPoolPass':all(g['passed']for g in gates),'orderBlockIdleConditions':len(blockGates),'orderBlockPassedCount':sum(g['passed']for g in blockGates),'allPredeclaredOrderBlocksPass':all(g['passed']for g in blockGates),'technicalQualificationPassed':all(g['passed']for g in gates+blockGates),'rows':rows,'gates':gates,'orderBlockGates':blockGates,'sourceChanged':False,'sameActualCameraDPR':True,'frameSamplesPerVariantWidth':236,'idleSamplesPerVariantWidth':28,'coldSamplesPerVariantWidth':2,'old14AndInterruptedSupplementNotPooled':True,'diagnosticNotPooled':True,'all42QualifiedClaimed':False,'rawCheckpointFiles':sum(map(len,raw.values())),'rawSHA256':{p.name:H(p)for p in sorted((Q/'checkpoints').glob('*.json'))if p.name.startswith(('frame-','idle-','cold-'))},'limitations':['Actual Mac Chrome154 ANGLE Metal viewportemulation DPR1','CPUsubmit includes JSandpossible driverwait, notpresentedframe','Temperature/frequency unsupported; background userChrome notcontrolled','Cacheoff120ms256000Bps notsystemcold','No physicalphone/Safari/thermal guarantee'],'wholeQualityComplete':False};new(Q/'qualified-performance-summary.json',d);print(json.dumps({'poolPass':d['poolPassedCount'],'poolTotal':27,'blockPass':d['orderBlockPassedCount'],'blockTotal':len(blockGates),'qualified':d['technicalQualificationPassed'],'failures':[g for g in gates+blockGates if not g['passed']],'rows':[{'width':r['width'],'idleCPU':{v:x['CPU_idle_submit_ms']['median']for v,x in r['variants'].items()},'idleGPU':{v:x['GPU_idle_elapsed_ms']['median']for v,x in r['variants'].items()}}for r in rows]},indent=2))
else:raise ValueError(mode)
