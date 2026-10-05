# 09:00への引き継ぎ

08時回は候補05を採用。`runs/0800-jst/REPORT.md`、`comparison.html`、`source-manifest.json`、`best-state.json` を読む。初回 `baseline-initial/` と現在を必ず全景で比較する。

次回は、鉢と石台、石台と砂利、自然石の埋まり、苔の厚みと境界を一つの地面として改修する。現在の回廊・庭・主役の尺度を基準にし、必要なカメラと光の調整を連動させる。盆栽の細部だけに偏らない。PC/390/320で改善を確認し、退行したらその回の変更だけを修正・戻す。

盆栽・鉢・土台は `subject.scale=.62`、建物は実寸。盆栽全高は約1.8m、鉢幅約1.15m。元モデル座標の編集時はscaleを考慮する。PCは左寄り、縦画面は画面比率に応じた55〜63度の鑑賞角と距離。短い縦画面と幅広の縦画面も個別に検証した。

本回の環境はMac Chrome154 headless、ANGLE Metal Apple M1 Pro。GUIブラウザ操作、実機スマホ、Safari/Firefox、タッチそのもの、長時間負荷は未検証。DPR1/DPR2、7 viewport、リサイズ、reduced motion、context喪失/復旧、loading/WebGL不可の静止画を確認。フレーム測定は約1.4秒、29.9〜30.6fps。完全なcold startやGPU処理時間の測定ではない。

静止画は `public/still-*.webp` の7種。元画像は `runs/0800-jst/candidate-05-retina/` と `candidate-05-wide/`、対応は `stills.json`。造形・カメラ・光を採用変更したら最新の景色から再生成する。基準比較画像は `final/`、高密度の検証画像は `final-retina/`。

残る美的不足: 幹の平行溝・裂け方、土の塊、石の多面体感、葉の粒状感、背景植栽の紙片感、格子の反復、軒下の暗さ。受賞水準や写真級に達したとは扱わない。

Git基準は外部で作られた `feat/bonsai-night-scene` / `4ed0bd766278263c706c996788c662200880f8bf`。08時回の差分はローカル作業ツリーにあり、commitしていない。`site-source.tar.gz` で採用状態を保存済み。他者の変更を確認して保護する。親提供の既存PR参照は `external-reference.json`。公開許可や操作主体を推定せず、push/PR/mergeは行わない。

開始前に `run-state.json` と `improvement/.active-run/`、writer/ブラウザ操作を確認する。既存のread-onlyプレビューだけをwriterと扱わない。開発用5182は終了処理予定、本番5183は確認用。実際の最終状態はrunの `finish.json` を読む。プロセスが終了していれば `npm run dev -- --strictPort`、完成buildだけの確認は `npm run preview -- --port 5183 --strictPort`。

GPT-6 Astra / xhigh以上は親が実行設定で指定する。独立metadata未公開を別モデルの適用済み証拠にしない。08時回では新規スケジュールを作っていない。22時回で最終確認と一度の報告、23時までに全作業終了。通常成功通知は親への引き継ぎのみ。

追加点検: 左回廊の床の規則的な暗点はAO/shadowMapを切っても残存。診断は未採用で、10時の建築工程へ引き継ぐ。PCの初回JS heap採取値は約391〜392MiB。生成後の不要なgeometry/配列の保持を性能工程で点検する。Library画像保存はTLS接続エラーで未完了、IDなし。原本はrun内final/に保存済み。
