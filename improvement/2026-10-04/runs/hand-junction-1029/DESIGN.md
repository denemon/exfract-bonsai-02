# 工程14：共有面から枝を押し出す一件の編集cage

過去四案の共通原因は、S字の芯と枝を別の生成流れで作り、root/分岐に一様な太さや棚が残ること。旧surface変形、Skin、tangent contour+voxelを今回は使わない。写真の折り返す主幹・左肩・奥から右へ降りる枝を手読みし、方向の異なる不等な前後面を直接置く。

主幹は半径/円断面でなく、各stationの絶対座標を手で置いた非対称面。主幹の側面patchを開き、その境界頂点を枝の最初の面が共有する。枝を重ねて融合しない。奥のprimaryの面から右secondaryを出し、反対側の同じ節の腕を避ける。底は複数の偏った支持面を土へ埋める。低い部分に小さく不規則な実形状の通り穴を作り、単色で厚みと前後の流れを見せる。Catmull-Clarkはこの明示meshを補間するだけ。branch fan / loop / hole wallが編集source。

図柄は夜景・茶褐色幹・無文字・散在小石0を保持。最初はrough単色/neutral、木目/暗さで形状を補わない。上部/左主塊と小さい従属右群、鉢/土/台/庭は同時に見る。closed scale leafの実prototypeは維持、shoot中心と粗twigを新しい枝先に接続。元写真302×404は会話の実ピクセルを確認済み。低解像の2D手読で、3D測量ではない。原画像local取得の既知阻害には再試行しない。

一方式一件の構造試作。manifold/成分/zero-area/selfintersectionと単色主視点0/±12°を先に確認。通常PC/390/320も一回だけ保存し、独立レビューで根/枝接続/全体比率と具体的な理由を判定。NG時は同方式の候補を増やさず、失敗と有効な次手を保存。採用時のみsurface/UVと本番への変更、最終build/関連表示/負荷/reduced/fallbackをまとめて再検証。

軽量harnessは工程12のsrc/public/indexと現行QA scriptを読取参照。サイト全体/素材/網羅QAを複製しない。工程13の5208表示は保持。編集source/必要代表画像/差分/記録が成果。目標20MiB、上限100MiB、空き2GiB、専用profile再利用。過去成果/12状態/Git/旧55profilesは保護、購入/公開/automation/他project変更0。Sol/xhigh指定、runtime metadata未確認。
