工程16追記：最新の形状＋shader採用条件

自然な根元/太さ変化/曲がり/枝口を通常距離で読める候補一件を選んだら、そのgeometryを固定して素材比較へ進む。形状NGをnormalで隠さない。大きい輪郭/うねりはgeometry、中の割れ/剥がれと小さな粗さはnormal/bump。木metalness0、乾いた樹皮roughness高め、枝/摩耗部は控えめ差、色/roughness/normalは独立。sRGBのcolorとNoColorSpaceのnormal/roughness区分をThree0.185.1実sourceと公式MeshStandardMaterialページで確認済み。葉は推定樹種に合う鱗葉の寸法/付け方/密度差、控えめ新旧色差、表裏/透過は光方向と厚みに沿い、emissionなし、内部陰影を保持。

中立の柔らかい確認光から夜景へ。根土/枝元/葉重なりの陰影と暗部階調、過剰AO/bloomなし。提出は実renderの同camera/光/露出の前後：庭全景/盆栽全体/幹寄り。normal比較中はgeometry SHAを固定。スマホは主要輪郭/空隙/陰影を優先し微細bump/影解像度を調整する。形状/質感それぞれの採否と残問題を画像に対応して報告。未達なら次工程へ明記して分ける。

樹種はユーザー添付の細かい葉群・白いshari・赤褐色live veinから真柏系juniperを推定。品種/正式同定は不可。大宮盆栽美術館公式Tree Types and ShapesのJapanese Juniper写真を実ピクセル閲覧し、乾いた大面の折れ、細枝へ向きが変わる木目、密な鱗葉群と空隙を比較。閲覧写真は一時ファイルだけ、texture/サイト/配布物へ取り込まない。reference-source.jsonにURL/取得/閲覧状態を保存。Python urllibはローカルCAのTLSで失敗、system curlでTLS検証を維持した通常取得が成功。Libraryの再試行ではない。

