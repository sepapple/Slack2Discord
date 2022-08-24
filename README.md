# Slack2Discord

SlackからエクスポートしたJSONファイルをDiscordへインポートする。

## 使用方法
ローカル環境においてSlack2Discord.pyを実行することで、サーバに参加しているDiscordのBotが起動する。
この状態において、Discordの任意のテキストチャンネルで```:import```を入力することで、エクスポートしたSlackのファイル群をDiscordへインポートする。

## 前提条件
### Botの作成
- [Bot導入手法](https://discordpy.readthedocs.io/ja/latest/discord.html)のサイトを参考にBotを作成し、自身のサーバに招待する。
  - どの権限が必須かを検証できていないため、多めに権限を付与しておく方が良い
  - 招待方法はURLを作成後、そのURLをブラウザに打ち込めば、招待画面が現れる。
-
### 実行環境構築と実行方法
1. ```git clone git@github.com:sepapple/Slack2Discord.git```で、ディレクトリをローカル環境にclone
2. ```python3 -m venv <dir-path>/```による仮想環境の構築
3. ```source <dir-path>/bin/activate```で、仮想環境に入る
4. ```pip3 install -r requirements.txt```で、ライブラリをインストール
5. Slack2Discrod.pyの7行目のtokenをBot作成時に作成したものに変更
7. Slack2Discrod.pyの8行目のdir_pathをエクスポートしたディレクトリのパスを指定
6. ```python3 Slack2Discord.py or pymon Slack2Discord.py(開発用)```で、プログラム起動
7. ```deactivate```で、仮想環境から抜ける

## 開発用
- ```:delete```と入力することで、初期に存在するチャンネルのみの状態にすることが出来る(不要なチャンネルの全削除)

 
