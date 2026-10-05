# ローカルの文字なし3D候補

確認URL http://127.0.0.1:5214/ 。現在は最終buildを配信中。高い塀・実体のある前障子・夜空のR20を暫定全景bestに選び、premium完成は未達。

このフォルダーで `npm run preview` または `npm run dev`。両方とも127.0.0.1:5214なので同時起動しない。formal rootのnode_modulesと、同じ改善workspaceの既存モデル/木材質/Draco/地形をread-onlyで参照する。dist単独のportable exportではない。

通常は灰褐色/茶褐色の固定hero、dry shoji紙、空間hash木目、主役8/背景4sample shadowの条件。主役モデル/木UV/材質/灯は固定。常時animationなし、入力時だけ小さな視差。reduced motionと五比率の同じ完成実景stillを読込中/WebGL不可/context lossへ同期。

上位RESULT.md/comparison-final.html/qa/verification-summary.jsonを参照。PC/390/320/tall/wide/RetinaのactualMac Chrome表示、12functionalcasesは成功。実機スマホ/Safari/熱負荷は未検証。古木・植栽・砂利・スマホ競合・Retina tail/cold11.78秒は課題。サイト画面に文字を表示しない。
