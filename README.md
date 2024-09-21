# TochiCalc

測量図などのデータを使って、間口距離・奥行距離・想定整形地を計算するＥｘｃｅｌシートです。
 
## 入力

測量図の測点の座標を、Ｃ列、Ｄ列に入力します。

測点の名称をＡ列に入力します。

測点が多い場合は、7行目～12行目に行を追加します。

測点が少ない場合は、7行目～１２行目の行を削除します。

６行目、１３行目の行は削除しません。

間口の両端の測点の名称を、B34,B35に入力します。

## 計算結果

### 面積

B26 に表示されます。

面積の計算が不要な場合は、測点の一部を除いて入力しても良いです。

###  間口距離

C29 に表示されます。

B34,B35に入力した間口の両端の測点の間の距離です。

### 奥行距離

C39 に表示されます。

間口から、（垂直距離で）一番遠い測点（B38に名称を表示）の垂直距離を奥行距離とします。

### 想定整形地

間口に対して、左右（？）に一番はみ出している測点（B45,B46に名称を表示）を探します。

想定整形地の間口距離をC42に表示します。

## 縮尺

未記載

## 測点の入力の省略

概算で良ければ、近接している測点の入力を省略しても良いです。

奥行距離の計算だけならば、間口の両端２点と一番深いと思われる数点の入力だけでも良いです。

想定整形地の間口距離の計算だけならば、間口の両端２点と左右にそれぞれ一番はみ出していると思われる数点の入力だけでも良いです。

## 登記所備付地図データ

[法務省登記所備付地図データ](https://front.geospatial.jp/moj-chizu-xml-download/)には、各土地の各点の座標が含まれているので、このデータを利用することができます。

[Simaplotというソフトで見る](https://shoshinsha-kakeizu.hatenablog.com/entry/2023/01/31/190751)ことができます。

データの中には縮尺等が未設定のものがあるようです。その場合は上記の縮尺を設定します。

## xmlpoint.py

登記所備付データから、指定された土地の各点の座標を出力するプログラムです。

~~土地の指定を誤って、離れた土地を指定すると、永久ループするバグがあります（2024/9/21修正済み）~~

~~１２行目~~１６行目のstr_file_nameに、ダウンロードしたxmlファイル名を記載します。

~~１３行目~~１７行目のlist_chibanに、大字名・丁目名・地番を指定します。隣接する土地を複数指定することもできます。

指定された土地の各点の名称とX座標・Y座標を出力します。

指定された土地と土地の間の点は、除外しています。

## point.py

指定したjpgファイルを表示し、マウスクリックした座標を出力するプログラムです。

建物平面図などしかない場合に使います。

## 注意事項

上記の行数、セルは、測点の行を追加、削除する前の行数です。
