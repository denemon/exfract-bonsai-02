# 遠景の枝葉・庭の起伏を再設計した部分候補

背景の空間配置、枝に従う不規則な遠冠、庭の連続地形とモバイル構図を再設計し、工程18の独立したローカル候補を保存した。相対的な配置・葉群改善はあるが、目標の自然さと高級感は未達。本採用best-state/5208と工程17候補5210は変更していない。主役woodはedge-v02/bark-connected-cedar-v2を固定し、新sculpt carved-v02は保留のまま。

最終ビルド: http://127.0.0.1:5212/ 。比較元: http://127.0.0.1:5210/ 。`candidate/`で`npm run build`、`npm run preview`。ソース、素材、依存関係の一部を既存の新プロジェクト内から読み取り専用で参照するため、単独で移動できるexportではない。旧projectにはアクセスしていない。

## 変更と選定

先にDESIGN.mdで盆栽中心の庭、建築の後退と角度、石・連続地面・二つの遠木、PC/portraitの構図と予算19MiBを決めた。建築を[2.37,0,−2.86]へ移し、同じhousePointで開口・柱・梁・床と室内光を配置。奥境界はz−6.4で建築に終端を接続し、wideで急に見えていた左壁端を拡張した。写真面・ぼかし・散在小石・可視文字は使わない。

均等な水平葉房を並べる方法を離れ、3〜4個の不等な冠域へ実際の枝を伸ばし、枝端と内部の小枝へ6605枚の閉じた湾曲葉を付けた。冠域の楕円を表示するmeshはない。4prototypeの境界・辺向き・正のsigned volumeを実ブラウザで検証した。以前の扇形の葉と、黒いchipに見えた苔3394tuftは棄却。棄却記録・画像を保存し、最終sceneへは入れていない。

苔と砂利は同じ512px linear高さfieldをgeometryとmaterialで使う。左床の実mesh間隔を.035mとし、61,830triの連続地形へ不等なhummockと土際の落ち込みを作った。石2つは既存CC0scan、埋込みと根接触は同じ地表。鉢脚の台へのgapは最大0.575mm以内、植栽根は4〜7mm埋まる。これらは技術的接触の確認で、自然さの完成認定ではない。

PC通常はd3.65m、390 yaw−24°、320−26°、pitch8°。実頂点投影で390は横92.26%/縦40.53%、320は横92.18%/縦50.41%、冠から鉢・台まで切れない。工程17より縦占有は下がり、建築柱/軒との競合と余白は残る。縦長320×844は冠/鉢を収めるが主役が小さく、改善余地が大きい。

形状を固定した後、背景葉のmatte色、苔の小さな凹凸と建築木目を複合比較し、別比較でrearGlow power8.4→11.088を評価した。微差と左中景の読みを局所改善として保存した。黒い遠冠内部は未解消。材料比較は複合なので、各channelの独立効果を立証した扱いにはしない。主役木・葉・鉢shader、global exposure、hero keyは固定。

## 実表示・表示機能

最終コードを一度build成功。Mac Chrome154/ANGLE Metal Apple M1 ProでPC1440×900、390×844、320×568、wide1920×800、tall320×844を実表示した。PC全景・盆栽全体・幹寄りはR17と同じactual camera/target/FOV/exposure。QAが直接cameraを置いた診断ではstats.cameraはmainの通常構図記録のままで、row.comparisonCameraと全頂点投影が実際の構図。通常PCとスマホ写真の前後比較は構図差を含む。

代表画像はqa/final-scene/のpc.jpg・mobile-390.jpg・mobile-320.jpg・after-garden.jpg・after-bonsai.jpg・after-wood.jpg。最終source撮影後のrelease実表示で、actual camera、全頂点投影、geometry/fieldが一致した。重複写真を保存しないため最終buildはJSONで検証。スクリーンショットのbyte/pixel同一を主張しない。qa/release-verification.jsonにHTML/JS/CSS/WASMgzip復号SHAと元ファイル一致を保存。

同じ最終実景の完成静止画5比率をWebPへ変換し、初期inline背景と鮮明pictureへ同期した。crop/美化/参考写真背景への置換はない。実releaseの低速loading、WebGL2不可PC/390/320、動き低減、idle、制限付きdrag、wheel、実WEBGL_lose_context喪失/復帰の10ケース成功。reduced時はcamera入力不変、idle1秒frames1→1、通常drag±8°/距離3.65mを保持。意図的WebGL失敗warning3件と通常error0を区別。320/tall/wideのfallback元は実撮影・media設計で確認したが、wide/tallのWebGL不可分岐はこの工程では別case未実行。

## 性能

EXT_disjoint_timer_query_webgl2で固定camera31render、先頭2除外し29集計。baseline mobileのGPUは候補の実cameraを注入して同条件にした。DPRと実倍率を区別する。Macの短時間値を実スマホ・熱安定性・連続60fps保証へ転用しない。

| 条件 | DPR / 実倍率 | median / p95 ms | steady triangles |
|---|---:|---:|---:|
| before同camera before-garden | 1 / 1 | 9.39 / 14.36 | 1,403,058 |
| before同camera before-bonsai | 1 / 1 | 10.57 / 14.94 | 1,403,058 |
| before同camera before-wood | 1 / 1 | 12.86 / 13.48 | 3,046,918 |
| before同camera mobile-390 | 1 / 1 | 9.89 / 12.60 | 1,303,118 |
| before同camera mobile-320 | 1 / 1 | 10.07 / 12.42 | 1,303,118 |
| candidate pc | 1 / 1 | 10.49 / 15.74 | 1,368,238 |
| candidate after-garden | 1 / 1 | 9.13 / 12.86 | 1,368,238 |
| candidate after-bonsai | 1 / 1 | 10.72 / 13.16 | 1,368,238 |
| candidate after-wood | 1 / 1 | 12.47 / 14.45 | 3,012,098 |
| candidate mobile-390 | 1 / 1 | 10.27 / 12.67 | 1,268,298 |
| candidate mobile-320 | 1 / 1 | 9.65 / 12.57 | 1,268,298 |
| candidate-retina pc-retina | 2 / 1.6 | 12.67 / 13.22 | 1,368,238 |
| candidate-retina mobile-390-retina | 3 / 1.6 | 9.56 / 14.65 | 1,268,298 |

通常の低速ナビゲーション250KiB/s、latency120ms、cache off、script待機なしではfirst paint0.336秒、鮮明still1.893秒、navigation→3D15.255秒。3D初表示はまだ重い。idle継続RAFはなく、葉の常時揺れも入れていない。微小操作の視差のみ。実機スマホ/Safari/長時間GPU熱/連続gesture安定性は未検証。

## 未達と保護

遠冠の裸の軸と暗い内部、遠木上端の切れ、苔の滑らかなmat感、単調な建築木目、スマホの柱/軒との競合と縦余白、主役の太い均等な枝と茶褐色木の面は未達。添付画像の銀白色のねじれた枯れ木と赤褐色の生き筋を実見しているが、現在の主役でそれを達成していない。作者・独立レビューとも全景を高級な完成作品とは認定しない。機能/構造検査成功を見た目の完成と混同しない。

geometry SHA `2e79449acc970fab3b9e49c5610ee9b7ac01022d7762d8970c280261ecc9fc2b`、field SHA `008d852ef489b472af78dcbdc66c0b47f6a3911bea4ad70fa482c831a7b15592`。固定source7件も一致。木carved-v02の灰/夜選定と木shader仕上げは今回0。

現在source/production/16状態と工程17を含む存在する過去成果SHAは一致。親の外部PR7で削除された過去配列24件と非採用NPZ2件は引き続き欠落26件、manifest該当4件の歴史的完全保護は不合格。このwriterで復元/Git書込み/削除/push/PR/merge/公開/購入/automation作成0。Libraryは既報TLS阻害のため再試行0・ID0。確認画像はMacローカルに保存した。指定Sol/xhighの実行metadataは露出しておらず適用確認不可。

19MiBを事前予算、20MiBを目標にしたが、実測runtime cache増加を保守的に含めると超過する。Chromeが初期のtiny-cache flagsで自身のmutable cacheをevictionしたことを記録し、そのflagsは除去済み。負のprofile差を新規容量の控除にしない。過去成果を削除していない。最終値はfinish.json/qa/profile-footprint.json、100MiB上限/free2GiBを確認する。

## 幹寄り比較の追加検証

独立レビューで初回幹寄りJPEGの葉精細度差が指摘された。camera/FOV/exposureは一致していたが、寄り操作後の詳細葉の非同期ロード中に写真を取得し、初回比較を同LODまで厳密一致とは認定できない。この初回画像と記録は保持した。

追加qa/wood-settled-comparison/のbefore-wood.jpg/after-wood.jpgは両releaseに同foliage-lod=highを設定し、detailReady/highAvailableを確認後に同じ幹寄りactual cameraで撮影。可視主役meshのposition/normal/index/instance/world rowsと実SHA `ff3a5a3c674708473a334f7e8cd8f5a719d4a17fe4e90ec243333529d8bf3ed1`が一致、visibleLeafTriangles4,670,400、warning0。このforced-highは通常の自動leaf budget2,600,000を超える診断条件であり、通常性能tableと混同しない。comparison-final.htmlの幹寄りはこの追加pairを使う。本番コード/buildは変更していない。

最終容量（file allocated、manifest込み、負のcache差を控除しない）: own run 10.85MiB、own staging 0.15MiB。Chrome eviction後の観測最小からの増加 21.86MiBも計上した保守的合計 32.96MiB。20MiB目標未達、100MiB上限内、free 3.53GiBで2GiB下限内。詳細はqa/profile-footprint.json。
