# 工程21 独立最終採用レビュー

判定：R21への暫定best更新は不採用、R20を維持する。offsetの空間改善は部分成果として保存できるが、自然さとRetina負荷の両方を改善する採用条件を満たさない。premium完成=false。R20維持も完成認定ではない。

## 最終景と照合

qa/final-source-offsetのpc／mobile-390／mobile-320／mobile-tall／wideと、R20 qa/final-sourceの同5幅を実画素比較した。別配置39eの旧qa/final-source・retina-matched-abbaは最終景の根拠に使わない。

最終geometry SHA e72e923e56e86570fdb49465e1d34eece12b8ca14de9992cacbc45e3030abea8、field4bedbbe…、hero7b41aaf…を確認。shape-freeze-final記載の9 source SHAも実ファイルと一致。final-release8件はready=true、同geometry。actualCamera／FOV／露出／hero属性・行列・LOD／exactProjection／lightsを最終写真JSONの対応幅と独立照合して全件一致した。通常source/releaseログ0、可視文字空、overflowなし。

layout既定offsetへの修正を確認。strict-pairsは3組の同条件と本物93mesh／high4.67M葉三角形を記録（今回pair写真は再閲覧なし）。high診断をGPU値に転用しない。mineral-fast=1は未採用、既定0。家屋と有限灯も移動するため材質のみの比較ではない。

## 見た目の改善と未達

PCは前障子一枚の框・桟と開口・室内床の奥行きを同時に読める。高塀・夜空を保ち、鉢・低い台・石・苔岸・縁側が同じ場所に存在して見える。PC−18°（高さ69.83%、R20 67.22%）なので同一カメラ比較ではない。

390／tallではrear-screenの実除去により中央冠と枝間の後ろが背壁・室内陰影となり、格子が枝を横断する競合は明確に減った。3スマホのactualCamera・投影はR20と厳密一致し、高さ390 48.24%、320短尺52.01%、tall42.26%を維持。樹冠〜鉢〜台は切れず、低石と地面も残る。

320短尺の前障子は画外で、開口・側壁・背壁が見えるだけである。全スマホで前障子が読めるとは言えない。側壁の暗い縦帯が一部の冠の後ろに入り、tallの砂利余白も依然大きい。wide右端は家屋外に無植栽の水平地面と青い余白が現れ、箱庭の境界が弱く見える。

薄い閉葉・不等な端点は相対改善だが、近低木の葉束・疎な支持軸と遠木の反復的な輪郭は成熟した自然な植栽に届かない。varied砂利も広い一様な細粒面の印象が残り、苔は緑の粒状面として平坦に読まれる部分がある。

固定された灰褐色／茶褐色の主木は滑らかなS字、均質な腕、弱い根元支持が残る。数千万円級の名品として説得力を持つ造形は未達。原写真の白は現在の色要件ではなく形態参考である。

## 性能による採否

selected-offset-abbaとfinal-matched-gpuの最終e72 PC Retina実測を再集計した。同Mac Apple M1 Pro／camera・hero・key／実DPR1.6、各run31点の先頭2点を除外し、4run×29点＝116有効点を各版とも全て使用した。良い一回だけを選ばない。

| PC Retina pooled | median ms | p95 ms |
| --- | ---: | ---: |
| R20 | 17.525812 | 21.186250 |
| R21 | 17.904708 | 24.089124 |

最終performance-adoption-gate-final.jsonのmedianは中央2点平均、p95はnearest rankで、独立再計算が一致。旧performance-adoption-gate.jsonは上側中央値17.532124／17.944958の記録として保存されている。全有効点でmedian・p95とも改善せずgate=false。過去R20の28.77msや別配置の値を混ぜて改善とは主張しない。60fps・熱安定性の保証はない。

## 機能検証と限界

最終resilience/results.jsonはsuccess=true、12ケース。5幅の強制WebGL不可で完成静止画へ切替、reduced idleはframes1→1／pointer不変、通常限定入力・zoom、実context lossと復帰を確認した。ログ5件は全て強制WebGL不可の期待warning、unexpected0。通常releaseログ0と混同しない。

cold250KiB/s・120ms・cacheoff・script pauseなしで、FCP344ms、完成静止画1523ms、navigation→first3D11735.3ms。main開始からの10079.7msと起点を区別する。R20のstill1631.2ms／navigation→3D11777.3msとの差は小さく、別stageの負荷差もあるため速度改善率を立証しない。3Dまで約11.74秒は依然重い。

機能成功は美的完成やRetina採用条件の成功を意味しない。実機phone／Safari／長時間熱負荷は未検証。指定Sol/xhighの実runtime metadataは公開されず確認不可。

旧二レビューのSHAを確認し不変更。書込みは本レビュー一件のみ。コード・状態変更、ブラウザ・テスト起動なし。

記録時点（UTC）：2026-10-05T13:05:13+00:00
