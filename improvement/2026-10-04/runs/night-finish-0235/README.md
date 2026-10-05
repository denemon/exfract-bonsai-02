# ローカル盆栽3D・夜景の全景仕上げ

選定は `night-b / material-v2`、主役は保護済み `edge-v02`。**現在は限定的な改善版で、要求された高級な自然景観の完成には未達です。**

- 本番表示: http://127.0.0.1:5200/ （このMacのlocalhostのみ）
- 全景比較: `comparison.html`
- 詳細報告: `REPORT.md`、独立評価: `INDEPENDENT-REVIEW.md`
- 新規実装: `site/src/`、二案の編集原本: `variants/`、前工程との差分: `source-changes.patch`
- 最終PC/390/320/wide/tall/landscape: `qa/verification/`。選定PNGと6構図一致。

`site` 内で `npm run build`、`npm run preview`。既存の親プロジェクトにインストール済みの固定版Three0.185.1/Vite8.2.2を参照します。新規installやネット取得を要しません。5199の開発サーバーは保存時に停止しました。主役GLB・Draco・樹皮は保護された前工程への読み取り参照です。この工程フォルダ単体を切り離した配布物ではありません。

自作素材の編集再生成（既存出力を上書きしない空フォルダを指定）:

```sh
python3 site/scripts/make_ground_maps.py --output /tmp/bonsai-ground-new-source
python3 site/scripts/compress_ground_maps.py --source /tmp/bonsai-ground-new-source --output /tmp/bonsai-ground-new-runtime
```

NumPy/Pillowが必要です。このMacのPython3.12で4ファイルのバイト一致まで確認しました。PNGはRGB色/alpha微細height、WebPはheightを損失なしで保持。新規素材は自作のみ。既存樹皮の出典・CC0記録は前工程 `wood-surface-0000` に保持。

検査は `site/scripts/verify.mjs` と `capture.mjs`。ブラウザは同じ専用QA_PROFILEを一つずつ再利用してください。`.active` ロックがある間は同時起動しないでください。ページに検証UIや可視テキストはありません。
