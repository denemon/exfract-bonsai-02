# 次工程への条件

現在の作業基準・暫定全景bestはR20 depth-balance-1905。R21は相対的に枝間の背景が静かな候補だが、同条件Retina p95退行でbest採用しない。親が次工程を指示するまで新しい工程を開始しない。推定3〜4時間は完成保証や自動実行予定ではない。

R21実配置／前障子開き／rear-screen除去はpartial比較案として保持できる。ただし次に採用するにはR20と同時期・同actualpose・DPR・heroLOD/keyでGPUを比較し、遅い回も含める。今回の2Source+2finalbuild全116sampleで旧21.186ms/新24.089msという事実を引き継ぐ。compile/startupの間違った39e案を性能根拠に戻さない。粒度・葉の輪郭・影を消して数値だけを合わせない。wide右端の庭の境界、近低木の葉束・疎な支持、遠冠、平坦な苔と一様砂利を全景で再評価する。

木の造形作業は、直前の採用済み全景を比較基準として固定し、同camera/FOV/exposure/key/heroLODの実garden/bonsai/詳細woodを用意してから再開する。滑らかなS字を細かなshader模様だけで古木に見せる方法は採らず、根張り、基部の不等な隆起、枝の太さの推移、分岐の接続と空隙、側面の非対称な体積をnativegeometryで直す。既存carved-v02は未採用のまま。灰茶色/茶色の現要求を維持し、白い元画像は形態参考として使う。詳細woodはbare8meshでなく実93mesh・high4.67M葉の別診断を残す。

低速cold約11.7秒は依然未達。載せる形状と質感に必要なデータを調べ、lazyload・圧縮・デコードを測って判断する。最終5stillは全幅の完成実景に同期し、WebGL不可/context復帰/reducedmotionを最終buildで確認する。20MiBの事前予算を設け、Chrome/profile/cache/staging/三調整文書までpositivepeakで計上する。旧成果や未知cacheを削除して余裕を作らない。

20旧状態＋今回1状態、R20/R21全manifestと独立レビューを保護。PR8既済archive同tree／PR7外部欠落4manifest-entryを引き継ぎ、勝手なpull/reset/restore/delete/Gitwriteをしない。旧project、外部公開、push/PR/merge、購入、automation、Library再試行を行わない。実機phone/Safari/熱/Sol-xhigh metadata未検証を成功へ書き換えない。期限2026-10-10 23JST、次担当は親。
