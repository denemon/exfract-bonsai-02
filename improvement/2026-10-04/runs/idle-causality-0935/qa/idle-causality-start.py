from pathlib import Path
import os,json,hashlib,datetime,subprocess
ROOT=Path('/Users/kazuki.tanaka/dev0/exfract-bonsai-02');D=ROOT/'improvement/2026-10-04';P=D/'runs/aged-ensemble-0831';R=D/'runs/idle-causality-0935';S=Path('/Users/kazuki.tanaka/Documents/Codex/2026-10-04/task-2');J=lambda p:json.loads(p.read_text());H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert not R.exists() and not (ROOT/'improvement/.active-run').exists()
assert H(P/'delivery-manifest.json')=='f9e0b0992d71737719934595b4bac72032b88a420e1ea2fd130b5f386714c1a5'
assert H(P/'qa/final-receipt.json')=='1d65d48642229ab7693af939436800e2d6aa8fd155406d67ec0337a7c404a667'
m=J(P/'delivery-manifest.json')
for n,d in m['files'].items():assert H(P/n)==d['sha256']
for n,t in m['read_only_references'].items():assert os.readlink(P/n)==t and (P/n).exists()
protected=m['protected_old_state_sha256']|m['new_state_sha256'];assert len(protected)==36
for n,h in protected.items():assert H(D/n)==h
s=J(P/'start.json');profile=s['reused_qa_profile'];cache=s['shared_mutable_cache'];assert not Path(profile+'.active').exists()
proc=subprocess.check_output(['ps','-axo','pid,command'],text=True);assert not any('--user-data-dir='+profile in x for x in proc.splitlines())
for port,pid in [(5214,20598),(5215,20741)]:assert subprocess.check_output(['lsof','-nP',f'-iTCP:{port}','-sTCP:LISTEN','-t'],text=True).strip()==str(pid)
env={**os.environ,'GIT_OPTIONAL_LOCKS':'0'};head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,env=env,text=True).strip();assert head==s['git_head_at_start'];status=subprocess.check_output(['git','status','--porcelain','--untracked-files=no'],cwd=ROOT,env=env,text=True).rstrip('\n');assert all(x[3:] in ['improvement/2026-10-04/'+n for n in ['HANDOFF.md','IMPROVEMENT_PLAN.md','run-state.json']] for x in status.splitlines())
def allocation(p):
 total=0
 for b,ds,fs in os.walk(p,followlinks=False):
  ds[:]=[n for n in ds if not Path(b,n).is_symlink()]
  total+=sum(Path(b,n).stat().st_blocks*512 for n in fs if not Path(b,n).is_symlink())
 return total
free=os.statvfs(ROOT).f_bavail*os.statvfs(ROOT).f_frsize;assert free>=2*1024**3
now=datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
for n in ['qa/jobs','qa/checkpoints','design']:R.joinpath(n).mkdir(parents=True)
lock=ROOT/'improvement/.active-run';lock.mkdir();lock.joinpath('owner.json').write_text(json.dumps({'run':R.name,'thread':'01a103a2-f1bc-7187-8067-1fa594f8b0c6','started_at_jst':now.isoformat()},indent=2)+'\n')
start={**s,'stage':33,'run':R.name,'started_at_jst':now.isoformat(),'midpoint_due_jst':(now+datetime.timedelta(hours=2)).isoformat(),'stage_latest_end_jst':(now+datetime.timedelta(hours=4)).isoformat(),'protected_state_sha256':protected,'protected_stage32_manifest_sha256':H(P/'delivery-manifest.json'),'protected_stage32_receipt_sha256':H(P/'qa/final-receipt.json'),'profile_allocated_bytes_at_start':allocation(profile),'cache_allocated_bytes_at_start':allocation(cache),'staging_allocated_bytes_at_start':allocation(S),'free_disk_bytes':free,'tracked_status_at_start':status,'trial_preview':'http://127.0.0.1:5215/compare/r32/','selected_root_run':'growth-garden-0729','protected_TOP_PID_at_start':20598,'comparison_PID_at_start':20741,'sourceChangesPlanned':False,'interruptedStage32SupplementNumericRawAvailable':False,'qualified42Claimed':False,'library_retry_count':0,'library_image_ids':[]}
R.joinpath('start.json').write_text(json.dumps(start,indent=2)+'\n')
R.joinpath('qa/live-filejobs.mjs').write_text((P/'qa/live-filejobs.mjs').read_text().replace('runs/aged-ensemble-0831','runs/idle-causality-0935'))
R.joinpath('DESIGN.md').write_text('''工程33: R32のPC改善・390/320/Retina非退行の景色を固定し、未解決idle CPUの因果判断を閉じる。R31TOP5214は合格判断まで保護。前回数値raw未保存中断の42成功主張なし。診断は計測プロファイラ/関数内訳・同内容control・旧木肌factorial、qualificationは無instrumentation。既存27tol固定、idleABBAとBAAB各14samples/variant/widthを別集計・pool28。各cohort直後新規checkpoint、completed原子rename同期保存、sample rawもcohortごと保持。温度取得unsupported、負荷/電源/順序/待機/JIT/GC証跡を記録し原因不明は断言しない。見た目とsource固定、原因が実装なら不可視の修正のみ。採用判断前の造形大改修なし。文字/小石0、灰茶幹/高塀/右前障子/夜空/個別camera維持。20MiB/sharedassets/profiles。旧削除/Gitwrite/push/PR/merge/外部公開/購入/Libraryretry0。''')
protocol=J(P/'qa/performance-protocol.json');protocol.update({'stage':33,'run':R.name,'idle':'ABBA then BAAB,4cohorts/variant/width,7samples/cohort after2400ms actual idle,3priming,28valid/variant/width; block14 andpool28 both assessed','idleOrderBlockRule':'For each of2orderblocks andpooled width, idleCPUmedian/p95 andidleGPUmedian/p95 must pass existing fixed tolerances; no hiddenfailedblock by pool','checkpoint':'Eachcohort immediately fsync ownexclusive JSON+directory; incremental per-sample journal is persisted onreceipt from browser; incomplete cohort never pooled','diagnosisDoesNotQualify':True,'diagnosticConditions':['R31','R32','R32 oldwoodmaterial','R32 exactR31content control'],'qualificationsAfterDiagnosisOnly':True,'historicalStage32PrimaryRetained':True,'interruptedStage32SupplementCountsOnlyNoNumbers':True,'noRepeatUntilPass':True,'thermalObservation':'pmset therm unsupported, actual die temperature/frequency unavailable; report this limitation','warmIdle':'Existing3 priming/noextra30activewarmup for comparability. Separatediagnostic30warmup factor notmixed.'})
R.joinpath('qa/performance-protocol.json').write_text(json.dumps(protocol,indent=2)+'\n')
freeze=J(P/'selected-scene-freeze.json');R.joinpath('qa/protected-r32-scene.json').write_text(json.dumps({'run':P.name,'manifestSHA256':H(P/'delivery-manifest.json'),'freeze':freeze,'shapeMaterialBackgroundChangeCount':0},indent=2)+'\n')
for n in ['HANDOFF.md','IMPROVEMENT_PLAN.md']:
 p=D/n;p.write_text(p.read_text()+f'\nStage33 {R.name}: R32固定、idleCPU因果診断→同閾値checkpoint再qualification。TOPPID20598、必要な比較PID20741を保持。中断42主張なし。\n')
D.joinpath('run-state.json').write_text(json.dumps({'stage':33,'run':R.name,'status':'in_progress_idle_causal_diagnosis','selected_root':'growth-garden-0729','writer_active':True,'started_at_jst':now.isoformat(),'midpoint_due_jst':start['midpoint_due_jst'],'stage_latest_end_jst':start['stage_latest_end_jst'],'deadline_jst':s['deadline_jst'],'protected_old_states':36,'budget_bytes':20971520,'overall_goal_complete':False,'library_retry_count':0,'TOP_PID':20598,'comparison_PID':20741,'TOP_port':5214,'comparison_port':5215},indent=2)+'\n')
print(json.dumps({'run':R.name,'start':now.isoformat(),'R32FilesVerified':len(m['files']),'statesProtected':36,'free':free,'profileBaseline':start['profile_allocated_bytes_at_start'],'TOPunchanged':20598,'comparisonNeededDuringDiagnosis':20741},indent=2))
