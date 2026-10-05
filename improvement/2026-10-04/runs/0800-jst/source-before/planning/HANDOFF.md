# 08:00への引き継ぎ

この回は初回計画・保全・既存ローカル定期実行の読み取り確認だけ。サイト実装、カメラ、照明、素材、静止画、初回QA結果を変更していない。

## 次の実装回の入口

1. 日本時間2026-10-04 08:00以降であること、23:00までの残時間、親の実行設定がGPT-6 Astra・xhigh以上であることを確認する。
2. `run-state.json`、作業ロック、実行中のwriter/ブラウザ検証、既存ユーザー変更を確認する。重複なら触らず親へ報告する。
3. `IMPROVEMENT_PLAN.md` と `AWARD_REFERENCES.md`、`baseline-initial/manifest.json` を読む。初回画像3点を必ず実ピクセルで見る。
4. 08時枠は空間の想定尺度・主役と建築の距離・PCと縦画面カメラ・光の序列を一緒に改修する。細かな木目や葉だけを先に磨かない。
5. PC1440×900、390×844、320×932を初回比較用に維持し、加えて390×740、320×568など短い縦画面を確認する。短い画面の改善が初回比較の構図を悪化させないかを見る。
6. 実表示を確認して候補を評価し、良好な状態を保存。採用する場合はサイズ別fallbackを最新の景色へ同期する。未完了は時刻付き記録へ残す。

## ローカル確認結果

- `.codex/sqlite/codex-dev.db` をread-only接続で照会: ローカルautomation総数0、`exfract-bonsai-02`対象0、対象run履歴0。ID/状態の該当なし。
- `.codex/automations` は存在しない。ユーザーcrontabなし。ユーザーLaunchAgentsは空。システムLaunchAgents/LaunchDaemons内に対象パスの指定は見つからない。
- プロセス・listen socketの確認で対象writer、browser-qa、Playwright、Vite、対象Chrome debugプロセスは見つからない。一般のCodex exec-serverは稼働している。クラウド側の他スレッド稼働をこの検査だけでは証明できないため、親が単一実行を管理する。
- 5182/5183のプレビューは現在停止している。初回DELIVERY.mdの「起動中」は初回終了時点の履歴。次の実装回に必要なサーバーを起動する。この計画回では起動していない。
- モデル: 現在の実行モデルを確定できるmetadataは、この環境では取得できなかった。`CODEX_MODEL` / `CODEX_REASONING_EFFORT` は未公開、該当threadのローカルsession記録なし。ローカルdefault configは `gpt-6.1-sol` / `xhigh` であり、現在のcloud委譲モデルの証拠ではない。GPT-6 Astra適用済みとは断定しない。親側の設定確認が必要。
- 定期実行は作成・更新していない。要求された開始08:00、毎時、最終22:00回、絶対期限23:00は計画値で、実際の設定完了を意味しない。親が設定後に一度だけユーザーへ報告する。

## 保存・検証の注意

- 初回source、build、静止画、QA一式は `baseline-initial/site-and-evidence.tar.gz`。SHA256をmanifestで記録。初回画像は同ディレクトリにPC/390/320を別置き。
- `best-state.json` は初回を参照。更新は実表示による全景比較で採用した場合だけ。
- 毎回の記録テンプレートは `RUN_TEMPLATE.md`。通常成功の通知は不要。重要な阻害、重複実行、期限に影響する遅延は親へ具体的に報告。
- Library保存は初回に正規helperでブロック済み。今回の必須成果はローカル。Library取得や転送の制限回避、TLS検証無効化、推測URL使用をしない。
- 旧 `/Users/kazuki.tanaka/dev0/exfract-bonsai/`、他プロジェクト、既存ユーザー変更を保護する。push/PR/merge/公開/応募/有料素材購入は禁止。
