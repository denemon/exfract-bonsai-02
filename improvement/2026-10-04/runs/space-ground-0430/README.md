# ローカル盆栽3D：建築と自然石の工程

night-b / space-v2を限定採用。**高級な自然景観としての完成品質には未達です。**

確認: http://127.0.0.1:5204/ 。比較資料 comparison.html、詳細 REPORT.md、独立評価 INDEPENDENT-REVIEW.md、次の範囲提案 NEXT-STAGE.md。

実装はsite/src。PC/390/320などの最終画像はqa/verification、建築/石近接はqa/selected-stills。二案はvariants。編集石はassets/editable、元PBR glTFはassets/source。source-changes.patchとASSET-CREDITS.mdも保存。

site内でnpm run build、npm run preview。固定Three0.185.1/Vite8.2.2を参照し、追加install不要。主役/Draco/樹皮/地面の微細素材は前工程への読み取りリンクで、このrunだけを切り離した配布物ではありません。旧成果はそのまま。不要previewは停止し、今回の本番5204のみ保持。

地面は新しい空の出力先に再生成できます。PythonにはPillow/NumPyが必要です。

```sh
python3 site/scripts/make_terrain_field.py --design site/src/terrain-design.json --output /tmp/bonsai-terrain-new
```

地面3出力は実際に再生成してバイト一致済み。石の再生成方法/未検証範囲はASSET-CREDITS.md。Library再試行なし、添付IDなし。実行モデルmetadataは未確認です。
