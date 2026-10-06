# Stage30：近景の尺度と接続、TOPはR27保持

正式先 /Users/kazuki.tanaka/dev0/exfract-bonsai-02。TOP http://127.0.0.1:5214/ はR27 program-state-0426。候補 http://127.0.0.1:5214/compare/r30/ はgrown-v02/normal/near-shore-v02。同じ形・光・cameraで前庭だけのbaseline比較は ?garden-finish=baseline。大形native/鉢/2800spraysの再作成0。前の7freeze SHAとR27 render-partition SHAを維持。

事前の独立案で、近景低木から苔岸・実二石・砂利へ続く一つの地形を目標に決定。旧低木の厚い約3–4mm葉片/規則7節を、0.3–0.6mmの非対称に曲がる閉じた4葉型、22–40mm長/不等2–5節の実枝支持に変更。初回はwindingの向きとgeometry color属性なしvertexColors指定で黒い葉を作った。実画像/閉体積診断で発見しoutward/indexとinstanceColor専用設定へ修正、raw失敗4像を保持。別光追加0。4tap陰影をcloneにも明示適用。

V01正しい10実像で葉の尺度は改善したが、最後の節が枝長.60未満195/369、裸先中央値35.9mmで黒い扇が先に読めるため全景gate不合格。一回のV02構造修正でouter節を.90–.96へ、選んだ実小枝から20–35mm前後分岐166を支持し2–4葉群を置いた。2033leaf/32528tri、裸先最大16.29mm。親軸と4葉型を固定、浮いた葉雲/均一球/板/散在小石追加0。第三修正0。

近地形の細格子をx=-1から-.62へ延伸（65952tri）。同じ512 RGBA soil/moss fieldを局所だけ修正し、既存起伏と岸の厚み/normalを控え、約83mmの岸移行と実3根位置の有限密度差/土摩耗を連続fieldに組み込む。苔の点や盛り上がりを装飾として増やさない。flatseat/後景/外域236599pixels SHA一致。二石の実triangle補間による埋まり: boulder01 buried7160/above7100/contact-crossing1054、rock09 buried2674/above3954/crossing760。fieldと実mesh差最大2.346/2.261mmでゼロでなく、全接地指標の一律改善とは主張しない。石transform/geometry、鉢4feet↔土台接触は保持。4leafprototype閉体積正/非二面edge0、散在小石0。高塀・右前障子・建築開口/厚み・夜空・照明は同一source。

V02通常夜PC1440x900/390x844/320x568、同3幅中立、夜盆栽/幹寄り/近庭9像。6全景の全native木attribute/index/world、2800leafworld、actualcamera/light/hero/projectionがR29normal beforeとexact一致。全3幅樹冠から鉢/台石uncut、text0/overflow0。独立review: PCは硬い葉反復が減って尺度感前進。390320は小改善/概ね同等、主役/庭/障子退行なし。ただし全3幅で明確優越false。薄葉と実末端支持、根土境界は局所候補合格。広い苔の滑らかなmat、低木の扇骨格、後景冠、名品古木としての造形と全景品格は未達。高級庭全体完成false/TOP採用false。test数やmesh閉体積を美的完成と混同しない。

保存候補として5default構図pc/mobile390/mobile320/mobiletall/wideの完成WebPを空の自己所有directoryへ新規保存し、inline5画像も同じ景色へ同期。読み込みで実compact要求hold→完成画、WebGL不可5構図、3幅idle無RAF/控えた操作範囲/reduced、実context loss/restore、DecompressionStream無しHTTP gzip、basic11case成功。Mac Chrome154/M1Pro/ANGLEMetalのdesktop emulation。finalbuild成功。TOP actualPC390320のJPEGは保護R27完成JPEGとbyte一致、TOP WebGL不可3成功。HTTP decoded18identity一致。詳細 qa/integration-*、qa/special-top-final、qa/served-final-identity.json。独立候補のfallback同期は採用を意味しない。

R27CPU対策sourceとactualstable partition/72→12batch/finite light envelope更新を確認。現在のqualified同条件CPU/GPU pair・idle・cold suiteは未実施。親とNEXT指示の全3幅明確優越gateを満たさず、採用performanceの実行/採用を保留した。R27の既存CPU中央値3.5/2.4/2.3ms、idleGPU36.211ms/coldfirst3D11.987s/390GPU+.544msは以前の参考値でR30速度保証ではない。idle/cold gap解決false。現在highLOD、実phone/Safari/熱負荷/要求model実metadataも未検証。

最初writer/Git/関連AGENTS/空き31.641GB/旧32states/R29sealを確認。final全既存保護SHA監査、旧32states維持、新garden-scale-study-state.jsonだけで33states。HEAD2347a151a05015f0049e4b0fd8f01545ac9afed3固定、許可3coorsのみtracked変更。歴史外部PR7削除26paths/4manifestentry完全性false、復元/olddelete0。旧project/他project access/Gitwrite/push/PR/merge/外部公開/購入/automation0。Library親指定retry0/IDs0。Terminal大input auto-review拒否はjob_ref専用の短い入力へ解決、後続旧QA overwrite防止assertionは新規audit名で解決。HTTP試験で誤r27modelURL404は実mainのr25URLへ修正、actualTOP正常。geometry変更ではなく検証修正記録を保持。

Chrome41320exit0/profileguard解除、writer解除。単一5214previewPID28897/session14655継続。23JPG/rawfailures、5完成WebP、source/比較/接地/freeze/最終QAを保存。正増加20MiB予算はprofile観測peak・sharedcache・workspace staging・coors/newstateを含めqa/capacity-final.json、manifest/receiptでseal。連続peakは未測定。deadline10/10 23JST。
