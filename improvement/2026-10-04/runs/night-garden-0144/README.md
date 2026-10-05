# Night garden B — local Three.js scene

全景配置の工程成果。**名品の古木と高級庭園の完成品質は未達です。** 現在の実装は無文字の実3Dで、画像の変形ではありません。通常画面は静かな夜と茶褐色の木。`REPORT.md`、`comparison.html`、`INDEPENDENT-REVIEW.md`を参照。

確認： http://127.0.0.1:5198/ （このMacのlocalhostのみ）

```sh
cd /Users/kazuki.tanaka/dev0/exfract-bonsai-02/improvement/2026-10-04/runs/night-garden-0144/site
npm run preview
```

上記ポートは保存時に起動済み。再開時に限り起動する。ソースの開発は`npm run dev`で5197。既存rootのnode_modulesを解決し、Three0.185.1/Vite8.2.2を使用。`npm run build`がローカルdistを作る。外部公開はしない。

- `site/src/scene.js`：夜空/光、縁側と厚い開口、境界、石、苔、接地の計測。
- `site/src/garden-geometry.js`：庭の地面、自然石、枝/葉の立体。`garden-materials.js`：粗い石・木・土/砂利/苔の材料。
- `site/src/main.js`：PC/各モバイルのカメラ、操作、reduced motion、WebGL fallback。指/マウスで小さく視点移動、ピンチ/ホイールで近景、ダブルクリックで戻る。可視の操作文字やUIは置かない。idle時の常時描画なし。
- `scene-variants/layout-a/` と `layout-b/` は二案の4ファイル原本。Aの完全再現にはAの原本を別の新規作業先で使う。現在の`?layout=a`だけでは、後の共通修正まで戻らない。
- 主役は保護された `../local-edges-0056/models/edge-v02-editable.blend` と `edge-v02.glb` を参照。今回の再彫刻・複製なし。`public/models`・`bark`・`draco`と`dist`の参照リンクを含むので、siteだけを別Macへコピーしても自己完結しない。
- 樹皮は既存工程の[Chinese Cedar Bark](https://polyhaven.com/a/chinese_cedar_bark)、Charlotte Baglioni、[CC0](https://polyhaven.com/license)。4WebP375600B。追加の外部素材取得・購入なし。
- 四つのfallbackは実Chromeで撮った選定場面。`public/still-manifest.json`にソース/モデル/画像ハッシュ。HTMLに小さい同場面画像を内包し、WebP→WebGLへ置換。初期サムネイルは低解像度。将来の見た目変更後は古いfallbackを流用しない。
- QAは一つの専用profileを排他再利用。既存profileの中身/旧55profileは削除していない。`QA_PROFILE`を明示してChromeジョブを一つずつ実行。`qa/verification/results.json`49検査、`qa/gpu-performance/results.json`実GPU。Macの画面寸法エミュレーションであり、実スマホ/Safari/熱持続試験は未実施。

元の盆栽写真は会話内の実ピクセルを確認済み。元ファイルのLibrary取得と今回の画像保存IDは、既報の公式helper初期化TLS阻害により未取得。今回Library再試行なし。選定された夜景PC画像のローカル実体も確認した。全成果はMacへ保存。

既存成果/旧プロジェクト不変更、Git書込/push/PR/merge/外部公開/有料購入なし。次工程は`NEXT-FINISH.md`。
