# native木の単色造形ゲート：不採用

新しい連続木一案grip-v01と一回の局所修正版v02を作り、通常の庭PC・390・320、盆栽全体・左右25度・幹根近接で実見した。作者/独立レビューとも形状NG。S字の太い管、丸い枝元、左右の尖った根の裾が主に読まれるため採用せず、材質仕上げと形状凍結へ進めていない。完成品質は未達。通常 http://127.0.0.1:5214/ は選定R22のまま。新案は /compare/r23/ の灰色診断だけ。

節ごとに位置/半径/奥行/roll/広い前凹みを定め、枝元・根を幹内へ重ね、一度のvoxel weldで一体surfaceを作った。v02は土高さを仮定.36から実.393へ訂正し、旧twigへの末端route、枝内側、根の沈みと断面を修正。体積は.107753→.096062。微細shaderを使っていない。実装は全高共通の極座標lobes/Gaussian凹みに依存しており、狙った部位ごとの体積造形にはならなかった。凹みは縦溝として読まれ、係数変更では自然な古木へ達していない。参照302×404ユーザー写真は実ピクセル確認済み、後面/根は推定。灰茶色/茶褐色指定を維持、白/銀木の再導入なし。

各native18,002vertex/36,000tri/閉成分1、boundary/nonmanifold/core非隣接交差0。Blender再読込みでpositions/faces/normals/3UV/color/authoring_version一致。これはcore単独の構造検査であり、古木の美的合格やretained Terminal twig hierarchyとの接続・交差品質を証明しない。near像の短い棒・切端・段差は残る。新木のUV/masksは暫定のみ。native/GLB/author script/controlsと二つの失敗形を保存した。

最終build4回成功（最終受入コードは qa/build-final-verified.log、途中helper失敗後のbuild-final.logはsuperseded）。最終PC1440×900/390×844/320×568をMac Chrome154で実表示。可視文字0/overflow0/通常console0。同camera/FOV/exposure/key/R20実庭で比較。gray-v02-fixed-garden が形判定画像、final-trial-built-pc390320 が最終default both版。v01左右は鉢下端の診断cropがありv02では距離3.25の全体像で解消、幹closeは意図したcrop。独立レビューはv01/v02の灰形と生成codeまで、後続routing/機能/容量を独立合格した扱いではない。

新core replace後に工程22renderer包絡を再計算。外縁の葉/鉢が同じためnative+deferred high boundsと有限5光の寄与0判定はR22と一致。72native低葉group→12表示group、high/mixed bypass等のrenderer codeは変更0。background geometry SHA dadb0605…/field4bedbbe0…は全case同じ。rejected木のGPUは再計測しておらず、性能採用の主張0。既存selectedのCPU増加、cold11.8849s、idle35.556541msを残した。steady p95とidleを混ぜない。

選定TOPのPC390320新実写真は工程22最終写真とJPEG bytes・decoded pixels完全一致、native hero SHA7b41aaf1…/全物理景観/灰茶材質/camera/key70/exposure1保持。qa/selected-root-preservation.json。26配信decoded SHAでTOP/R20/R21/R22/R23 HTML/JS/CSS/5構図stillsを各diskへ照合。新比較の5completed gray WebPと5媒体別inlineも自身の実景へ同期。実contextlossはtrial320/TOP390で各自身の静止画へ復帰、trial390 reduced idle1秒frames1→1。動作全QA、WebGL非対応再注入、contextrestore、cold/perf再測定は不採用なので今回重複実行せず、selectedR22の検証は qa/selected-root-resilience とREPORTを参照。関連確認を全機能合格と呼ばない。

次は NEXT_NATIVE_WOOD.md。共通のradius式をやめ、厚い一体surfaceの根座・短い屈曲・枝肩・上体を直接造形する。葉の末端は固定し、一次枝とtwigの内側routeは連続性のため作り直す。通常灰の一案が選べる時だけ凍結→独立材質へ。今回の方法で三案目を作らない。2h途中予定より前に不合格が確定したため終了し、時間を埋める反復をしない。

20MiB容量はqa/capacity-final.jsonにrun・共有profile観測正peak/cache正増分・staging/pycache正増分・三coordinator全量・新stateを計上、負evictioncredit0。旧23状態/R22全manifest/review/critical source-productionをSHA検証。既知外部PR7の26削除/歴史manifest4欠落は未復旧、historical completeness=false。writer自身のみrelease、5214単一preview継続、5208保護。Gitwrite/push/PR/merge/公開/購入/旧projectアクセス/旧run削除/Library retry/automation0。画像Library ID0（既知helper TLS阻害、再試行禁止）、Macローカル保存。実phone/Safari/熱/要求Sol-xhigh実metadataは未検証。overall goal=false、期限10/10 23JST。
