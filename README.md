# exfract-bonsai-02

月明かりの枯山水と古木。現行の `user-rake-final-v03` を編集・ビルドできる構成です。

```sh
npm ci
npm run dev                         # http://127.0.0.1:5182/
npm run build
npm run preview -- --port 5183      # ビルド確認
QA_URL=http://127.0.0.1:5183/ QA_FULL=1 npm test
```

- `src/`: 現行シーンと描画処理。`src/modules/` は採用版のモジュール名を保持しています。
- `public/`: 必要なモデル、テクスチャ、Draco、画面比率別の静止画。
- `models/`: 採用された幹・根と小枝の編集用 Blender ファイル。
- `scripts/browser-qa.mjs`: Chromeで通常表示、動き低減、操作、context喪失・復旧を確認。`CHROME_PATH` でChromeの実行ファイルを指定できます。
- `THIRD_PARTY.md`: 素材とライセンス。

現在表示中の `http://127.0.0.1:5214/` は変更していません。配信に必要な33ファイルだけを `improvement/2026-10-04/runs/continuous-fork-0935/builds/` に保持しています。通常の開発・ビルドはこの旧配信ディレクトリに依存しません。

未コミットだった `improvement/2026-10-04/HANDOFF.md`、`IMPROVEMENT_PLAN.md`、`run-state.json` と前回の削除記録は変更せず残しています。これらの過去の参照先には今回削除したものがあります。旧自律作業は再開しません。

検証出力 `qa/` と生成物 `dist/` はGit管理対象外です。WebGL不可・JS読込前には完成静止画を表示します。実機スマホ、Safari、熱負荷、賞水準の品質・性能は未認定です。
