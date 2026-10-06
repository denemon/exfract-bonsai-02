# 工程22 R20性能派生の独立レビュー（補正前・凍結）

判定：補正前R22は不採用、TOPはR20維持、premium完成=false。描画最適化の方向は支持するが、PC／wideの左奥の植栽が暗くなる退行を実見した。親が原因を確認し再検証へ移ったため、本書を補正前記録として凍結する。

## 実見と独立照合

R22 qa/final-source-best-derivativeの5JPEG、qa/final-production-best-derivativeのPC／390／320の3JPEG、R20 qa/final-sourceの同5幅を実画素閲覧した。今回は1440×900／390×844／320×568／320×844／1920×800が一致する。

source・productionの5resultsをR20と独立照合し、viewport／actualCamera（FOV・露出）／native hero属性・行列・LOD／exactProjection／全8lightsがすべて一致した。背景geometry SHAもdadb0605015e297c8a91edcedb3f7c07db4b5a95f305534475ae34310f4880ccで一致。5件ready=true、通常ログ0、可視文字空、overflowなし。ただしこれらは背景材質・shader・完成画素の一致を測る項目ではない。

## 見た目と原因

配置・主役占有はR20を保つ。390／320／tallで冠〜鉢〜台と右前障子が残り、wideの右境界も保つ。

一方、PC／wideの左奥の樹冠は、旧R20写真で見えていた緑と不規則な輪郭が暗くなり、塀と同化する。主役・室内・地面がおおむね一致していても、背景を含む全景の保全を合格とできない。sourceとproductionのPCでもこの差を実見した。

独立指摘の後、親はR21由来のmicro=masked／gravel=variedがR22 defaultsに残り、R20 geometryを使っても背景材質処理が異なっていたと確認した。qa/superseded-acceptance.jsonもその原因と撤回範囲を明示する。default除去は親の報告であり、補正後build・写真は本書で未検証。geometry／lights一致から「performanceRenderOrganizationOnly」と判断した初期解釈は、採用根拠として使わない。

## 旧pixel・GPU資料の意味

best-derivative-pixel-equivalenceは、R22内の同sceneでoriginal→bothを比べた資料。両方が同じ誤ったdefaultsを使えば、R20本来の完成景からの材質差は検出しない。

記録上、bothの変更画素／最大チャンネル差はPC Retina50／21、390 11／22、320 1／6、tall900 8／25、wide900 23／26。RGBA平均絶対差最大約0.00015、original repeatは全0。72→12群・2800 instance matrix bit exactとnative復元の資料も確認した。high木近接のboth全RGBA差0も記録されている。これを全幅の完全画素一致、R20対R22の材質一致、通常low renderingの合格へ拡張しない。

matched-best-and-trial-equivalent-batchesのR20→R22→R22→R20を読み、各61点から先頭2点除外59点の中央値・nearest-rank p95を独立再計算して記録と一致した。

| 補正前PC Retina | median ms | p95 ms |
| --- | ---: | ---: |
| R20 a1 | 15.262749 | 15.295583 |
| R22 b1 | 12.279874 | 12.361333 |
| R22 b2 | 12.244874 | 12.386541 |
| R20 a2 | 15.447249 | 15.558750 |

実DPR1.6、tri 1,810,918維持、calls125→65という数値改善はある。しかし背景材質差を含む設定の測定なので、補正後のrender構成だけの改善として採用しない。superseded-acceptanceは旧写真・pixel／GPU・final performance／build／idle一式を採用根拠から外し、rawを保存すると記録する。

## 補正後の採用と木作業の再開条件

描画方式は候補として残せる。採用には、R20 root対R22 originalの同5幅で完成材質・framebufferの対照を成立させ、次に同scene内original対bothの微小差と実表示を確認する。補正後productionの全景退行なし、同条件ABBAの全有効点・Retina p95改善、通常LODと木近接high双方の正しい復元、idle resume／cold／reduced motion／実context loss復帰を最終buildで確認する必要がある。現在実行中の12paired cases等を、本書では成功済みとして扱わない。

この性能派生の保全・採用が成立したら、背景・光・カメラを一つの基準として凍結し、native木の根張り・支持・局所断面・枝の太さの変化へ作業を戻せる。主木の滑らかなS字、均質な腕、弱い根元支持と近接葉品質は未達。灰褐色／茶褐色を保ち、中立形状と通常夜景を同条件で比較し、shader・最適化成功と名品盆栽の造形達成を分ける。庭もR20で未達のままである。

実機phone／Safari／長時間熱負荷は未検証、60fps保証なし。書込みは本書一件だけ。ブラウザ・テスト・広域filesystem auditを起動せず、旧レビュー・コード・モデル・状態は変更しない。補正後の判定は別レビューへ分け、本書を凍結する。

記録時点（UTC）：2026-10-05T14:30:03+00:00
