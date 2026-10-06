# 工程21：主役と障子を分離した夜の箱庭

完成像は高い実塀、右側の丁寧な前障子、夜空を保ち、盆栽の輪郭の後ろに静かな余白がある庭。PCでは木・石・苔と右奥の縁側/室内の厚みが読め、スマホでは樹冠/鉢/低い台が切れず、障子の格子と競合しない。R20を作業基準/暫定bestに固定。木の造形/灰褐色/UV/材質/key70/露出は変更しない。

物理的な家屋の位置・向き・境界との接合、障子の実開き方、各比率のカメラを先に比較する。viewによって建築を消す/移す偽装はしない。実室内/屋根/床/縁側支持/有限灯を一緒に移し、基礎・柱接触・塀端接合を確認する。植物は枝に付いた閉じた葉を維持し、支持軸の自然な葉分布と三株の異なる枝量、近低木の不規則な緩い面を整える。砂利は物理粒度の変化・少量の土粉/葉の影と苔との境を同じ空間fieldで表す。

実Mac ChromeでR20現Retinaを再測定し、背景材質の微細凹凸、影map、closed leafの描画/overdrawを個別ablationする。測定だけの非表示は診断と明示し、製品では主要輪郭/空隙/陰影を削らない。採用には見た目と同条件Retina p95の改善の両方を要求する。必要ならbackgroundの高周波だけを前計算/距離に応じた正常なfilterにし、色/木目/物理縮尺を守る。

形状選定後にgeometry/field/cameraを凍結し、材質と夜光を比較。庭/盆栽/幹寄りは実camera/FOV/exposure/key/hero attribute/LOD/投影を揃える。最終PC/390/320/tall/wide/Retina、読込still、WebGL-null/reducedmotion/context復帰、通常cold250KiB/s+120msを最終buildで確認。実機スマホ/Safari/熱負荷は未検証と明記。背景が目標へ近づいた理由と木の再開条件を記録する。

優先容量20MiB、事前17.75MiB。最新best/20旧状態/各manifestを保護。必要最小の実写真/記録、共有read-onlyモデル/素材、同Chromeprofile/同5214origin。Chrome正増分peakとcache/staging/調整文書/新状態まで計上し、旧成果・unknowncache削除/負evictioncredit0。best5208と最新5214だけ。Library再試行なし、ID0。GitのPR8はobjectと現成果を読み取り照合し、自動pull/reset/restore/writeしない。旧projectaccess/公開/購入/automationなし。期限10/10 23JST、要求Sol/xhighの実runtime未公開。
