# Stage25 根座・接続・木目flow：暫定ローカル反映

正式作業先 /Users/kazuki.tanaka/dev0/exfract-bonsai-02。確認先 http://127.0.0.1:5214/ は新R25。R22は /compare/r22/、R24は /compare/r24/ に原byteで残る。R25比較は /compare/r25/?candidate=root-v02&wood-finish=normal 。外部公開0。

R24上部の改善した量塊を保持し、根元の二柱を局所的に一つの支持体積へ戻した。read-only reviewで薄い裾を指摘後、v02は土際14controlだけを変え、左根肩に22mmの上面厚と約20mmの前後厚、右根に短さ/前方向を与えた。中央を再び割らず、upper40..113とnative twigを維持。実soil埋cap、closedcore/nonmanifold/selfintersection0とfresh native reopen全positions/normals/faces/UV/color一致。これらは構造証拠で美的完成証明ではない。

fieldを実controlから再計算し、主幹を近い横root軸へ誤配分する問題と角UVの横補間を修正。U周期1、V実長を分離しcornerunwrap。checker/色だけで右根横縞が弱まり、幹枝の流れが読める。49native/render点でUV2のV反転、材径式1-runtimeUV2.y整合を実測（誤差最大6.10e-5）。木金属度0、乾いた灰茶/茶褐色、roughness.90..995、sRGB色/Data他map、色→粗さ→弱normalを独立に比較。34本の不均一・有限V2.8m割れatlasと.2.. .8mmworld浅bump、fine normal.12.. .17。形nativeとcanonical19材質/compactケースの全wood属性、2800nativeleaf worldmatrix/instancingは一致。

余分な旧woodをdecodeする二重modelロードを、2wood Draco bufferだけのlossless置換へ統合。その他のnative nodes/meshes/accessors/bufferViewsをbyte保護。compressedモデル781,479→661,394byte。scene全転送は割れ/高品質staticを含み2.610→2.654MBの単回測定で、速度改善としない。

5完成WebPを実MacChromeの個別defaultcameraで保存し5inlineも同景色へ同期、versionedURLで旧trial画像cacheを回避。Mac60比較/性能ケース、5完成static構図、機能11項目（実loading・WebGL不可5構図・3幅入力/idle/reduced・context実復旧・DecompressionStream不可）、冷間2、TOP6、UV49点を記録。TOP3幅JPEGは反映前完成像とbyte一致。可視文字/overflow/外部font/network0。実PC・390x844・320x568表示、背景/土台/鉢含め鑑賞。実phone/Safari/thermalは未検証。

定常は同Mac/同pose/light/scene、DPR1.6、ABBA各版118点、30warmup61query先頭2除外。GPU p95 PC12.485→12.490ms、39015.946→16.032ms、32013.205→13.160ms。CPUmedian PC4.35→5.20ms、3903.90→4.50ms、3203.90→4.10ms（約5..20%増）、CPU p95は今回旧以下。2400ms idleを別にABBA14点/版、GPUp9534.501→35.397ms、CPUmedian4.9→5.3ms。HTTPcacheoff120ms/250KiB/sの単回coldはFCP320→312ms、fullstill1809.5→2069.6ms、3D11895.1→11983ms。性能向上・非退行・60fps合格を主張しない。

read-only独立reviewは全景3幅でR22より良いとの判定。上記CPU/読み込みコストを明記し、ローカル暫定採用。広い滑面と単純なturn、土際裾/尖端、接写graftと均質woodgrain、名木らしい複雑な古木・庭の高級感は未達。全体完成false。次は NEXT_LOCAL_AGE_AND_CPU.md 。

QAのみの失敗も保存：初回native record変数衝突（export前）を修正、freeze記録のcwd誤りを初material表示前に修正、special probe regex/初期DOMpoll/失context後ext再取得を修正。元failureと正しい再検証を分離。誤model画像/未整合textureを成功に含めない。最終sourcebuild成功、配信decoded19資産identity、TOP3width+fallback確認。Chrome87239 cleanexit0/guard除去、唯一5214server3356はR25candidate。旧5208は変更なし。

旧25statesと全既存旧成果SHAを保護。歴史的外部PR7削除26paths/manifest4entryの完全性は引き続きfalseで、復元せず現存分を検証。HEAD2347a151a05015f0049e4b0fd8f01545ac9afed3 unchanged。Gitwrite/push/PR/merge/外部公開/購入/automation/旧project access/旧成果delete0。Library既知helperTLS阻害につきretry0・imageIDs0。localJPEGは qa/special-stills/{pc,mobile-390,mobile-320}.jpg 。
