# 工程18 背景実像の独立レビュー

対象はbackground-depth-1608。初回initial-shapeのPC/390/320とshape-v02のPC/390/320、計6JPEGを実ピクセルで確認した。R17のPC/390/320と生成目標は制作前レビュー時に実見済み。書込みはこのrunのqa/background-review.mdだけで、R17のfreeze、コード、モデル、他runは変更していない。browser/agentは起動していない。

## v02のmacro採否

**背景全体の自然なmacroとしてはNG。建築配置と境界の相対改善は認める。**

初回では境界wall/瓦の線が室内へ入り、室内の奥行きを塞ぐ大きい物理矛盾があった。v02で境界が建築の接続部に終了するようになり、畳/奥壁/卓の室内が再び読める。R17に比べて近い太柱と軒が主役右冠の真後ろを大きく塞ぐ状態も減った。この配置の改善は実像にある。

一方、遠冠は依然、太いfern状の房が裸の細い支持軸に離れて付く。冠ごとの量塊の厚さ・内部・前後重なりを鑑賞するより、葉の尖った長房とfan軸の方向が目立つ。初回より葉は詰まるが、目標の不規則に重なる自然な背景冠には達していない。3/4の支持量塊や前後halfExtentsを実装したことを、実像で量塊が成立したと換算しない。

苔は左前景/石際へつながる地形としては一体だが、通常距離ではまだ広い滑らかな緑マットに見える。小さい地形の明暗はあるものの、谷・中尺度の隆起・薄い苔端を明瞭に鑑賞できる段階ではない。DESIGN_RESPONSEの35mmgrid、26〜42mm rise、512fieldは技術値で、これだけで自然な苔の造形成功とは評価しない。現在の光で表情が弱いことと、実shapeのmacro不足は分ける必要がある。

PCでは主役と室内の間に砂利の距離が生まれ、同じ庭としての配置は改善したが、主役の根/木shape保留、疎な中景maple、遠冠の輪郭、苔の表情が残る。全景のpremium品質や美術館のような品格は未達。

## 表示記録と比較範囲

initial-shape、shape-v02のresultsは各3件ready=true、text空、scroll=false、logs0。PCのcameraは両者ともposition[0,1.4659103,3.8899906]、target[0,.78,0]、distance3.95で、主役の全vertex投影境界も同じ。木を固定したまま背景差を診断している条件と整合する。v02の背景runtime SHAは9203185784a9cf20363a36d6dee49b40431bad4a81bd04c078913ba7816d3598。

v02では建築と遠冠が変更され、mobileのtargetも変更されている。従って初回とのmobile差を、camera変更と背景shape変更の一項目だけの独立効果として記述しない。建築/樹根のcontact metadataは浮き懸念の位置確認に使えるが、すべての接触影・石周囲の自然さを独立保証するものではない。build/fallback/performanceはこの実像レビューでは未認定。

## スマホは余白の交換であり拡大改善ではない

resultsのexactProjection.boundsから、主役subjectの全vertex投影幅・高さ・上下余白を計算した。R17の同じ形式の記録と比べても、横幅を維持した正面寄りcameraが主役の高さを減らしていることが分かる。

| 記録 | 幅% | 高さ% | 下余白% | 上余白% |
| --- | ---: | ---: | ---: | ---: |
| R17最終390 | 92.14 | 42.42 | 30.86 | 26.72 |
| R18初回390 | 92.27 | 36.92 | 33.28 | 29.80 |
| R18v02 390 | 92.27 | 37.21 | 28.49 | 34.30 |
| R17最終320 | 92.02 | 53.60 | 25.09 | 21.31 |
| R18初回320 | 92.32 | 46.11 | 28.73 | 25.16 |
| R18v02 320 | 92.32 | 46.54 | 23.83 | 29.63 |

v02で盆栽は画面下側へ移り、土台下の砂利余白は減るが、上部の空/屋根の余白が増える。高さ自体は初回からほぼ変わらず、R17より小さい。樹冠・鉢・土台が切れないことと、主役存在感の改善は別。『砂利余白を減らした』とは言えるが、『盆栽を大きく鑑賞できる構図へ改善した』とは言えない。

柱との競合減少と左の境界/空の回復には利点がある。ただし390では上部の大きい青空と、下側に置かれた小さい主役の関係が強い。320でも冠は収まるが、静かな箱庭を鑑賞する十分な主役階層として完成認定するには不足する。このcameraを純粋な総合改善として選ばず、得た距離と失った主役サイズを記録する必要がある。

## 次の広葉prototype比較への独立判断

閉じたhero frond原型を遠冠へ使うことは、長い尖ったfern輪郭の一因と考えられる。7〜9cmの閉じた湾曲広葉に替える一回の表現比較は妥当。遠景を主役と別の庭木として描き分ける方向にも合う。

ただし実像には、葉がfan軸沿いに束になり、量塊間が裸の枝で離れる配置も見える。原型だけが単独原因であると断定する証拠はまだない。同じ支持軸と配置を保ってprototypeを変更した比較で、葉の輪郭と量塊充填のどちらが改善したかを見られる。

各枝の両側に同寸の葉を二列・等間隔で並べると、広葉でもfern/bottlebrushの反復は再発する。固定する3/4支持量塊を基準に、葉の長さ/向きの違いだけでなく、量塊内部と前後の短い枝を葉群が占めるかを通常PCで確認する必要がある。支持軸の固定は比較の基準として可であって、自然形状の最終freezeではない。葉を替えた方法名や枚数でmacroを合格扱いにしない。

次の比較に進む判断を支持するが、v02を自然な遠冠として選定し、素材だけで完成へ進める判断は支持しない。室内干渉の修正/柱競合の減少という部分改善、遠冠/苔/mobile主役存在感の未達を分けて保存するのが正確。追加browser/agentは起動せず、コード/モデルは編集していない。


## v03広葉化・苔細部の実像判定

qa/shape-v03/のafter-garden、mobile-390、mobile-320の3JPEGをすべて実ピクセルで確認した。resultsは3件ready=true、text空、scroll=false、logs0。背景runtime SHAは3件とも01b7496c79f482703792b3f5a9ca01871730e0ba3e57c93ef8f5355d7fdbe79b。主役のexactProjection boundsはv02と同じで、木を固定した背景比較と整合する。

### v03は不採用

広葉に変更したことで葉の外縁は以前の尖ったshootと異なるが、PCの冠はfan軸の先に束が離れて付く輪郭を維持する。裸の幹と長い支持枝が冠間をつなぎ、葉はその端だけに集まって見える。三次元の冠内部を短い枝と葉が占有する印象にはならず、目標の厚い不規則な樹冠としてmacroはNG。4774枚のclosed bent leaf、16tri、支点が実twig上にあるという技術値は、自然な冠の成立証拠に置き換えない。

初回から改善した室内wall干渉と柱/軒の競合は戻っていない。ただし遠冠の束と中景mapleの疎な支持軸が見え、PC全体を鑑賞できる背景品質には未達。mobileは主役収容を維持するが、v02で記録した高さ占有/上部余白は変わらず、主役サイズの改善はない。

苔の追加細部はPC左前景と両mobileで、地面上の孤立した黒い点として明瞭に見える。元の緑の面に細かい植物が自然に生えた印象より、黒い散布物が置かれた印象が強い。今回の追加geomは、この通常距離の質感を悪化させている。3394sprig/高さ9〜17mm/122184tri、共有地形に1mm埋めたrootは位置・負荷の情報で、自然な苔の外観達成とは別。v03をshape選定してmaterial finishへ進む判断は支持しない。

### 次の支持構造一回への条件

支持枝の先でfanを繰り返す方法を止め、既存の不等な3D冠内部へ短い枝を分岐させ、内枝と前後の葉群で占有する組み直しは、現像の原因に対応している。次の一回を支持する。葉prototypeだけを変更して自然さが成立するという仮説は今回支持されなかった。

樹冠のvolume名や端点への成長アルゴリズムだけで合格にしない。通常PCで、内側にも枝/葉が続いて裸の棒が房同士をつなぐだけの状態を減らせるか、前後の量塊が部分的に重なるか、外周の不等な輪郭と少数の大きい間隙を同時に保てるかを審査する。均一な密度の丸い雲に置換しても別の未達になる。全景で冠が読めることを先に確認し、新finishで輪郭の問題を隠さない。

### 苔の色・微小shadow校正への条件

同じ実mossMapをroot位置で校正すること、短い細部のcastShadowを解除することは妥当な診断修正。サブセンチ〜1cmの細部が低解像度shadow mapで離れた黒い点になる状態を避ける考えに合理性がある。大石/建築/木/地形のcontact shadowと空間のglobal shadowは維持し、強いAOで点を覆う方法にしない。

ただし黒い点の原因をalbedo/shadowだけと断定する独立証拠はまだない。同じroot色でも、sprigの面の向き・normal・受光と、低密度で孤立した輪郭が点を残す可能性がある。world位置からtextureへ対応するroot UV、sRGBからlinearへの変換、ground側の混色/光の乗算が整合しているかを確認する。校正後に点が消えても、以前の平滑な緑マットへ戻っただけなら苔全体の造形課題は未達。

次像では散在物の印象が消えることに加え、連続した低丘、短い谷、石へ上がる苔、土/砂利へ薄く移る端が同じ場所の植生として読むかを評価する。修正実行前に効果を完成認定しない。

判定: v03不採用、shape選定なし、新material finish未評価。支持構造と苔校正の一回の修正は可。レビュー担当の変更はR18のこの文書だけで、コード・モデル・R17・他runは不変。browser/agentは起動していない。


## v04-outward：局所形状改善と未採用の苔細部

qa/shape-v04-outward/のafter-garden、mobile-390、mobile-320、mobile-390-angleの4JPEGを実ピクセルで確認した。resultsは4件ready=true、text空、scroll=false、logs0。4件の背景shape SHAは134a7a3ed33bc3869d76d246e499792bd1e45f75402b24188e5670e856fa82ae、field SHAは008d852ef489b472af78dcbdc66c0b47f6a3911bea4ad70fa482c831a7b15592。PCcameraはR17比較と同じdistance3.95/position[0,1.4659103,3.8899906]/target[0,.78,0]を維持する。

### 遠冠は局所相対改善として保存可

R17の長いpad/frondの反復、R18v03のfan軸端に葉束を付けた輪郭より、v04では小さい枝の不等な分岐とばらつく葉群の外周へ近づいた。全冠が同じ先細りの房として立つ印象は弱まり、葉の向こうに不規則な支持枝が続く包絡が見える。これは物理形状の局所相対改善として保存できる。endpoint-guidedの方法名やclosed leaf6605枚という数値だけで合格扱いにした判断ではなく、実シルエットの差を認めたもの。

ただし木の量塊間には裸の細枝がまだ長く露出し、冠内部は暗い。通常PCでは十分に厚い前後の冠と葉層を鑑賞できず、遠冠上端の一部も切れる。R17から目標の厚い自然な樹冠へ到達したわけではない。背景の冠として疎な印象が残り、中景mapleも支持軸が強く見える。

従って『遠冠形状の局所相対改善を比較candidateとして保持』は可。『自然な遠冠macro/全景premiumの完成選定』はNG。現構造を限定したbasisとして後続の素材の読みを評価することには反対しないが、材質・照明を改善した結果で残る冠の疎さを完成へ換算しない。これまでのfan反復そのままのv03と、今回の実分岐の局所改善は分けて記録する。

### 苔追加frondは非採用に同意

法線の外向き修正後も、PC左前景と両mobileに黒い葉chip状の散布が見える。以前より点の形が平たくなったが、連続した細かい苔の植生には見えない。positive closed component/外向きという技術条件が成立していても、外観の問題は残る。現metadataにはrootでの実mossMap校正と微小castShadow解除が記録されているため、color/shadowの修正だけで解決するという仮説はこの像では支持されなかった。

この追加frond objectsを非採用としてsceneから外し、連続した実heightfield・低丘・薄端だけを選定対象に戻す判断に同意する。孤立したchipを消すことは適切だが、元の苔面が平滑に見える課題まで解決したことにはならない。

今回の134a7a…のshape SHAにはその非採用frondが含まれる。除外後の最終sceneは別geometryなので、最終freezeは新しいruntime/source SHAと除外後の実像で記録する必要がある。この4像だけでfrondなし最終candidateを実見したとは記述しない。

### 390 yaw−24と未表示の320−26

mobile-390-angleはyaw−24/pitch8/距離5.934974で、主役投影幅92.26%、高さ40.53%、下余白27.06%、上余白32.41%。−12の高さ37.21%から増え、冠〜鉢〜土台は画面に入る。建築後退により旧R17ほど太柱が直後で支配する状態は減り、室内開口と左境界も残る。この一枚を−12より良い390の候補として保持する判断を支持する。

ただしR17の高さ42.42%より小さく、上部の空/屋根と下部砂利の余白、右冠と柱の重なりは残る。スマホの主役階層や庭の広がりが完成したとの評価ではない。対象viewportごとのgeometry収容と見た目の両方を維持する必要がある。

このbatchのmobile-320はyaw−16で、提案する最終−26ではない。320−26の構図採否は未評価。今回4枚から両幅の最終cameraを一括認定しない。

判定: 遠冠の物理形状は局所相対改善として保存可、自然さ完成/全景macro採用は未達。追加苔frondは非採用。390−24は相対構図改善、320−26とfrond除外後の最終像は未確認。レビュー担当はこのR18文書だけ変更し、コード/モデル/R17/他runを変更せず、browser/agentも起動していない。


## frond除外後の固定形状と素材・夜光の別比較

qa/selected-shape/のPC/390/320とqa/finish-comparison/のmaterial/refined・light/refinedの2JPEG、計5枚を実ピクセルで確認した。各resultsはready=true、text空、scroll=false、logs0。全5件のgeometryは2e79449acc970fab3b9e49c5610ee9b7ac01022d7762d8970c280261ecc9fc2b、fieldは008d852ef489b472af78dcbdc66c0b47f6a3911bea4ad70fa482c831a7b15592で新freezeに一致。geometry-freeze.jsonの7sourceも現在ファイルのSHAを独立計算して一致を確認した。

非採用の苔frondを除外し、黒い葉chipの散布が消えた判断は適切。連続地形・自然石・苔面の関係を候補として保持できる。ただし平滑な緑マットの外観は戻っており、苔の完成ではない。

selected-shapeの320 yaw−26は実見できた。幅92.18%、高さ50.41%で、旧−16の46.54%から主役サイズを回復し、樹冠・鉢・土台は収まる。390−24とともに、正面寄りの小さい主役より良い個別候補として支持する。ただしR17の高さ42.42%/53.60%に対し今回39040.53%/32050.41%で、絶対的な主役サイズの改善とは言わない。建築後退による距離と競合減少、残る余白を分けて評価する。

素材比較のbaselineはselected-shape/after-garden。background-finish=refined/background-light=baselineのPC像は、葉色・苔/建築micro normalをまとめた複合material比較で、個々の効果を独立立証する像ではない。実差は小さく、明るい乾いた葉の設定でも遠冠内部はほぼ黒い。苔と柱の微細responseも通常距離で明確な材料品質達成を断言できるほどではない。過剰な光沢や大きい発光で隠す状態は見えず、比較candidateとして保存は可。自然な冠・上質な素材の完成採用はNG。

次のlight/refinedは同material/refinedで、source上はrearGlow8.4×1.32=11.088だけの変更。左中景mapleの葉・幹が少し読みやすくなり、既存の庭の光として距離を補助する。大きいhaloや主役より強い発光面は見えない。この局所相対改善候補としての保存を支持するが、far crownの暗部・裸枝・疎さや苔の表情は解決しない。

PCの三段階は同camera/geometryで比較できる。一方、この5枚のmobileは素材/光のrefined適用前であるため、最終refinedの390/320への影響はまだ実見していない。resultsのbackgroundFinish欄は旧finish=material-v01を示すため、新しいbackground-finish/background-lightの区別は各URLとsourceで確認した。全world lightsが同じという比較ではなく、material段階とrearGlow段階を分けた比較として記録する。

結論: 固定形状と個別mobileの局所相対改善、素材/夜光の比較candidate保存は可。自然macro・全premium完成・木shape/shaderは未達。新finishを適用したmobileとbuilt/fallback/performanceは、この節の時点では未確認。担当の変更はR18のこの文書だけ。


## 最終実景・静止画source・ビルド検証の独立所見

qa/final-scene/{pc,after-garden,after-bonsai,after-wood,mobile-390,mobile-320}.jpgの6枚とqa/fallback-extended-source/{wide,mobile-tall}.jpgの2枚を実ピクセルで確認した。R17のqa/final-browser-verified/から全景・盆栽・幹寄り・旧390/320の5JPEGもread-onlyで再実見した。最終refined素材＋rearGlow11.088のmobileはこの時点で確認済み。追加browser/agentは起動していない。

比較cameraの確認を訂正する。最初にstats.cameraを診断撮影の実cameraと誤読したが、PC診断3種はrow.comparisonCameraが実値である。position/target/FOV38/exposure1はR17同名3種と一致する（purpose文は違う）。全景のdistance3.95、盆栽のposition[0,1.34782954,3.22032135]、幹寄りのposition[-.02,.91442504,1.36949047]を照合した。幹寄りは意図的なcropで、全冠が切れるのは収容失敗ではない。通常pcは3.65へ寄せた別構図、mobileもR17の−30/−33から−24/−26へ個別変更しているため、通常pc/旧mobileとの違いを背景単独効果にしない。また室内光源は建築に伴い移設され、rearGlowも変更されている。同camera/FOV/exposure・固定hero key/materialの比較であり、全world lightが不変の比較ではない。

### 実景の採否

建築を右奥へ退けたことで、通常PCと同camera全景とも盆栽と室内の間に庭の距離が生まれた。近い太柱と軒が主役を囲い込む状態は減り、床・短い支持脚・開口・室内奥を分けて読める。境界が室内へ入り込んだ初回の破綻は最終像では見えない。鉢と低台の接触、石の埋まり、砂利と苔の連続も保たれ、通常幅で別々の展示物が浮く印象はない。この空間配置と連続地形は局所相対改善として保存できる。通常PC3.65では台石を含む主役投影高さ67.22%（同条件全景3.95は61.82%）となり、庭の広がりと主役の存在感の候補として成立している。

遠冠はR17の大きなpad/frond反復より、不等な小枝と小さな葉群の外周に近づいた。しかし裸の細枝が長く露出し、黒い葉群と空の穴が強く、厚みのある成熟した植栽にはまだ見えない。境界の長い水平帯と平滑な室内壁も依然強く、建築の各部を作ったことを鑑賞品質達成へ換算できない。苔chipの非採用は適切だが、残したheightfield＋微細responseの苔は通常距離で緑のマットとして読む。石と砂利は比較的落ち着いている一方、苔・樹冠・建築の材料の説得力には差が残る。refined素材と夜光に過剰な濡れた光沢や大きいhaloは見えず、控えめな比較候補として保存可。ただし美術館や高級旅館の完成景色とは認定しない。

390−24/320−26は樹冠から鉢・台石まで画面内で、開口・境界・地面の関係も読める。固定主役全vertex投影（台石を含む）の幅/高さは390で92.26%/40.53%、320で92.18%/50.41%。旧R17の高さ42.42%/53.60%より小さく、主役サイズの絶対改善ではない。建築の後退による競合減少は支持するが、上部の空/軒、下部の砂利余白、右冠と柱の重なりは残る。wide sourceは庭と室内の距離がよく分かるが、広い苔面の平滑さも露出する。320×844のmobile-tall sourceは全主役が収まる一方、主役がさらに小さく、上下余白が大きい。極端な縦長比率での存在感は未達として残す。

主役woodはedge-v02の茶褐色の滑らかなS量塊・均質な腕・弱い根支持がそのまま見える。参考写真の銀白色deadwoodと赤褐色live筋を持つ名品の古木造形は未達。背景の局所改善やshader/build成功によって、この主役を完成採用しない。さらに幹寄りの実JPEGではR17の左葉群は細かなspray、R18は角の立つ大きい葉の集合に見える。保存stats.foliageLODは両方low/highAvailable=falseだが、撮影時点の実LODまで一致する証拠にはならない。原因は独立確認できていないため、近接葉の表現まで厳密同一として背景単独改善を立証しない。幹の輪郭固定と庭の空間差を読める範囲で比較した。

### 静止画と最終ビルドの検証範囲

qa/fallback-source.jsonの5source JPEGと5encoded WebPのSHAを独立計算し、全件manifest一致を確認した。実景からの形式変換として保存され、完成像の代替として利用できる。読み込み実像qa/resilience/loading-pc.jpgも実見し、文字や空白画面でなく最終の庭を表示することを確認した。wide/tallはsource画像の確認であり、この2比率のWebGL不可分岐を実ブラウザで確認したとは記述しない。

qa/final-browser-verified/results.jsonの6件とdev写真時resultsを独立照合し、actual camera、exactProjection、geometry/field SHAが全件一致した。背景geometryは2e79449acc970fab3b9e49c5610ee9b7ac01022d7762d8970c280261ecc9fc2b、fieldは008d852ef489b472af78dcbdc66c0b47f6a3911bea4ad70fa482c831a7b15592で固定。final buildの6件ready=true/text空/scroll=false/logs0。release-verification.jsonはbuild成功とHTML/JS/CSS/WASMのgzip復号SHA一致を記録する。最終ビルドで同camera/形状/投影の再検証は成立するが、builtのJPEG6枚を別途実見したことやpixel-identityは主張しない。

qa/resilience/results.jsonは10case success=true。無停止cold（250KiB/s、latency120ms、cache無効、scriptReleaseMs:null）はfirst paint/FCP336ms、鮮明still1.8933s、navigation→first3D15.2555s。script開始基準のfirstFrameMs13.5162sとnavigation基準15.2555sを混同しない。3D開始は重く、R17との僅かな秒差を速度改善の根拠にしない。記録上は実WEBGL_lose_contextのloss/restore、getContext nullのPC/390/320で適切な静止画、reduced idle1000msのframes1→1とpointer camera不変、通常入力yaw8°/pitch12°、wheel距離変更を確認できる。通常logs0と、WebGL不可3件の意図的catch warningを分ける。これらは実行記録の確認であり、静止画未保存ケースを実ピクセル審査したとは言わない。

GPUはqa/final-browser-verified・baseline-browser-verified・retina-browser-verifiedを独立読込し、31renderから先頭2を除いた29sampleのmedian/p95を再計算して一致した。DPR1の候補通常PCは10.49/15.74ms、390は10.27/12.67ms、320は9.65/12.57ms。実render pixelRatio1.6のretinaケースはPC12.67/13.22ms、3909.56/14.65ms。EXT_disjoint_timer_query_webgl2がsupportedでinvalid=false。R17をR18 exact mobile poseで測り直したbaselineとの値は小幅に上下し、一貫した性能向上は立証しない。これは同じMac GPUでの描画時間で、phone幅/DPRエミュレーションを実機スマホ性能へ外挿しない。firstFrameや三角形数をGPU性能の根拠にしていない。実機スマホ/Safari・長時間/熱負荷は未検証。

最終判定: 空間配置・連続地形・不等な遠冠輪郭・控えめな素材/夜光の局所相対改善としてR18候補を部分保存するのは妥当。自然な遠冠、苔の実在感、参考に沿った名品盆栽、全景の高級な完成品質は未達。cold3D15.26sも残る。機能/ビルド/GPU記録の成功を美的完成へ換算せず、best/production変更を支持しない。レビュー担当の書込みはR18のこの文書のみ。R17レビューは45764B/SHA ee2a431d44cfa77304c29afb7cd8f72e387cab9e1fa31c6da07f392c8b978660のまま再確認した。他run・コード・モデル・状態は変更していない。


## settled high幹寄りpairの補足とレビュー凍結

追加のqa/wood-settled-comparison/{before-wood,after-wood}.jpgの2枚を実ピクセルで確認した。実build5210/5212へfoliage-lod=highを指定しdetailReady/highAvailable成立後に撮影したpairである。results.jsonは両ready=true/text空/scroll=false/logs0、level=high/changed=false/highGroups72/visibleGroups72、visibleLeafTriangles4,670,400で一致する。

comparisonCameraのposition/target/FOV38/exposure1、exactProjectionが一致することを独立照合した。可視hero93meshのposition/normal/index/instances/instanceMatrix/world rowsが全件一致し、このrowsのcompact JSONからSHAを独立計算して両方ff3a5a3c674708473a334f7e8cd8f5a719d4a17fe4e90ec243333529d8bf3ed1に一致した。背景を除いた実hero geometryの同一性が、この追加証跡では成立する。

実像でも左右葉群は同じ細かなsprayとして読み、初回R18幹寄りにあった粗い角葉との差を今回の前後差として混入させていない。建築の右奥への後退、床/開口の距離、砂利と左苔面の違いを同主役・同cameraで比較できる。幹そのものの滑らかなS量塊、腕の均質さ、根支持の弱さは前後とも残り、背景改善による古木造形達成は認めない。

初回幹寄り写真のLOD/撮影時点の限界は保存記録として維持し、追加pairで解消したcontrolled close比較と分ける。今回の強制highは通常leafBudget2,600,000を超える診断設定であり、通常描画や前節GPU tableの状態・性能証拠には用いない。geometry SHAは素材/光の同一性まで証明するものではなく、背景光源移設とrefined素材/夜光の変更を宣言した比較として扱う。

最終採否は変えない。R18の局所相対改善は部分保存可、自然な冠/苔/名品盆栽/全景の完成採用は未達、cold3D15.2555sも残る。この補足を最後としてレビューを凍結する。担当はR18のこの文書だけ追記し、コード/build/モデル/R17/他runを変更していない。
