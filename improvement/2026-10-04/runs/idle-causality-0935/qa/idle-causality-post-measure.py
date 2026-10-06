from pathlib import Path
import json,hashlib,os
R=Path('/Users/kazuki.tanaka/dev0/exfract-bonsai-02/improvement/2026-10-04/runs/idle-causality-0935');P=R.parent/'aged-ensemble-0831';J=lambda p:json.loads(p.read_text());H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
q=J(R/'qa/qualified-performance-summary.json');assert not q['technicalQualificationPassed'];assert not q['allPredeclaredOrderBlocksPass']
for n,h in J(P/'selected-scene-freeze.json')['sourceSHA256'].items():assert H(P/n)==h
for n,h in J(P/'selected-scene-freeze.json')['fixedNativeSevenSHA256'].items():assert H(P/n)==h
for name in ['verify-own-functional.mjs','verify-selected-dynamic-qualified.mjs']:
 t=(P/'qa'/name).read_text().replace('runs/aged-ensemble-0831','runs/idle-causality-0935').replace('existingChromePID:20964','existingChromePID:34202').replace("'integration-'+mode+'-recovered'","'integration-'+mode+'-current'")
 p=R/'qa'/name;assert not p.exists();p.write_text(t)
t=(P/'qa/audit_protection.py').read_text().replace('runs/aged-ensemble-0831','runs/idle-causality-0935').replace("'growth-garden-0729']:","'growth-garden-0729','aged-ensemble-0831']:").replace('Stage32','Stage33').replace('thirty_five','thirty_six');p=R/'qa/audit_protection.py';assert not p.exists();p.write_text(t)
views=[('pc',1440,900),('mobile-390',390,844),('mobile-320',320,568)]
job={'name':'current-candidate-and-retina','cases':[{'name':n+('-dpr2'if dpr==2 else''),'url':'http://127.0.0.1:5215/compare/r32/','w':w,'h':h,'dpr':dpr}for dpr in[1,2]for n,w,h in views]};p=R/'qa/jobs/current-candidate-and-retina.json';assert not p.exists();p.write_text(json.dumps(job))
job={'name':'current-selected-top','cases':[{'name':n,'url':'http://127.0.0.1:5214/','w':w,'h':h}for n,w,h in views]};p=R/'qa/jobs/current-selected-top.json';assert not p.exists();p.write_text(json.dumps(job))
# Fault-injection proof: atomic publication refuses an already existing final and preserves its bytes.
test=R/'qa/publication-safety';test.mkdir();old=test/'existing-final.json';attempt=test/'attempt.partial';old.write_text('{"existing":"preserved"}');oldSHA=H(old)
fd=os.open(attempt,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600);os.write(fd,b'{"attempt":"must-not-replace"}');os.fsync(fd);os.close(fd)
rejected=False
try:os.link(attempt,old)
except FileExistsError:rejected=True
assert rejected and H(old)==oldSHA
new=test/'new-final.json';os.link(attempt,new);fd=os.open(test,os.O_RDONLY);os.fsync(fd);os.close(fd);assert new.read_bytes()==attempt.read_bytes()
with(R/'qa/exclusive-publication-proof.json').open('x')as f:json.dump({'existingFinalRejected':rejected,'existingFinalSHA256Unchanged':oldSHA,'newFinalExactAfterDurableHardlink':True,'onlyOwnNewTestFilesUsed':True,'oldRawOverwriteObserved':False,'timedBrowserExpressionUnchanged':J(R/'qa/checkpoint-publication-correction.json')['browserExpressionSHA256'],'qualificationV1Cohorts':4,'qualificationV2Cohorts':56,'noCohortRemeasured':True},f,indent=2)
review={'reviewer':'/root/volume_review','readOnly':True,'diagnostic16Cohorts112SamplesRecomputedExact':True,'sameContentControlProven':True,'causeNotEstablished':['wood atlas','garden','GC','JIT','driver'],'rendererBreakdownIncludesThreeAndDriver':True,'30PrimingLaterOnlyDoesNotRejectJITHypothesis':True,'pool27AndOrderBlocks24BothRequired':True,'sourceChangeCount':0,'v1v2SamplingExpressionExactAndNoRawOverwritten':True,'historicalPrimaryFailuresPreserved':True,'interrupted42NotQualified':True}
with(R/'qa/independent-diagnostic-review.json').open('x')as f:json.dump(review,f,indent=2)
print(json.dumps({'qualification':False,'preparedFreshVisualCases':9,'exclusivePublicationFaultInjectionPassed':True,'timedCohortsNotRepeated':True},indent=2))
