import argparse

import pynotificator


def beep_notify():
    parser = argparse.ArgumentParser(description='Beep Notification')
    parser.add_argument('--times', '-t', type=int, default=1,
                        help='The number of times of beep sound')
    args = parser.parse_args()

    bn = pynotificator.BeepNotification(args.times)
    bn.notify()


def desktop_notify():
    parser = argparse.ArgumentParser(description='Desktop Notification')
    parser.add_argument('--message', '-m', default='PyNotificator',
                        help='Content of notice')
    parser.add_argument('--title', '-t', default='',
                        help='Title of notice')
    parser.add_argument('--subtitle', '-s', default='',
                        help='Subtitle of notice')
    parser.add_argument('--icon', '-i', default='',
                        help='Icon of notice')
    parser.add_argument('--nosound', action='store_true',
                        help='Disable notification sound')
    args = parser.parse_args()

    dn = pynotificator.DesktopNotification(
        args.message, args.title, args.subtitle, args.icon, not args.nosound)
    dn.notify()


def slack_notify():
    parser = argparse.ArgumentParser(description='Slack Notification')
    parser.add_argument('--message', '-m', default='PyNotificator',
                        help='Content of notice')
    parser.add_argument('url', help='Incoming Webhook URL')
    args = parser.parse_args()

    sn = pynotificator.SlackNotification(args.message, args.url)
    sn.notify()


def discord_notify():
    parser = argparse.ArgumentParser(description='Discord Notification')
    parser.add_argument('--message', '-m', default='PyNotificator',
                        help='Content of notice')
    parser.add_argument('url', help='Discord Webhook URL')
    args = parser.parse_args()

    dn = pynotificator.DiscordNotification(args.message, args.url)
    dn.notify()


def line_notify():
    parser = argparse.ArgumentParser(description='Line Notification')
    parser.add_argument('--message', '-m', default='PyNotificator',
                        help='Content of notice')
    parser.add_argument('token', help='LINE Notify token')
    args = parser.parse_args()

    ln = pynotificator.LineNotification(args.message, args.token)
    ln.notify()
