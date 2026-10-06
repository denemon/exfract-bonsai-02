# 工程19：箱庭の全体配置を組み直した候補

文字のない実3Dサイトを、斜めの右奥建築・中央の盆栽・左の苔と石・後景植栽が連続する空間として再配置した。太い独立柱の競合と苔の均一なmatは相対的に改善した。一方、数千万円級の名品が自然に似合う高級旅館・美術館の景色という全体目標は未達。テスト成功を美的完成とは扱わない。本採用と既存bestの変更は行っていない。

確認URLは http://127.0.0.1:5214/ 。コードは `candidate/` と `background/`。PC/390/320の実景は `qa/final-scene/pc.jpg`、`mobile-390.jpg`、`mobile-320.jpg`。`comparison-final.html` に同カメラの変更前後、素材・光の段階比較、wide/tallと読み込み画像をまとめた。画像はMac Chrome154の実WebGL描画であり、生成目標画像を背景に貼ったサイトではない。

## 最終の空間と光

建築は−28°の実3D斜め配置で約3.15mの連続bayと約2.54mの奥行き。近い独立柱を厚い木壁の返しへ変更し、屋根・梁・縁側支持・畳・開口・奥の室内を同一座標へ配置した。PCと390では右の室内の深さはまだ十分に読めず、wideで強く見える。境界は後方z−4.96、中景樹は[−3.55,−3.80]、後景樹は[1.40,−6.80]。中景の根中心と境界面の距離1.16mは位置確認値であり、枝全体の干渉検証を意味しない。

中景・後景の2樹は不均等な13冠域、物理的に伸びる枝と30,724枚の閉じた葉を持つ。形状保証だけで自然な樹冠の見え方は達成していない。低い地形の連続fieldを苔・土・砂利の境界と石の埋まりに共有し、自然石は2個、散らした小石meshは0。主役の鉢・低い土台は共有既存形状を保持。鉢脚4点の実レイ接触差は約+0.0005〜−0.575mm。地面の全接触を数値だけで美的合格とはしない。

CC0のambientCG Moss001の実写色と変位を512pxへ縮小し、45cmの物理tileとして苔に使った。13mm微細凹凸と低い地形の盛りを分け、木・陶器・石・苔・砂利を過剰な発光や濡れた反射で補っていない。葉の背面は実光源の減衰・影に従う24%の透過近似。庭灯は中景26.4/後景18.48、樹の後方から壁へ向けず照射。主役のkey/exposure/wood shaderは固定。現在の木色基準は灰褐色/茶褐色、元写真の白色は形態参考だけとし再導入していない。

PCは距離3.65/FOV38/yaw0/pitch10、390はFOV54/yaw−24/pitch8、320はFOV54/yaw−28/pitch8。縦横fitは別計算で中央切り抜きではない。ただし全表示の占有高さはPC67.22%、39040.36%、320×568で51.27%、320×844では34.30%。樹冠・鉢・土台を収めても、長い縦画面の盆栽が小さく、上下の空・砂利の余白が過剰という課題が残る。

## 変更前後と固定の証拠

最終geometry SHA `3f53d7ad1647b7c6256d4e01a78c7c1e5506d5a4ccc38b1e912ac1e961b3e9c9`、terrain field SHA `4bedbbe02d16e01b661f942107c643660e6f28f1740f783508a85a9a73d755dc`。初回固定9fd5f5da…は根と境界の近接修正で置換した。修正前を `qa/shape-freeze-before-root-clearance.json`、修正理由を `qa/freeze-amendment.json` に保存し、修正後の素材・光5比較は全て同一geometryとなる。`qa/finish-design.json` は最終倍率1.32に訂正した。

工程18のリリースを変更せず、garden/bonsai/woodを同じ実camera/FOV/exposureへ合わせて撮った。見えている主役93meshのposition/normal/index/instance/world SHAと葉LOD、投影が3組すべて一致。庭の形状・素材・有限庭灯と室内光の位置変更は宣言した。woodだけforced-highで詳細葉の完了を待ち、両側4,670,400葉triで一致させた診断画像。通常性能・通常葉budgetとは分ける。

## 最終検証

最終コードで `npm run build` を1回実行して成功。配信されたHTML/JS/CSS/WASM/苔mapのdecoded SHAがファイルと一致。最終リリース6構図とretina2構図はready/文字なし/overflowなし/予期しないconsole error0。ソース撮影と最終buildの実camera/主役/背景geometry/投影一致を確認し、同じ写真を重複保存していない。ソースとreleaseの画素完全一致は主張しない。

機能10caseを実Mac Chromeで確認：制限付きcold navigation、WebGL不可PC/390/320、reduced motionのidle/input、通常制限入力/zoom、実context loss/recovery。自動カメラ移動や常時葉の揺れはなく、入力時だけ穏やかな視差。reduced motionではidle1→1frameとpointer無変化。5比率の完成実景をWebP静止画にして読込中・WebGL不可・context lossへ同期。wide/tallのWebGL-null分岐は個別未検証。

実GPUは31renderの先頭2を除いた29値。p95はnearest rank。同じApple M1 Pro、viewport/DPRのエミュレーションで、実機スマホの値ではない。

| 測定 | 実倍率 | median ms | p95 ms | steady triangles |
|---|---:|---:|---:|---:|
| candidate / pc | 1 | 17.45 | 20.66 | 1,748,806 |
| candidate / after-garden | 1 | 17.84 | 20.77 | 1,748,914 |
| candidate / after-bonsai | 1 | 16.68 | 18.77 | 1,748,806 |
| candidate / mobile-390 | 1 | 12.01 | 21.38 | 1,748,914 |
| candidate / mobile-320 | 1 | 11.74 | 19.81 | 1,748,914 |
| retina / pc-retina | 1.6 | 25.59 | 31.24 | 1,748,806 |
| retina / mobile-390-retina | 1.6 | 14.40 | 19.80 | 1,748,914 |
| baseline_same_camera / before-garden | 1 | 17.59 | 24.10 | 1,368,238 |
| baseline_same_camera / before-bonsai | 1 | 19.17 | 22.24 | 1,368,238 |
| baseline_same_camera / mobile-390 | 1 | 11.75 | 17.06 | 1,282,806 |
| baseline_same_camera / mobile-320 | 1 | 12.08 | 16.75 | 1,282,806 |

PC通常p95約20.66ms、retina実倍率1.6で31.24ms。60fpsを保証できず、通常のGPU負荷が残る。同時期同カメラの工程18結果も保存したが、Macの負荷変動を含むため速度改善は主張しない。cold250KiB/s/120ms/cache offの通常navigationではFCP332ms、鮮明still2.7752秒、初回3D17.6985秒。静止画で景色は出るが、3D開始は重い。実機スマホ、Safari、長時間熱負荷は未検証。

## 未達と保存上の限界

主役は滑らかなS字の量塊、均等な枝腕、弱い根張りが残る。古木のねじれ・えぐれ・枝の縮まり・空隙の自然さは目標との差が大きい。遠景は裸の軸と枝先の葉束、近い低木の露出軸、砂利の均質な粒度、標準幅での建築奥の読みにくさ、モバイルの縦余白が残る。独立レビュー `qa/background-review.md` も完成採用NG/相対改善のみ保存とする。

実装・写真・独立レビュー・検証・manifestをこの新runへ保存。候補は共有既存モデル/材質/Dracoをread-onlyで参照するため、`candidate/dist` 単独のportable exportではない。既存の17状態、過去成果、source/production/nativeは変更しない。新しい18番目の `background-reframe-study-state.json` だけを追加し、本採用bestは保護。所有済み5210/5212/5213のみPID/cwd照合後停止し、best5208と最新候補5214を保持。

20MiBの推奨新規容量目標は未達。自身のrunだけでなく再利用Chromeプロフィールの正増分、共有cache・staging・3調整文書を保守的に計上し、100MiB上限/free2GiBと分けて報告する。任意のcache/旧成果削除、負のeviction creditは0。最終数値は `finish.json` と `qa/capacity-final.json`。Library公式helperの既報TLS失敗へ再試行0、Library ID0、確認画像はローカル保存。

外部のGit archivalが工程中にHEADをf13d8ab…からf40904c…へ進めた。workerのGit書込みは0。既報の外部削除26件、過去manifest該当4欠落は残るため歴史全体の完全保護は不合格。存在する保護成果・17状態のSHA一致とは分ける。復元・削除・push・PR・merge・公開・有料購入・automation作成は0。要求Sol/xhighの実runtime metadataは未公開のため未検証。
