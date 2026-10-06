# R22 補正後の独立レビュー

判定：材質を含むR20景色の回復を確認し、補正R22をrender基準の採用候補として支持する。補正後の性能・機能ゲートは今回未確定のため、正式採用は保留。R20を暫定景観bestとして保持する。高級箱庭・名品盆栽の完成判定は不合格のまま。

## 実見と背景の回復

corrected-production-pixel-and-source の pc／mobile-390／mobile-320／mobile-tall／wide の5JPEGを実ピクセル閲覧し、R20 final-source の対応5景と比較した。PC rawは2880×1800、スマホとwideはDPR1。

前回の不採用理由だったPC・wideの左遠冠の暗化は今回の補正で解消した。苔の明暗、低木の葉、障子の紙と室内の明るさもR20基準に戻っている。主役・塀・庭・家屋の位置関係に肉眼で新しい退行を認めない。390／320／tallでも冠から鉢と低い土台を保ち、右側の実障子と室内の関係はR20同等。

## 完成画素の同一性とrender方式の差

corrected-r20-cross-page-framebuffer/results.json の10 rowsを直接対にして再照合した。既存R20 build対補正R22 render=originalは、PC Retina2304×1440、390×844、320×568、320×844、1920×800の5幅全てで全RGBA SHAがbit一致する。各対のactualCamera、hero、exactProjection、lightsも等しい。corrected-r20-framebuffer-proof.json の5対宣言と整合する。材質挙動を含む完成像について、前回のgeometry／light同一だけの根拠不足を解消する。

ただし、これは最適化前のoriginal同士の証明。補正productionのoriginal→bothには下記の少数差が残る。

| render buffer | 変更pixel数 | 最大channel差 |
|---|---:|---:|
| 2304×1440 | 50 | 21 |
| 390×844 | 11 | 22 |
| 320×568 | 1 | 6 |
| 320×844 | 12 | 20 |
| 1920×800 | 11 | 15 |

全RGBA平均絶対差の最大はtallの0.00025363（channel範囲0–255）。original repeatは全0。肉眼退行は認めないが、bothまで全画素bit一致とは記さない。前回900高のtall／wideとは異なる今回の844／800実測を採用する。

同resultsのmatrix proofはnative72→display12、2800 instancesの行列bit exact、native hierarchy復元を示す。wood-highはnative93 meshes、high葉4,670,400 triangles、batchActive=false。original／batch／light-cull／both全て変更pixel0・同SHA。6診断のready=true、可視文字空、overflow=false、logs0を確認した。新paired検証の完了とは区別する。

## 品質の未達と次の作業

灰褐色・茶褐色の現色要件を維持する。白deadwoodは写真の形態参考であり、白の再導入を完成条件にしない。主役の大きく滑らかなS字の本体、似た腕状の枝、土際の根支持の弱さが依然普通の樹形彫刻として読める。近接葉の説得力も未達。補正はこれらを直していない。

庭には物理的な塀、奥行きのある開口、厚い障子と埋石がある。しかし遠冠の疎な枝軸、低木の反復的な葉、苔の均質な細粒面と砂利の平坦さが残る。390／tallでは冠・枝間の後ろに障子格子が続き、主役の輪郭と競合する。tall下部の広い砂利余白も維持される。静けさと空間統一の相対基準にはなるが、美術館級の品格・自然な成熟庭・数千万円級の盆栽の説得力には届かない。

補正後のrender採用条件を確かめ、景観基準を固定した後はnative木の作業へ戻るべきである。固定したカメラ・光・露出で、根から短い屈曲・不等な枝肩へ荷重がつながる実体積を、中立像と通常夜景で先に審査する。現在の滑らかなS形をshaderで完成扱いしない。

## 採用の保留条件

補正前の5写真と性能・build・idleの採用資料はsuperseded扱いのまま保持する。旧ABBAの良い値を補正build2の性能証明へ移さない。補正後のpaired12 cases、GPU、idle／resume、cold、reduced motion、WebGL不可／context recoveryは未確定。成功も速度改善も未確認。

正式render採用には、補正buildの同条件paired検証とGPU分布（中央値・p95、同LOD／Retina）で退行がないこと、静止画fallback・idle復帰・入力／context動作、無停止coldのnavigation→3Dと鮮明stillを確認する必要がある。まだ60fps、cold高速化、実機phone／Safari／熱安定を保証できない。視覚・同一性は通過、性能／機能は保留、美的完成は不合格。

画像と指定JSONを読む独立レビューのみ。Chrome／測定／広域auditは起動せず、新規本書だけ保存。旧二レビュー・過去成果・code・状態は不変更。

確認時刻UTC: 2026-10-05T14:41:01+00:00
