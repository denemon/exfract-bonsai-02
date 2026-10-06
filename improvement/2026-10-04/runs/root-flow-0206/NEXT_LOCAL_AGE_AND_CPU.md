# 次工程：新R25を保護し、局所的な古木の立体性とCPU経路を調べる

R25 root-v02 / normal-v4を暫定TOPとして保持する。今回の局所根座・graft・flow改善を後退させない。幹の広い滑面、単純なturn、土際の裾・右尖端、近接graft、木目の均質さ、高級な庭全体の説得力は未達。材質や暗さで形が完成したと扱わない。

最初にwriter/free/20MiB見積り。旧27statesとR25manifest/receipt、R22/R20空間・5stillsを保護する。新native候補一件に分離し、上部輪郭・樹冠2800spraysの実world/instancing、鉢/soil/土台/高塀/右前障子/camera/lightを固定。参照実pixelsを再確認し、既存nativeの局所controlを使って枝母面と隣接した短い幹面の立体性を直す。共通円筒半径/S全再生成/Gaussian全丸め/plane shave/装飾白銀を使わない。まずgray通常PC390320/左右/woodとneutralを確認。閉mesh/selfintersection/soil埋まりは構造証拠で美的承認と分ける。

CPU中央値は今回PC+0.85ms/390+0.60ms/320+0.20ms、GPUp95はほぼ同範囲。完成still+260ms、cold3D約12秒、idleGPUp95約35.40msが残る。形・光・葉を落とさず、同一固定sceneのrender/CPU区間を分解して原因を確認する。改善を実証できなければ速度向上と言わない。steadyとidle/coldを分け、手法を変えて速い数字を採らない。

新候補が通常全景でR25以上と確認された場合にのみ、関連負荷/機能/own5static/inlineの同期後に新runのroutingで暫定採用。trialをTOPへ混ぜない。Library既知TLS阻害のretry0、20MiB/sharedasset/profile/cache/単一5214、旧成果削除/他project/Gitwrite/push/PR/merge/公開/有料購入/毎時automation0。10/10 23JST期限。actualphone/Safari/thermal/Sol-xhigh実metadataは未検証。
