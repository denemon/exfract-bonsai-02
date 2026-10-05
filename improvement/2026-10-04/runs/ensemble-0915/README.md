# ローカル確認用の保存工程

通常表示は工程12の保護版。新しい全体骨格二案は非採用。名木の造形・庭の高級感は未達です。REPORT.mdとcomparison.htmlで結果を確認できます。

確認中のproduction: http://127.0.0.1:5208/

再起動: このrunのsiteへ移動し `npm run preview`。再buildは `npm run build`。開発表示は `npm run dev` (5207)。必要なThree/Viteは正式作業先の既存node_modulesから解決し、immutable assetsは読取linkで共有します。runだけを別所へ移しても依存asset/nativeは付属しません。

比較診断: `?ensemble=graph-v01` / `?ensemble=graph-v02`。通常表示へ採用しない低詳細モデルで、可視文字はありません。単色 `&study=clay`、裸幹 `&bare=1`、方向 `&yaw=55`。

selected-editable.blendは保護nativeへのread-only link。sculpt/graph-*.controls.jsonは新骨格と葉群、models/graph-*.jsonはexact面/位置。restore_graph.pyは検査だけならnativeを保存せず、明示的な --output の新ファイルへだけ編集用保存できます。比較画像/動画はqaへ保存、加工したスクリーンショットはありません。Library IDなし。
