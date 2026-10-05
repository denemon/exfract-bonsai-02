# 背景を先に進めたローカル候補

背景の配置・開口・地面・夜の室内光を再構成し、部分的な改善候補を保存した。目標の高級な景色は未達で、本採用のbest-stateと5208は更新していない。盆栽はedge-v02の茶褐色木を固定し、新sculpt v02は選定前で保留した。

候補のビルド版: http://127.0.0.1:5210/ 。比較元: http://127.0.0.1:5208/ 。`candidate/`で`npm run build`、`npm run preview`。既存の依存関係と素材を読取り専用で参照するため、単独で移動できるexportではない。外部公開はしていない。

## 判断と変更

ユーザーの14:14JST指示を受け、目標PC画像と現行PC/390/320を実見し、背景を先に選んだ。建築の位置・厚み・開口、地形の連続性は木の古木造形より変更箇所と検証を確定しやすく、全景への効果が大きい。根拠は`PRIORITY_DECISION.md`、`comparison-priority.html`。目標画像は外観比較のみ、3D空間や静止画の代替に取り込んでいない。添付盆栽画像の白い枯れ木/赤褐色筋/非対称葉群は実ピクセルを見て造形判断に使ったが、その形状を完成できたとは認定しない。

右建築を後退させ、軒下、柱の厚み、室内床と奥壁を読める配置へ変更。奥境界に実形状の瓦屋根、異なる距離の枝付き閉じた葉の樹冠、左の埋石と連続する苔/土/砂利の地形を設けた。512pxの同じlinear data fieldを地形と苔・石際に使う。散在小石0、可視文字0。建築内へ暖光を合わせ、小さな紙灯具だけ弱い発光を許した。濡れた光沢や背景写真面は使っていない。

遠冠massはv03より厚くなったが、房と水平padの反復が残る。390の右から見る案は建築が画外へ消えるため不採用。最終390 yaw−30°/320−33°、pitch8°は実頂点で樹冠・鉢・低台を収める。PCは距離3.95mの庭全景。操作でこの距離が急変する問題を修正した。

背景形状SHA `89a0df0c3188adde1ce5088e16b5cf19193e30a439a1f95c581c7bb7aedd7822`、field SHA `d693f80323ce6e7ce693dcb6098a0c29619a70f5c1085e94d577d325e4614e40`。形状を固定して、石の橙色を抑え、木目、砂利/苔の微細起伏と空色を比較した。これは複合した相対改善で、各normal/bumpの効果を個別立証した扱いにはしない。主役の木・葉・鉢のshaderは変更していない。

## 実表示と機能

最終コードのbuild成功。Mac Chrome154でPC1440×900、390×844、320×568を実表示。全景/盆栽全体/幹寄りは前後で実camera/FOV/exposure同じ。背景と室内光は意図した変更対象。通常capture警告・例外0、可視文字なし、overflowなし。寄りは意図した診断構図であり樹全体は切れる。通常PC/390/320では冠〜鉢〜低台は切れない。

実renderの完成景色5構図を静止画に使い、最初の小さなinline背景から鮮明なpictureへ切り替える。PC/390/320のWebGL2不可分岐、実WEBGL_lose_contextの喪失/復帰、1秒idleのframes1→1、reduced motionで入力不変、通常入力8°制限と距離3.95m保持、wheel鑑賞を検証。意図したWebGL2失敗3件のcatch warningは通常エラーと区別した。これは実機スマホ/Safari検証ではない。

画像: `qa/final-browser-verified/pc.jpg`、`mobile-390.jpg`、`mobile-320.jpg`、`after-garden.jpg`、`after-bonsai.jpg`、`after-wood.jpg`。失敗表示: `qa/resilience/`。元の失敗build/参照不足/ブラウザ失敗ログも保存した。

## 表示性能

実GPUはANGLE Metal Apple M1 Pro。EXT_disjoint_timer_query_webgl2の31render、先頭2除外・29集計、撮影と同じ固定camera。DPRと実描画倍率を分ける。初回triangleは影描画を含むのでsteady値と混同しない。

| 条件 | DPR / 実倍率 | median / p95 ms | steady triangles |
|---|---:|---:|---:|
| baseline before-garden | 1 / 1 | 9.48 / 12.50 | 1,204,122 |
| baseline mobile-390 | 1 / 1 | 9.43 / 11.65 | 1,109,030 |
| baseline mobile-320 | 1 / 1 | 9.16 / 11.42 | 1,109,030 |
| candidate pc | 1 / 1 | 10.50 / 11.78 | 1,403,058 |
| candidate mobile-390 | 1 / 1 | 9.84 / 12.49 | 1,303,118 |
| candidate mobile-320 | 1 / 1 | 9.36 / 11.87 | 1,139,438 |
| candidate-retina pc-retina | 2 / 1.6 | 12.76 / 14.41 | 1,403,058 |
| candidate-retina mobile-390-retina | 3 / 1.6 | 9.52 / 14.41 | 1,303,118 |

通常の低速回線(250KiB/s、latency120ms、cache off、script待機なし)はfirst paint 0.32秒、鮮明な静止画 1.87秒、navigation→3D 15.18秒。main開始→3Dは 13.45秒。先の14.13秒はmain開始からでnavigation指標ではなかった。gzipはJS680130→179389B、wasm192420→63458B。JS/HTML/CSSの復号SHAを最終distと照合し、WASMも終了時に追加照合して既存read-only sourceと一致した(`qa/wasm-decoded-verification.json`)。独立レビューのWASM確認は転送bytes/source unchanged記録まで。低速回線での3Dはまだ重く、速いと認定しない。Macの短時間GPU値をスマホ実機/連続60fps/熱安定性の保証へ転用しない。

## 未達と保護

遠冠の自然さ、苔の滑らかなマット感、弱い建築木目、古木の幹面と均等な枝、スマホの柱/軒との競合と砂利余白は未達。追加1920×800では左境界の端が急に見える。全景の美術品質は作者・独立レビューとも合格としない。機能/構造検査成功は美的完成の根拠ではない。

sculpt v01は灰/夜ともNG。直接編集v02は26,000tri、閉成分1、Euler2、境界/非多様体/非隣接交差0、native再読一致として保存したが、灰/夜の実見と選定は未実施。木のshader仕上げは0。`wood-pause.json`と`models/carved-v02-editable.blend`が再開用。

現行source/production/15状態と存在する過去成果SHAは一致。外部PR7に対応する過去配列24件と非採用NPZ2件の欠落をGit読取と実在で確認した。歴史的manifest該当4件は欠けるため完全な過去保護監査は不合格。復元/Git書込み/削除/push/PR/merge/公開/購入/自動化作成は本writerで0。旧projectへのアクセス・変更0。外部GitHEAD変化と容量を本writerの変更に混同しない。先のD24は26へ明示訂正した。

Libraryへ確認画像3枚を正規helperの一括処理で保存しようとしたが、tools/listのTLS接続段階で失敗。ID0、再試行0。ローカル画像は全て残る。容量は`finish.json`/`qa/profile-footprint.json`参照。20MiB目標は超過、100MiB上限/最低free2GiBで評価。指定Sol/xhighのactual metadataは露出しておらず適用確認不可。
