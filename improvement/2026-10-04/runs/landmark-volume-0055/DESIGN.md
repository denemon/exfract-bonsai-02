# 工程24：厚い一体表面の局所面と枝口

原302×404と公式寿雲2画像を実見。rootはほぼ立つ偏った塊、middle短い圧縮屈曲、upper斜めに返る広い面。後面・根は推定。灰茶色/茶褐色、white/silver0。横冠は原参考と既存末端位置に合わせ、追加参考の縦冠をコピーしない。

過去carved-massはellipsoid/径pathをvoxel unionしfinite wedgesとplane shavesで前面を削った。今回は既存S/voxel塊を出発点にせず、前/側/後の独立XYZランドマークで厚い閉じたcontrol surfaceを新設。根座、圧縮turn、枝肩、upperの異なる局所patchを接続、凹面の側返り/終端をsupport edgesで明示。sectionの頂点数/面役割を部位ごとに変え、共通radius/lobes/Gaussianを全高へ流さない。uniform smoothing/全体plane shaving0。subdivision前からdepth/荷重を保つ。枝口は共有境界を使い、上/後長く下面短く、左右の口/接続長は異なる。露出後早く減径。根は実soil surfaceへ貫通、尖裾ではなく3D異径支持。

旧twig内側支持routeを新primaryへ接続し、末端node/葉2800spraysは固定。旧枝originを新木へ強制しない。灰全景PC390320/左右25°でS管・丸腕・尖裾が支配せず、厚み/根支持と自然さが明確に改善していればmaterialへ進める。小grain・細面・隠れた末端微接続は後段課題、major厚み/root/branchNGを色/影/葉で隠さない。独立レビューと先に共有、方法名/閉成分だけでは合格にしない。

R22 TOP固定、R20R21R22R23 immutable経路、24旧状態保護。新r24だけ比較、20MiB共通asset/profile/cache/5214再利用。CPU増加/cold11.8849s/idle35.556541msは別工程未達。採用時のみ必要QA/static更新、非採用は必要比較/保護確認。Library retry/Gitwrite/旧削除/他project/purchase/publish0。期限10/10 23JST、Sol xhigh actual metadata未公開。
