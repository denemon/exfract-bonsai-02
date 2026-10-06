from pathlib import Path
import json,hashlib,subprocess,os,datetime
ROOT=Path('/Users/kazuki.tanaka/dev0/exfract-bonsai-02');D=ROOT/'improvement/2026-10-04';R=D/'runs/growth-garden-0729';J=lambda p:json.loads(p.read_text());H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();s=J(R/'start.json')
assert J(ROOT/'improvement/.active-run/owner.json')['run']==R.name
assert J(R/'qa/qualified-performance-summary.json')['all_predeclared_nonregression_conditions_pass']
assert J(R/'qa/independent-selected-visual-review.json')['visual_gate_passed']
assert J(R/'qa/selected-final-invariants.json')['passed']
assert J(R/'qa/integration-functional/results.json')['passed']
assert J(R/'qa/completed-scene-five-verification/results.json')['allFiveBitIdenticalProtectedR30']
assert J(R/'qa/dynamic-selected-scene-proof.json')['passed']
assert J(R/'qa/served-comparison-identity.json')['passed']
for n,h in s['protected_state_sha256'].items():assert H(D/n)==h
f=J(R/'selected-scene-freeze.json');assert all(H(R/n)==h for n,h in f['source_SHA256'].items());assert all(H(R.parent/'garden-scale-0634/background'/n)==h for n,h in f['read_only_garden_source_SHA256'].items());assert all(H(R.parent/'grown-core-0554'/n)==h for n,h in f['fixed_native_7_SHA256'].items())
env={**os.environ,'GIT_OPTIONAL_LOCKS':'0'};assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,env=env,text=True).strip()==s['git_head_at_start'];status=subprocess.check_output(['git','status','--porcelain','--untracked-files=no'],cwd=ROOT,env=env,text=True).rstrip('\n');assert all(x[3:]in['improvement/2026-10-04/'+n for n in['HANDOFF.md','IMPROVEMENT_PLAN.md','run-state.json']]for x in status.splitlines())
for port,pid,run in [(5214,28897,'garden-scale-0634'),(5215,63853,R.name)]:
 assert subprocess.check_output(['lsof','-nP',f'-iTCP:{port}','-sTCP:LISTEN','-t'],text=True).strip()==str(pid)
 cwd=subprocess.check_output(['lsof','-a','-p',str(pid),'-d','cwd','-Fn'],text=True);assert str(D/'runs'/run/'candidate')in cwd
 cmd=subprocess.check_output(['ps','-p',str(pid),'-o','command='],text=True);assert 'vite' in cmd and 'preview' in cmd
gate={'stage':31,'at_jst':datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).isoformat(),'criterion':'PC overall clear improvement plus390/320 nonregression and qualified technical conditions','visual_pass':True,'qualified_nonregression_pass':True,'functional_pass':True,'dynamic_legacy_both_and_original_fallback_actualPNG_parity':True,'completed_five_actual_and_inline_synced':True,'native_and_garden_source_frozen':True,'selected':'grown-v02_normal_R30near-shore-v02_stable','R31_experimental_crest_v01_v02_adopted':False,'provisional_adoption_authorized':True,'whole_high_end_garden_complete':False,'overall_goal_complete':False,'all_widths_clear_improvement_required':False,'protected_TOP_PID_before':28897,'comparison_PID_before':63853,'post_transition_TOP_verification_pending':True,'evidence_sha256':{n:H(R/n)for n in ['qa/qualified-performance-summary.json','qa/independent-selected-visual-review.json','qa/selected-final-invariants.json','qa/integration-functional/results.json','qa/completed-scene-five-verification/results.json','qa/dynamic-selected-scene-proof.json','qa/served-comparison-identity.json','selected-scene-freeze.json']}}
with(R/'adoption-gate.json').open('x')as out:json.dump(gate,out,ensure_ascii=False,indent=2)
(R/'routing.json').write_text(json.dumps({'adopted':True,'relatedQAComplete':True,'selected_root':R.name,'prior_root':'program-state-0426','selected_scene':'grown-v02_normal_R30near-shore-v02','trial_run':R.name,'experimental_V01V02_adopted':False,'gate':'adoption-gate.json','overall_goal_complete':False},indent=2)+'\n')
p=R/'candidate/vite.config.mjs';t=p.read_text();assert t.count('port:5215')==2;t=t.replace('port:5215','port:5214').replace('// Unadopted trials never replace the user TOP. Only an explicit completed\n// local gate record can select this unchanged-R20 performance derivative.','// Qualified provisional adoption is explicit in the local gate and routing record.\n// Unadopted crest experiments remain on separate comparison paths.');p.write_text(t)
print(json.dumps({'gate_created':True,'next':'Stop only verified owned28897/63853;build finalconfig;start own5214 and verify TOP','whole_complete':False}))
