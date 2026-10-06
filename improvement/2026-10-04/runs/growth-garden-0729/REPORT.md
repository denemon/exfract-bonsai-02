# Stage31 — qualified改善版の暫定採用

grown-v02木大形とR30 near-shore-v02庭の統合を、R27から暫定採用。採用基準はPC普通鑑賞距離の総合改善、390/320同等か改善、qualified技術条件。全幅それぞれの明確優越を要求した旧gateを修正し、名品古木・高級庭の全体完成はfalseを維持した。

独立レビューはR30旧holdに重大な視覚退行を認めず、PC改善/390320非退行を認定。旧holdの具体要因は過剰な全幅優越条件とqualified性能/idle/cold未実施。今回、R27同origin比較、全景/盆栽/幹寄り/中立base-normalを実見し同じ視覚判断。幹の部位厚みと短い返り、近景の薄葉/支持枝/根土岸は改善。主役・鉢台石・障子の関係は維持。

新しい庭案は均等扇根を親軸に接続する主従枝、連続地形18–32mmの低いcrest、density低起伏の一案。主役木・葉数2033/薄葉4型/166fork、二石/台座の保護域を固定。V01の普通距離画像9枚で長い裸枝・角張りが先に見え、PCはR30を超えず390植栽層弱化。1回の修正V02で芽を手前へ、短い右枝を低く前へ戻したが、長い斜め軸と開いた枝角が残り、PCの明確前進なし。320概ね同等。独立レビューと自分の実見で不採用、第三修正0。形固定のdensity baseline比較も保存。最終defaultはread-only R30庭へ戻し、V01/V02は /compare/r31/crest-v01.html・crest-v02.html だけに残した。実験の形状成功を完成品質と混同しない。

最終選択6全景はR30とnativewood全属性/world、2800主役sprayworld、actualcamera/light/exposure、主役hash/projectedboundsが一致。中立木base-normalは同形同光。grown-v02 native/GLB/compact/制御/inspection/roundtrip/shapeproof7SHA固定、native再作成0。R27rendererソースbyte同一、actual8physical光/同5shadow、72→12batchと有限5光包絡が有効。両案programkey100frames0は別診断であり性能合格の代用にしない。

| 幅 | 版 | CPU submit med/p95 ms | active GPU med/p95 ms | idle GPU med/p95 ms | cacheoff first3D median s | 完成fullstill median s |
|---|---|---|---|---|---|---|
|pc|r27|3.600 / 5.100|10.361 / 12.934|21.266 / 28.640|11.972|2.156|
|pc|candidate|3.350 / 4.900|10.414 / 14.539|26.175 / 28.890|12.155|2.030|
|mobile-390|r27|2.100 / 4.900|9.751 / 12.650|17.202 / 21.955|11.479|1.387|
|mobile-390|candidate|2.400 / 5.000|9.775 / 12.801|20.857 / 22.583|11.494|1.453|
|mobile-320|r27|3.300 / 5.000|9.362 / 12.519|15.994 / 21.750|11.381|1.249|
|mobile-320|candidate|3.550 / 4.800|9.541 / 12.822|18.390 / 21.198|11.398|1.316|

activeはABBA/BAAB、30warm/61各cohort先頭2除外、236/版/幅。CPUはuninstrumented描画submit、GPUはEXT_disjoint実elapsed、毎sample actualrender+1確認。idleは各sample実2400ms以上待機、ABBA14/版/幅。coldは120ms遅延256000B/s cacheoff ABBA2/版/幅。事前非退行tolerance18条件通過。PCactiveGPU p95増加約1.605ms、idleGPUmedianPC約4.909ms・idleCPUmedian3.15→4.85ms増加は隠さず記録、性能一律改善とはしない。旧R27測定は参照だけ。初回3D約12秒とidleGPU負荷は残課題。実phone/Safari/熱/持続FPS/systemcold/highLODは未検証。CPUは提示完了frame時間を意味しない。測定用expression余分なbraceは失敗記録を保存して修正し、同事前protocolで実測、サイトruntimefailureではない。動的初回は古いoriginal72葉群対stable12batch比較helperを移しstrict失敗。settled R27/R31とも30画素差・max26・mean.0001173・bbox一致で待ち不足ではなく既知batch差。strict original/batch完全同値は主張せず、正しいlegacyboth比較と無効時original fallbackへ修正し失敗/診断を保存した。

最終build成功。actual完成5WebPはR30保護写真とbyte一致しread-only aliasで再利用、inline5同期。basic11case（読込保留静止画、noWebGL5、入力/静止/reduced3、実contextlossrestore、DecompressionStreamなしHTTPgzip）成功。現在木包絡でpublic legacyboth/stable（有効3）とoriginal/stable保守fallback（無効3）PNG動的case parity、有限光/木local/instanceversion変更で保守fallbackを確認。served comparison/adopted decodedidentity、最終TOP PC3903203D/JPG同選択版byte一致とnoWebGL3を確認。文字0、overflow0、remote/font0。PC/390/320の樹冠鉢土台uncut。使用ChromeはMac上の実ブラウザでviewport emulation、実端末の検証ではない。

5214はgate記録後だけ更新。旧28897と比較63853の専用cwd/processを確認してSIGINT、新TOPPID90351/session75979。Chrome72496正常終了/profileguard解除、writer解除。新study/provisionalbest2、旧33stateSHA全保持→35。旧成果削除0、GitHEAD固定/許可3coorsのみ。外部歴史PR7既削除26paths/4manifestentriesのため過去完全性false、存在する全保護fileはSHA確認。Libraryretry0/IDs0、以前のTLS阻害を再試行していない。push/PR/merge/外部公開/購入/automation/旧projectaccess0。20MiB追加allocationはcapacity-final/receiptで保守計上する。

全体完成false。幹の広い滑面と滑らかな肩、苔mat、扇軸が残る近景、遠冠の自然さが残る。名品古木や高級旅館庭の十分な説得力をまだ認定しない。木の大形を再び局所膨張で追わず、次の一案は ordinary-distance全景で自然な地形/成長方向を成立させる骨格を編集前にレビューし、現暫定bestを固定基準にする。受入gateを再び全幅明確優越へ戻さない。

時刻 2026-10-06T08:26:02.415731+09:00、工程54.0分。期限2026-10-10 23JST内。要求Sol xhighの実runtime metadataは未検証。成果と証跡はこのrun、確認用PC390320はqa/adopted-top-final/。
