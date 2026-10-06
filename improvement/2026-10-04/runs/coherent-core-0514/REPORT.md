# Stage28：主幹一体の試作は未採用

正式先 /Users/kazuki.tanaka/dev0/exfract-bonsai-02。TOP http://127.0.0.1:5214/ はR27 program-state-0426のまま。R25 root-v02/normal-v4/original葉、R27 CPU改善を保護。全目標完成false、盆栽と箱庭の美的完成を主張しない。比較 /compare/r28/?candidate=core-v02 は灰色の未採用形状、読込/WebGL不可時はR27完成静止画をread-only参照する研究用で、最終同期版ではない。

先に DESIGN.md で完成像・配置・camera・光・素材の順序を決定。実添付302x404のねじれ/幹筋/横に広がる非対称葉群と空隙はpixel確認済み、後続のgraybrown/夜空/高塀/右前障子指定を維持。今回は木材質0trial。R25 actualnativeを出発点とし、root0..19/upper100..113/rootcaps/枝先/terminaltwig/2800spraysを保護、主面を独立XYZで不等厚みに変更し、既存枝母境界の変位をneckへ減衰。前面一箇所に2finite支持点を共有topologyで追加。均一noise/円筒radius/板overlay/全断面支持ring/均一溝は使っていない。ただし元の断面列と長い前面位相が支配形を残した。

V01は斜めの折返しが突出した唇/巻いた帯に見え、ordinary gray夜PC390320/neutralで形gate不合格。V01native/export/写真/logを保持し、同一proposalの一回のV02修正だけを実施。322/323の突出と高低差を後退、対角crease .34→.04、直下と上行の前側・後側厚みを一体で調整。V02の唇は弱くなったが、長い広面と対角折れが依然ねじった帯/折ったSとして読める。PC/neutral左右/390で残り、320でbeforeを明確に超える古木の量塊にならない。根の二柱化や鉢/庭との縮尺退行はなく、樹冠空隙と支持は保てたが、それを主幹美的改善と混同しない。独立volume_reviewも20実画像で不合格、R27維持/材質へ進まない/第三微調整0に合意。

実Mac Chrome154/M1Pro/ANGLE MetalでV02 before/core10組20JPG。夜PC390320、中立PC390320/bonsai/left/right/wood。actualcamera・全光設定・全モデル投影bounds・葉world SHAが各組で一致、terminaltwig全属性/index/world一致、native mainpositionが変わったことを確認。wholePC390320は樹冠から鉢までuncut。woodは意図した近接cropで、whole判定を置き換えない。V02 control324/face355、evaluated5418v/10832tri、volume.10388059、boundary/nonmanifold/nonadjacentintersection0。rootcapsは実soil下>.035m、mainroot0..19保護。これらは構造だけの成功、自然な古木の合格ではない。形不合格のためnative最終freeze/reopen・材質個別trial・候補完成stills・候補性能/完全functionalを実施していない。

失敗も保持：初期nativeauthorのrecord参照KeyErrorを修正後再生成、誤URLlighting=neutralの5組は実nightでneutral判断から除外しwood-light=neutralでactualmodeを確認した7組を撮り直した。集計初回は投影頂点数まで一致をassertして失敗、V02追加topologyで105projectedvertices増えたためboundsとcountを分離し記録。初回HTTPは稼働preview旧regexのV02 Content-Encoding欠如を検出、ブラウザ自体はDecompressionStreamでactualV02を読めており、最終preview再起動後12decodedHTTPidentity成功。自動承認reviewは汎用QAhelperの未使用still分岐が既存aliasへ書けるとして実行拒否。拒否helperは実行せず、既存write機能を削ったTOP専用helperで解決、共有成果への上書き0。qa/automatic-review-rejection.json/qa/http-first-failure.json等に保存。

最終build成功（build-final-unadopted.log, build-gray-v01.log, build-v02-form.log）。最終previewでTOP3幅actualJPEGはR27完成JPEGとbyte一致、TOP3幅WebGL不可時も指定済み完成WebPを表示。runnable/文字0/overflow0、reduced状態で検証。TOPHTML/R27bundle/5完成WebP/R25compact/未採用V01V02、decodedHTTP12一致。R27renderer src/render-partition.jsのSHA完全一致。R27 CPU改善のソースと表示を守ったが、今回性能を再測定した意味ではない。未採用形gate後はTOP/build/配信/保護だけの必要QAに限定、材質やGPU全検証を追加していない。

R27の既存性能課題は引継ぎ参照値：CPU中央値PC3.5/3902.4/3202.3ms、program再選択26/25/26→0。390GPU p95+.544ms、idleGPU36.211ms、cold3D11.987s/完成still2.09sは未達のまま。今回解消を主張しない。実phone/Safari/thermal/モデルSol-xhigh実metadataは未検証。主幹自然さ、上枝肩、葉spray反復、背景植栽/苔、全景の名品に似合う品格も未達。次は NEXT_MAIN_TOPOLOGY.md で元の長い面位相自体を再設計する一件を提案し、今回第三candidateは作らない。

旧30states/R25/R26/R27/全現存旧manifest SHAを保護、GitHEAD 2347a151a05015f0049e4b0fd8f01545ac9afed3 unchanged、許可3coors以外のtracked変更0。新coherent-core-study-state.jsonだけ追加、暫定選定statesを更新しない。歴史外部PR7削除26paths/4manifestentryは未復元/完全性false。旧project access/olddelete/Gitwrite/push/PR/merge/外部公開/購入/automation0。Libraryは親指定retry0/IDs0で再試行なし。Chrome87858と98274はcleanexit0、writer/profileguard解除。単一5214は今回previewPID97661/session41616、前ownedPID87791をSIGINTで終了。期限10/10 23JST。

成果：models/core-v01-editable.blend/core-v02-editable.blend、sculpt/author_main*.py、qa/shape-comparison-proof.json、qa/independent-shape-review.json、qa/special-top-final/results.json、delivery-manifest.json/qa/final-receipt.json。候補画像はqa/gray-night-whole-*-v02/とqa/gray-neutral-actual-*-v02/、TOP確認画像はread-only参照 ../program-state-0426/qa/special-stills/{pc,mobile-390,mobile-320}.jpg。容量実allocated/共有profile正増加/peak観測/共有cacheはqa/capacity-final.json。
