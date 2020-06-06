<div align="center"><img src="https://raw.githubusercontent.com/higurashi-takuto/pynotificator/master/assets/logo.svg" alt="PyNotificator logo" width="30%"></div>
<h4 style="text-align: center;">Python / コマンドラインから様々な通知を簡単に送るためのライブラリ</h4>

## 概要
実行時間の長いプログラムなどの実行時、

- 「 **Slack で受け取れたらな〜** 」
- 「 **音鳴らしてくれたらな〜** 」
- 「 **通知飛ばしてくれればな〜** 」

と思ったことはありませんか？

<h4>それ、できます。<br>そう、PyNotificator ならね。</h4>

PyNotificator は Python のプログラム / コマンドラインからビープ音・通知センター、Slack、Discord、LINE にメッセージを簡単に送信できるライブラリです。

## インストール
このリポジトリを以下のコマンドでインストールします。動作環境は `Python >= 3.6` です。

```shell
pip install pynotificator
```

## 使い方
### コマンドラインツール
#### ビープ音
```shell
$ beep-notify [-h] [--times TIMES]
```

#### 通知
```shell
$ center-notify [-h] [--message MESSAGE] [--title TITLE]
                [--subtitle SUBTITLE] [--nosound]
```

#### Slack
```shell
$ slack-notify [-h] [--message MESSAGE] url
```

#### Discord
```shell
$ discord-notify [-h] [--message MESSAGE] url
```

#### LINE
```shell
$ line-notify [-h] [--message MESSAGE] token
```

### Python
#### インポート
使用するクラスのみをインポートすることを推奨します。

```python
# ビープ音を使用したい場合
from pynotificator import BeepNotification
```

#### macOS、Linux のビープ音
お使いの Mac、LinuxPC から音を出せます。

```python
# 引数は音を鳴らす回数です。
bn = BeepNotification(3)
bn.notify()
```

#### macOS 通知センター
お使いの Mac に通知を送れます。

```python
cn = CenterNotification('本文', title='タイトル', subtitle='サブタイトル', sound=True)
cn.notify()
```

実行サンプル

<img src="https://raw.githubusercontent.com/higurashi-takuto/pynotificator/master/assets/center-sample.png" alt="CenterNotification Sample" width="30%">

#### Slack
Slack の Incoming Webhook を利用し、メッセージを送信します。
[Slack API](https://api.slack.com/apps) より、Webhook 用の URL を取得してください。

```python
sn = SlackNotification('本文', 'https://hooks.slack.com/services/xxx')
sn.notify()
```

#### Discord
Discord の Webhook を利用し、メッセージを送信します。
サーバー設定 > ウェブフック より、Webhook 用の URL を取得してください。

```python
dn = DiscordNotification('本文', 'https://discordapp.com/api/webhooks/xxx')
dn.notify()
```

#### LINE
LINE Notify を利用し、メッセージを送信します。
[LINE Notify](https://notify-bot.line.me/) からトークンを発行してください。

```python
ln = LineNotification('本文', 'xxx')
ln.notify()
```

## クラス図
![クラス図](https://raw.githubusercontent.com/higurashi-takuto/pynotificator/master/assets/classes.png)

## ライセンス
[MIT License](https://raw.githubusercontent.com/higurashi-takuto/pynotificator/master/LICENSE)

## 作成者
[higurashi-takuto](https://hgrs.me/)
