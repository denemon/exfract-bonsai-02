# 工程32 aged-ensemble-0831

採用保留。PC全体の改善、390/320とDPR2表示の非退行を独立実見で確認したが、一次技術25/27でidleCPUmedian390/320が不合格。補測は実行環境接続復旧で中断し数値raw未保存、評価不能。TOPはR31同内容を復旧して維持。名品古木・高級庭の完成は未達、overall_goal_complete=false。

2026-10-06T08:34:09.383401+09:00開始、2026-10-06T09:26:04.393738+09:00終了、所要51.9分。期限2026-10-10 23:00JST。編集前に幹滑面/枝肩と近景低木/根土の二領域を独立選定。単色形の全景/幹/左右14像→形固定→同形で色/粗さ/normalの独立比較→庭形/密度比較17像→Retina6像。主輪郭/根/末枝geometry/2800sprays/鉢/土台/高塀/右前障子/夜空/光/カメラを保護。添付参照は実ピクセル確認済みだが、現在形が参照品質へ到達したとは認定しない。

aged-v01はR29grown-v02の閉じたnative面への有限coupledXYZ4strokes。119頂点変更、最大16.547mm native/10.921mm world、4106mask保護。閉面/非多様体/交差0、freshBlender再読込、native7SHA固定。単色では支持面が幹寄り/左右で少し読みやすいだけで、通常距離の形だけの明確な改善は未立証。変位量やQA成功を美的完成の根拠にしない。losslesscompactgzip641251B、2800foliage/accessor/instance buffers保護。compact-model-proof-v02.jsonは引継ぎファイル名で、内容版はaged-v01。

木肌は成長UVへ有限43medium/710smallのatlas、worldheight1.3/.28mm、main/branch方向と周期angularU、V2.8native m/1.848world m。色/粗さ/normalを同aged形・同R30庭で比較。乾いた灰茶色として成立するが旧normal-v4→v5の利得は小さい。均一noise/輪郭displacement追加0。低木は2033葉/369短枝/166fork/4閉じた薄葉形を保持、既存支持を低く短く運んで葉占有を根近くへ戻した。PC改善の主因はこの形で、R31長裸主軸/crest失敗は再発せず。13根位置/7mm埋まり固定。苔R/G553pixelのみ実根と低木下で変更、全heightBlue・236599保護pixelはbyte一致。新crest/点tuft/小石/葉追加0。28背景mesh、二石/4鉢足接触、後景/建築geometry保護。

PCは識別できる改善、390/320非退行。390左端植栽は切れた弱い断片、広い滑面・滑らかな枝肩・低木葉反復・苔広面・疎な遠冠が残る。RetinaはMacChrome154/ANGLEMetalのCDP DPR2、canvascap1.6（PC2304×1440/390624×1350/320512×908）の実描画。物理モニタ撮影/実機スマホではない。高密度でも新丸dent/薄lip/濡れた光沢退行は確認せず、古木の完成とは判断しない。

最終buildと復旧後同source build成功。own完成5WebP＋inline5同期。新Chrome20964でbasic11case（実モデル保留静止画、noWebGL5、静止/入力制限/reduced3、実contextlossrestore、DecompressionStreamなしHTTPgzip）成功。現在aged包絡でpubliclegacyboth/stable有効3、original/stable保守fallback無効3のPNG SHA parity成功。R27render-partition source byte一致。original72対batch12のstrictpixel完全一致や既知R27/R31の30pixel差解消は主張しない。最終candidate PC390320実JPGはqa/final-candidate/、形/葉/庭/光/投影は固定候補とexact。文字/overflow/remote/font0。復旧後機能成功を性能failureの代替にしない。

一次性能の事前27条件の25通過、390idleCPUmedian2.250→4.600ms（+2.350/許容.750）と3203.800→4.650ms（+.850/許容.760）が不合格。PC3.700→4.450msは+.750境界通過。新failureを根拠に一度だけABBA+BAAB補測を事前記録、同source/閾値/待機/DPR、一次/順序別/全42/各cohortを分ける方針だった。しかしexecutor key changed during session recoveryで旧TOP90351/compare7840/Chrome99940/測定Nodeが終了、consoleはPC8/3908/3202cohort件数だけを保存しCPU/GPU数値rawは未保存。42集計・通過を復元/推測しない。一次raw保持、原因のGC/driver/周波数断定0、閾値変更/合格まで再測定0。旧Chromeexitcode不明、新Chromeの終了結果を別記。

|幅|active CPU median/p95 ms R31→候補|active GPU median/p95 ms|idle CPU median ms一次14|idle GPU median/p95 ms一次14|cold first3D median秒|候補完成静止画秒|
|---|---|---|---|---|---|---|
|pc|2.200/4.600→2.300/4.700|10.126/13.570→10.382/13.354|3.700→4.450|22.962/28.761→25.177/29.304|12.047→12.267|2.008|
|mobile-390|3.500/5.000→2.900/4.900|9.205/12.390→9.479/12.134|2.250→4.600|17.060/21.431→19.560/22.388|11.482→11.665|1.435|
|mobile-320|2.000/4.200→2.400/5.000|9.110/12.018→9.410/12.412|3.800→4.650|18.860/21.891→20.311/22.205|11.378→11.586|1.306|

active236/版/幅、idle14/版/幅、cold2/版/幅、同Mac/旧Chrome99940/同5215origin/DPR1。CPUはrender submissionでpresentedframeではない。coldはcacheoff120ms256000B/s simulated、systemcoldではない。一次の数値は接続問題前に完了・保存済み。補測は評価不能で追加有効sample0。性能一方向改善/60fps保証0。3D約12秒とidle負荷は未解消。実phone/Safari/熱/持続FPS/highLOD/実行モデルmetadata未検証。

TOP http://127.0.0.1:5214/ はR31同source、復旧PID20598 session63808。候補 http://127.0.0.1:5215/compare/r32/ はPID20741 session95539。source35state/R31manifest全SHAを確認して復旧、旧R31へ書込なし。今回のstudy-stateを新規保存し既存bestは変更しない。

20MiBはownrun/sharedprofile・cache正増分/STAGING/coordinator/新state/guardを保守算入。最終capacity/manifest/receiptで確認。旧35state全SHAと保護source/production/旧manifestを再確認。既知externalPR7欠損26actual paths/4manifest entriesは復元・削除せず、既存全SHA確認と歴史完全性falseを明記。Library retry0/ID0、Gitwrite/push/PR/merge/公開/購入/毎時automation/旧projectアクセス/旧deliverable削除0。
