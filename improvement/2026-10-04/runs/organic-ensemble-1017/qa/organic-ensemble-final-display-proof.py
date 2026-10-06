from pathlib import Path
import json,hashlib
R=Path('/Users/kazuki.tanaka/dev0/exfract-bonsai-02/improvement/2026-10-04/runs/organic-ensemble-1017');J=lambda p:json.loads(p.read_text());H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
r=J(R/'qa/final-candidate-and-retina/results.json');assert len(r['results'])==6 and not r['logs']
d=J(R/'qa/integration-functional-current/results.json');assert d['passed'] and len(d['results'])==11
dyn=J(R/'qa/dynamic-selected-scene-proof.json');assert dyn['passed'] and len(dyn['results'])==6
selected=R.parent/'idle-causality-0935';old=J(selected/'qa/current-selected-top/results.json')['results'];new={x['name']:x for x in r['results']};checks=[]
for x in r['results']:
 assert not x['text'] and not x['overflow'];assert x['stats']['model']['authoringVersion']=='living-v01';assert x['diagnostic']['smallStones']==0
 dpr=2 if x['name'].endswith('dpr2') else 1;ret=x['diagnostic']['retina'];assert ret['devicePixelRatio']==dpr and ret['rendererPixelRatio']==min(dpr,1.6)
 bounds=x['exactProjection']['bounds'];assert all(0<=bounds[k]<=1 for k in bounds)
 checks.append({'name':x['name'],'viewport':x['viewport'],'dpr':dpr,'pixelRatio':ret['rendererPixelRatio'],'drawingBuffer':ret['drawingBuffer'],'fullHeroBounds':bounds,'calls':x['stats']['drawCalls'],'triangles':x['stats']['triangles']})
for n in ['pc','mobile-390','mobile-320']:
 o=next(x for x in old if x['name'].endswith(n));a=new[n]
 for k in ['actualCamera','lights','exactProjection']:assert o[k]==a[k],k
freeze=J(R/'selected-scene-freeze.json')
for n,h in (freeze['sourceSHA256']|freeze['fixedNativeSevenSHA256']).items():assert H(R/n)==h
baselineR27=R.parent/'program-state-0426/candidate/src'
for n in ['render-partition.js','foliage-lod.js']:assert H(R/'candidate/src'/n)==H(baselineR27/n)
with (R/'qa/final-display-invariants.json').open('x') as f:json.dump({'checks':checks,'sameR31CameraLightsExactProjection3':True,'native7SHAAndFrozenSourceExact':True,'R27RendererAndFoliageCodeExact':True,'functional11Pass':True,'dynamic6Pass':True,'sameCompletedFiveFullWebPAndInline':J(R/'qa/completed-inline-sync.json')['inlineAndFullSameCompletedScene'],'NoVisibleTextNoOverflowNoSmallStones':True,'physicalPhoneSafariThermalUnverified':True,'overallGoalComplete':False},f,indent=2)
with (R/'qa/independent-final-visual-review.json').open('x') as f:json.dump({'reviewer':'volume_review','finalActualPixels':6,'PCOverallImprovementComparedR31':True,'mobile390Nonregression':True,'mobile320Nonregression':True,'DPR2VisualNonregression':True,'remaining':['Broad main smoothfaces/triangle shoulder','Foldedleaf repetition','390leftplant fragment','Uniform mossmat'],'wholeHighEndGardenComplete':False,'TOPAdoptionBeforeQualification':False,'componentCPURegressionUnresolved':True,'temporaryBudgetLimitMiss':True},f,indent=2)
print('Final6Mac actualDPR photos, sameR31camlightprojection3, functional11/dynamic6/native-source exact verified.')
