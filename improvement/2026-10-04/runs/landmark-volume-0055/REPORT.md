# 厚い連続木の通常灰ゲートを進め、独立材質試作まで完了

新しい一体表面 landmark-v01 と、枝口だけを局所分割したv02を制作した。作者と独立レビューは、通常全景の下幹の荷重塊・短い屈曲・枝肩の厚みに明確な改善を認め、v02を独立材質試作へ進める一案として選定した。これは自然な名品古木の完成合格/TOP採用ではない。根前面の揃った二柱、中段の広い滑面、左枝元の線、右小突起、木目のflow未達が残る。TOP http://127.0.0.1:5214/ はR22を維持し、全景の完成品質と性能の未達を継続する。

原302×404ユーザー写真の実ピクセルと、さいたま市大宮盆栽美術館の寿雲/Shimpaku公式2写真を実見して方針を決め、造形前に根支持・輪郭・厚みの通常距離基準を独立reviewへ共有した。追加写真を背景やtextureへ転用していない。元写真の正確な品種は未確認、後面/根は推定。共通radius/lobes/Gaussianを全高へ流す方法を離れ、部位別の独立XYZ、異なるloop数/面役割、有限凹面、短い圧縮turnの編集可能表面を作った。旧ellipsoid/voxel union＋全体plane shaving失敗案は再利用していない。方法名は完成根拠でなく、v01には反復する膜状枝口が残った。

v02はv01 nativeを開き、既存202点の座標を保って枝口の母面内側へ小さいopening・短いdepth neck・中間sectionを追加した。枝肩を広い膜から針へ直につなぐ面を分割し、端にsupportを追加。元のmain/rootを丸め直していない。根の実土面ray検証は保持され、異なる3方向capは土の下へ埋まる。v02 control322vertex/354face、evaluated5394vertex/10784tri、volume .089746252、boundary/nonmanifold/core非隣接交差0。native再読でpositions/faces/authoring_version一致、normals/3UV/colorsもhash snapshotを保存。構造成功は美的完成やtwigとcoreの全接続/交差品質の証明でない。根/枝の残りは形課題として明記した。

form-freeze-for-material.jsonでnative/GLB/制御点・normals・全UV/colorsを試作範囲だけ固定。base（木#66584b roughness.96、twig#514236/.97）→color(texture色)→roughness(.94-.995)→normal(.20)を同geometry/camera/lights/葉/露出で比較した。shapegray roughness1は別形状診断で、gray→colorを厳密な色だけの差とは呼ばない。旧material v1はcolorだけoffsetがありroughness/normalと位置がずれたため、新aligned版では全mapへ同じoffset後UVを使用。弱いnormalを次試作基準に選んだが、通常距離で差は小さく主改善は色texture。白/銀・emissive・metalness0、過剰glossで形を隠す扱いなし。既存ローカルCedar001 mapsは暫定、元盆栽のscan/樹種一致ではない。右根の横縞はcolor段階からのUV flow課題で、map位置合わせやgrainで根形状解決とはしていない。

49実ブラウザcaseをMac Chrome154で保存、visible文字/overflow/unexpected console0。8caseの旧gray-landmark-v02はsource追加後のbuild更新漏れにより旧edge-v02を表示していた。レビューが検出し作者の改善判断を撤回、無効資料のまま全て保存した。正規gray-landmark-v02-verified8像は全actualVersion landmark-v02をassert、以降材質キーv2-alignedと木全fieldSHA8381f8ad…もassertしている。旧unaligned材質9caseはsuperseded。最終build5回目は qa/build-material-with-base-final.log。最終コードPC1440×900/390×844/320×568画像は qa/final-aligned-material-pc390320。bothのbatch/light partition有効、fullShadowUpdates2、fresh native/deferred-high包絡と5有限光寄与0を確認。wood近接の葉LODはmixed・2,484,020triで、allhighとは記録しない。通常3幅では冠/鉢/土台の関係を保つが、390で根二柱と障子格子の競合も残る。表示成功と名品の説得力は区別している。

旧TOPの新PC390320写真はR22最終写真とJPEG bytes・decoded pixels完全一致、native hero7b41aaf…/R20 background dadb0605…/field4bedbbe0…を保持。最終36配信decoded SHAでHTML/JS/CSS/stills/新GLB2をdisk照合。新trialは不採用の診断でdefaultgray、材質比較は /compare/r24/?candidate=landmark-v02&wood-finish=normal。trial読込/WebGL fallbackはcompleted R22 sceneを保持するread-only参照で、新形状の5静止画同期は今回実施しない。TOPのfallback/reduced/context等はR22で検証済み、今回は不採用なので関連全QAやGPU/cold/idleを重複実行していない。新trialのfallback同形同期・全機能QA・性能合格は未検証。選定R22のCPU増加、cold3D11.8849s、idle p95 35.556541msは未達のまま（Stage22測定値、今回再測定0）。steady GPU値とwakeを混ぜず60fpsを主張しない。実phone/Safari/熱/Sol-xhigh実metadataは未検証。

次は NEXT_LOCAL_ROOT_AND_FLOW.md。v02で得た灰全景の改善を引き継ぎ、根座の偏りと枝内側接続を一体表面上の局所編集として直す。共通係数/S管/全高溝へ戻らない。根二柱が通常3幅の主読みに残るかを灰で再判定し、次形は別runでのみ再凍結。UVは実際の面の伸び/継ぎ目を部位で直し、色/normalで根を隠さない。全木を白/銀へ戻さず灰茶/茶褐色を継続する。

20MiBはqa/capacity-final.jsonで正allocated増分を保守的に計上。旧24状態とR23/R22全成果をSHA保護、既知外部PR7の26削除/4歴史manifest欠落は未復旧、historical completeness=false。自身writerを解放し、共有profile/cacheと単一5214を維持。Chrome終了/guard解除。Gitwrite/push/PR/merge/公開/購入/旧projectアクセス/旧run削除/Library retry/automation0。Library画像ID0（既知helper TLS阻害、親指定の再試行禁止）、確認画像はMac内に保存。期限10/10 23JST、overall goal=false。
