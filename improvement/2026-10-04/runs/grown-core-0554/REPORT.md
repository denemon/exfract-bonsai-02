# Stage29：大形固定と材質比較、TOP未採用

正式先 /Users/kazuki.tanaka/dev0/exfract-bonsai-02。TOP http://127.0.0.1:5214/ はR27 program-state-0426。R29はgrown-v02を大形の材質研究用固定形として保存し、既存normal-v4を暫定木肌基準に保存。完成古木・完成材質・全景完成・TOP採用はfalse。比較URL http://127.0.0.1:5214/compare/r29/?candidate=grown-v02&wood-finish=normal 。default比較はgray。研究用fallbackはR27完成静止画のread-only aliasで新形と未同期。

先に実添付302x404と公式盆栽美術館写真をpixel確認し、通常距離の非一様な幹芯、屈曲と枝母接続を計画。S輪郭自体は参照に存在し、長い均一前面/薄い肩/横断lipが問題。R25実連続surfaceを5394vへapplyし、荷重部・短い圧縮と反対側支持・裏側上行芯・枝母支持を有限C2 XYZ sculptで結合。noise/radius列/overlay/一周ring/溝追加を採用理由にしない。最大移動32.062mm。root z<=.50、上枝先、terminal、全2800sprays、UV/color/index保護。V01閉じた丸い圧痕は実gray画像レビューで重大形状欠点と判断。V02はその部分だけをactualsurface前→側→裏へ短く開いたpathへ置換し、残る芯と支持を保持。第三形状0。

V02 ordinarygray夜PC1440x900/390x844/320x568、neutral同3幅/bonsai/左右/wood10実像。camera/alllight/投影bounds/leafworld一致、before10画像はR28からbyteコピーせず読み取り参照、actual旧model属性/worldが旧beforeと一致。R28の横断lip/折れた帯の再発なし、局所厚みと不等な屈曲の改善、支持と樹冠空隙/鉢/台石/庭の関係維持。独立reviewは大形固定→材質研究へ進む判定。上側滑面/小枝肩step/単純なroot先は残り、細部を理由に大形全再設計をしない。これは名品古木の完成認定ではない。

native5394v/5392faces/10784tri、volume.092209m³、boundary/nonmanifold/nonadjacentintersection0。freshBlender reopenでnative position/index/UV/color、strictprotected3134、root/terminalをexact照合。初回unmodified照合の失敗はMathutils近似比較/微小falloffで9頂点最大7.45e-9m、exactlist記録を1489変更へ修正。旧失敗logを保持。V02結果を誤って空のV01結果名へ書いた点は、新ファイルをproper-v02名へrenameしpath修正JSON保存。形改善と混同しない。geometry-freeze.jsonが7実ファイルSHAを固定し、その後native改変0。native内部のpre-gate表示ではなく外部freeze証明がauthoritative。

固定形でbase/color/roughness/normalを独立増分比較。夜PC4、夜wood4、中立wood4、normal中立PC/夜中立3903205、計17実Chrome画像。全native属性/index/world、leafworld、camera/light/projection一致。既存R27/R25灰茶wood shader/無料汎用Cedar001を再利用し新shader0。粗さ.90..995/metal0、normal.12..17、fissureheight<=.8mm、geometry大起伏32mmを分離。色の寄与が最大、rough/normal全景差は小さい。乾いた反射と控えめな近接陰影を保持、濡れた艶/発光/強い溝で主幹を隠していない。独立reviewもnormal段階を暫定基準として保存に賛成。真柏固有の名品木肌完成は未達、中立下幹/内側の読みやすさも余地。17像と7freezeSHA一致はqa/material-comparison-proof.json、評価はqa/independent-material-review.json。

finalbuild成功（qa/build-final-study.log）、HTTP decoded12一致：TOP/R27HTMLbundle/5完成stills/R25compact/新V01V02。R27renderer src/render-partition.js exact。実3幅night/neutralで樹冠→鉢→台石uncut、text0/overflow0/reduced実設定。現在のperformance/fullfunctional/fallback/TOPactualbrowser再試験/新完成5stills同期は未実施。TOPactual3幅/WebGL不可は前R28の確認を参照し、R29の確認と偽らない。R27既存CPU中央値3.5/2.4/2.3ms、program再選択26/25/26→0のsource保護だけではR29速度証明にならない。idleGPU36.211ms/coldfirst3D11.987s、390GPU+.544msは未達のまま。実phone/Safari/thermal/Sol-xhigh実metadata未検証。

次の全景品質は近景低木・苔岸・埋石・砂利の同じ縮尺の自然な接続。低木の反復房/硬い葉片、苔の一様なmat、古木と背景全体の品格は残る。NEXT_WHOLE_QUALITY.mdで固定大形と暫定木肌を基準に進め、細筋追加量や閉mesh/test数を美的完成としない。

旧31statesと既存各runSHA維持、新grown-core-study-state.jsonだけ追加で32states。HEAD2347a151a05015f0049e4b0fd8f01545ac9afed3不変、許可3coors以外tracked変更0。历史外部PR7削除26paths/4manifestentry完全性false、今回復元/削除0。旧project access/Gitwrite/push/PR/merge/公開/購入/automation/olddelete0。Library親指定retry0/IDs0。Chrome6910 cleanexit0/profileguard解除、writer解除。単一5214previewPID12216/session81232。期限10/10 23JST。20MiBのactualallocated、profile観測peak正増加、staging/coors/state全計上はqa/capacity-final.json。連続peakは未測定。

native models/grown-v02-editable.blend、compact models/hero-grown-v02.glb.gz、freeze/素材計画/検証JSON/全37JPG/rawfailuresを保存。最終normal夜画像はqa/material-night-pc-normal/normal-pc.jpg、qa/material-night-390-normal/normal-390.jpg、qa/material-night-320-normal/normal-320.jpg。Library添付ID0。
