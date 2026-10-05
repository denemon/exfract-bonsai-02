# 自然石の素材と編集原本

[Boulder01](https://polyhaven.com/a/boulder_01) — Rico Cilliers。 [Rock09](https://polyhaven.com/a/rock_09) — Jenelle van Heerden。 [Poly Haven asset license](https://polyhaven.com/license) はCC0。無料の公開素材を使用し、購入はありません。クレジットはこの制作記録に置き、サイト画面に文字を追加していません。

正規APIが返すURLから取得したglTF/bin/1k JPEGを assets/source に保持。総7,736,407B。各URL/size/MD5/SHA256は assets/provenance.json。サイトはローカルの変換済みモデルと素材だけを読むため、実行時にPoly Haven APIへ接続しません。

assets/editable/*.blend は形状とUVの編集原本。元PBR材質付きglTFは assets/source。runtimeは site/public/rocks の2GLB/6WebP。2つで35,416tri、GLB204,904B、maps1,553,346B、計1,758,250B。色/法線1024、ARM512lossless。元JPEGは保持。

最初の変換ではUV分割頂点のまま簡略化し、破れた面が生じました。qa/space-v2 と qa/stone-diagnosis は失敗診断として保持。頂点を同一位置で連結し面法線を再計算してから簡略化した最終形状は境界edge0。qa/rock-conversion-diagnosis.json に前後の数値を保存。バグのある画像は最終成果画像に使用していません。

安全な再生成は新しい空の出力先を指定します。

```sh
/Applications/Blender.app/Contents/MacOS/Blender --background --python-exit-code 1 --python site/scripts/prepare_rock_geometry.py -- --output /tmp/bonsai-rock-geometry-new
python3 site/scripts/convert_rock_maps.py --output /tmp/bonsai-rock-maps-new
```

原本と最終変換ファイルのhash、閉じた形状、実Chromeの表示を検証。上記パラメータ化した再生成コマンド全体の再実行/出力バイト一致は未検証です。地面の再生成は別途3出力のバイト一致まで確認済みです。assets/rock-conversion-recipe.py は成功時の正確な作業記録で、既存出力を上書きするため再実行用には使わないでください。
