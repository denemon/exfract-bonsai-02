# ローカル確認用の文字なし3D候補

現在の実build: http://127.0.0.1:5214/ 。完成品質は未達、既存bestへの本採用なし。成果・画面・性能は上位 `RESULT.md`、`comparison-final.html`、`qa/verification-summary.json` を参照。

このフォルダーで `npm run preview`（localhost5214）または `npm run dev`（localhost5213）。共有の正式プロジェクトnode_modules、ancient-volume-0810のモデル/材質/Draco、読み込み時静止画とCC0苔mapをvite.config.mjsで配信する。`dist` 単独では共有assetを含まない。外部へ公開する実装ではなく、ローカル共有asset参照候補。

最終buildは1回で成功し、その出力を実Mac Chrome154のPC1440×900、390×844、320×568、retina2構図で検証した。通常パラメーターはrefined素材/refined光を既定とする。常時animationなし、制限付きdrag/zoomのみ。reduced motion、完成景色の読込中・WebGL不可・context loss fallback対応。サイト画面にロゴ・メニュー・見出し・説明・ラベルはない。

主役の木は灰褐色/茶褐色の既存edge-v02を固定。形状は自然な古木の目標に未達。実機スマホ/Safari/長時間GPU熱負荷は未検証。performanceはRESULTに実測値とcold17.70秒の限界を記録した。3D正常表示と美的完成は分けて評価する。
