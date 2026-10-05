# 工程14：共有面の接合だけ改善、候補は非採用

正式先の `runs/hand-junction-1029/` に一件の新しい構造を保存しました。**差し込みの棚は消えましたが、自然な名木の古木造形と庭全体の高級感は未達。候補cage-v01は非採用、通常景色の美的変更0です。** 保護版の工程13production（工程12と同じ景色）5208を維持。作者と独立レビューの判定は一致しています。

## 違う接合方法と検査

過去のS網surface、Skin、断面tube+voxelを利用せず、184絶対座標/175面を直接指定した一つの共有面cageを新規作成。主幹の面patchを開き、同じ境界vertex IDsを枝の最初のfanが使います。奥の主枝の面から右従属枝を出し、根～幹～主要枝を一つの編集meshにしました。Subsurf2が補間し、実貫通穴一つを持ちます。枝/根/孔の7頂点groupと184点のnativeが編集できます。35,224B GLB、98,265B core-only blend、評価5,744tri。全scene/native/assetの複製なし。

初回の奥枝断面が曲がる経路と整合せず、非隣接交差70。枝元の共有境界を保って、その断面方向とvertex対応だけを修正しました。最初の実表示前のgeometry修理で、別の外観候補ではありません。途中のAST修正失敗と起動失敗もログに保持。最終は1成分2,872頂点、boundary0/nonmanifold0/nonadjacent intersection0、最小面積0.0000258683、正volume0.14028679、Euler0/genus1。native読み戻しは184点/175面/頂点group/共有境界exact、位置error0/体積差0。これを美的品質の合格とは扱いません。BVHの非隣接判定は設定epsilonの検査で、あらゆる数学的交差の証明ではありません。

同じclosed scale leaf prototypeを保持し、2800shootの中心を六葉群へ移動、枝先へ小twigを接続。葉primitiveの均一球/板へ置換していません。通常候補の木はrough単色、UV/masksはplaceholderで樹皮仕上げなし。元302×404添付の実ピクセルを確認しましたが、ローカル原画像は取得していません。Libraryの前の公式helper TLS阻害を保持し、再試行0/IDなし。

## 七枚の代表像による判断

同一Mac Chrome154のPC1440×900、390×844、320×568、全景単色正面、裸幹単色0/−12/+12度を実表示してrawPNG保存。390/320はDPR3模擬でrenderer cap1.6、実機スマホではありません。候補version、program compile、可視文字0、scroll0、通常のshader/JavaScript warnings/exceptions0を確認。全景の樹冠/鉢/台は切れず、庭との新しい重大な干渉や見た目上の大きな浮きは見られません。framing値は既存fitの標本/envelope値で、全頂点exact投影を再実施していません。

中央の差し込み棚と上部主軸の段が、共有面によって単色正面/限定視差で消えました。この接合方法は保存する価値があります。しかし根際の狭い丸い支持、均質S、左中枝と頂部左枝の長い三角膜、長く滑らかな主幹帯が残ります。整った楕円穴の縁は、侵食された木筋より造作彫刻として目立ちます。樹冠の左右差/小さい右群は保ちますが、根張りと幹の凝縮、葉群/鉢の説得力に置換を支持する改善はありません。通常色の暗さを除いた単色±12°でも問題が残りました。**一件で止め、追加候補/非採用への表面仕上げ0。** 背景の庭/建築/素材/光は比較定数として保持し、背景まで改善したとは報告しません。詳しくはreference-reading.md と qa/independent-review.md。

## 軽量実装と確認の範囲

harnessは工程12src/public/indexをread-only参照し、六つの既知anchorだけメモリで変更。独自plugin、crown controls、coupling module、coreだけを追加。サイトcopy0、public素材copy0、既存production source変更0。初回serverを終了するshellの背景で起動したため接続拒否が出ました。失敗記録を残し、保持される専用foreground sessionとnative config loaderで起動し直して七表示が成功しました。元のbuild、camera/input/render、normal表示は変更していません。

採用しなかったため、変更のない72+7網羅QA、production画像、build、GPU/低速load/motion/復帰/fallbackを再実行していません。工程13のbuild/検査/GPU p95PC12.107/39013.301/32012.495ms、低速3D19.766/19.262/19.136秒は保護sceneの既存結果です。今回候補の性能合格を示しません。七表示の初回triはshadow pass込みでPC3,493,290/3903,398,198/3203,409,898、closed low葉868,000tri。定常値やGPU負荷へ読み替えません。harnessの読込/不可時stillは保護景色のままなので、候補専用の一致fallback完成とは扱いません。

単色は0/±12度だけ。側面/背面/大角度、今回候補のGPU/load/motion/reduced操作/failure、実機スマホ/Safari/熱/長時間は未検証。保護版でも全60fps細かい時間aliasing、LOD境界、人間によるMP4連続再生品質は未検証のままです。指定Sol/xhigh、runtime model metadata未確認。

## 保存と保護

必要source、core native一件、代表rawPNG7枚、差分、比較HTML、geometry/native/visual records、独立reviewを保存。旧project/Git/既存12状態/全過去成果/旧55profileを保持し、旧成果削除0。新profile0、同一専用profileだけ再利用。夜/茶褐色/実3D+shader/通常可視文字0/散在小装飾石0を保持。push/PR/merge/公開/購入/automation0。Library新画像IDなし。最終容量/保護/プロセスは finish.json と integrity-verification-after-records.json。

次は同じfanの係数や穴を増やさず、土際の不等な支持と短い体幹、狭く短い枝口へ収束するedge flowを先に設計する必要があります。共有面は手段として継承できますが、方式を変えたことだけを品質改善と認定しません。NEXT-STAGE.md。親が次工程を判断し、本runは一件の非採用記録で固定します。
