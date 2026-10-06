現在TOP：http://127.0.0.1:5214/ （保護したR25選定）
候補：http://127.0.0.1:5214/compare/r26/ （age-v01 / botanical葉、未採用）

再起動は以下です。port5214の現在PID32648が生きている間は追加serverを起動しないでください。

```sh
cd /Users/kazuki.tanaka/dev0/exfract-bonsai-02/improvement/2026-10-04/runs/age-leaf-0342/candidate
npm run preview
```

R26のvite configがTOP/compareを分離。依存・共通資産・profile・cacheを再利用、旧成果削除0。外部公開0。
