# 工程22：確認URLをbestに固定し、景色を守って描画負荷を整える

最初に5214通常TOPを選定best R20に戻す。今後も未採用候補をTOPへ差し替えず、R21は /compare/r21/、今回R22は /compare/r22/ と明示する。build・stills・モデル/素材の参照を分け、WebGL不可・初回ロードでも各パス自身の実景を出す。R20/R21のsource/dist/写真/レビュー/状態は不変更。

目指す景色は高い実塀、右の前障子と厚み/開口のある家屋、夜空、灰茶色の主木を持つ文字のない庭。R21の390/tallで静かになった枝間は部分成果として候補に残す。主木geometry/material/UV/world/key70/exposure1を固定し、輪郭・空隙・主要影を削らず滑らかに表示する。散在小石なし。背景の負荷を要素別に計測し、shaderで形状不合格を隠さない。

同Mac Chrome/実actualpose/FOV/exposure/heroLOD/DPRを固定。warmup30renderの後、61点計測・先頭2点除外59sample、old→new→new→oldを採用比較の一単位とし、全sample/中央値（偶数中央2点平均）/nearest-rankp95/CPUsubmitも残す。disjointは失敗扱い。通常PC/390/320とRetinaを確認。計測中にbuild/重いfilesystemauditを並行しない。既存R21の退行21.186→24.089msは歴史証跡、今回同時期比較での改善と混同しない。

既存の動的処理・静的shadow invalidation・frustum/culling・attributes/instancing・材質の不要計算などを診断し、必要な見た目に影響しない負荷を優先して除く。非表示/単純材質は診断だけ。候補の採用には全景の視覚退行なしと同条件Retina p95改善の双方を要求する。採用しない場合TOPはR20のまま。最終build/関連機能/5still/reduced/context実表示を確認し、木nativeform/root/taper作業に戻る条件を更新する。

21旧状態、R20/R21全manifest、独立レビューを保護。20MiB事前16.5MiB予算、共有read-onlyasset/Chromeprofile/cacheと5214originを再利用。最小実写真/1最終build/必要rawmetricsのみ。Chrome観測positivepeak・cache・staging/pycache・三coordinator・新状態も計上。旧成果/unknowncache削除/負evictioncredit0。5208歴史bestと5214だけ。Gitread-only、外部archiveHEAD2347を確認、PR7歴史欠落を復旧しない。旧projectaccess/外部公開/push/PR/merge/購入/automation/Library再試行0。実機phone/Safari/熱/Sol-xhigh実runtime未検証、期限10/10 23JST。
