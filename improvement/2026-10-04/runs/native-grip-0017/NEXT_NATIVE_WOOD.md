# 次milestone：直接造形の通常距離ゲート / 一案

工程23の極座標断面を流すmethodは不採用。中心線・径・roll・Gaussian凹みを変えても、根〜冠の主な読みがS管のまま。coeff反復・全高溝・別生き筋円筒・old finを削る反復へ戻らない。1候補＋1局所修正後NGで止めた。形凍結・material finish0、TOPはR22。

次は全高共通のradius式から離れ、根座・下の短い屈曲・第1枝肩・上体を独立に触れる一体の厚いsurfaceを直接編集する。部位ごとに前面/側面/後面を異なる3D制御点と終端面で作り、広い凹面が側へ返るところとその終点を実形状で定める。断面厚みを保持して巨大plateを作らない。自動ellipsoid union後の全体plane shavingは以前失敗済み。macro体積を最初に固定し、微細彫りやnormalで管を隠さない。

既存葉は末端到達のみの制約へ。一次枝originや内部routeを固定すると、幹から丸い腕と古いtwigの切端が出る。既存Terminal twig hierarchyの内側支持路も新primaryに連続するように作り直す範囲が必要（葉位置と数は変更しない）。今回core単独の交差0は、coreとretained twigsの接続/交差品質の証明ではない。枝の下面を短く締め、上/後だけ長く幹へ入る肩と外側減径を灰で読む。根は左右の尖った裾を描くのでなく、別方向/高さの塊が実soil .393〜.417へ潜る途中を作る。

次の到達点は「材質へ進める一案のgray形状選定」。最初の30〜45分で厚い前/側/後の体積配置と枝/根を描き、1〜2時間でR20実庭・PC390320・左右25度・根幹近接の候補を評価。同gray/key70/exposure1/現cameraで管・腕・裾が主なら落とす。合格時だけnative/GLB/制御点/positions/normals/UV/masksをSHA凍結し、独立color/roughness/normalと葉・光検証へ。合格前の「gray colorを変える」「深い影/白木にする」は行わない。隠れ面/根の推定、品種未確認を記録。

selected R22 TOP・R20/R21/R22経路・旧24状態（旧23＋native-grip-study-state）を保護。新trialは次runパスだけ、共有asset/profile/cache/5214、20MiB事前計画。旧run削除/Library retry/Gitwrite/公開/購入/automation0。model変更後はfresh native+deferredhigh包絡/有限光寄与0/full shadow invalidation。CPU増加、cold11.8849s、idle35.556541msは未達のまま別perf工程で測る。steadyとwakeを混同しない。実phone/Safari/熱/Sol-xhigh actual metadata未確認。10/10 23JST期限、親が直ちに次milestoneへ。
