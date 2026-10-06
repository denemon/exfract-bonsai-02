from pathlib import Path
import json,statistics,math
R=Path('/Users/kazuki.tanaka/dev0/exfract-bonsai-02/improvement/2026-10-04/runs/aged-ensemble-0831')
J=lambda p:json.loads(p.read_text())
def stats(a):
 a=sorted(a);return {'n':len(a),'median':statistics.median(a),'p95':a[math.ceil(.95*len(a))-1],'min':a[0],'max':a[-1]}
raw={m:J(R/f'qa/qualified-{m}/results.json')for m in ['frame','idle','cold']};assert all(d['passed']for d in raw.values());rows=[];gates=[]
for width in ['pc','mobile-390','mobile-320']:
 variants={}
 for variant in ['r31','candidate']:
  f=[r for r in raw['frame']['results']if r['view']['name']==width and r['variant']==variant];i=[r for r in raw['idle']['results']if r['view']['name']==width and r['variant']==variant];c=[r for r in raw['cold']['results']if r['view']['name']==width and r['variant']==variant]
  assert len(f)==4 and len(i)==len(c)==2
  cpu=[x for r in f for x in r['cpuSubmitMs'][r['excludedFirst']:]];gpu=[x for r in f for x in r['gpuElapsedMs'][r['excludedFirst']:]];igpu=[x for r in i for x in r['gpuElapsedMs']];assert len(cpu)==len(gpu)==236 and len(igpu)==14
  variants[variant]={'CPU_submit_ms':stats(cpu),'GPU_active_elapsed_ms':stats(gpu),'GPU_idle_elapsed_ms':stats(igpu),'CPU_idle_submit_ms':stats([x for r in i for x in r['cpuSubmitMs']]),'actual_idle_wait_ms':stats([x for r in i for x in r['actualIdleWaitMs']]),'cold_first3D_ms':stats([r['navigationToFirst3DMs']for r in c]),'cold_completed_still_ms':stats([r['timing']['completedStillMs']for r in c]),'cold_FCP_ms':stats([next(p['startTime']for p in r['actualPaintEntries']if p['name']=='first-contentful-paint')for r in c]),'cold_encoded_body_bytes':stats([sum(x['encodedBodySize']for x in r['resources'])for r in c]),'cold_transfer_bytes':stats([sum(x['transferSize']for x in r['resources'])for r in c]),'draw_calls':f[0]['drawCalls'],'triangles':f[0]['triangles'],'actual_camera':f[0]['state']['camera']}
  assert all(r['state']['version']==('grown-v02'if variant=='r31'else'aged-v01')for r in f+i+c)
  assert all(r['state']['pixelRatio']==1 for r in f+i+c)
 assert variants['r31']['actual_camera']==variants['candidate']['actual_camera']
 for metric,quantile,fixed,ratio in [('CPU_submit_ms','median',.5,.15),('CPU_submit_ms','p95',1.5,.2),('GPU_active_elapsed_ms','median',1,.15),('GPU_active_elapsed_ms','p95',2,.15),('GPU_idle_elapsed_ms','p95',3,.15),('cold_first3D_ms','median',800,.1),('CPU_idle_submit_ms','median',.75,.20),('CPU_idle_submit_ms','p95',1.5,.20),('GPU_idle_elapsed_ms','median',3,.20)]:
  b=variants['r31'][metric][quantile];c=variants['candidate'][metric][quantile];tol=max(fixed,b*ratio);gates.append({'width':width,'metric':metric,'quantile':quantile,'baseline':b,'candidate':c,'delta':c-b,'predeclared_allowed_delta':tol,'passed':c-b<=tol})
 rows.append({'width':width,'variants':variants})
d={'stage':32,'candidate':'aged-v01_aged-growth-v01_low-occupied-rootshade-v01_stable','raw_valid':True,'all_predeclared_nonregression_conditions_pass':all(g['passed']for g in gates),'same_actual_camera_DPR_verified':True,'frame_samples_per_variant_width':236,'idle_samples_per_variant_width':14,'cold_samples_per_variant_width':2,'rows':rows,'gates':gates,'method':'Pooled balanced ABBA/BAAB active frames; nearest rank p95; separate ABBA idle and cacheoff cold; actual draw assertion and non-disjoint elapsed queries; oldR31 results reference only','limitations':['CPU measured render submission, not end-to-end presented frame','Mac Chrome desktop viewport emulation, not actual phone or Safari','Cacheoff simulated120ms256000B/s, not actual system cold start','Thermal conditions and sustained realphone FPS not qualified','Small cold cohort; timing variability remains'],'overall_quality_completion':False}
with(R/'qa/qualified-performance-summary.json').open('x')as f:json.dump(d,f,ensure_ascii=False,indent=2)
print(json.dumps(d,ensure_ascii=False,indent=2))
