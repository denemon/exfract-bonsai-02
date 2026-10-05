# 工程17 carved-v01・中立初回surfaceの独立レビュー

判定：現v01は形状未合格。blocking unionとfinite wedge cutを、完成した古木のsurface sculptとしては扱わない。baked meshを直接彫る一度の具体修正へ進める価値はあるが、下記の丸いrim/中央突起/面の役割を先に直す。素材で隠さない。

## 実見したもの

qa/neutral/neutral-main-front.jpg、neutral-main-left12.jpg、neutral-main-right12.jpgの灰色3枚を全て実見した。geometry-inspection.json、design/direct-sculpt-plan.jsonも読んだ。葉なし本体＋根＋主要/二次枝、QA鉢proxyで、通常夜景やPC390320はまだ見ていない。ユーザー添付302×404の盆栽を実見した観察を継続する。裏の厚み・根/枝起点・carve深さは作者推定。

## 表示の成果と未達

一枚の大きいfinは消え、厚みと別方向の量塊、土中へ異なる方向の支持、枝の短い節と分岐を作った。単色でも量塊を3Dとして読める点は前案と違う。

しかし上/下のfinite positive ellipsoidが、閉じた丸いrimとして残る。上は目、下は唇に似た同じ形の膨らみ、中間のshort front lipは独立した丸い突起に見える。coreの右側は均等な丸い腹、主要枝は曲がりに沿う丸い肘とS腕である。三視点でこの印象が続くため、現形状を自然な老木として選ばない。

残因はvoxelのsmoothだけではない。正の丸いreturnをそのまま残し、その中にcutを置いたため、cutter断面をtriangle wedgeへ変えても外周は楕円のrimになった。source名がdeadwood return、cutが非pillという計画上の役割は、表示で達成した事実ではない。

保存技術記録は13,002vertices/26,000tri、閉成分1、boundary/nonmanifold/nonadjacent0、volume .1769727。独立担当は再計算していない。上限へdecimateしたこと、技術gateの通過は自然さの判定と分ける。

## direct sculpt案の可否

source masses/voxel/decimationを再調整せず、baked v01と同topologyの実surfaceを有限の斜めplaneで削り、非対称の短いchisel面を作る方針は妥当。これこそblockingから先へ進む具体修正である。全体を再smoothして面を消すのでなく、目立つ丸いrimを片側から芯へ戻し、異なる面の法線・厚み・終端を実geometryに残す。

下のplane centerXZ(.005,.655)、radius(.205,.2)、originY-.128と、上center(-.215,1.04)、radius(.145,.105)、originY-.09は、現在の主な膨らみを削る範囲として妥当な開始案。max inward .07/.08は局所で大きいため、残る芯と旧cut壁を確認する。数字自体を自然な面の保証にしない。

実行前に直したい点は三つ。

### 1. 中央突起をmask境界に残さない

short front lipのcenterXZ(-.13,.79)はlower shaveの楕円境界付近。falloffが強いとここだけ残り、二つのrimを削っても丸い鼻/こぶになる。lower shaveの有効範囲を左上へ非対称に広げ、同じplaneへ統合して突起をcoreにほぼflushへ戻す。別の小さいoval凹みを追加しない。

局所を足す開始案ならXZcenter(-.13,.79)、radius(.09,.12)、originY-.115前後、max inward .04〜.055。ただしlower planeとの連続と残厚を優先し、独立した第三の傷の形にしない。source volumeを削除し直す案ではなく、既存baked surfaceの過剰な突出を削る案。

### 2. eyeの片端を開き、別gashを足さない

現upper oblique facetはXZ(-.165,1.02)→(-.05,1.14)で、eyeの右上に別の斜め傷を足しやすい。優先すべきは閉じたrimの片側を芯/側面へ削り戻し、同じ厚い輪で囲まれた形を壊すこと。例えばXZ(-.21,1.035)→(-.31,1.02)の短い左向きの開き、width .025〜.04/depth .025〜.035を開始案とする。元のcutと接続し、一端だけが外へほどけることを実像で確認する。両端同じround capの短い溝を二つ並べない。

lowerにも同じ傷を配らず、下は斜めの広面が側へ返り、上は短い破断という違いを残す。lower/side/upperを連結して土際〜肩の新しい全高S谷にしない。

### 3. branchに線でなく面を一つ残す

現branch strokeのwidth .018〜.027、depth .01〜.019は細いgashや溝になりやすい。少なくとも上主枝ではwidth .045〜.06程度の平底/斜めplaneの面として、片側だけを.015〜.025以内で削る開始案を推す。反対側の凸面、別径の節、短い折れは残す。左/右/上すべてに同じ長手溝を付けず、live側の滑らかさも許す。面を枝元からtipまで全長へ延ばさない。

一回のsurface sculptでは大きい枝pathや根支持が完全に直るとは保証しない。現primaryの肘/腕の輪郭がなお同じ美しいSに見えるなら、細い溝が増えてもmacro未達とする。

## field編集の範囲と検査

planeにfront_onlyがあるだけでなく、strokesにも前向き外表面/局所depthのgateを明記する。XZ maskだけで背面や既存cutの壁も一括+Yへ動かすと、木の厚みを圧縮し、faceのfoldや交差を作る。実法線と面の向きに沿って限定する。片側に開く処理でも貫通穴・孤立lip・極端に薄い膜を作らない。

強いmask境界で新しい細長いtriangleや折返しを作らず、同topology/closed component/残厚/face crossingを元の適切なgateで確認する。source metadataやsame topologyの維持だけでは無交差や自然さを認定しない。新しい実surfaceは別candidateとして保存し、初回v01と検査/画像を保持する。

## geometryとnormalの役割

geometryで直すもの：丸いrimと独立突起、露出面の大きい方向/厚さ、片端の実際の破断、根と枝の付根、限定視差でも変わる大きい裂け、輪郭・接触に影響する欠け。これをnormalで隠さない。

geometry選定後のnormal/bumpへ回すもの：面の中の細かい木目、毛羽、小さい乾いた割れ、薄い剥がれと粗さ。全景の輪郭や枝元を変えない小さな凹凸に限る。色/roughness/normalは独立比較し、textureで現在の目/唇/ゴム腕が木らしく見えたことを形状合格に置換しない。

一度のdirect sculptを同じ中立正面/±12と、近い冠を含む同条件の夜庭PCgarden/bonsai/trunk＋390/320で再判定する。自然な一件を選べたらSHA固定→shaderへ。形状未達なら理由を残して分け、さらにsource楕円/voxelの係数反復を続けない。

現在の通常夜景全景・shader仕上げ・性能/motion/fallback・実機/Safariはこのレビューで未確認。独立担当は本レビューのみ新規保存し、mesh/コード/他runを変更していない。

## v01通常夜景とdirect sculpt追加判断

同じworkerの再開後、qa/browser-v01のafter-garden.jpg / after-bonsai.jpg / after-wood.jpg / after-mobile-390.jpg / after-mobile-320.jpgの5枚を全て実見した。親の略称after-390/320ではなく実在のafter-mobile-*を読んだ。results.jsonは10capture/全after ready/capture logs空。ここではafter5枚を実見したので、before10枚全てを実見したとは扱わない。新しいブラウザ起動・画像編集はしていない。

夜庭でも初回surfaceは形状未合格。上下のclosed oval rim、中央の丸い突出、右側の腹が通常距離でも強く見える。幹寄りでは短いcutが木部の裂けより、膨らんだrimへ付けた暗い線に見える。無texturebrownの条件なので細かい木目未仕上げは別に置くが、現在の未達はnormalで直す細部だけではない。

前工程の遠い三葉群と比べ、現在の冠は近づき、上冠へ長い細twigで持ち上げる印象が減った。左群・上群・低い右群の非対称な階層は読める。しかし枝の腕と肘はまだ滑らかで、主木中央の閉じた丸いrimが主役の品位を妨げる。葉を近づけただけで本体のNGは消えない。庭の石/鉢/低い台/縁側と開口/光は維持され、画像に新たな大きい浮遊は見えないが、背景や高級な全景の完成認定はしない。

390/320は切れず、上冠から鉢/台と建築の関係が残る。afterの冠〜台bboxは390で幅約68%/高約36%、320で幅約68%/高約44%。390の上下空間と両者の下側砂利の余白が主役の存在感を弱める点は残る。小幅でも目/唇状の丸rimは見えるため、今回のsculptは微細な溝を増やすのでなく、この露出した大形を優先する。

### 反映予定の修正範囲を支持する

親報告の中央lipをlower同planeへ統合した局所mask、upper左片端を開く処理、上枝のwidth .055〜.06の有限平面、front/outward normalとdepthgateは、先の三提案と整合する。計画として支持し、まだ実surfaceの達成とは認定しない。左右枝へ同じ溝を配らない方針も妥当。

追加のcore右側の有限斜面（maxX削り.04、z.48〜.86）と、土際前面（centerXZ(.13,.405)、radius(.20,.085)、maxY削り.065）は、現在の腹と丸い根接合を抑える範囲として支持する。一回の同baked sculptのscopeであり、source mass/voxel/decimationの再反復や第三候補を要求していない。

安全かつ形状を保つ実装条件は以下。

- 根前shaveとlower rimはz.45〜.49で範囲が重なる。変位を単純加算して二重に削らず、同じ目標面または許容最大変位へ統合する。部位ごとに実残厚を測り、約.08〜.10の芯という目安を名前だけで満たした扱いにしない。
- 低い右主枝の起点z.84付近は、core右planeをz.78〜.86でfadeして口の厚みと外向きの接続を残す。枝元を細い三角膜や棚へ変えない。
- 土際のheight Zは動かさず、左右root buttressと背面を対象から除外する。source yはdepth方向で、+Yへの削りは高さを上げる処理ではない。深いcut壁と裏面も法線/depthで除外する。
- 同topologyでもface折返し/交差が起こり得る。変位後の閉成分・area・交差・残厚を確認し、元v01と変更記録を保持する。全体smoothで面を再び丸くしない。

以上の条件下で一度のdirect sculptへ進める。新geometryは同じ灰色3視点と通常夜景PC/390/320で再判定する。今回の冠/背景/光を固定し、surface geometryの変更を分けて比べる。geometryが自然に選べた時だけSHA固定→shader独立比較。現v01は未合格で、素材仕上げ・性能・motion/fallback・実機/Safariの完成認定はしていない。独立担当の変更はこのレビュー追記のみ。
