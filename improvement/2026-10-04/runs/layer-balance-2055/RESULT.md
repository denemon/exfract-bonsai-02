# 工程21：配置の相対改善を候補保存、暫定best更新は見送り

2026-10-05T22:01:16.436912+09:00。最新ローカル候補は `layer-balance-2055`、作業基準と暫定全景bestは `depth-balance-1905` のまま。全体premium完成は不合格。 http://127.0.0.1:5214/ は今回候補の最終build、旧R20は http://127.0.0.1:5214/compare/r20/ 。歴史root best5208も保持する。`comparison-final.html` で全景と厳密比較を確認できる。

## 空間と自然さ

実家屋を [2.45,.02,−3.25] / yaw−14°へ置き、前障子を3本の実レールで右へ開いた。後ろの格子・紙・桟の組を外し、厚い背壁、実床、側壁、梁、開口と室内灯を残す。同じ物理空間を全画面で使い、幅に応じて家屋や植栽を消す処理はない。PCは−18°、390/短320/長320は−40/−30/−45°の独立カメラ。高い実塀2.321m、前障子の框と組子・薄紙、夜空を維持した。

390と長320では中央の樹冠・枝間から格子が離れ、PCでは前障子と奥行きある開口が同居する。主役の投影高さは PC69.83%、39048.24%、短32052.01%、長32042.26%。全5幅で樹冠〜鉢〜台が投影内に収まる。短320の前障子は画外。wide右端では家屋外の平らな地面が露出し境界の説得力が弱い。自然景として完成したとは判定しない。

植物の不等な端点・枝葉数を調整し、葉の断面を薄い閉じた形へ変更。葉は実枝に接続し、12群の遠木葉と1群の近低木葉、合計29,535枚を使う。球／板／浮遊葉への置換はしていない。葉束・疎な支持軸・規則的な対葉の印象は残る。砂利の種子ごとの径と明暗を不等にし、7mm程度の粒度、最大3.3mmの微小高さを同一fieldへ付けた。素材仕上げの変更であり、粒が一様な面として読まれる問題や平坦な苔を解消したとは主張しない。

主役は灰褐色／茶褐色のedge-v02、形・UV・材質・世界行列・キー70・露出1を固定。元写真の白は現色要件でなく形態参考。滑らかなS字、均等な太い枝腕、根張りと古さの造形は未達で、今回の背景改善を名品盆栽の造形合格に転用しない。

## 最終検証と性能の採否

| 検証 | 実測・判定 |
| --- | --- |
| 最終build | 成功。compile2回、最初は起動配置不具合・未同期stillのため明示的にsuperseded。最終dist一組、旧index/固有JSはQAへ保存 |
| Mac Chrome実表示 | PC/390/320/tall/wide/Retina3幅の8件。文字0、overflow0、runnable全成功、unexpectedconsole0 |
| Sourceとbuild | geometry/camera/hero/LOD/投影/有限光が全8件一致、配信HTML/JS/CSS/素材/5still計14file decodedbytes SHA一致。画素完全同一の主張はしない |
| 厳密garden/bonsai/wood | 3組、同camera/FOV/exposure/key/hero属性/行列/LOD/投影。木詳細は実93mesh、high葉4,670,400triangle。bare8meshの代用なし |
| 頂点再利用 | 13背景meshの展開後position/normal/UV/木目/boardseed/world/triangleがrawbits完全一致、輪郭や三角形を削除せず再利用 |
| 機能 | 12件成功。通常低速load、5比率のWebGL不可still、reducedmotion、微小drag/zoom、実contextloss/recovery。5期待warn、unexpected0 |
| 実Cold | 250KiB/s、120ms、HTTP cacheoff、scriptpause無し。完成景still1.523秒、navigation→3D11.735秒。R20の1.631/11.777秒に対して小差、依然重い |
| Retina採用gate | 旧R20中央値17.526 / p9521.186ms、新R21中央値17.905 / p9524.089ms。各116sample、中央値は中央2点平均。**不合格、R20best維持** |

Retinaは同Mac/実camera/FOV/露出/hero/LOD/key/実DPR1.6でR20→R21→R21→R20をSourceと最終buildの双方で実行し、全29有効sample×4回を各案へ集計した。遅い回を除いていない。新案p95は旧より約13.7%悪化。過去の旧28.775msより小さくても、同時期比較の改善条件を満たさない。各回の値と31rawsamplesは `qa/performance-adoption-gate-final.json` / `qa/final-matched-gpu/results.json` に残す。通常PC p95旧24.981→新24.087ms、390実DPR1.6旧22.273→新21.977msの小差は、Retina全景gateの代わりにしない。60fps・長時間の熱安定は保証しない。

微細bump off、影2tap、背景map256、植物非表示は診断だけ。製品は主要輪郭・枝間・全5caster、主役2048/背景512、主役8/背景4tapをR20から維持。`mineral-fast=1` の背景鉱物だけの前計算比較も大きな安定改善を示さずdefault0として未採用。木目・紙の繊維は元のhashを維持。完全ゼロの苔coverageで不要な材質fetchを省く枝分岐と、正確なvertex reuseだけを今回候補へ残す。

## 途中の不具合と証跡

モジュール初期化がmainのquery補完より先に走り、空URLの家屋だけ選定前separateを使う不具合を最終照合で検出した。defaultをoffsetに修正し、選定済み形状e72へ一致させ、5全景・3厳密比較・性能・buildを再検証した。旧 `qa/final-source` / `qa/strict-diagnostics` / `qa/retina-matched-abba` は39eの別配置として保存し、最終採否に使わない。元freezeと初回compileも残す。砂利JSの引用構文エラーと空meshを抽出した診断は失敗／無効証跡として保存し、成功数に含めない。

最終geometry `e72e923e56e86570fdb49465e1d34eece12b8ca14de9992cacbc45e3030abea8`、field `4bedbbe02d16e01b661f942107c643660e6f28f1740f783508a85a9a73d755dc`、hero `7b41aaf17bbf8c4689ae3a67986ea05df8e7403f30ed221bbe1fcff8e8e43e8d`。最終freezeは `qa/shape-freeze-final.json`。機能成功と美的完成度を区別する。独立採否レビュー `qa/adoption-review.md` は保存後に本文を変更しない。

## 保護・容量・未検証

20旧状態とR20全成果をSHAで保護し、今回状態を別追加する。Git PR8はobject/現HEAD/536archive blobをread-only照合、pull/reset/restore/writeはしていない。既報PR7外部削除26pathと歴史manifest4欠落は未復旧、歴史完全保護は不合格のまま。存在するcritical source/production/native/旧状態は最終auditで照合する。

実allocatedblocksは `qa/capacity-final.json`。runだけでなく共有Chrome観測正増分peak、共有cache正増分、今回staging/pycache、三調整文書、新状態まで計上する。自動evictionの負額credit0、旧/unknown成果やcache削除0。新規実写真・再検証・superseded独自JSも計上する。Library既報公式helper TLS阻害への再試行0、ID0。旧projectaccess/公開/push/PR/merge/購入/automation0。

実機スマホ、Safari、長時間熱負荷、要求Sol/xhighの実runtime metadataは未検証。次工程は親が決める。期限10/10 23JST。今回の候補をbestに更新せず、空間改善だけを将来の性能改善と併せて再評価できる形で保存する。
