# 工程20：高い塀・前障子・夜空を備えた暫定全景best

現在の作業基準と暫定全景bestを `depth-balance-1905` に更新する。高い塀、実体のある前障子、夜空という追加依頼を実3Dの一つの空間として実装した。以前の暫定基準R19より、PCの開口奥とスマホの主役サイズ・後景の関係が改善した。数千万円級の盆栽にふさわしい美術館・旅館の品質という全体目標は未達。相対的な暫定採用と完成採用を分ける。歴史best5208と18旧状態は変更していない。

確認URL http://127.0.0.1:5214/ 。コード `candidate/` と `background/`、最終実写真 `qa/final-source/pc.jpg` / `mobile-390.jpg` / `mobile-320.jpg` / `mobile-tall.jpg` / `wide.jpg`。`comparison-final.html` に選定・変更前後・素材・全景・読み込みをまとめた。サイトの表示文字は0。確認資料には説明があるが、実サイトにはロゴ・名前・説明・メニュー・ラベルを追加していない。

## 空間と主役

後方の境界は実高さ2.321m、木板・三段の横桟・柱・厚い笠木・瓦・基礎を持つ。右端を家屋の外側の返しに接続し、室内を横断していた試作を修正した。基礎下端−45mmで遠い地面にも埋まり、サンプル7点は全て正の埋まり値。主役の鉢脚4点の実レイ接触差は約+0.0005〜−0.575mm。全接触・全枝干渉を保証する検査ではない。

右奥の家屋はfront[1.85,0,−3.8]、yaw−18°、横scale.76。約3.65mの前面に各851mm幅・2.062m高の障子を三枚、近い側に965mmの開口を置く。50mmの框、約10mmの組子、停止した横桟と深さをずらした交差、0.5mmの紙面、敷居・鴨居・引手を実形状にした。0.5mmは選定したモデル寸法で、実在製品仕様の引用ではない。紙は組子の裏面に接し、6mmの板状試作は不採用。奥行き2.54mの床、床の間、低い台と小さな灯り、厚い側壁、梁、縁側支持、瓦屋根を同一座標に構成。床の間の背面・上部の空隙を実壁厚で閉じ、空が室内の継ぎ目から見える症状を修正した。

自然石2個と既存の連続地形fieldで苔・土・砂利の境を共有。新しい周辺の木は[−3.35,−5.65]、[.55,−7.25]、さらに家屋の奥[5.8,−5.9]の三株。三番目は非対称の別配置・枝構成を持ち、スマホにも屋根上の後景を残す。閉じた葉の全形状と枝を保持し、植栽単位のinstance boundで画面外をfrustum除外する。合計31,080枚、三株×四prototypeの12batch、各16triangleの閉じた曲がった葉であり、球・板・木のない葉雲ではない。閉形状の検査成功を自然な樹冠の完成と混同しない。枝先束・裸軸の人工感は残る。

主役の灰褐色/茶褐色edge-v02造形とbark-connected-cedar-v2材質を固定した。元の添付画像の実ピクセルは確認し、幹のねじれ、枝の空隙、横広がりの参考とした。現在の色基準では白色を再導入していない。原写真のような古木の削れ・ねじれ・生き筋の自然さは未達で、滑らかなS字の量塊と均等な枝腕が大きな課題。carved-v02は保留・未選択、gray/nightの再選定と木の追加仕上げはこの工程では行っていない。

## カメラ・夜の光・素材

PCは正面/FOV38/距離3.65/target[0,.78,0]、390×844はyaw−40°、320×568は−30°、320×844は−45°、スマホのpitch6°/FOV54。単純な中央切り抜きではなく、主役の投影から個別fitした。主役全体の占有高さはPC67.22%、39048.24%、32052.01%、縦長32042.26%。旧R19の39040.36%/縦長32034.30%より大きい。−50/−60°試作はさらに大きくしたが、障子と冠の重なり・後景消失が強く不採用。現構図でもスマホの障子と冠の重なりは残る。

空は深い青の夜空と控えめな星。月/skyと主役の暖かいkey70を維持し、室内・後景の有限光源を実配置に合わせた。紙は乾いた繊維・微細な法線と18%の背面照射散乱近似で、発光面にしていない。元の空間hashの木目を保持し、6mm砂利の9近傍計算を事前計算tileへ置換。背景の苔色512RGB/高さ128、石法線256/ARM128を既存CC0ローカル材料から派生し、石の色mapと主役の形/UV/材質は維持した。派生6asset計195,808B。新URLに分け、旧R19の素材を変更していない。

影の実測ablationで16sample filterと背景微細計算が負荷源と分かった。主役PCF8・背景PCF4、主役map2048・周辺map512を選んだ。五つのshadow castは全て保持。影を消す、主役や葉を暗くする、主役のLODを落とす処理で速度改善していない。3D texture近似の計測も保存したが、最終は元の空間木目を保つhash。最終recipeは `PERFORMANCE_DESIGN.md`。

## 最終検証と限界

`npm run build` は計2回。初回は自分のrelease-helperの誤った可視mesh期待値で静止画同期が止まった時点のcompileで、最終検証対象から外した。bare診断は実際8mesh、詳細葉を含むforced-highは別に93meshを実撮影して一致確認した。同期後の2回目が最終buildで、物理的な最終distは一組、JSchunkは同じ。`qa/build-attempts.json` に記録。最終配信14ファイルのdecoded byte/SHAがlocal fileと一致。

Mac Chrome154実ブラウザでPC、390、320、縦長320、wide、Retina3構図の計8表示がsourceと同camera/主役/背景geometry/field/全light/投影で一致。文字0、overflow0、予期しないconsole0。実写真を重複保存せずsource写真を参照し、source/buildの画素完全一致は主張しない。固定geometry SHA `dadb0605015e297c8a91edcedb3f7c07db4b5a95f305534475ae34310f4880cc`、field SHA `4bedbbe02d16e01b661f942107c643660e6f28f1740f783508a85a9a73d755dc`。garden/bonsai/forced-high woodの変更前R19/後R20は同実camera/FOV/exposure/主役attribute・matrix・LOD・投影/key70で3組一致。背景と有限光の配置、微細shadow filterの変更は宣言。woodの4,670,400葉triangle allocationは診断専用で通常性能値には使わない。

機能12case成功：cache無効の通常cold navigation、WebGL-null PC/390/320/tall/wide、動き低減idle/input、通常制限drag/zoom、実context loss/recovery。待機中の連続RAFなし、reduced motionは1→1frame/drag無変化。五比率の最終実景のstatic WebPは計465,196B、inline小画像と併用し、読み込み/WebGL不可/context lossへ同期した。低速250KiB/s・120msの通常navigationはFCP324ms、鮮明な実景static1.631秒、初回3D11.777秒。旧R19の2.775/17.699秒より短い観測だが、11.78秒はなお重い。

| 実測 | 実倍率 | median ms | p95 ms | triangles |
|---|---:|---:|---:|---:|
| finalR20 / pc | 1 | 13.35 | 16.91 | 1,810,918 |
| finalR20 / mobile-390 | 1 | 13.38 | 15.91 | 1,591,238 |
| finalR20 / mobile-320 | 1 | 9.46 | 12.50 | 1,603,654 |
| finalR20 / pc-retina | 1.6 | 15.81 | 28.77 | 1,810,918 |
| finalR20 / 390-retina | 1.6 | 11.03 | 19.18 | 1,591,238 |
| finalR20 / 320-retina | 1.6 | 12.35 | 17.69 | 1,603,654 |
| samecameraR19 / pc | 1 | 18.02 | 21.93 | 1,748,806 |
| samecameraR19 / mobile-390 | 1 | 14.75 | 22.22 | 1,736,606 |
| samecameraR19 / mobile-320 | 1 | 17.01 | 21.00 | 1,748,914 |
| samecameraR19 / pc-retina | 1.6 | 23.18 | 24.47 | 1,748,806 |
| samecameraR19 / 390-retina | 1.6 | 16.82 | 22.90 | 1,736,606 |
| samecameraR19 / 320-retina | 1.6 | 15.11 | 24.27 | 1,748,914 |

同期間・同cameraの旧R19に対し中央値は改善。PC通常13.35/16.91ms、Retina実倍率1.6では15.81/28.77ms。Retinaのp95は旧R19の24.47msより退行した。負荷変動がある29sampleなので、60fpsや全機種の滑らかさは保証しない。実機スマホ、Safari、長時間熱負荷、要求model/effortの実runtime metadataは未検証。Macの幅エミュレーションを実機スマホ検証とは呼ばない。

## 採用と保存

best5208と工程17/18/19を同camera/exposure/key/主役で比較し、R19を最初の明示作業基準/暫定bestに選んだ。高塀・前障子・夜空の最終R20は相対的な全景改善として採用する。`qa/adoption-review.md`（SHA `784b1b1e0b5550f1c9f490c8a3601c39bf57b9076a819fcbc9a9864f12d28868`）は最終actual source4像とrelease8/strict3pairs/GPUを独立確認し、暫定R20best・premium未達を支持。機能QAはレビュー保存後に完了した別証跡 `qa/resilience/results.json` と `qa/verification-summary.json` で確認し、レビュー本文を後から変更していない。

新しい別状態 `depth-balance-study-state.json` と `provisional-best-depth-balance-state.json` を追加し、歴史best/18旧状態を上書きしない。code/五写真/比較/独立レビュー/検証/manifestはこのrunに保存。共有既存assetはread-onlyで参照し、dist単独のportable exportではない。サーバーはbest5208と現候補5214だけ、Chrome検証は終了。旧プロジェクトへのアクセス/変更なし。workerのGit書込み/push/PR/merge/外部公開/購入/automationは0。

優先20MiB容量は自分のrunだけでなく共有Chromeの観測正増分peak、cacheの正増分、staging、三調整文書、新状態を計上する。自分の計測JSONの空白だけを削減し、全parsed値と実写真は保存した。旧成果・unknown cache削除、負のeviction creditは0。最終容量は `qa/capacity-final.json` と `finish.json`。100MiB上限/free2GiBとは分ける。既報の外部削除26/歴史manifest4欠落は残り、歴史全体の完全保護は不合格。存在する保護成果/18旧状態/直前R19全125file/6symlinkは一致。Library公式helperの既報TLS阻害へ再試行0、Library ID0。

完成目標は残る：古木のnative造形、枝の先細り・根張り・非対称の空隙、遠冠/近い低木の自然な密度、均質な砂利、スマホの冠と障子の競合、GPU tail/cold速度。テスト成功や変更量を完成度とは扱わない。
