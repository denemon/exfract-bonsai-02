Stage34 organic-ensemble-1017は幹枝肩と庭植栽の実改修を行い、視覚ゲートを通したが性能資格を満たさず保留。TOPはR31 growth-garden-0729/5214 PID20598を保持。比較試案は http://127.0.0.1:5215/compare/r34/ 、PID61480/session69250。完成した高級庭の認定はfalse。

開始2026-10-06T10:18:06.162914+09:00、終了2026-10-06T10:51:44.403013+09:00、33.64分。最大二領域: 広い滑面/枝肩の量感と、近中遠植栽の反復・支持内占有。高塀/右前障子/夜空/乾いた灰茶木/無文字/散在小石0、同camera/8物理光/縮尺を保持。参考302×404は先行実ピクセル参照を継承。新Library取得・retryなし。

六つの有限XYZ成長面をnative閉面へ直接彫刻。初回枝肩非隣接交差1を保存前に修正し、ログ保持。最終1066頂点変化、native最大56.306956mm/world37.162591mm、3274mask保護。5394verts/5392faces/10784tri、volume0.096048962599、boundary/nonmanifold/非隣接交差0。根/末枝/属性UV/color/index/全boundsと葉配置を保持、freshBlender再読込一致。単色14枚の同camera/light/projection/nativeLeafWorld7対、独立形採否固定後、素材12枚の同形6対を分離。v5は細かな乾いた肌の僅かな改善で、形改善の根拠にはしない。7nativeSHAはqa/fixed-living-shape-v01.json。

庭は近景2033thinclosedleaf/369shoot/166forkを維持し、非対称な曲率と向き・実支持を調整。前根を25cm内側/16cm奥へ移し、実地面への7mm埋まりをraycast確認。遠景3樹/18冠regionを維持、支枝内側へ占有を寄せて実葉26964へ(旧31080)減。初回v01の厚い豆/折れ葉感は棄却し、葉表裏の実間隔0.50〜0.82mmへ一回修正。木形living-v01固定の庭v02正規8枚と中立全庭で採否を評価。BLUE高さ全一致、236599保護pixel完全一致、312RGpixelのみ変更。二埋石、鉢足、建築を保持。

最終PC390320+DPR2の6実Chrome画像をrootと独立reviewerが実見。PC総合改善、390/320非退行。DPR2はcanvascap1.6。樹冠・鉢・土台の投影とR31 camera/light3幅一致。広い滑面と三角肩、折れ葉反復、390左植栽部分像、苔面均一さは残る。写真/scan-grade/数千万円級の完成とは主張しない。

最終build53modules成功、最終full5WebPとinline5同期、HTTPHTML/modelgzip/still5全body一致。freshChrome61609: loading/noWebGL5幅/idleframe0/boundedinput+reduced3幅/contextlossrestore/noDecompressionStreamの11、影authority/灯移動/invalidnative/instancefallbackの実PNGparity6成功。R27renderer/foliagecode完全一致。実phone/Safari/高LOD/熱・frequency未検証。Mac Chrome154/ANGLEMetalのviewportemulation。

有限component14はコード旗で幹/材質/近景/遠景/同内容controlを分離、390activeCPUmedian2.05→3.60ms/GPU10.311→9.909ms。順序間変動が大きく因果確定なし。R33PC CPU1.70→2.60とR32/R33失敗は未解決記録を保持。最終資格は一回だけ60cohort、rawを各cohort直後wx/fsync/hardlink排他保存。最初からlosslessgzip、old14/診断/中断42をpoolせず、既存9tol変更0。active236、idle28、cold2/variant/width。pool26/27、idle順序別19/24。CPUはrender同期submit時間で、連続idleCPU使用率やpresentedframeではない。GPUは実EXT query、温度/frequencyunsupported、userChrome/background負荷未制御、coldはcacheoff120ms256000Bpsでsystemcoldではない。

| 幅 | 版 | activeCPU med/p95 ms | activeGPU med/p95 ms | idleCPU med/p95 ms | idleGPU med/p95 ms | first3D median ms | completedstill median ms |
|---|---|---|---|---|---|---|---|
| pc | R31 | 3.500/5.100 | 11.228/17.896 | 3.450/6.200 | 24.528/29.994 | 12075.2 | 2026.0 |
| pc | R34 | 2.450/4.800 | 11.162/19.060 | 3.100/6.300 | 23.291/28.755 | 12263.8 | 2005.3 |
| mobile-390 | R31 | 2.000/4.500 | 10.135/13.772 | 3.250/5.800 | 17.712/22.561 | 11473.1 | 1444.4 |
| mobile-390 | R34 | 1.900/4.700 | 10.073/13.583 | 4.650/6.200 | 19.777/22.354 | 11700.2 | 1456.7 |
| mobile-320 | R31 | 2.700/5.000 | 9.732/13.374 | 3.650/5.400 | 17.225/22.076 | 11392.9 | 1317.9 |
| mobile-320 | R34 | 2.950/4.700 | 9.516/12.991 | 2.800/5.800 | 19.001/22.788 | 11589.7 | 1330.9 |

未達条件:
- pool mobile-390 CPU_idle_submit_ms median: 3.250000→4.650000、Δ1.400000、許容0.750000
- ABBA pc GPU_idle_elapsed_ms p95: 26.415999→31.710874、Δ5.294875、許容3.962400
- ABBA pc CPU_idle_submit_ms median: 3.100000→4.350000、Δ1.250000、許容0.750000
- ABBA mobile-390 CPU_idle_submit_ms median: 2.950000→5.000000、Δ2.050000、許容0.750000
- ABBA mobile-390 GPU_idle_elapsed_ms median: 15.795833→20.455354、Δ4.659521、許容3.159167
- ABBA mobile-320 GPU_idle_elapsed_ms median: 16.339687→19.713145、Δ3.373458、許容3.267937

予算は本工程中に一時超過。qa/capacity-transcode-record.jsonの観測charge 21483520B、上限超過512000B。共有profile増分と最終DPR出力の見積り不足であり、全期間20MiB合格はfalse。旧sealed成果物には触れず、本工程新生成の庭v01results一件のみgzipへ可逆移行、元全バイトSHA完全復元を検証、numericraw破棄0。最終charge/実freeはcapacity-final.jsonを参照。旧状態37/旧sealedsource/HEAD保護、Gitwrite/push/PR/merge/公開/購入/自動化/旧projectアクセス/Libraryretry0。LibraryIDs=[]。
