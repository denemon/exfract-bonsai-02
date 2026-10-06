from pathlib import Path
import json,hashlib,datetime,subprocess,os
ROOT=Path('/Users/kazuki.tanaka/dev0/exfract-bonsai-02');D=ROOT/'improvement/2026-10-04';R=D/'runs/growth-garden-0729';J=lambda p:json.loads(p.read_text());H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();s=J(R/'start.json');perf=J(R/'qa/qualified-performance-summary.json');post=J(R/'qa/post-transition.json');pid=post['preview_pid'];session=post['preview_session']
assert perf['all_predeclared_nonregression_conditions_pass'];assert J(R/'qa/adopted-top-final/results.json')['passed'];assert J(R/'qa/served-adopted-identity.json')['passed'];assert J(R/'qa/chrome-lifecycle.json')['exitCode']==0
assert not Path(s['reused_qa_profile']+'.active').exists();owner=ROOT/'improvement/.active-run/owner.json';assert J(owner)['run']==R.name
assert subprocess.check_output(['lsof','-nP','-iTCP:5214','-sTCP:LISTEN','-t'],text=True).strip()==str(pid);assert not subprocess.run(['lsof','-nP','-iTCP:5215','-sTCP:LISTEN','-t'],capture_output=True,text=True).stdout.strip()
for n,h in s['protected_state_sha256'].items():assert H(D/n)==h
now=datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)));elapsed=(now-datetime.datetime.fromisoformat(s['started_at_jst'])).total_seconds()/60
state={'stage':31,'run':R.name,'status':'qualified_provisional_adoption','selected_root':R.name,'previous_TOP':'program-state-0426','selected_scene':'grown-v02/normal/R30near-shore-v02/R27stableRenderer','candidate_adopted':True,'R31_crest_v01_v02_adopted':False,'criterion':'PC overall improvement plus390320 nonregression and qualified technical conditions','PC_overall_improvement':True,'mobile390_nonregression':True,'mobile320_nonregression':True,'all_three_widths_clearly_superior':False,'current_qualified_performance_measured':True,'current_idle_cold_measured':True,'qualified_performance_nonregression_pass':True,'native_rebuild_count':0,'fixed_grown_7_SHA':s['fixed_grown_shape'],'R30_garden_read_only':True,'scatteredSmallStones':0,'text_visible':0,'final_three_images':[f'runs/{R.name}/qa/adopted-top-final/{n}.jpg'for n in ['pc','mobile-390','mobile-320']],'preview':'http://127.0.0.1:5214/','preview_pid':pid,'preview_session':session,'whole_high_end_garden_complete':False,'overall_goal_complete':False,'remaining_quality':['broad smooth wood and branch shoulders','moss mat and low shrub growth direction','distant irregular crowns'],'performance_limits':['PCactiveGPUp95+1.605ms','idlemedian increased especiallyPC+4.909ms','cacheoff first3D around12sec','realphone Safari thermal and highLOD not qualified'],'library_retry_count':0,'library_image_ids':[],'protected_old_states':33,'ended_at_jst':now.isoformat()}
blob=json.dumps(state,ensure_ascii=False,indent=2)+'\n';newstates=['growth-garden-study-state.json','provisional-best-growth-garden-state.json']
for n in newstates:
 with(D/n).open('x')as out:out.write(blob)
rows=[]
for row in perf['rows']:
 for variant in ['r27','candidate']:
  m=row['variants'][variant];rows.append('|'+row['width']+'|'+variant+'|'+f"{m['CPU_submit_ms']['median']:.3f} / {m['CPU_submit_ms']['p95']:.3f}"+'|'+f"{m['GPU_active_elapsed_ms']['median']:.3f} / {m['GPU_active_elapsed_ms']['p95']:.3f}"+'|'+f"{m['GPU_idle_elapsed_ms']['median']:.3f} / {m['GPU_idle_elapsed_ms']['p95']:.3f}"+'|'+f"{m['cold_first3D_ms']['median']/1000:.3f}"+'|'+f"{m['cold_completed_still_ms']['median']/1000:.3f}"+'|')
report=f'''# Stage31 — qualified改善版の暫定採用

grown-v02木大形とR30 near-shore-v02庭の統合を、R27から暫定採用。採用基準はPC普通鑑賞距離の総合改善、390/320同等か改善、qualified技術条件。全幅それぞれの明確優越を要求した旧gateを修正し、名品古木・高級庭の全体完成はfalseを維持した。

独立レビューはR30旧holdに重大な視覚退行を認めず、PC改善/390320非退行を認定。旧holdの具体要因は過剰な全幅優越条件とqualified性能/idle/cold未実施。今回、R27同origin比較、全景/盆栽/幹寄り/中立base-normalを実見し同じ視覚判断。幹の部位厚みと短い返り、近景の薄葉/支持枝/根土岸は改善。主役・鉢台石・障子の関係は維持。

新しい庭案は均等扇根を親軸に接続する主従枝、連続地形18–32mmの低いcrest、density低起伏の一案。主役木・葉数2033/薄葉4型/166fork、二石/台座の保護域を固定。V01の普通距離画像9枚で長い裸枝・角張りが先に見え、PCはR30を超えず390植栽層弱化。1回の修正V02で芽を手前へ、短い右枝を低く前へ戻したが、長い斜め軸と開いた枝角が残り、PCの明確前進なし。320概ね同等。独立レビューと自分の実見で不採用、第三修正0。形固定のdensity baseline比較も保存。最終defaultはread-only R30庭へ戻し、V01/V02は /compare/r31/crest-v01.html・crest-v02.html だけに残した。実験の形状成功を完成品質と混同しない。

最終選択6全景はR30とnativewood全属性/world、2800主役sprayworld、actualcamera/light/exposure、主役hash/projectedboundsが一致。中立木base-normalは同形同光。grown-v02 native/GLB/compact/制御/inspection/roundtrip/shapeproof7SHA固定、native再作成0。R27rendererソースbyte同一、actual8physical光/同5shadow、72→12batchと有限5光包絡が有効。両案programkey100frames0は別診断であり性能合格の代用にしない。

| 幅 | 版 | CPU submit med/p95 ms | active GPU med/p95 ms | idle GPU med/p95 ms | cacheoff first3D median s | 完成fullstill median s |
|---|---|---|---|---|---|---|
{chr(10).join(rows)}

activeはABBA/BAAB、30warm/61各cohort先頭2除外、236/版/幅。CPUはuninstrumented描画submit、GPUはEXT_disjoint実elapsed、毎sample actualrender+1確認。idleは各sample実2400ms以上待機、ABBA14/版/幅。coldは120ms遅延256000B/s cacheoff ABBA2/版/幅。事前非退行tolerance18条件通過。PCactiveGPU p95増加約1.605ms、idleGPUmedianPC約4.909ms・idleCPUmedian3.15→4.85ms増加は隠さず記録、性能一律改善とはしない。旧R27測定は参照だけ。初回3D約12秒とidleGPU負荷は残課題。実phone/Safari/熱/持続FPS/systemcold/highLODは未検証。CPUは提示完了frame時間を意味しない。測定用expression余分なbraceは失敗記録を保存して修正し、同事前protocolで実測、サイトruntimefailureではない。動的初回は古いoriginal72葉群対stable12batch比較helperを移しstrict失敗。settled R27/R31とも30画素差・max26・mean.0001173・bbox一致で待ち不足ではなく既知batch差。strict original/batch完全同値は主張せず、正しいlegacyboth比較と無効時original fallbackへ修正し失敗/診断を保存した。

最終build成功。actual完成5WebPはR30保護写真とbyte一致しread-only aliasで再利用、inline5同期。basic11case（読込保留静止画、noWebGL5、入力/静止/reduced3、実contextlossrestore、DecompressionStreamなしHTTPgzip）成功。現在木包絡でpublic legacyboth/stable（有効3）とoriginal/stable保守fallback（無効3）PNG動的case parity、有限光/木local/instanceversion変更で保守fallbackを確認。served comparison/adopted decodedidentity、最終TOP PC3903203D/JPG同選択版byte一致とnoWebGL3を確認。文字0、overflow0、remote/font0。PC/390/320の樹冠鉢土台uncut。使用ChromeはMac上の実ブラウザでviewport emulation、実端末の検証ではない。

5214はgate記録後だけ更新。旧28897と比較63853の専用cwd/processを確認してSIGINT、新TOPPID{pid}/session{session}。Chrome72496正常終了/profileguard解除、writer解除。新study/provisionalbest2、旧33stateSHA全保持→35。旧成果削除0、GitHEAD固定/許可3coorsのみ。外部歴史PR7既削除26paths/4manifestentriesのため過去完全性false、存在する全保護fileはSHA確認。Libraryretry0/IDs0、以前のTLS阻害を再試行していない。push/PR/merge/外部公開/購入/automation/旧projectaccess0。20MiB追加allocationはcapacity-final/receiptで保守計上する。

全体完成false。幹の広い滑面と滑らかな肩、苔mat、扇軸が残る近景、遠冠の自然さが残る。名品古木や高級旅館庭の十分な説得力をまだ認定しない。木の大形を再び局所膨張で追わず、次の一案は ordinary-distance全景で自然な地形/成長方向を成立させる骨格を編集前にレビューし、現暫定bestを固定基準にする。受入gateを再び全幅明確優越へ戻さない。

時刻 {now.isoformat()}、工程{elapsed:.1f}分。期限2026-10-10 23JST内。要求Sol xhighの実runtime metadataは未検証。成果と証跡はこのrun、確認用PC390320はqa/adopted-top-final/。
'''
with(R/'REPORT.md').open('x')as out:out.write(report)
nexttext='''# 次の全体品質milestone

暫定bestはgrown-v02/normal/R30near-shore-v02、R31crest案不採用を固定する。高塀・右前障子・夜空・乾いた灰茶木・文字0・散在小石0、主役7SHAとcamera/光を保護する。

次は庭の一つの構造案を先に全景設計・独立レビューする。近景植栽は均等に伸びる裸軸を避け、低く埋まる主幹から外光へ自然に連なる葉の占有形/成長方向を決める。苔は同じ土壌面の厚みと歩留まりのある境界から起伏を作り、長い細いcrestを視覚上の筋にしない。葉数増加/点tuft/小石追加/無制限micro修正を主眼にしない。幹量塊は固定。普通距離PC390320から一空間として改善か評価し、形と材質は別比較する。

PC全体前進+390320同等/非退行+必要技術条件で改善版の暫定採用を認め、全体完成とは別扱い。一案一回修正まで、上回らなければ保存してやめる。幹の滑面/肩と遠冠は残課題として管理し、終盤は主役と庭の全景説得力を独立レビュー。idlemedian負荷/約12secfirst3Dは残性能課題で、qualified実測のない成功宣言はしない。

20MiB段階budget/sharedread-only/profile/cache/新規QA output/旧保存0delete、writer/Git/free外部変更preflight。5214は資格通過後だけ更新。10/10 23JSTまで、Libraryretry0、公開購入Gitwrite他projectaccess0。
'''
with(R/'NEXT_WHOLE_QUALITY.md').open('x')as out:out.write(nexttext)
finish={'stage':31,'run':R.name,'ended_at_jst':now.isoformat(),'elapsed_minutes':elapsed,'candidate_adopted':True,'selected_TOP':R.name,'selected_scene':state['selected_scene'],'experimental_V01V02_adopted':False,'whole_high_end_garden_complete':False,'overall_goal_complete':False,'trial':'http://127.0.0.1:5214/compare/r31/','preview_pid':pid,'preview_session':session,'Chrome_pid':72496,'Chrome_exit':0,'writer_profile_guard_removed':True,'new_state_sha256':{n:H(D/n)for n in newstates},'protected_old_states':33,'current_states':35,'library_retry_count':0,'library_image_ids':[]}
with(R/'finish.json').open('x')as out:json.dump(finish,out,indent=2)
handoff=f'''# 確認用サイト

TOP http://127.0.0.1:5214/ はStage31 {R.name}をqualified暫定採用。grown-v02 normal/R30near-shore-v02/R27stableRenderer。PC総合前進、390320同等/非退行。全体高級庭完成false、V01V02crest案は不採用。

REPORT/NEXT/qualified-performance-summary/selected-final-invariants/independent-selected-visual-reviewは runs/{R.name}/。PC390320確認JPGは同qa/adopted-top-final/。完成5WebP read-only R30 byte一致+inline同期、basic11/dynamic6/finalTOP6/build/HTTPidentity成功。性能18事前条件通過、active236・idle14・cold2/版/幅を現在実測。PCactiveGPU p95+1.605ms、idlemedian+4.909ms、first3D約12秒は残課題。

暫定bestはこの統合、旧R27は/compare/r27/。R31新庭は/compare/r31/crest-v01.html・crest-v02.htmlだけ。幹7SHA/camera/光/architectureを固定、2033thinleaf166fork/地形65952tri/石と鉢接触保持。幹滑面肩・苔mat/低木扇軸・遠冠自然さは未達。旧33states保持/newstudy+provisionalbest2→35、HEAD固定/許可3coorsのみ。Chrome72496exit0/profilewriter解除、単一5214PID{pid}/session{session}。20MiBseal、Libraryretry0/IDs0、実phoneSafari熱高LOD/runtime metadata未検証。外部歴史完全性false、禁止操作0、deadline10/10 23JST。
'''
(D/'HANDOFF.md').write_text(handoff)
(D/'IMPROVEMENT_PLAN.md').write_text(f'# 進行計画\n\nStage31 {R.name}終了。資格を満たしたR29木+R30庭をR27から暫定採用。新crest案V01/V02は棄却。PC総合改善+390320非退行+技術gateを維持し、全体完成false。\n\n'+nexttext)
(D/'run-state.json').write_text(json.dumps({**finish,'status':'completed_qualified_provisional_adoption','selected_root':R.name,'writer_active':False,'deadline_jst':s['deadline_jst'],'capacity_receipt':'runs/'+R.name+'/qa/final-receipt.json'},indent=2)+'\n')
owner.unlink();owner.parent.rmdir();print(json.dumps(finish,indent=2))
