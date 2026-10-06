現在の確認用TOP：http://127.0.0.1:5214/ （R27 CPU改善、R25景色維持）
同候補：http://127.0.0.1:5214/compare/r27/
元選定：http://127.0.0.1:5214/compare/r25/
未採用形/葉：http://127.0.0.1:5214/compare/r26/

現在5214はPID58952/session16449が単一で起動中です。生きている間は追加serverを起動しないでください。終了後の再起動：

```sh
cd /Users/kazuki.tanaka/dev0/exfract-bonsai-02/improvement/2026-10-04/runs/program-state-0426/candidate
npm run preview
```

R27vite configが保存routingを読みTOPを選定します。既存model/atlas共通資産はread-only再利用。外部公開0。全景美的完成false。
