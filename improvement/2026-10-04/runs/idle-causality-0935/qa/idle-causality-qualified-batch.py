from pathlib import Path
import subprocess,json,hashlib,os,datetime
R=Path('/Users/kazuki.tanaka/dev0/exfract-bonsai-02/improvement/2026-10-04/runs/idle-causality-0935');P=R.parent/'aged-ensemble-0831';J=lambda p:json.loads(p.read_text());H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert J(R/'qa/diagnostic-summary.json')['rawCohorts']==16
f=J(P/'selected-scene-freeze.json')
for n,h in f['sourceSHA256'].items():assert H(P/n)==h
for n,h in f['fixedNativeSevenSHA256'].items():assert H(P/n)==h
selected={'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scene':'R32 unchanged aged-v01/aged-growth-v01/low-occupied-rootshade-v01/R27stable','selectionReason':'Finiteinstrumenteddiagnosis didnotestablish causal sourcefix; unchangedscene only. Fresh27samepooltol+24idleblocktol, no diagnostic/old/raw-interruption pool','sourceAndNativeSHA256Exact':True,'sourceChanged':False,'qualificationRepeatsAllowed':0,'CPUcauseIdentified':False,'thresholdChangeCount':0,'protocolSHA256':H(R/'qa/performance-protocol.json'),'runnerSHA256':H(R/'qa/cohort.mjs'),'diagnosticSummarySHA256':H(R/'qa/diagnostic-summary.json'),'ChromePID':34202,'TOPPID':20598,'comparisonPID':20741,'DPR':1,'activeSamplesPerVariantWidth':236,'idleSamplesPerVariantWidth':28,'coldSamplesPerVariantWidth':2,'oldPrimary390320FailuresRemainValid':True,'all42QualifiedClaimed':False}
with(R/'qa/selected-before-qualification.json').open('x')as x:json.dump(selected,x,indent=2)
log=(R/'qa/qualified-console.log').open('x')
for mode,count in [('idle',8),('frame',8),('cold',4)]:
 for view in ['pc','mobile-390','mobile-320']:
  for cohort in range(count):
   p=subprocess.run(['node','qa/cohort.mjs',mode,view,str(cohort)],cwd=R,capture_output=True,text=True);log.write(p.stdout+p.stderr);log.flush();os.fsync(log.fileno());print(p.stdout.strip(),flush=True)
   assert p.returncode==0,p.stderr
print('QUALIFIED_ALL60_CHECKPOINTS_SAVED',flush=True)
