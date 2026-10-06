# Stage27：景色を保つCPU改善版を暫定選定

正式先 /Users/kazuki.tanaka/dev0/exfract-bonsai-02。ローカル確認：http://127.0.0.1:5214/ 、比較：http://127.0.0.1:5214/compare/r27/ 。R25の形/root-v02・木normal-v4・original葉・夜空/高塀/右前障子を保つ描画改善だけ。R26 age-v01/botanical-v1は統合していない。新しい美的改善や高級箱庭の完成を主張せず、全目標完成false。

最初にscene/camera/light/materialを固定する方針を DESIGN.md に記録。実添付pixelは銀白のねじれ/生きた幹筋/非対称に横に広がる葉群と枝間空隙の参考として確認済み。後続のgraybrown夜景指定を維持。今回のgeometry・物理素材・カメラ・光の縮尺変更0。完全図の造形が課題なので、CPU改善でそれを完成扱いしない。

Three0.185.1 installed official sourceを照合。旧同Sceneの8→3ライト切替でWebGLLights versionが更新され、WebGLRendererがmaterialのprogram設定を毎frame選び直していた。SceneをWeakMapで区別する公開render stateの仕組みに合わせ、背景/主役それぞれのpublic Sceneを持たせ、原灯8個から作った色pass専用の参照灯BG8/Hero3を使う。元physical Sceneがnativegeometryを一度だけ所有し、元8灯と全casterで影を更新。参照灯はsource.color/target/shadow/mapを共有、worldとintensity/cutoff/cone/layersを追従し、影mapを追加しない。内部APIやThree本体patch0。色pass中だけshadow autoUpdateを止めfinallyで戻す。固定native world/geometry/position-version/leafinstance-version/count/envelopeと除外灯transform/cutoff/coneを監視、証明無効時はbatchも解除し元の全native葉/全8灯へ戻る。任意leafgeometryを宣言済み包絡外へ変形する一般保証はない。

実Mac Chrome154/M1Pro/ANGLE Metalで元124meshのposition/normal/index/world/instance/visibility/materialtype SHA、元8物理灯、5GPU影map SHAが一致。新11参照灯はsource identity/worldが一致。default5完成WebPとPC390/320JPEGはR25とbyte一致。旧both対newstableはinitialPNG0pixel差、high葉の実ロード5全景+幹/葉近接7PNGも完全一致。dynamic6PNGはstatic・autoUpdate=true・主灯移動・除外灯移動・woodlocal移動・instanceVersion変更の追従/保守的復帰を確認。初回のoriginal72群対oldbatch12群は30/1,296,000pixel差（最大channel26、mean.0001173）でstrictPNG比較失敗し、生証跡3PNGとfailureを保存。新方式対旧bothの差ではなく、旧batch shadow同深度等の限界。v02でもfallback時batchを保持したため失敗、v03で元native葉に復帰して6件合格。失敗を削除していない。

最終v03＋最終still buildで、同pose/DPR2 cap1.6/scene/材質/LOD、ABBA+BAAB4cohort/版/幅、30warm61GPUqueryfirst2除外=236sample/版/幅。実JS submit時間とGPUtimerを分けた。先行v02 perf-final系を最終集計へ混ぜていない。

|幅|CPU median R25→R27(ms)|CPU p95(ms)|GPU p95(ms)|
|---|---|---|---|
|PC|5.0→3.5|6.5→4.9|13.639→13.522|
|390|3.75→2.4|6.3→5.0|13.487→14.031|
|320|4.0→2.3|6.0→5.0|13.139→12.450|

最終同page both/stable/stable/bothでkeycounter26/25/26→0、program数増加なし、draw65/60/61・triangles1,803,162/1,583,482/1,595,898同数。独立した同page未instrumentGPUtimingでもCPUが下がる。CPU改善は同Mac条件に限る根拠を得たが、390GPU p95+.544ms、先行cohort順序揺れ/同pageGPU増加もraw保存。GPU全面改善/厳密非退行/60fps/実機mobile性能を主張しない。歴史的+0.85ms全量の原因を確定した意味でもない。

idleは2400ms待機14sample/版でCPUmedian4.95→2.5ms、GPU p9535.973→36.211msで未達。coldはcacheoff120ms250KiB/s単回、FCP300→296ms、完成still2200.3→2089.5ms、first3D12025.4→11987.4ms、transfer2,654,119→2,656,315B/22requests。約12秒の3Dロードと約36msのidleGPUは未解決。単回の小差からロード改善は断定しない。

独立reviewはCPU限定の暫定更新に賛成。造形の最大課題は広い滑面と均質なSの主幹。R26 gray全景/neutral/左右、木base/color/roughness/normal、葉original/botanical夜景/neutralを分けて評価。葉艶/小枝肩は小改善でも支配形は残り、R27へ小変更を累積していない。次は NEXT_COHERENT_MAIN_CORE.md の主幹一体の量塊を一件で直す。近接枝接続/根裾、同型spray反復、背景植栽/苔の自然さ、全景の名品に似合う品格も未達。

4build成功。own5完成full/inline/versionedURL同期。actual loading1/WebGL不可5/PC390320idle入力reduced3/contextlossrestore1/DecompressionStream不可HTTPgzip1=11pass。TOP actual3D3幅JPEGはownとR25完成像一致、TOP noWebGL3幅の完成像も確認。runnable shader/可視文字0/overflow0/外部font・page外部network0。decodedHTTP26identity一致。実phone/Safari/長時間熱/連続diskpeak/要求gpt-6.1-sol xhigh実metadataは未検証。

QA Chrome59010 exit0/profileguard除去、単一5214previewPID58952/session16449を保持。旧28statesとR25/R26manifest/全現存旧成果SHA維持。外部の歴史的PR7削除26paths/4manifestentryは未復元・完全性false。HEAD 2347a151a05015f0049e4b0fd8f01545ac9afed3 unchanged、tracked変更は許可された3coorsのみ。Gitwrite/push/PR/merge/公開/購入/automation/旧project access/旧delete0。Libraryは既知TLS阻害への親指定retry0、imageIDs0。

成果：candidate/src/render-partition.js、qa/special-stills/{pc,mobile-390,mobile-320}.jpg、qa/performance-final-summary.json、qa/final-native-light-shadow-image-proof.json、qa/high-leaf-and-near-PNG-proof.json、qa/dynamic-public-scene-proof-v03.json、delivery-manifest.json/qa/final-receipt.json。容量は qa/capacity-final.json に実allocated/正増加/peak観測/共有再利用を記録。
