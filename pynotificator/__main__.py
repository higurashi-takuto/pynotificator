import argparse

import pynotificator


def beep_notify():
    parser = argparse.ArgumentParser(description='ビープ音を鳴らす')
    parser.add_argument('--times', '-t', type=int, default=1,
                        help='ビープ音を鳴らす回数')
    args = parser.parse_args()

    bn = pynotificator.BeepNotification(args.times)
    bn.notify()


def center_notify():
    parser = argparse.ArgumentParser(description='通知を飛ばす')
    parser.add_argument('--message', '-m', default='PyNotificator',
                        help='通知の内容')
    parser.add_argument('--title', '-t', default='',
                        help='通知のタイトル')
    parser.add_argument('--subtitle', '-s', default='',
                        help='通知のサブタイトル')
    parser.add_argument('--nosound', action='store_true',
                        help='通知音を無効化')
    args = parser.parse_args()

    cn = pynotificator.CenterNotification(
        args.message, args.title, args.subtitle, not args.nosound)
    cn.notify()


def slack_notify():
    parser = argparse.ArgumentParser(description='Slack に通知をする')
    parser.add_argument('--message', '-m', default='PyNotificator',
                        help='通知の内容')
    parser.add_argument('url', help='Incoming Webhook の URL')
    args = parser.parse_args()

    sn = pynotificator.SlackNotification(args.message, args.url)
    sn.notify()


def discord_notify():
    parser = argparse.ArgumentParser(description='Discord に通知をする')
    parser.add_argument('--message', '-m', default='PyNotificator',
                        help='通知の内容')
    parser.add_argument('url', help='Discord の Webhook の URL')
    args = parser.parse_args()

    dn = pynotificator.DiscordNotification(args.message, args.url)
    dn.notify()


def line_notify():
    parser = argparse.ArgumentParser(description='Line に通知をする')
    parser.add_argument('--message', '-m', default='PyNotificator',
                        help='通知の内容')
    parser.add_argument('token', help='LINE Notify のトークン')
    args = parser.parse_args()

    ln = pynotificator.LineNotification(args.message, args.token)
    ln.notify()
