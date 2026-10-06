from pathlib import Path
import os,json,hashlib,datetime,subprocess,shutil
ROOT=Path('/Users/kazuki.tanaka/dev0/exfract-bonsai-02');D=ROOT/'improvement/2026-10-04';P=D/'runs/idle-causality-0935';B=D/'runs/aged-ensemble-0831';R=D/'runs/organic-ensemble-1017';S=Path('/Users/kazuki.tanaka/Documents/Codex/2026-10-04/task-2');J=lambda p:json.loads(p.read_text());H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert not R.exists() and not(ROOT/'improvement/.active-run').exists()
assert H(P/'delivery-manifest.json')=='b3671a593202ce57d63143cef979866730a1f6c7bac9fda013a9b66106efd07a' and H(P/'qa/final-receipt.json')=='77b8599bffb935e9ac42859928da9ac3ca51a0944d171b5bfc90eb7e076b6809'
m=J(P/'delivery-manifest.json')
for n,d in m['files'].items():assert H(P/n)==d['sha256']
for n,t in m['read_only_references'].items():assert os.readlink(P/n)==t and(P/n).exists()
protected=m['protected_old_state_sha256']|m['new_state_sha256'];assert len(protected)==37
for n,h in protected.items():assert H(D/n)==h
s=J(P/'start.json');profile=s['reused_qa_profile'];cache=s['shared_mutable_cache'];assert not Path(profile+'.active').exists()
assert not any('--user-data-dir='+profile in x for x in subprocess.check_output(['ps','-axo','pid,command'],text=True).splitlines())
assert subprocess.check_output(['lsof','-nP','-iTCP:5214','-sTCP:LISTEN','-t'],text=True).strip()=='20598'
assert not subprocess.run(['lsof','-nP','-iTCP:5215','-sTCP:LISTEN','-t'],capture_output=True,text=True).stdout.strip()
env={**os.environ,'GIT_OPTIONAL_LOCKS':'0'};head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,env=env,text=True).strip();assert head==s['git_head_at_start'];status=subprocess.check_output(['git','status','--porcelain','--untracked-files=no'],cwd=ROOT,env=env,text=True).rstrip('\n');assert all(x[3:]in['improvement/2026-10-04/'+n for n in['HANDOFF.md','IMPROVEMENT_PLAN.md','run-state.json']]for x in status.splitlines())
def allocation(p):
 t=0
 for b,ds,fs in os.walk(p,followlinks=False):
  ds[:]=[n for n in ds if not Path(b,n).is_symlink()]
  t+=sum(Path(b,n).stat().st_blocks*512 for n in fs if not Path(b,n).is_symlink())
 return t
free=os.statvfs(ROOT).f_bavail*os.statvfs(ROOT).f_frsize;assert free>=2*1024**3
now=datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
for n in['candidate/src','candidate/public/stills','qa/jobs','qa/checkpoints','models','materials','background','sculpt','design']:R.joinpath(n).mkdir(parents=True)
lock=ROOT/'improvement/.active-run';lock.mkdir();lock.joinpath('owner.json').write_text(json.dumps({'run':R.name,'thread':'01a103a2-f1bc-7187-8067-1fa594f8b0c6','started_at_jst':now.isoformat()},indent=2)+'\n')
start={**s,'stage':34,'run':R.name,'started_at_jst':now.isoformat(),'midpoint_due_jst':(now+datetime.timedelta(hours=2)).isoformat(),'stage_latest_end_jst':(now+datetime.timedelta(hours=4)).isoformat(),'protected_state_sha256':protected,'protected_stage33_manifest_sha256':H(P/'delivery-manifest.json'),'protected_stage33_receipt_sha256':H(P/'qa/final-receipt.json'),'profile_allocated_bytes_at_start':allocation(profile),'cache_allocated_bytes_at_start':allocation(cache),'staging_allocated_bytes_at_start':allocation(S),'free_disk_bytes':free,'tracked_status_at_start':status,'trial_preview':'http://127.0.0.1:5215/compare/r34/','selected_root_run':'growth-garden-0729','protected_TOP_PID_at_start':20598,'comparison_PID_at_start':None,'sourceChangesPlanned':True,'R32CPUPrimaryFailureHeld':True,'R33CPUandGPUFailUnidentifiedCause':True,'R33PCActiveCPU1_70to2_60Unresolved':True,'library_retry_count':0,'library_image_ids':[]}
R.joinpath('start.json').write_text(json.dumps(start,indent=2)+'\n');R.joinpath('routing.json').write_text(json.dumps({'adopted':False,'relatedQAComplete':False,'selected_root':'growth-garden-0729','trial_run':R.name},indent=2)+'\n')
for p in(B/'candidate/src').iterdir():
 if p.is_file():shutil.copyfile(p,R/'candidate/src'/p.name)
for p in(B/'background').iterdir():
 if p.is_file():shutil.copyfile(p,R/'background'/p.name)
for n in['index.html','package.json']:shutil.copyfile(B/'candidate'/n,R/'candidate'/n)
for n in['grown-v02-editable.blend','grown-v02.glb','hero-grown-v02.glb.gz']:R.joinpath('models',n).symlink_to('../../grown-core-0554/models/'+n)
for n in['aged-v01-editable.blend','aged-v01.glb','hero-aged-v01.glb.gz']:R.joinpath('models',n).symlink_to('../../aged-ensemble-0831/models/'+n)
for n in['aged-growth-v01.webp','growth-fissures.webp']:R.joinpath('materials',n).symlink_to('../../aged-ensemble-0831/materials/'+n)
v=(B/'candidate/vite.config.mjs').read_text().replace("r31=resolve(here,'../../growth-garden-0729/candidate');","r31=resolve(here,'../../growth-garden-0729/candidate'),r32=resolve(here,'../../aged-ensemble-0831/candidate');").replace('r31|r32)','r31|r32|r34)').replace("key==='r31'?r31:here","key==='r31'?r31:key==='r32'?r32:here").replace("key==='r32')&&","key==='r32'||key==='r34')&&").replace("if(key==='r32'&&!isfile(file)){folder=resolve(r31,'public')","if(key==='r34'&&!isfile(file)){folder=resolve(r32,'public')").replace("key==='r32'&&!preview","key==='r34'&&!preview").replace('/qa/r32/','/qa/r34/').replace("base:'/compare/r32/'","base:'/compare/r34/'").replace('aged-v0[12])','aged-v0[12]|living-v01)')
R.joinpath('candidate/vite.config.mjs').write_text(v)
for p in(R/'candidate/src').glob('*.js'):
 t=p.read_text().replace('/compare/r32/','/compare/r34/');p.write_text(t)
p=R/'candidate/src/main.js';t=p.read_text().replace("||'aged-v01'","||'living-v01'").replace("['aged-v01','aged-v02'","['living-v01','aged-v01','aged-v02'").replace("stats.gardenFinish=baselineGarden?'R29-baseline':'low-occupied-rootshade-v01'","stats.gardenFinish=baselineGarden?'R29-baseline':'organic-occupied-v01'");p.write_text(t)
p=R/'candidate/index.html';p.write_text(p.read_text().replace('/compare/r32/','/compare/r34/'))
p=R/'candidate/package.json';d=J(p);d['name']='bonsai-organic-ensemble';p.write_text(json.dumps(d,indent=2)+'\n')
R.joinpath('qa/live-filejobs.mjs').write_text((P/'qa/live-filejobs.mjs').read_text().replace('runs/idle-causality-0935','runs/organic-ensemble-1017'))
R.joinpath('DESIGN.md').write_text('''工程34。完成像は成熟木の不均等な面方向と枝肩の厚みが読め、庭の近中遠の低木・樹冠が一つの土と光の中に連なる静かな夜庭。最大二領域: 主役の広い滑面S/枝肩量感と、庭植栽の反復した扇軸・葉/遠冠の疎な支持。PC390320を先に全景比較、カメラと8物理光/縮尺/高塀/右前障子/夜空/乾いた灰茶木/文字0散在小石0固定。

主役は大中の成長面をnative閉面へXYZ連動で彫刻。根・末枝・葉・鉢と属性/位相は保護。surface noiseだけで合格させず、灰形の中立光/夜景、全庭/盆栽/幹寄りで量塊をレビューし採否固定→同形の素材比較。植栽は葉の形と実支持分枝を不均等な占有形へ、390左fragmentと遠冠も全空間で評価。苔BLUE地形/2埋石/鉢足接触は保持。密度・軸・遠冠の各コード旗で切り分け可能。背景を暗くして欠点を隠さない。

R32保留、R33PC CPU1.70→2.60/idle順序別不合格原因未特定のまま引継ぐ。合格待ち小差反復なし。実装負荷rawはcohort直後排他永続保存、既存tol変更なし、見た目と技術別評価。PC総合改善+手機同等非退行なら改善候補、重大負荷・実不具合未解決時は保持。5214R31PID20598は保護、候補5215。finalbuild/必要QA/5完成stillとinline/reduced/WebGLfallback同期/Retina実browser、実phoneSafari熱未検証を分ける。20MiB新増分/shared reuse/旧削除Gitwrite公開購入Libraryretry0。''')
for n in['HANDOFF.md','IMPROVEMENT_PLAN.md']:
 p=D/n;p.write_text(p.read_text()+f'\nStage34 {R.name}開始: 幹枝肩量感と庭植栽実改修。R32/R33性能原因未解決保持、TOPR31PID20598保護、5215/r34試案。\n')
D.joinpath('run-state.json').write_text(json.dumps({'stage':34,'run':R.name,'status':'in_progress_real_form_and_planting_revision','selected_root':'growth-garden-0729','writer_active':True,'started_at_jst':now.isoformat(),'deadline_jst':s['deadline_jst'],'protected_old_states':37,'budget_bytes':20971520,'overall_goal_complete':False,'library_retry_count':0,'TOP_PID':20598,'TOP_port':5214,'comparison_port':5215},indent=2)+'\n')
print(json.dumps({'run':R.name,'started_at_jst':now.isoformat(),'protectedStates':37,'previousFilesVerified':len(m['files']),'free':free,'profileBaseline':start['profile_allocated_bytes_at_start'],'TOPUntouched':20598},indent=2))
