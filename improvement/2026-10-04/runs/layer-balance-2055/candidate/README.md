# 文字のない夜の箱庭・工程21候補

ローカル http://127.0.0.1:5214/ 。今回候補のproduction build。暫定bestはR20、http://127.0.0.1:5214/compare/r20/ で確認する。premium完成不合格、Retina同条件p95退行のため未採用。RESULT.md / comparison-final.html / NEXT-STAGE.md参照。

`npm run dev` / `npm run build` / `npm run preview`。既存最終distとQAを消さないこと。Vite8.2.2/Three0.185.1とモデル/主役材質/LOD/Draco、R20素材を同一正式project内でread-only参照する。単独コピーで持ち出せるバンドルではない。publicDir=falseの意図的共有構成。外部ネットワークassetの要求なし。公開・購入なし。

空URLで選定済みoffsetを使うstartup初期値を修正。全幅で同一物理家屋・植物・庭を使う。PC−18°と各mobileのfitを別設計。本文/ロゴ/リンク/ラベル0。idleの連続RAFなし。reduced motionではdrag/zoomを抑制。loading/WebGL不可/contextloss時はfinal-source-offsetから変換した5実景のresponsive WebPと同景のinline preview。

最終code build成功、MacChrome8幅＋機能12case＋配信14file一致。coldstill1.523秒/3D11.735秒、Retina全116sample p95旧21.186ms/新24.089msで未達。物理phone/Safari/熱は未検証。

診断queryには mineral-fast=1、index=original、micro=original、gravel=baseline、space=balanced がある。製品選択はmineral-fast=0相当／正確なindexed／masked／varied／offset。診断と別配置の値を最終製品の成功に転用しない。QA材質比較を再現するときはURLのspaceを明示する。
