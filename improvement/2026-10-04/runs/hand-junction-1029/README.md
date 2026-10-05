# 一件の共有面構造の保存

cage-v01は非採用。REPORT.md、comparison.html、qa/independent-review.md に結果があります。保護版の通常表示は http://127.0.0.1:5208/ 。古木造形と庭全体の高級感は未達です。

このrunはサイトのコピーではありません。harness は工程12のsrc/public/indexと正式作業先node_modulesを読取参照し、既知の六anchorだけメモリ上で変更します。画像/素材の複製0。静的比較HTMLはローカルで開けます。通常サイトの無文字条件は維持し、QA文書はサイトとは別です。

診断を再起動する場合は harness へ移動し、正式作業先の node_modules/.bin/vite を `--config vite.config.mjs --configLoader native --host 127.0.0.1 --port 5209 --strictPort` で起動。`?manual=junction-v01`、単色は `&study=clay&yaw=0`、裸幹は `&bare=1&frame=shared`。限定左右はyaw=-12/12。読込中/failureの画像は保護版stillであり、候補と一致する本番fallbackを作ったとは扱いません。

models/junction-v01-editable.blend は184点175面の一つの芯と7頂点group、未適用Subsurf2だけを持つ98kBの編集sourceです。鉢・葉・庭は同梱せず参照。sculpt/authored_cage.py と authored-cage.json が絶対座標/共有境界/面/階層を保持。harness/manual.controls.json が全2800shootの中心配置、manual-preview.js が新枝先へ接続する小twigを持ちます。UVはplaceholder、樹皮仕上げはありません。

sourceを再生成する時は別の新規runへsourceをコピーし、models/qaを作成してください。scriptは既存GLBがあると停止します。この保存runや保護sourceを上書きして再exportしないでください。検査だけなら `Blender --background models/junction-v01-editable.blend --python-exit-code 1 --python qa/native_readback.py` の出力を新規先に変えて実行。読み戻しではcontrol位置/面がexact、volume差0を確認済みです。

screenshotsはqa/cage-v01の7枚のrawPNG。画像加工/大量の重複QA/Library保存は行っていません。Library画像IDなし。
