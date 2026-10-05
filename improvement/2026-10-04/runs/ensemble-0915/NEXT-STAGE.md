# 次工程の提案：短い体幹と枝接続を手動共有meshで作る

現在最良は工程12の保護版。工程13A/Bは非採用。最大の差は、滑らかで長いS字体幹＋腕＋別房という全体の組立て。材質追加では解けない。幹/枝の不等な量塊と短い接続面を手動の共有meshで設計し、葉群/鉢と同時に全景低詳細ゲートを通す。graph+taper+voxelの係数反復を止める。工程12性能を保持。

1. 添付写真の実ピクセルとwhole sceneを再確認し、根/第一主枝/樹冠下端/大きい空隙/鉢比率を一枚の低詳細3D配置として決める。302px写真の手読み比率は概略、3D実測とは扱わない。
2. 今回のgraphは階層位置の編集sourceとして使えるが、tangent contourの自動unionをもう繰り返さない。低い太い幹の前後面・短いbranch fan face・複数の非対称量塊を一つの編集meshとして手動でつなぐ。中央左の段/差し込みと楔根を最初に排除。control mesh/face hierarchyを保存、orphan/zero-area/閉成分/接続も検査。
3. 上部群と左群の厚み/前後重なり、小さい従属右群、鉢/土/台を同時に全景で見る。裸幹だけの成功を採用根拠にしない。PC390320/単色front55°を独立判定、明確な改善が出た時だけdirectionUV/rough bark/nativeを仕上げる。
4. 予算はclosed葉LODと工程12load-pcf8-v1を保持。通常定常tri1.204M以下、外部3.8MB程度、低速3D22秒以内、GPU p95PC39015ms以下を目安。現在bundle分割+2405B/鮮明still遅延を結果に残す。改善がない構造をデータ量やtestsで完成と呼ばない。
5. 動作は短い実record/same-pose一致を保存済み。次にLOD境界を跨ぐ操作と全rate時間aliasingを具体的に検査するなら必要な条件を一回だけ追加し、長時間/実機未検証を維持。通常idleは止め、reduced/fallbackを保護。

保護: 正式新規runのみ。旧exfract-bonsai変更禁止、既存11状態/成果/Git/全55profilesを維持。新nativeは最良一件だけ、immutable assets/selected nativeは読取reference。新規100MiB/空き2GiB。Library再試行/新profile/無承認削除/有料購入/公開/Git書込み/automationなし。Sol/xhigh指定と実metadata未検証を区別。親が10/10 23JSTまで判断する。第三案をこの工程では作らない。
