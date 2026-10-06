from pathlib import Path
import json,os,hashlib,datetime,subprocess,signal,time,urllib.request
ROOT=Path('/Users/kazuki.tanaka/dev0/exfract-bonsai-02');D=ROOT/'improvement/2026-10-04';R=D/'runs/idle-causality-0935';P=R.parent/'aged-ensemble-0831';A=R.parent/'growth-garden-0729';J=lambda p:json.loads(p.read_text());H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();q=J(R/'qa/qualified-performance-summary.json');s=J(R/'start.json');now=datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
def new(p,d):
 with p.open('x')as f:json.dump(d,f,ensure_ascii=False,indent=2);f.write('\n')
assert not q['technicalQualificationPassed'] and q['poolPassedCount']==26 and q['orderBlockPassedCount']==20
assert J(R/'qa/chrome-lifecycle.json')['pid']==34202 and J(R/'qa/chrome-lifecycle.json')['exitCode']==0 and not Path(s['reused_qa_profile']+'.active').exists()
assert J(R/'qa/integration-functional-current/results.json')['passed'] and len(J(R/'qa/integration-functional-current/results.json')['results'])==11
assert J(R/'qa/dynamic-selected-scene-proof.json')['passed'] and len(J(R/'qa/dynamic-selected-scene-proof.json')['results'])==6
assert J(R/'qa/final-build-proof.json')['passed'];audit=J(R/'integrity-verification-after-records.json');assert audit['protected_states_count']==36
assert all(H(D/n)==h for n,h in s['protected_state_sha256'].items())
for n,h in J(P/'selected-scene-freeze.json')['sourceSHA256'].items():assert H(P/n)==h
for n,h in J(P/'selected-scene-freeze.json')['fixedNativeSevenSHA256'].items():assert H(P/n)==h
m=J(P/'delivery-manifest.json')
for n,d in m['files'].items():assert H(P/n)==d['sha256']
proof=[]
for group,previous,dpr in [('current-candidate-and-retina',P/'qa/final-candidate',1),('current-candidate-and-retina',P/'qa/retina-final-before-after',2),('current-selected-top',A/'qa/adopted-top-final',1)]:
 for name in ['pc','mobile-390','mobile-320']:
  p=R/'qa'/group/(name+('-dpr2'if dpr==2 else'')+'.jpg');old=previous/(('after-retina-'if dpr==2 else'')+name+'.jpg');assert H(p)==H(old)
  proof.append({'photo':str(p.relative_to(R)),'actualJPEGExactPrevious':True,'old':str(old.relative_to(ROOT)),'sha256':H(p),'DPR':dpr,'rendererDPR':min(dpr,1.6)})
new(R/'qa/final-visual-identity-proof.json',{'rows':proof,'all9ActualJPEGExact':True,'sceneCodeChanged':False,'PCOverallImprovementOverR31CarriedFromR32':True,'390320AndDPR2NonregressionCarriedFromR32':True,'rootAgentActuallyViewedCandidate6AndSelected2':True,'wholeHighEndQualityComplete':False,'residuals':['Wide smoothwoodplanes andsmoothbranchshoulders','Repeatedshrubblades','Broad mossmat','390clippedleftplantingfragment','Sparse distantcrowns']})
new(R/'qa/independent-qualified-review.json',{'reviewer':'/root/volume_review','readOnly':True,'all60RawSHAAndMedianNearestRankP95RecomputedExact':True,'poolPassed':26,'poolTotal':27,'orderBlockPassed':20,'orderBlockTotal':24,'failures':5,'samplerAndThresholdsUnchanged':True,'activeEach236IdleEach28ColdEach2':True,'ChromePID':34202,'DPR':1,'v1First4v2Remaining56':True,'sourceCauseUnidentified':True,'keepR31Agreed':True,'diagnosticOldPrimaryInterruptedSupplementNotPooled':True,'wholeQualityComplete':False})
# Verify exact own process identity and HTTP content before stopping the unneeded candidate server.
proc=subprocess.check_output(['ps','-p','20741','-o','pid=,ppid=,command='],text=True).strip();assert 'vite/bin/vite.js preview --config vite.config.mjs --configLoader native' in proc
cwd=subprocess.check_output(['lsof','-a','-p','20741','-d','cwd','-Fn'],text=True);assert '\nn'+str(P/'candidate')+'\n' in cwd
for port,pid in [(5214,20598),(5215,20741)]:assert subprocess.check_output(['lsof','-nP',f'-iTCP:{port}','-sTCP:LISTEN','-t'],text=True).strip()==str(pid)
http=[]
for port,path,expected in [(5214,'/',A/'candidate/dist/index.html'),(5215,'/compare/r32/',P/'candidate/dist/index.html')]:
 with urllib.request.urlopen(f'http://127.0.0.1:{port}{path}',timeout=10)as res:body=res.read()
 assert hashlib.sha256(body).hexdigest()==H(expected);http.append({'port':port,'path':path,'exactProtectedIndex':True,'sha256':H(expected)})
os.kill(20741,signal.SIGTERM)
for i in range(30):
 live=subprocess.run(['lsof','-nP','-iTCP:5215','-sTCP:LISTEN','-t'],capture_output=True,text=True).stdout.strip()
 if not live:break
 time.sleep(.1)
assert not live;assert subprocess.check_output(['lsof','-nP','-iTCP:5214','-sTCP:LISTEN','-t'],text=True).strip()=='20598'
procAll=subprocess.check_output(['ps','-axo','pid,command'],text=True);assert not any('--user-data-dir='+s['reused_qa_profile'] in x for x in procAll.splitlines())
new(R/'qa/process-and-http-final.json',{'candidatePIDVerifiedBeforeStop':20741,'candidateCWD':str(P/'candidate'),'command':proc,'candidateStopSignal':'SIGTERM','candidatePort5215Stopped':True,'TOPPID20598Unchanged':True,'TOPPort5214ExactR31':True,'HTTPBeforeStop':http,'QAChrome34202Exit0':True,'dedicatedProfileProcessRemaining':False,'userChrome1033Untouched':True})
R.joinpath('selected-code').symlink_to('../growth-garden-0729/candidate');R.joinpath('candidate-code').symlink_to('../aged-ensemble-0831/candidate')
new(R/'decision.json',{'stage':33,'candidate':'aged-ensemble-0831','candidateAdopted':False,'selectedRoot':'growth-garden-0729','technicalQualificationPassed':False,'pool26of27':True,'orderBlocks20of24':True,'allFailedConditions':[g for g in q['gates']+q['orderBlockGates']if not g['passed']],'visualGainRetained':True,'sourceCauseUnidentified':True,'measurementNoiseOnlyExplanationNotEstablished':True,'productSceneChanges':0,'qualificationRepeats':0,'historicalStage32PrimaryFailuresRemain':True,'interruptedStage32SupplementSuccessClaimed':False,'all42QualifiedClaimed':False,'comparisonServerStopped':True,'wholeQualityComplete':False})
state={'stage':33,'run':R.name,'status':'completed_held_after_finite_causal_diagnosis_and_fresh_qualification','candidateAdopted':False,'selectedRoot':'growth-garden-0729','poolPass':26,'poolTotal':27,'orderBlockPass':20,'orderBlockTotal':24,'causeIdentified':False,'sceneChanges':0,'rawQualificationCohorts':60,'rawDiagnosticCohorts':16,'oldStatesPreserved':36,'currentStates':37,'actualCurrentPhotos':9,'all9JPEGExactPrevious':True,'overallGoalComplete':False,'TOPPID':20598,'TOPPort':5214,'comparisonPortStopped':5215,'ChromeExit0':True,'startedAtJST':s['started_at_jst'],'endedAtJST':now.isoformat(),'LibraryRetryCount':0,'LibraryImageIDs':[]}
new(D/'idle-causality-study-state.json',state)
new(R/'finish.json',{**state,'protectedOldStatesSHA256':s['protected_state_sha256'],'newStateSHA256':H(D/'idle-causality-study-state.json'),'elapsedMinutes':(now-datetime.datetime.fromisoformat(s['started_at_jst'])).total_seconds()/60})
lines=['工程33はR32採用保留で終了。TOP5214はR31/PID20598を維持。候補5215/PID20741はcwd/command/portを検証して安全停止した。R32景色の造形・素材・カメラ・光の変更0、旧36状態SHAを保持、新study1で37状態。','', 'R32一次25/27のidleCPU390/320failureは有効な旧記録として保持。前工程の接続中断補測は数値rawが無く、42成功とは扱わない。今回の有限診断16cohort/112値と資格60cohortは完全に別集計。資格の各variant/幅はactive236、idle28、cold2。3priming/2400msの待機描画と30warmupのactiveを区別し、ABBA/BAAB順序別14も集計。','', '同じ内容のcontrolでCPU中央値2.7→4.7ms、R31で4.9→2.5msの変動があった。renderer区間の幅は大きいが、Three処理とdriver同期呼び出しを分離できず、素材・庭・GC・JIT・driverの原因帰属は未立証。30primingも一貫した改善ではなく、後半だけのためJIT否定には使わない。原因を特定した不可視修正を入れる根拠がないためsite code変更0。','', '新資格はpool26/27、idle順序別20/24。不通過は下表の5件。閾値は変更0、診断/旧14/中断補測は混入0、再測定0。同一Mac Chrome154/ANGLE Metal/DPR1、PC1440×900/390×844/320×568。pmset温度・周波数取得unsupported、負荷平均と電源は区間前/整定後/後にraw記録。ユーザーChromeは停止していない。これを計測誤差だけとして退行を解消したとは言えない。','', '| 不通過条件 | baseline ms | candidate ms | delta ms | 許容差 ms |','|---|---:|---:|---:|---:|']
for g in q['gates']+q['orderBlockGates']:
 if not g['passed']:lines.append(f"| {g.get('block','pool')} {g['width']} {g['metric']} {g['quantile']} | {g['baseline']:.4f} | {g['candidate']:.4f} | {g['delta']:.4f} | {g['predeclared_allowed_delta']:.4f} |")
lines+=['', '| 幅 | active CPU median R31→R32 ms | active GPU median/p95 R31→R32 ms | idle CPU median R31→R32 ms | idle GPU median/p95 R31→R32 ms | 制限回線 first3D R31→R32 ms |','|---|---|---|---|---|---|']
for row in q['rows']:
 a,b=row['variants']['r31'],row['variants']['candidate'];fmt=lambda key:f"{a[key]['median']:.3f}→{b[key]['median']:.3f}";gp=lambda key:f"{a[key]['median']:.3f}/{a[key]['p95']:.3f}→{b[key]['median']:.3f}/{b[key]['p95']:.3f}"
 lines.append(f"| {row['width']} | {fmt('CPU_submit_ms')} | {gp('GPU_active_elapsed_ms')} | {fmt('CPU_idle_submit_ms')} | {gp('GPU_idle_elapsed_ms')} | {fmt('cold_first3D_ms')} |")
lines+=['', 'idleCPUは常時CPU使用率ではなく2.4秒待機後の1回g.render同期時間。GPUは非disjoint EXT_elapsedの実query。coldはcacheoff/120ms/256000Bpsの模擬制限回線でsystemcoldではない。R32の完成静止画ロードはPC2018ms/3901446ms/3201329ms、inlineFCP約306～308ms、first3D約11.62～12.30秒。DPR2/canvas1.6は表示を確認したが性能qualificationはDPR1のみ。実phone/Safari/温度・周波数/実高LODは未検証。','', '保存器はcohortごとfsyncし数値を即時保存。初期4idle PCはv1、残56はfinalをhardlinkで排他的に発行するv2。timed browser式SHAは前後同一、warmup/順序/閾値変更0。旧final拒否と新final耐久書込みのfault-injectionを自分の新規fixtureだけで実施し成功。既存raw上書き0。最初の計測前ジョブ引用失敗は別のsetup記録で保持、Chrome33661exit0、計測値の損失0。最終Chrome34202exit0/profileguard解放。','', 'R31/R32の最終buildを新規QA出力へ作成し、全生成ファイルが保護済みproductionとbit exact。既存dist上書き0。R32 functional11（loadingstill、WebGL不可5、idle/input/reduced3、contextlossrestore、noDecompressionHTTPgzip）とdynamic6が合格。機能合格と性能不通過は別。','', '9枚を新Mac Chromeで撮影保存し、R32PC/390/320＋DPR2/cap1.6の6枚、R31TOP3枚の全JPEGが対応する旧写真とbit exact。root agentは新R32全6と選定R31PC/390を実ピクセル閲覧。R32のPC全体改善と390/320/Retina非退行の旧評価を保持するが、全体高級庭完成はfalse。広い滑らかなS字幹と枝肩、反復する低木葉、苔mat、390左端植栽fragment、疎な遠冠は残課題。','', '主役・鉢・台石の全体fit、接触、石の埋まり、苔と砂利の接続、高塀/右前障子/夜空/灰茶幹/文字0/散在小石0は同一固定scene。R32 native7/freeze source14、R31/旧全成果、36状態SHAを検証。過去外部PR7の26実path/4manifestentry欠損は既知のままhistorical complete false、存在する保護fileは全SHA検証。復元・削除・Gitwriteは行わない。','', '参照コードはselected-code→R31とcandidate-code→R32のread-only alias。確認画面 http://127.0.0.1:5214/ 。候補再開を必要とする次runはguard/port/cwdを先に調べ、R32candidateでnode ../../../../../node_modules/vite/bin/vite.js preview --config vite.config.mjs --configLoader nativeを使用。現在5215は停止。','', 'Libraryretry0/画像ID[]。push/PR/merge/外部公開/有料購入/毎時automation/旧project access/既存成果削除0。deadline10/10 23JST。今回形材の大改修は性能判定より先に進めていない。次の最大まとまりはNEXT_WHOLE_QUALITY.md。']
with(R/'REPORT.md').open('x')as f:f.write('\n'.join(lines)+'\n')
with(R/'NEXT_WHOLE_QUALITY.md').open('x')as f:f.write('''次は通常距離の全景で読める、主役の幹の大きい量感と庭の植栽の空間構成を最大のまとまりとして編集前に選定する。R32の広い滑面/滑らかな枝肩へ微小溝だけを増やさず、成長方向へ開く有限の面返り・厚み・圧縮肩をnative閉面へ彫刻する。根/末枝/樹冠空隙/鉢/主輪郭は守り、単色PC/盆栽/幹寄り/両側で成立してから形を固定し、同形で木肌を比較。旧閉じたdent/装飾環/均一noiseへ戻らない。灰茶幹/高塀/右前障子/夜空/無文字/散在小石0と固定cameraは維持。

相手の庭はR32低いleaf占有を参考にするが、反復薄葉・独立fan/長裸軸・苔mat・390左fragment・疎遠冠が未達。主役を囲む近/中/遠の支持枝と根、露出地形、有限の葉密度を一つの配置として編集前に選定。tuft/石追加で埋めず、2石の埋まり/4鉢足/地面高さfieldを保護し、PC390320とRetina実表示で全体の自然さを評価する。材質増加/テスト成功と完成度を混同しない。

性能は今回一回の資格でpool26/27と順序別20/24、R32保留。診断は原因未特定。同条件repeat-until-passや事後threshold緩和はしない。新たな測定が必要なら、文書でsample power/順序/状態・温度取得限界と条件を先に定め、各cohort即時排他checkpointを使う。採用基準はPC全体改善+390320/Retina非退行+qualified技術、全体完成は別。選定R31をbaselineに比較し、採用前のbuild/静止画/inline/reduced/context同期を完了する。

TOP5214/R31/PID20598、候補5215停止、Chrome/profileguardなし、旧36状態保護+study1=37。新run作成前にwriter/Git/空き/PID/cwd/port/manifest/source/native/budgetを確認。20MiB/sharedassets reuse/旧削除Gitwrite公開購入他project変更0/Libraryretry0、deadline10/10 23JST。
''')
for n in ['HANDOFF.md','IMPROVEMENT_PLAN.md']:
 p=D/n;p.write_text(p.read_text()+f'\nStage33 {R.name}終了: 原因未特定、R32保留。新資格pool26/27・idle順序別20/24、一次failure維持/中断42主張なし。景色変更0/9新JPEG旧完全一致/build2/functional11/dynamic6pass。TOPR31PID20598/5214保持、候補20741/5215安全停止、Chrome34202exit0。36旧状態保護+study1=37、全体完成false/Libraryretry0。\n')
D.joinpath('run-state.json').write_text(json.dumps({**state,'writer_active':False,'deadline_jst':s['deadline_jst'],'budget_bytes':20971520},ensure_ascii=False,indent=2)+'\n')
lock=ROOT/'improvement/.active-run';assert J(lock/'owner.json')['run']==R.name;(lock/'owner.json').unlink();lock.rmdir()
print(json.dumps({'run':R.name,'elapsedMinutes':J(R/'finish.json')['elapsedMinutes'],'candidateAdopted':False,'causeIdentified':False,'poolPass':26,'orderBlockPass':20,'TOPPID':20598,'candidatePID20741Stopped':True,'writerAndProfileGuardsRemoved':True,'currentStates':37,'ninePhotosExact':True},indent=2))
