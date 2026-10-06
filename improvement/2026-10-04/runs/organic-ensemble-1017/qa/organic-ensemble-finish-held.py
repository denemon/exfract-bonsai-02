from pathlib import Path
import json,hashlib,os,datetime,subprocess,shutil,gzip
ROOT=Path('/Users/kazuki.tanaka/dev0/exfract-bonsai-02');D=ROOT/'improvement/2026-10-04';R=D/'runs/organic-ensemble-1017';S=Path('/Users/kazuki.tanaka/Documents/Codex/2026-10-04/task-2');J=lambda p:json.loads(p.read_text());H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
s=J(R/'start.json');q=J(R/'qa/qualified-performance-summary.json');v=J(R/'qa/final-display-invariants.json');c=J(R/'qa/capacity-transcode-record.json')
assert not q['technicalQualificationPassed'];assert v['functional11Pass'] and v['dynamic6Pass'];assert J(R/'qa/chrome-lifecycle.json')['exitCode']==0;assert not Path(s['reused_qa_profile']+'.active').exists()
assert '✓ built' in (R/'qa/build-final.log').read_text()
for n,h in s['protected_state_sha256'].items():assert H(D/n)==h
freeze=J(R/'selected-scene-freeze.json')
for n,h in (freeze['sourceSHA256']|freeze['fixedNativeSevenSHA256']).items():assert H(R/n)==h
assert hashlib.sha256(gzip.decompress((R/'qa/garden-planting-shape-v01/results.json.gz').read_bytes())).hexdigest()==c['originalSHA256']
for port,pid in [(5214,20598),(5215,61480)]:assert subprocess.check_output(['lsof','-nP',f'-iTCP:{port}','-sTCP:LISTEN','-t'],text=True).strip()==str(pid)
now=datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)));duration=(now-datetime.datetime.fromisoformat(s['started_at_jst'])).total_seconds()/60
rows=[]
for r in q['rows']:
 for variant,label in [('r31','R31'),('candidate','R34')]:
  z=r['variants'][variant];f=lambda n:f"{z[n]['median']:.3f}/{z[n]['p95']:.3f}";rows.append(f"| {r['width']} | {label} | {f('CPU_submit_ms')} | {f('GPU_active_elapsed_ms')} | {f('CPU_idle_submit_ms')} | {f('GPU_idle_elapsed_ms')} | {z['cold_first3D_ms']['median']:.1f} | {z['cold_completed_still_ms']['median']:.1f} |")
fail=[x for x in q['gates']+q['orderBlockGates'] if not x['passed']]
failureText='\n'.join(f"- {x.get('block','pool')} {x['width']} {x['metric']} {x['quantile']}: {x['baseline']:.6f}→{x['candidate']:.6f}、Δ{x['delta']:.6f}、許容{x['predeclared_allowed_delta']:.6f}" for x in fail)
report=f'''Stage34 organic-ensemble-1017は幹枝肩と庭植栽の実改修を行い、視覚ゲートを通したが性能資格を満たさず保留。TOPはR31 growth-garden-0729/5214 PID20598を保持。比較試案は http://127.0.0.1:5215/compare/r34/ 、PID61480/session69250。完成した高級庭の認定はfalse。

開始{s['started_at_jst']}、終了{now.isoformat()}、{duration:.2f}分。最大二領域: 広い滑面/枝肩の量感と、近中遠植栽の反復・支持内占有。高塀/右前障子/夜空/乾いた灰茶木/無文字/散在小石0、同camera/8物理光/縮尺を保持。参考302×404は先行実ピクセル参照を継承。新Library取得・retryなし。

六つの有限XYZ成長面をnative閉面へ直接彫刻。初回枝肩非隣接交差1を保存前に修正し、ログ保持。最終1066頂点変化、native最大56.306956mm/world37.162591mm、3274mask保護。5394verts/5392faces/10784tri、volume0.096048962599、boundary/nonmanifold/非隣接交差0。根/末枝/属性UV/color/index/全boundsと葉配置を保持、freshBlender再読込一致。単色14枚の同camera/light/projection/nativeLeafWorld7対、独立形採否固定後、素材12枚の同形6対を分離。v5は細かな乾いた肌の僅かな改善で、形改善の根拠にはしない。7nativeSHAはqa/fixed-living-shape-v01.json。

庭は近景2033thinclosedleaf/369shoot/166forkを維持し、非対称な曲率と向き・実支持を調整。前根を25cm内側/16cm奥へ移し、実地面への7mm埋まりをraycast確認。遠景3樹/18冠regionを維持、支枝内側へ占有を寄せて実葉26964へ(旧31080)減。初回v01の厚い豆/折れ葉感は棄却し、葉表裏の実間隔0.50〜0.82mmへ一回修正。木形living-v01固定の庭v02正規8枚と中立全庭で採否を評価。BLUE高さ全一致、236599保護pixel完全一致、312RGpixelのみ変更。二埋石、鉢足、建築を保持。

最終PC390320+DPR2の6実Chrome画像をrootと独立reviewerが実見。PC総合改善、390/320非退行。DPR2はcanvascap1.6。樹冠・鉢・土台の投影とR31 camera/light3幅一致。広い滑面と三角肩、折れ葉反復、390左植栽部分像、苔面均一さは残る。写真/scan-grade/数千万円級の完成とは主張しない。

最終build53modules成功、最終full5WebPとinline5同期、HTTPHTML/modelgzip/still5全body一致。freshChrome61609: loading/noWebGL5幅/idleframe0/boundedinput+reduced3幅/contextlossrestore/noDecompressionStreamの11、影authority/灯移動/invalidnative/instancefallbackの実PNGparity6成功。R27renderer/foliagecode完全一致。実phone/Safari/高LOD/熱・frequency未検証。Mac Chrome154/ANGLEMetalのviewportemulation。

有限component14はコード旗で幹/材質/近景/遠景/同内容controlを分離、390activeCPUmedian2.05→3.60ms/GPU10.311→9.909ms。順序間変動が大きく因果確定なし。R33PC CPU1.70→2.60とR32/R33失敗は未解決記録を保持。最終資格は一回だけ60cohort、rawを各cohort直後wx/fsync/hardlink排他保存。最初からlosslessgzip、old14/診断/中断42をpoolせず、既存9tol変更0。active236、idle28、cold2/variant/width。pool{q['poolPassedCount']}/27、idle順序別{q['orderBlockPassedCount']}/24。CPUはrender同期submit時間で、連続idleCPU使用率やpresentedframeではない。GPUは実EXT query、温度/frequencyunsupported、userChrome/background負荷未制御、coldはcacheoff120ms256000Bpsでsystemcoldではない。

| 幅 | 版 | activeCPU med/p95 ms | activeGPU med/p95 ms | idleCPU med/p95 ms | idleGPU med/p95 ms | first3D median ms | completedstill median ms |
|---|---|---|---|---|---|---|---|
{chr(10).join(rows)}

未達条件:
{failureText}

予算は本工程中に一時超過。qa/capacity-transcode-record.jsonの観測charge {c['observedConservativeChargeBefore']}B、上限超過{c['overByBytes']}B。共有profile増分と最終DPR出力の見積り不足であり、全期間20MiB合格はfalse。旧sealed成果物には触れず、本工程新生成の庭v01results一件のみgzipへ可逆移行、元全バイトSHA完全復元を検証、numericraw破棄0。最終charge/実freeはcapacity-final.jsonを参照。旧状態37/旧sealedsource/HEAD保護、Gitwrite/push/PR/merge/公開/購入/自動化/旧projectアクセス/Libraryretry0。LibraryIDs=[]。
'''
with (R/'REPORT.md').open('x') as f:f.write(report)
with (R/'NEXT_WHOLE_QUALITY.md').open('x') as f:f.write('''R34は視覚改善候補として保存、R31TOP維持。R32/R33原因未特定とR34数値失敗を消さない。小差合格待ち再測定はしない。次は同内容control/幹/近景/遠冠/材質の既存旗を用い、実レンダ経路のJS/driver/背景proxy/初期化後GCをコードと描画要素で切り分け、実装変更が根拠を持つ場合だけ必要な資格を一回実測。閾値を都合よく変更しない。見た目と負荷は別。

全体品質残差: 広い滑面/左上三角肩、葉の折れ形反復と遠冠上端、390左植栽部分像、苔matの均一さ。次の造形は最大二つを普通全景で再選定、現living-v01量感を壊さず、実枝葉の厚み/支持/奥行き・地面境界から設計する。背景を暗くせず形採否→同形素材。木の追加長溝・丸dent・薄lip、裸扇軸、大豆葉、点tuft/小石を反復しない。

開始容量guardはsharedprofileの観測peakと最終画像予定量を予約。新rawは最初からgzip、同じ巨大metadataを各画像へ複写しない。旧sealed版削除/旧raw上書きは0、今回新raw可逆移行1と一時budgetmissは保持。5214PID20598/5215PID61480の現在CWD/commandとwriter/profguard/Git/freeを先に確認。実phone/Safari/熱、高LOD/runtime metadataは未検証。Libraryretry0。deadline10/10 23JST。
''')
state={'stage':34,'run':R.name,'status':'held_visual_gain_performance_failed_and_temporary_budget_miss','candidateAdopted':False,'selected_root':'growth-garden-0729','PCOverallVisualImprovement':True,'mobile390320DPR2Nonregression':True,'poolPass':q['poolPassedCount'],'poolTotal':27,'orderBlockPass':q['orderBlockPassedCount'],'orderBlockTotal':24,'technicalQualificationPassed':False,'temporaryBudgetLimitExceeded':True,'budgetOverByBytes':c['overByBytes'],'currentNewRawLosslessTranscodeCount':1,'R32R33CauseUnresolved':True,'sourceChanges':True,'oldStatesPreserved':37,'newStates':1,'currentStates':38,'TOP_port':5214,'TOP_PID':20598,'comparison_port':5215,'comparison_PID':61480,'overall_goal_complete':False,'started_at_jst':s['started_at_jst'],'ended_at_jst':now.isoformat(),'Library_retry_count':0,'Library_image_ids':[]}
with (D/'organic-ensemble-study-state.json').open('x') as f:json.dump(state,f,ensure_ascii=False,indent=2)
for n in ['HANDOFF.md','IMPROVEMENT_PLAN.md']:
 p=D/n;p.write_text(p.read_text()+f"\nStage34 {R.name}終了: PC総合視覚改善/390320+DPR2非退行、資格pool{q['poolPassedCount']}/27・idle順序別{q['orderBlockPassedCount']}/24未達で保留。TOPR31PID20598保持、候補5215/r34 PID61480。build/11functional/6dynamic/5full+inline同期pass、完成false。20MiB一時超過{c['overByBytes']}Bを保持、新生成raw1件losslessgzip/旧sealed削除0。37旧state保護+study1=38。Libraryretry0。\n")
D.joinpath('run-state.json').write_text(json.dumps({**state,'writer_active':False,'deadline_jst':s['deadline_jst'],'budget_bytes':20971520,'TOPSession':63808,'comparisonSession':69250},ensure_ascii=False,indent=2)+'\n')
with (R/'finish.json').open('x') as f:json.dump({**state,'endedAtJST':now.isoformat(),'durationMinutes':duration,'ChromeExit0':True,'profileGuardRemoved':True,'writerRemovedAfterReport':True},f,indent=2)
lock=ROOT/'improvement/.active-run';assert J(lock/'owner.json')['run']==R.name;(lock/'owner.json').unlink();lock.rmdir()
print(json.dumps({'held':True,'poolPass':q['poolPassedCount'],'blockPass':q['orderBlockPassedCount'],'temporaryBudgetOverBytes':c['overByBytes'],'TOPPID':20598,'candidatePID':61480,'statesCurrent':38,'durationMinutes':duration,'writerRemoved':True},indent=2))
