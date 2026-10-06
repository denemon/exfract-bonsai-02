# 工程22：R20の景色を保つ描画基準を選定

通常 http://127.0.0.1:5214/ は最初にR20へ復元し、PC・390px・320pxを実確認した。未採用R21は /compare/r21/ へ隔離。全ての採用ゲート後、R20の物理形状・材質・カメラ・全8光源を保持したR22描画版を暫定bestに選定した。R20原版は /compare/r20/、選定版は /compare/r22/。現物R20/R21/旧21状態は変更していない。サイトの可視文字0。高塀2.321m、右前障子、夜空、灰茶色の木、散在小石なしを保持。

72の不透明低詳細葉groupを同geometry/material/worldごと12drawへ表示統合した。2800 instanceのFloat32行列をbit exactly連結し、native93meshは描画後に復元。高詳細・混在LOD・instanceColor・非identity親では元描画へ戻す。native geometry/material/UVを削減していない。木全包絡と高詳細葉包絡に対して距離または角度から寄与0を証明した5有限光だけ、主役の色パスから除外。背景には全8光源、影は完全sceneから生成。shadow更新時は初回等のみ完全色パスを一度余分に実行し、続く背景色パスで消去する。完全影を捨てる手法ではない。

R21 offsetは390枝間改善があるが320前障子/広幅境界の退行があり不採用を保持。R20位置と前障子を保って奥の小障子だけ外すpartialも、390の枝間改善がほぼなく不採用。R20形状を一切変えない性能派生を採った。

途中で直接shadowMap.renderがrenderer内部状態外で例外になり、完全renderによるshadow更新へ修正。さらに独立目視で、R21 micro=masked/gravel=variedのdefaultをR20派生へ残したため奥樹冠が暗くなる退行を発見した。qa/superseded-acceptance.jsonに旧写真・旧final GPU/idle/buildを採用対象外と明記し、全生データと旧unique JS/indexを保持。両defaultを除去。geometry/光源一致だけを見た目の一致として扱った初期判断を撤回した。

補正R22 render=original対R20既存buildの全RGBA SHAは、同じPC Retina2304x1440/390x844/320x568/320x844/1920x800の5幅全bit一致。材質・shader・textureの完成画素まで一致を確認した。その同じ景色をbothへ変えるとPC50画素/39011/3201/tall12/wide11のみ差が残る（max21/22/6/20/15、各182k〜3.3M画素中）。original repeat差0。optimized renderの完全画素一致は主張しない。高詳細木native93mesh/葉4,670,400triangleではbatch無効・allRGBA差0。補正5写真を独立実見し、肉眼退行なしという支持。独立レビュー時はpaired/idle/機能未完了であり、それらは後のworker検証として分けた。

| 同Mac Chrome viewport | R20 GPU median / p95 ms | 補正R22 GPU median / p95 ms | p95改善 |
| --- | --- | --- | --- |
| retina | 15.299999 / 15.523916 | 12.183000 / 12.637250 | 18.59% |
| mobile-390 | 10.874041 / 15.276499 | 9.276374 / 12.337916 | 19.24% |
| mobile-320 | 11.131896 / 15.328958 | 9.073708 / 12.406291 | 19.07% |

各条件ABBA、30warmup、61measure先頭2除外、各variant59x2=118 raw点、中央値中央2点平均、p95 nearest rank。RetinaはDPR2入力/cap1.6/実2304x1440、MSAA4。PCtri1,810,918を保持、calls125→65（390 120→60、320 121→61、同tri）。CPU submit中央値はRetina3.0→3.7ms、390 2.7→4.3、320 4.2→5.0に増加。GPU値はend-to-end FPSではない。

2400msidle後の単発render14点/variantはR20中央値33.453583/p9540.117916→R22 32.677333/35.556541ms。small sample、熱/クロックを測れていない。steady12.64msを常時の操作応答とは扱わない。旧工程21のshort warmup p9521.186250→24.089124ms退行は保存し、今回のwarmup/時期差だけで原因解決したとは主張しない。同時期のR20/R21/要素診断と最終同条件の改善を分離した。

build合計3回。1回目は素材defaultを取り残した不採用build、2回目は見た目修正、3回目は明示採用記録がある時だけTOPを選ぶ最終routing。最終renderer bundleは2/3回目同一。共有assetsの複製なし、旧unique JS/index保存。candidateと選定TOPで各12機能ケース成功（各5WebGL不可の想定warning以外unexpected0）。完成5still、reduced motion/input停止、idle RAFなし、限定pointer/wheel、実context loss/復帰を確認。TOPのPC390320実3D画像も保存し、R20/R21比較URL分離を再確認。HTML4/画像15/JS CSS2、配信21byte SHA照合成功。

選定TOPのcold HTTP cache、120ms latency/250KiB/s、script保留なし: 最初のpaint 320.0ms、完成still 1630.3ms、navigation→3D 11884.9ms。初回3D約11.88秒は未達。Mac Chrome154 ANGLE Metal M1Proの実engine、viewport emulation。物理iPhone/Android、Safari、長時間熱負荷、実行model metadataは未検証。

旧21状態/R20166files3links/R21149files3links/既存critical source・productionをSHA検証。GitHEAD2347a151a05015f0049e4b0fd8f01545ac9afed3は不変、tracked変更は3coordinatorのみ。既知の外部PR7削除26path/歴史manifest4missingは保存したままなのでhistorical completeness=false。旧projectアクセス・旧成果削除・Git write・公開・購入・automation・Library retry0。Libraryは既知helper TLS阻害と再試行禁止、現在cloud skillsも未提供、画像ID0。確認画像はMacに保存した。

最終容量はqa/capacity-final.jsonを正とする。run全量、共通profile正の観測peak、cache正の観測growth、own staging/pycache、全3coordinator、2新状態を20MiB以内で計上。負eviction credit0。source/native参照はread-only再利用。最終manifest/receiptに全保存対象を固定。

完成品質は不合格。固定S・根張り・枝径/断面・近接葉・植栽/苔砂利・スマホ枝間は残る。今回は背景とrenderの基準を揃えた工程。次はNEXT_NATIVE_WOOD.mdの一案native造形→単色選定→SHA凍結→材質検証へ戻る。shaderで形状不合格を隠さない。
