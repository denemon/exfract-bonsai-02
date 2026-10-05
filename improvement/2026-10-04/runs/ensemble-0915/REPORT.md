# 工程13：全体骨格二案は非採用、工程12の景色を維持

正式作業先の新しい `runs/ensemble-0915/` で実装・検証。**工程は保存済みだが、名木の古木造形と庭全体の高級感は未達。** 通常表示を美的に改善したとは報告しない。添付302×404の実ピクセルを会話で確認し、幹・枝・葉と鉢の比率を参照した。Library原画像のローカル取得は前工程の公式helper TLS問題で阻害、今回は再試行しない。生成夜景参考は方向の比較用で、背景画像表示には使わない。

## 方法と失敗を変えた範囲

前のA/Bは同じS字surface、分岐境界、六房、鉢比率を維持したまま面や溝を変更し、帯/靴/棚へ退行した。今回は38節点37辺の新しい骨格、低い左主枝・奥の主枝から降りる従属右枝、上部の前後葉群を一緒に設計。全2800shootの中心を移し、閉じた葉prototype自体の回転/縮尺は維持。新しい粗いtwigを同じ枝先へ接続した。鉢・土・台・庭・建築・光・カメラを比較条件として保持。

最初のSkin共有接続はboundary28/nonmanifold32/nonadjacent666で生成ゲート失敗。保存ログのみ。単純円筒の貼り合わせを最終形にせず、不等でねじれた断面、異なる前後中心、共有voxel体積へ切り替えた。各木約17,500tri/91.6〜91.8kB、元のS網/枝originは利用しない。低詳細段階で通常PC390320、単色の全景前/55°/裸幹、独立レビューを行った。

v01は根と体幹が細いSの支柱に見える。v02は根と第一枝の支持を増やし葉群を下げたが、中央左の棚/差し込み、均質なSと楔根、長い露出幹が残った。**双方非採用。第三案/非採用形状の樹皮仕上げなし。** 境界/非manifold/非隣接交差0でも美的完成ではない。補助検査でv02に土中約5µmの3頂点2面の孤立残渣を発見。単一solid認定もしない。failed証拠を保存し、修正して成功と呼ばない。

新しいgeometry、骨格/六葉群controls、再生成script、exact mesh記録と復元scriptを保存。Blender復元は位置/面/体積error0。最良native4.79MB/hero原本は読取linkのみ、新しい大きなnativeコピー0。通常sceneはedge-v02/space-v2/night-b/load-pcf8-v1を維持。6構図の選定・production・工程12PNGがバイト一致。既存9source moduleとcamera/input/render部も一致。実3D+shader、可視文字0、散在する小装飾石0。

## 最終build/表示/性能

Build成功。72表示/操作/reduced-motion/復帰/fallback検査、追加7deferred-detail/通信失敗/API不可検査が通過。通常のshader/JavaScript例外なし。WebGLを意図的に無効にした2警告は区別。非採用診断chunkもproductionの390/320/単色で検証。通常3Dは新しい診断chunkを読み込まない。JS共有core分割により外部は各幅+2,405B、追加request1。見た目の完成度とは別の結果。

|実Mac Chrome|PC1440×900|390×844|320×568|
|---|---:|---:|---:|
|GPU p95 ms/60有効samples|12.107|13.301|12.495|
|定常tri|1,204,122|1,109,030|1,120,730|
|初期静止画表示機会ms|404.8|503.5|465.6|
|FCP ms|408|504|460|
|鮮明静止画表示機会ms|2337.5|1068.6|798.6|
|3D完了ms|19765.9|19262.2|19136.4|
|外部encoded bytes|3,733,189|3,605,681|3,589,855|

GPUはM1Pro、EXT_disjoint_timer_query_webgl2で62描画し先頭2除外。390/320はDPR3を模擬しrenderer1.6、実機スマホではない。工程12p95PC14.549/39012.803と同じgeometry/shader。計測差を最適化成果と呼ばない。低速はcacheoff150ms/200000B秒、幅ごと1回。工程12の3D19.941/19.208/19.095秒とほぼ同範囲。鮮明静止画は前工程よりPC約261/390209/320122ms後ろ。初期2RAF時刻はpaint opportunityで、実FCP/初期PNGと別に残す。詳細の遅延取得は約2.682秒、491629B、粗いclosed葉の景色を保持。

5fallbackは同じ選択sceneから425990B、HTML20130B。全景PC/390/320/長い縦/横長/landscapeを保存。320の枝先/鉢/台は切れず、個別yawとfitを維持。背景の厚み/room/support/自然石/ground配置は前工程のまま。主木の均質S、庭のmoss境界、左背景植栽、roomとskyの描写はまだ美術品質へ届かない。

## 動作の確認範囲

実際のpointer dragで7位置を往復、PC/390/leaf-detailの同じcamera9組がPNG完全一致、idle3条件も一致。最終productionでも再確認。さらに実Chrome連続RAF±3.2°を2.2秒記録し各133〜134描画、LOD切替0。66rawJPEG、timestampを保持したMP4三本を保存。約10fpsで採取し、作者と独立レビューが連続frameの明暗飛び/葉や影の消失を確認した範囲では大きな破綻なし。**MP4連続再生の人間評価、全60fpsの細かな時間aliasing、LOD切替瞬間、Safari、実機スマホ、熱/長時間動作は未検証。** 自動一致/短いrecordを全般的なちらつき完成評価に替えない。

## 保護と次工程

旧作業先、Git、既存11状態、全過去成果を保持。新しい成果/同じ専用profileの増分を100MiB内、空き2GiB以上に収める。旧55profiles/過去成果削除0。確認用PNGのbyte-identicalコピーだけ読取linkへ置換し、元画像byteと全pathを維持。raw screenshot加工0、有料購入/push/PR/merge/外部公開/automation0。初回previewを誤ったancestor rootで起動し接続確認が失敗したため、所有権を確認してその自分のprocessのみ停止し、run/siteへ修正。tracked/sourceへの変更はない。失敗ログも保存。

Library新規保存/画像IDなし、再試行0。指定Sol/xhigh、実model metadataは未確認。次は同じgraph+taper+voxelの係数・溝反復を止め、主幹の不等量塊と短い枝接続を手動共有meshで作り、葉群/鉢と同時に低詳細全景ゲートを通す。詳細はNEXT-STAGE.md。次工程の開始は親が期限10/10 23JSTまで判断する。
