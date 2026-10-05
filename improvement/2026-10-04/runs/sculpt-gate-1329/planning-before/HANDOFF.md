# 限定視差候補のローカル実装・検証完了 — 2026-10-04T13:00:01+09:00

現在の候補は `runs/hybrid-runtime-1224/site/`。完成画像と限定視差の11:32承認を実装済み。PC・390・320を維持し、横長と正方形を追加。全景実3Dの旧方針へ戻さない。

先に `runs/hybrid-runtime-1224/REPORT.md`、`finish.json`、`comparison.html` を読む。production previewは http://127.0.0.1:5187/ 、PID9172。主確認画像は同run `final/desktop.png`, `final/mobile-390.png`, `final/mobile-320.png`。Retina/無WebGL/読込中と11画角の証拠も保存。source/buildのZIP、manifest、性能JSONあり。実装と検証は完了したが、最高品質達成とは扱わない。

Library納品は不可。create/prepare/finalizeが公開されているためツール未提供のdirect fallbackは適用しない。公式helperのTLSエラーが未解決でIDは0件。今回アップロード再試行はしていない。`library-route-check.json` に根拠あり。AndroidはMacのlocalhostを閲覧できないため、親はこの添付阻害を説明する。転送調査を繰り返さない。

3D効果は写真を浅い連続面に投影した最大約1.3pxの奥行き差。遠景の基準面固定、自由回転/拡大/常時移動なし。モバイル/動き低減は静止。準備中・noWebGL・context lossでも完成画像を維持。単一3D盆栽の完全再投影とは称さない。原写真の直接ImageGen入力は未実施、視認特徴から生成した経路もreportへ記録。

正式rootとproductionは09 bestの17/10ファイルmanifestに一致したまま。`best-state.json`は保護し、新候補の所在を `candidate-state.json` へ分離。初回、08/09、hero-rebuild-1016、hybrid-1132も保持。5183は09 best、5185は未採用実3D、5186は画像選定ページで継続。現候補の開発サーバーのみ停止してproductionへ切替済み。

このwriterのactive-runを解放した。13時の新規並行実行は行わず、同じ作業を完了した。以後は親による画質/体験レビューと22時最終確認・23時終了。物理Android/iOS、Safari、実回線、4K、電池/発熱は未検証。push/PR/merge/公開/応募/有料購入/旧作業先変更/スケジュール変更なし。
