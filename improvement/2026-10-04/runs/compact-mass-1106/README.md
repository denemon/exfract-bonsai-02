工程15の非採用一案compact-v01の保存先です。完成サイトの納品認定ではありません。REPORT.mdとqa/independent-review.mdに形状の不合格と検証限界を記録しています。

comparison.htmlをブラウザーで開くと7 raw PNG、制作図2枚、以前の画像を読取参照で比較できます。文字はQA資料だけにあり、サイトにはありません。保存PNGは加工していません。

models/compact-v01-editable.blendはcore-onlyの編集可能cage、GLBは同じcoreのbrowser用。葉・鉢・庭は共有baselineにあり、nativeに複製していません。sculpt/build_compact.pyとcompact-cage.jsonが制作記録。再読の一致はqa/native-readback.json。失敗7回の接合gateログも残しています。外観候補は一件です。

harnessは自己完結したsite copyではありません。ancient-volume-0810/site、正式root/node_modules、および明示的mutableなhand-junction-1029/qa/vite-cacheを参照します。現在5209は停止済み。読取診断を再起動するならharnessをcwdとして次を実行し、?compact=compact-v01を指定します：

```
/Users/kazuki.tanaka/dev0/exfract-bonsai-02/node_modules/.bin/vite --config vite.config.mjs --configLoader native --host 127.0.0.1 --port 5209 --strictPort
```

再起動には別工程でport/ownershipを確認すること。過去manifestや凍結済みoutputを書換えない。診断のfallbackは保護版の景色で、非採用候補固有のfallbackではありません。保護したproduction5208は別プロセスのまま保持しています。

source-change.patchは今回の小さいsource四点だけを新規追加として記録し、適用指示ではありません。finish.jsonとdelivery-manifest.jsonを最終の状態・容量・integrity証拠として参照。Library IDなし、正規helperで以前のTLS阻害、今回retry0。旧project、Git、公開系操作は行っていません。
