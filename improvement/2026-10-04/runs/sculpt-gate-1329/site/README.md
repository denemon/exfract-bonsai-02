# 実3D盆栽・工程1の検証用候補

完成作品ではありません。連続した幹・主要枝、枝に基づく立体の葉、代表素材を検証する候補です。保護対象の09bestは置き換えていません。外観の合否とブラウザ検証の合否は、親ディレクトリの `REPORT.md` に分けて記録します。

## ローカル実行

このディレクトリで `npm run dev`、または `npm run build` → `npm run preview`。確認先は `http://127.0.0.1:5188/`。既に同じ候補のサーバーが稼働している場合は二重起動しません。依存関係はThree.js 0.185.1とVite 8.2.2です。

画面に可視文字やメニューはありません。通常表示は実際の立体をWebGL2で描画します。読み込み中・WebGL2不可・コンテキスト喪失時には、同じ候補のブラウザ描画から保存した静止画を表示します。生成した写真調の参考画像はランタイムの背景や代替表示には使いません。

PCは正面、縦画面は左側からの別カメラです。ドラッグによる小さな角度変更だけを許可し、常時の描画ループはありません。`prefers-reduced-motion: reduce` ではドラッグによる動きも抑えます。縦長320px画面では樹冠全体を収めると盆栽の占有率が低くなるため、構図の完成判定は未達です。

## 検証用表示

- `?study=clay&bare=1`：葉を非表示にした単色の幹・枝。
- `?study=clay&bare=1&yaw=25` / `yaw=-25`：斜めからの形状。
- `?study=clay&bare=1&reference=previous`：失敗した旧モデルとの比較。
- `?study=material`：中立色の背景と照明で素材を確認。
- `?study=material&detail=wood` / `leaf` / `pot`：代表素材の拡大。
- `?study=normals&detail=wood`：法線を確認。

これらは制作確認用です。製品画面にはリンクやラベルを出しません。

## ソースとモデル

`src/main.js` は読み込み・実形状からのカメラ調整・入力・代替表示、`src/materials.js` は素材ごとのPBRシェーダー拡張、`src/scene.js` は照明と建築の仮配置です。背景の庭・植栽・砂利・建築素材は未完成です。

`../sculpt/generate.py`、`foliage.py`、`support.py` はBlender用の元コードです。主要な幹・枝・根は同じ連続面に統合し、生き筋はその面上の材質属性で分けています。葉は小枝の階層から配置した立体の鱗葉で、12種類のメッシュをGPUインスタンシングします。Blenderの材質は簡易プレビュー用で、ウェブの詳細シェーダーはJavaScript側にあります。

再生成は新しいバージョン名を使います。

```sh
/Applications/Blender.app/Contents/MacOS/Blender --background --factory-startup --python-exit-code 1 --python ../sculpt/generate.py -- --out ../models --version next-study --foliage
```

Blender座標の長さに0.66を掛けてウェブ空間へ配置しています。鉢幅は約1.06m、台から樹冠まで約1.5mです。背面や隠れた枝は参考画像から確定できないため推定造形です。途中版のBlenderファイルが `.blend.gz` で保存されている場合は、別の宛先へ展開して開いてください。圧縮前後の一致はアーカイブ記録で検証します。

## 検証

`npm run capture` はMacのChromeで比較画像を保存します。`npm run verify` はPC・390px・320px、文字・切れ・はみ出し、動き低減、WebGL不可、コンテキスト復旧、低速読み込みを確認します。ブラウザは専用の一時プロファイルで起動し、終了時にそのプロファイルを削除します。

性能値は同じMac上の測定です。スマホ幅やDPRのエミュレーションは、実Android・iPhoneのGPUやメモリを再現しません。ブラウザテストの成功を、造形や景色が完成した根拠にはしません。
