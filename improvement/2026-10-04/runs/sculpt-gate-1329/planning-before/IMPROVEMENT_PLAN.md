# 完成画像 + 限定視差 — ローカル候補完成

11:32承認の方式を維持。実3D全景維持より画像品質を優先する。最高品質はテスト数や実装量で決めない。

完了: 3主構図を生成保存して比較、同一傾向の横長/正方形を追加、写真を浅い連続立体面へ投影する限定視差を実装。PCマウスだけに約1pxの応答、遠景の基準面固定、モバイルと動き低減は静止。loading/noWebGL/context lossの完成画像を保持。

完了: production build、11画角、基本3構図DPR2、noWebGL、JS読込停止、動き低減変更、context復帰、idle停止、リサイズをMac Chromeで確認。最終各suiteの警告/例外0。コード、production、原画像、比較、スクリーンショット、性能とmanifestをruns/hybrid-runtime-1224/へ保存。

未解決: Library添付は公式helperのTLSエラー。preparedツール自体は公開済みでdirect fallbackは適用しない。追加転送試行を続けない。Androidへ画像を添付できていないことを親へ明示。

次: 親/ユーザーの実画レビュー。必要な具体的修正だけを同候補へ行う。物理端末/Safari/実回線/4Kは未検証とする。22時最終検証、23時終了の親管理を維持し、毎時の別writerを勝手に増やさない。

正式root/productionは09bestを保護。候補所在はcandidate-state.json。best-state.jsonを無断で置換しない。初回/08/09/hero-rebuild-1016/hybrid-1132も保持。Git書込み・push・PR・merge・公開・応募・購入・旧作業先変更・スケジュール変更なし。
