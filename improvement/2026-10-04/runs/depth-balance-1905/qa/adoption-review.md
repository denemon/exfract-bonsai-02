# 工程20：最終local buildの暫定採用確認

確認時点：2026-10-05 11:29 UTC（20:29 JST）。qa/final-source/{pc,mobile-390,mobile-320,mobile-tall}.jpgの4実像を確認し、release-verification.json、strict-pairs.json、final-release/results.json、matched-r19-gpu/results.jsonを独立読込した。final-source元resultsとの照合も行った。旧レビューは全て保持する。

**暫定全景bestはR20を選ぶ。R19へ戻す理由になる新しい視覚退行は見えない。premium完成はfalse。** 最終surface=shoji-v01、grain=hashのmicro変更は、前のfinal-spatial-reviewの採否を実質的に変えない。高塀/前障子/夜空、PCの室内奥、スマホの主役サイズと背景冠/前景を同時に残す関係が維持されている。hashの木目/微細表現と紙応答は派手な発光や濡れた光沢を増すものには見えず、全景の構図/縮尺/素材階層に明白な新しい崩れを見ない。pixel単位同一を主張する判断ではない。

最新の高塀2.321mと厚みのある前障子、見える深い夜空は新指示の方向に合う。PCの敷居/縁側/畳/奥壁の距離がR19より読みやすく、header接合に空が見える以前の症状も今回見えない。390−40°/通常320−30°/縦長−45°では樹冠から鉢/台石が収まり、屋根上の実冠と左前景を残す。主役占有高さ48.24%/52.01%/42.26%を維持し、R19の小さい縦長像から改善した関係を保つ。

未達は残る。主冠と障子格子の重なり、疎い前景低木/裸軸と葉束の遠冠、粒状の苔丘と均質な砂利面、縦長の上下約29%余白は完成ではない。灰褐色/茶褐色で固定したwoodの滑らかなS量塊/均質な腕/弱い根支持も未解消。原写真の白を現在の色基準へ戻さず、普通の木の色であっても名品の形態に届いていないことを分けて評価する。

## releaseと比較条件

最終freezeはgeometry dadb0605015e297c8a91edcedb3f7c07db4b5a95f305534475ae34310f4880cc、field4bedbbe02d16e01b661f942107c643660e6f28f1740f783508a85a9a73d755dc。8 geometry source SHAの現ファイルとの一致を確認した。final sourceの全幅はhero93mesh/lowLOD SHA7b41aaf17bbf8c4689ae3a67986ea05df8e7403f30ed221bbe1fcff8e8e43e8dを保持。main.jsでquery未指定時のgrain=hash/surface=shoji-v01設定も確認した。

releaseの8case（PC/390/320/tall/wideとPC/390/320retina）は全件ready=true/text空/overflow=false/logs0。各caseと対応final-source rowのactualCamera/hero/exactProjection/全lightsの一致を独立照合した。geometryも全8で最終freezeに一致する。release JSONはbuild確認成功、build executions2、one physical final dist、all programs runnableを記録する。独立browser/build再実行はしていない。source raw画像をbuiltのpixel同一証明とはしない。wide画像は今回実見対象ではなく、metadataのrelease一致確認だけである。

strict-pairsはgarden/bonsai/woodのcamera/FOV/exposure/hero属性・matrix/LOD/projection/key一致を記録し、背景形状/材料/室内・木の有限光配置とhero PCF16→8のmicro filter変更を宣言する。主役geometry/材質/key固定と、影filterの宣言変更を混同しない。woodはforced-high93mesh/4.67M leafの診断cropで、別のleaf0/wood8mesh裸木診断と分ける。このレビューで対応wood実画像を新たに実見したものではない。

## 同camera GPUの改善と残るtail

matched-r19-gpuの6caseと新releaseの対応caseで、actualCamera/hero/projection/key70が一致することを独立照合した。同Mac/ANGLE Metal Apple M1 Pro、31renders/初め2を除いた29sample、同pixelRatioのGPU query。元samplesからmedianとnearest-rank p95を再計算して報告値と全件一致した。背景を含む全版の負荷比較で、改善を個々のmicro変更の単独効果にはしない。

| 構図/実効pixelRatio | R19 median/p95 ms | R20 median/p95 ms |
| --- | ---: | ---: |
| PC/1 | 18.017 / 21.925 | 13.347 / 16.907 |
| 390/1 | 14.750 / 22.217 | 13.378 / 15.907 |
| 320/1 | 17.015 / 21.005 | 9.460 / 12.497 |
| PC/1.6 | 23.180 / 24.473 | 15.806 / 28.775 |
| 390/1.6 | 16.823 / 22.904 | 11.028 / 19.180 |
| 320/1.6 | 15.109 / 24.267 | 12.350 / 17.691 |

全caseでmedianは改善し、PC/1とmobileのp95も改善する。一方、PC retinaのp95は24.473→28.775msへ退行する。新PC通常p95も約16.67msを少し超え、retinaのtailは大きい。短いMac GPU queryの改善を60fps保証、CPUを含む総frame時間、実機スマホ/Safari/長時間熱負荷の成功へ換算しない。tall/wideには今回GPU sampleがない。

cold/reduced/WebGL-null/contextlossの最終機能QAはこの依頼時点で進行中で、今回資料から成功を仮定しない。旧R19の機能検証値を新releaseへ転用せず、cold完了/静止画表示/復帰の最終結果は別の証跡で確認する。容量20MiB維持の独立監査もこの採用レビューでは行っていない。

最終採用判断は『視覚上の次基準/暫定全景best=R20、premium完成=false、最終機能/coldと性能の総合合格は保留』。追加geometry作業を本レビューから要求しない。担当が作成したのはこの新規qa/adoption-review.mdのみで、source/state/browser操作はない。selection-review、spatial-review、final-spatial-reviewの既報SHA保持を独立確認した。
