# ローカル盆栽3D：植栽と地面の構造

`night-b / growth-v2` を限定採用。**高級な自然景観としての完成品質には未達です。**

- 本番表示: http://127.0.0.1:5202/ （このMacのlocalhost）
- 全景比較: `comparison.html`、詳細: `REPORT.md`、独立評価: `INDEPENDENT-REVIEW.md`
- 実装: `site/src/`、二案の編集原本: `variants/`、差分: `source-changes.patch`
- PC/390/320/wide/tall/landscape: `qa/verification/`、地面近接: `qa/selected-stills/ground-detail.png`

`site` 内で `npm run build`、`npm run preview`。親プロジェクトの固定版Three0.185.1/Vite8.2.2を参照し、追加installは不要です。開発5201は停止済み。本番5202を保持。主役GLB、Draco、樹皮、既存微細地面素材は保護済み前工程への読み取りリンクなので、このフォルダだけを切り離した配布物ではありません。

地面の編集再生成（Pillow/NumPyがあるPython、既存出力を上書きしない空ディレクトリ）:

```sh
python3 site/scripts/make_terrain_field.py --design site/src/terrain-design.json --output /tmp/bonsai-terrain-new
```

同一環境でPNG/WebP/manifestの3出力がバイト一致することを検証済み。terrain-design.jsonの境界、盛り上がり、裸地の窪みが編集原本です。背景植栽の個体別主軸と分岐はgarden-geometry.jsにあります。ノイズだけで形を作る構成ではありません。

Libraryは既報の公式helper TLS阻害により再試行なし・IDなし。確認画像はすべてローカル保存です。
