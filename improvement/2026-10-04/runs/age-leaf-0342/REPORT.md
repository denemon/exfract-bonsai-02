# Stage26 局所古木・葉・CPU診断：比較用保存、TOPはR25継続

正式作業先 /Users/kazuki.tanaka/dev0/exfract-bonsai-02。http://127.0.0.1:5214/ は選定R25 root-v02/normal-v4を保持。新候補は http://127.0.0.1:5214/compare/r26/ 。外部公開0。

参考の添付実pixelを確認。主幹と枝のねじれ、非対称で横に広がる葉群と枝間の空隙を観察し、継続指示の灰茶幹/夜景/高塀/右前障子を維持した。R25 actual nativeから32controlだけ変更。屈曲の不均一な縦稜線と隣の浅凹面、first-left/low-rightの局所枝肩、rightsoil-lineを短く調整。全control322/face354、core10784tri、boundary/nonmanifold/nonadjacent selfintersection0、根cap実soil埋まりを確認。twig/2800sprayの配置を維持。閉meshは美的合格を示さず、twig接合の全体weldを証明したものでもない。

grayの夜景/neutral通常PC390320、幹寄り/左右を実MacChromeで確認。独立reviewは屈曲の面変化と小枝元/根肩改善を認め、材質へ固定してよいと判断。保存nativeをfresh Blenderで再開き全positions/normals/faces/角UV/色一致、form-freeze記録後だけ色→粗さ→normalを独立比較。木材質はR25の乾いたgraybrown/茶褐色normal-v4を維持し、全木属性/index/worldhashは13比較で共通。古木の完成を材質強調で代替したと扱わない。

葉は閉じたscale形・法線・全2800sprayworld/matrixを保護。original .78roughnessと、botanical .86roughness/.055弱backscatter/frontenergy.945を夜景全景3幅とneutral寄りで比較。実shadow/減衰後の物理直接光だけ、emissive0/alpha1。細かい艶と裏向き小葉が少し改善し、内部陰影/空隙を維持するとの独立評価。shape/物理scene/light/cameraを変えず、candidate内でbotanicalを選択。R25その他nativebufferはlossless置換で保護、候補modelgzip660,906B（R25 661,394B）、triangle/drawcounts同数。

CPU対策は既存72葉LOD状態の厳密cacheとbatch毎frameUUID/matrix文字列生成の再利用。camera/projection/height/distance/forcedLOD/mesh及びancestor可視性/world/instanceVersion/envelope10invalidationsが従来計算と一致。MacPC390320でcache有無のactualJPEGがbyte完全一致。hotloop1000回×8pairedcohortではLOD中央値.00465→.00270ms/回と小さく、全体CPU改善を主張しない。プロフィールは別診断として160GPUtimerframes/250us sampling、rawnodesとexactfinalbundle位置を保存。getParameters/getProgram/cacheKey等が上位。ライト数を同Sceneで毎pass変えるためlight-state versionが変化し、materialprogram再選択が毎frame26回。both→batch→bothの実counter26→0→26（drawcalls65/triangles1,803,162同じ）が確認できた。これは避けられるCPU処理の一因で、前工程CPU+0.85ms全体の因果確定ではない。単一passへ変更して速い数字を採用する対策は今回行わず、GPU削減を維持する安定light-state方式を次工程へ。

最終同条件ABBA/各版118sample/幅、DPR1.6、同pose/space/light。CPUmedian PC4.10→4.55ms、3904.70→4.80ms、3203.85→3.80ms。GPUp95 PC12.928→13.309ms、39013.625→13.105ms、32013.002→13.166ms。旧cohortCPU中央値PC3.6/5.0、新4.9/4.0で順序の揺れが効果量より大きい。強い回帰断定も速度改善/CPU非退行/60fps認定もしない。idle2400ms14点/版のGPUp9534.650→35.066ms、CPUmedian4.40→4.40ms。cacheoff120ms250KiB/s単回cold：FCP296→308ms、completedstill2145.3→2116.4ms、3D11981.9→11955.2ms、page資産2,654,119→2,653,554B/22requests。cold12秒/idle35msは未解決。

見た目改善は小さく、PC負荷の改善証拠と高級全景の完成が不足するためR26はTOP未採用。R25保護を続ける。広い滑面、近接の匙状折返し/枝接続/根裾、同型spray反復、背景植栽/苔の自然さ、名品盆栽が自然に似合う高級空間は未達。全目標完成false。機能成功とは分ける。

最終sourcebuild5回成功、独立camera5完成WebP+同景色inline+versionedURLs。loading1/WebGL不可5/PC390320idle入力reduced3/actualcontextlossrestore1/DecompressionStream不可HTTPgzip1の計11pass。可視文字/overflow/外部font/page外部network0、runnable shader実確認。cacheframe3幅byte一致、TOP R25実PC390320は元完成JPEGとbyte一致、decodedHTTP21資産一致。QA初回cache診断が撮影jobと重なったため生recordを残し、job終了後単独で10項目を再検証し成功。最終Chrome32767 cleanexit0/profileguard除去。実phone/Safari/長時間熱/連続diskpeak/要求Sol-xhigh実modelmetadataは未検証。

成果：candidate/src/、models/age-v01-editable.blend、hero-age-v01.glb.gz、qa/special-stills/{pc,mobile-390,mobile-320}.jpg、qa/performance-final-summary.json。previewPID32648/session58340（R26configがTOP R25とcompare R26を分離）、historical5208無変更。旧27states/R25manifest全177filesと全現存旧成果SHAを保持。外部PR7の歴史的26削除path/4manifestentryは未復元・完全性false。HEAD2347a151a05015f0049e4b0fd8f01545ac9afed3 unchanged、Gitwrite/push/PR/merge/公開/購入/automation/旧project access/旧delete0。Library TLS既知阻害は親指示によりretry0/imageID0。

次は NEXT_PROGRAM_STATE_AND_LOCAL_FORM.md 。
