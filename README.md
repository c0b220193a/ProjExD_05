# アニマル大戦争
## 実行環境の必要条件
* python >= 3.10
* pygame >= 2.1

## ゲームの概要
にゃんこ大戦争からインスピレーションを受けたタワーディフェンスゲーム<br>
アニマルを出撃させて敵情を落とす<br><br>
(1キー) :ねこ　250円のユニット 量産できる 1のキーで出撃させる<br>
(2キー) :キリン　1200円のユニット　長射程から攻撃できる　２のキーで出撃される<br><br>
(Qキー：お財布アップグレード)<br>
レベル1　700円でレベル２にアップグレードできる　Qキーを押すことでアップグレードできる<br>
レベル2 1500円でレベル３にアップグレードできる　Qキーを押すことでアップグレードできる<br>
レベル3 上限4500円<br>
(Spaceキー)：一度だけ使うことができるビームを発射する

## ゲームの実装
###共通基本機能
* 城の生成
*背景の設定
### 担当追加機能
* 味方を追加する(担当：岩田)<br>ねこ　250円のユニット 量産できる 1のキーで出撃させる<br>キリン　1200円のユニット　長射程から攻撃できる　２のキーで出撃される
* 敵の追加(担当：平松)<br>敵がランダムに複数な種類で出力される（ランダムな時間で出てくる。キャラクターごとにステータスは異なる。）<br>敵城体力が1500以下になるとボスが出力される。
* 砲台の追加(担当：大柳)<br>一度だけ使えるビームを発射する スペースキーを押すことで大砲を使うことができる。
* お金機能の追加(担当：五十嵐)<br>レベル1　700円でレベル２にアップグレードできる　Qキーを押すことでアップグレードできる<br>レベル2 1500円でレベル３にアップグレードできる　Qキーを押すことでアップグレードできる<br>レベル3 上限4500円
* 敵と味方の城のhpが0になったとき段階的に爆発し崩壊する。(担当：森上)<br>→ゲームオーバーとゲームクリアの文字が出てゲームが終了する。
### ToDo
### メモ
* 城からビームを出す
