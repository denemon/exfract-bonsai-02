# 工程23：偏った断面と局所屈曲を持つ連続木

R20の高塀・右前障子・庭・全8光源・camera・鉢・土台・葉群と、工程22のselected TOPを固定する。未採用木は /compare/r23/ だけで比較。参考302×404写真は実見済み。写真の左へ折り返す古木、非対称な横冠、太さの変化、枝間を判断基準とし、隠れた後面や根は推定。最新指定の灰褐色/茶褐色、白/銀の再導入なし。

新methodは位置・断面・向き・偏りを個別に描いた短い節を、全体の成長軸へつなぎ、その内側へ枝元と根を深く重ね、一度の体積unionで連続した厚みを作る。巨大な前面plateを維持して削る方法、同じellipseを延々S字に流す方法、並んだ生き筋円筒、二本ridge、全高grooveは使わない。断面前面の一つの広い不均等な凹みは体積自身へ組み込む。根は3方向・異なる径・異なる高さから地中へ降り、枝元は幹内から長い非対称collarを持って先へ細る。屈曲は下幹の短い反転と上幹のゆるい上昇に強弱を分け、奥行にも変化を持たせる。

1候補、必要なら1局所修正まで。単色gray/roughness1/normalなしの木を、現実の庭PC390320、盆栽全体、左右±25度、根幹近接で見る。構造検査は美的合格の代用にしない。合格時だけgeometry/native/script/controls/normals/UV/masksをSHA凍結し、その後color・roughness・normalを独立に確認。落ちれば材質段階へ進めず、理由と次methodを返す。

renderer包絡は新木replace後に再計算、full shadowをinvalidate。shape途中はoriginal renderer可。合格後はbothの実包絡/0寄与証明とGPUを関連検証。CPU増加、cold11.8849s、idle35.556541msは別の未達。GPUsteadyとwakeを混ぜない。unadopted時は最終buildと代表実表示のみ、TOP/fallback/reducedの全QAを無駄に再実行しない。

20MiB新規保存、共有asset/profile/cache/5214だけ、旧23状態とR22全成果/レビューを保護。旧削除・Library再試行・Git書込・公開・購入・automation0。実phone/Safari/要求Sol-xhigh実metadataは未確認。途中2h/上限4h、10/10 23JST期限。
