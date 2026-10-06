# 次は主幹一体の量塊を、一件で直す

新工程の前にwriter、HEAD、許可されたtracked3coors、free2GiB、20MiBを確認。今回R27のmanifest/receipt、旧28states+新2states、R25native/root-v02、R26未採用trial、R27の5完成stills/CPU策をread-onlyで保護。既存成果削除0・旧projectアクセス0・Libraryretry0。現在TOPはR27、単一5214。新しい試作一件を別compareへ。旧selected statesを更新しない。

CPU状態安定化は検証済み。public per-pass Sceneとsource-shadow参照、native invalidation fallbackはR27実装を使う。新geometryに対して包絡/finite-light証明を必ず新しい実boundsで作り直す。参照objectの再利用だけで任意leafgeometry変更を保証しない。public completeSceneのshadow authorityとcached shadowを維持し、Three私有API/内部patch/画質を落とす値づくりは禁止。

最大の不自然さを一つに絞る：主幹が広い滑面の均質なSで、部位ごとに異なる厚み、短い折返し、軸を外れるねじれの量塊が読めない。R26の32control/葉艶は小改善で保存済みだが、この支配形を解消しない。微grain・小筋・新根肩の候補を増やさない。R25のactual native主幹を一体として作り直す一件を行う。

最初に全景完成像を決め、普通距離で効く太さの偏りと長手の凹凸面、折返しの奥行き、上行する軸のねじれ、母面から続く枝元を一つの構造として整える。全322controlsの一律noiseや均等section/tubeへ戻さず、屈曲ごとに内外の厚みと面幅を設計。主幹の軸を変えても末端枝/全2800sprays/world/樹冠外輪郭/枝間の空隙は保護する。鉢soil・低土台接触、土中rootcapsを保護する。

grayで夜景普通PC1440x900・390x844・320x568、左右1000x900、neutral普通距離を先に実Mac Chromeで比較。寄りの小差だけで採用しない。縮尺・graftの厚み・曲率/捩れと空隙・鉢の支持、背景全体と同じ場所にいる感を評価。独立read-only reviewを取り、通常距離の支配形が明確に改善しなければ未採用として理由を残す。native全項目をfresh Blender reopenで再照合し、閉mesh/boundary/nonmanifold/nonadjacent intersections/root burial/全sprayworldを確かめて形を固定してからだけ材質を比較する。

現景色のgraybrown/茶褐色乾いた粗面、夜空、高塀、右前障子、植物/苔境界、文字0・散在小石0を維持。色/roughness/normalは独立、normalの筋を増やして広い面を隠さない。R26botanical葉は保存済みで、主幹全景判定の後に固定形の葉だけ比較するなら一つに限る。

最終paired CPU/GPUはABBA+BAAB236sample/版/幅、idle2400ms14/版、cold120ms250KiB/s単回を分ける。R27はCPUmedian3.5/2.4/2.3msを得たが390GPUp9514.031(+.544)、idle36.211ms、cold3D11.987sec/still2.09secは未達。実phone/Safari/thermal/要求Sol-xhigh実metadata未検証。変化量・mesh/testpass・CPU成功を美的合格に使わない。own5full/inline/最終sourcebuild/functional11/high-near/dynamic/HTTPidentity/TOP actual同期、nativeと全景と負荷の判断が揃ったときだけ暫定選定を変える。deadline10/10 23JST、push/PR/merge/外部公開/購入/automation0。
