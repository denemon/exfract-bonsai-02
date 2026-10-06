from pathlib import Path
import json,hashlib,datetime,subprocess,os
R=Path('/Users/kazuki.tanaka/dev0/exfract-bonsai-02/improvement/2026-10-04/runs/idle-causality-0935');p=R/'qa/cohort.mjs';t=p.read_text();old=t
assert "renameSync(part,path)"in t
v1=R/'qa/cohort-v01.mjs';assert not v1.exists();v1.write_text(t)
t=t.replace('closeSync,renameSync','closeSync,linkSync,unlinkSync').replace('renameSync(part,path);','linkSync(part,path);unlinkSync(part);').replace('checkpointDurable:true,','checkpointDurable:true,checkpointImplementationVersion:"exclusive-link-v02",')
# Only node-side durable publication and a result label change. Browser timing expression is identical.
browser=lambda x:x[x.index('data=await ev(`(async()=>'):x.index('assert(data.supported')]
assert browser(old)==browser(t)
part=p.with_name('cohort-new-v02.mjs');assert not part.exists();part.write_text(t);os.replace(part,p)
note={'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Node result publication only, timed browserexpression exact','browserExpressionSHA256':hashlib.sha256(browser(t).encode()).hexdigest(),'v1SHA256':hashlib.sha256(old.encode()).hexdigest(),'v2SHA256':hashlib.sha256(t.encode()).hexdigest(),'firstQualificationStartedV1BeforeReviewResponse':True,'v1Retained':str(v1),'V1ExistingFinalOverwriteObserved':False,'V2AtomicHardlinkFinalExclusiveEEXIST':True,'completedQualificationRawBeforePatch':[x.name for x in (R/'qa/checkpoints').glob('idle-*.json')],'qualifiedProcessAtPatch':subprocess.check_output(['ps','-axo','pid,command'],text=True).splitlines(),'futureV2ResultLabel':'exclusive-link-v02','samplingWarmupOrderTolerancesChangeCount':0}
note['qualifiedProcessAtPatch']=[x for x in note['qualifiedProcessAtPatch']if 'node qa/cohort.mjs' in x and 'ps 'not in x]
with(R/'qa/checkpoint-publication-correction.json').open('x')as f:json.dump(note,f,indent=2)
print(json.dumps({k:v for k,v in note.items()if k not in ['qualifiedProcessAtPatch']},indent=2))
