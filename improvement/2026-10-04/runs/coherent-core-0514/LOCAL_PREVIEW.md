TOP：http://127.0.0.1:5214/ （R27保護）
未採用V02：http://127.0.0.1:5214/compare/r28/?candidate=core-v02
未採用V01：http://127.0.0.1:5214/compare/r28/?candidate=core-v01
R27：http://127.0.0.1:5214/compare/r27/

単一5214previewPID97661/session41616。起動中は追加serverを起動しない。終了後の再起動：

```sh
cd /Users/kazuki.tanaka/dev0/exfract-bonsai-02/improvement/2026-10-04/runs/coherent-core-0514/candidate
npm run preview
```

TOPはrouting.adopted=false/relatedQAComplete=falseによりR27固定。R28はgray研究用、完成fallbackはR27read-only参照で未同期。
