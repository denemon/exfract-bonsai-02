工程33はR32採用保留で終了。TOP5214はR31/PID20598を維持。候補5215/PID20741はcwd/command/portを検証して安全停止した。R32景色の造形・素材・カメラ・光の変更0、旧36状態SHAを保持、新study1で37状態。

R32一次25/27のidleCPU390/320failureは有効な旧記録として保持。前工程の接続中断補測は数値rawが無く、42成功とは扱わない。今回の有限診断16cohort/112値と資格60cohortは完全に別集計。資格の各variant/幅はactive236、idle28、cold2。3priming/2400msの待機描画と30warmupのactiveを区別し、ABBA/BAAB順序別14も集計。

同じ内容のcontrolでCPU中央値2.7→4.7ms、R31で4.9→2.5msの変動があった。renderer区間の幅は大きいが、Three処理とdriver同期呼び出しを分離できず、素材・庭・GC・JIT・driverの原因帰属は未立証。30primingも一貫した改善ではなく、後半だけのためJIT否定には使わない。原因を特定した不可視修正を入れる根拠がないためsite code変更0。

新資格はpool26/27、idle順序別20/24。不通過は下表の5件。閾値は変更0、診断/旧14/中断補測は混入0、再測定0。同一Mac Chrome154/ANGLE Metal/DPR1、PC1440×900/390×844/320×568。pmset温度・周波数取得unsupported、負荷平均と電源は区間前/整定後/後にraw記録。ユーザーChromeは停止していない。これを計測誤差だけとして退行を解消したとは言えない。

| 不通過条件 | baseline ms | candidate ms | delta ms | 許容差 ms |
|---|---:|---:|---:|---:|
| pool pc CPU_submit_ms median | 1.7000 | 2.6000 | 0.9000 | 0.5000 |
| BAAB mobile-390 CPU_idle_submit_ms median | 3.1500 | 4.0500 | 0.9000 | 0.7500 |
| BAAB mobile-320 CPU_idle_submit_ms median | 2.9500 | 4.7500 | 1.8000 | 0.7500 |
| BAAB mobile-320 CPU_idle_submit_ms p95 | 6.3000 | 8.1000 | 1.8000 | 1.5000 |
| BAAB mobile-320 GPU_idle_elapsed_ms median | 15.7460 | 19.0618 | 3.3158 | 3.1492 |

| 幅 | active CPU median R31→R32 ms | active GPU median/p95 R31→R32 ms | idle CPU median R31→R32 ms | idle GPU median/p95 R31→R32 ms | 制限回線 first3D R31→R32 ms |
|---|---|---|---|---|---|
| pc | 1.700→2.600 | 11.248/18.574→11.402/18.477 | 3.700→3.550 | 25.091/28.999→24.352/28.303 | 12076.800→12297.050 |
| mobile-390 | 2.450→2.200 | 10.217/13.605→9.674/13.214 | 3.600→3.550 | 18.998/21.496→19.144/23.065 | 11504.650→11707.000 |
| mobile-320 | 2.600→2.650 | 9.265/12.847→9.413/12.912 | 3.450→4.150 | 18.292/22.216→17.478/21.895 | 11399.350→11622.750 |

idleCPUは常時CPU使用率ではなく2.4秒待機後の1回g.render同期時間。GPUは非disjoint EXT_elapsedの実query。coldはcacheoff/120ms/256000Bpsの模擬制限回線でsystemcoldではない。R32の完成静止画ロードはPC2018ms/3901446ms/3201329ms、inlineFCP約306～308ms、first3D約11.62～12.30秒。DPR2/canvas1.6は表示を確認したが性能qualificationはDPR1のみ。実phone/Safari/温度・周波数/実高LODは未検証。

保存器はcohortごとfsyncし数値を即時保存。初期4idle PCはv1、残56はfinalをhardlinkで排他的に発行するv2。timed browser式SHAは前後同一、warmup/順序/閾値変更0。旧final拒否と新final耐久書込みのfault-injectionを自分の新規fixtureだけで実施し成功。既存raw上書き0。最初の計測前ジョブ引用失敗は別のsetup記録で保持、Chrome33661exit0、計測値の損失0。最終Chrome34202exit0/profileguard解放。

R31/R32の最終buildを新規QA出力へ作成し、全生成ファイルが保護済みproductionとbit exact。既存dist上書き0。R32 functional11（loadingstill、WebGL不可5、idle/input/reduced3、contextlossrestore、noDecompressionHTTPgzip）とdynamic6が合格。機能合格と性能不通過は別。

9枚を新Mac Chromeで撮影保存し、R32PC/390/320＋DPR2/cap1.6の6枚、R31TOP3枚の全JPEGが対応する旧写真とbit exact。root agentは新R32全6と選定R31PC/390を実ピクセル閲覧。R32のPC全体改善と390/320/Retina非退行の旧評価を保持するが、全体高級庭完成はfalse。広い滑らかなS字幹と枝肩、反復する低木葉、苔mat、390左端植栽fragment、疎な遠冠は残課題。

主役・鉢・台石の全体fit、接触、石の埋まり、苔と砂利の接続、高塀/右前障子/夜空/灰茶幹/文字0/散在小石0は同一固定scene。R32 native7/freeze source14、R31/旧全成果、36状態SHAを検証。過去外部PR7の26実path/4manifestentry欠損は既知のままhistorical complete false、存在する保護fileは全SHA検証。復元・削除・Gitwriteは行わない。

参照コードはselected-code→R31とcandidate-code→R32のread-only alias。確認画面 http://127.0.0.1:5214/ 。候補再開を必要とする次runはguard/port/cwdを先に調べ、R32candidateでnode ../../../../../node_modules/vite/bin/vite.js preview --config vite.config.mjs --configLoader nativeを使用。現在5215は停止。

Libraryretry0/画像ID[]。push/PR/merge/外部公開/有料購入/毎時automation/旧project access/既存成果削除0。deadline10/10 23JST。今回形材の大改修は性能判定より先に進めていない。次の最大まとまりはNEXT_WHOLE_QUALITY.md。
