import json
import platform
import subprocess
import time

import requests


class NotificationError(Exception):
    '''通知エラークラス

    通知に関するエラーを示す。
    '''
    pass


class BaseNotification:
    '''通知基底クラス

    通知を行うクラスの基底クラスとなる。
    '''
    def set_typed_variable(self, value, specified_type):
        '''型を確認して返す関数

        指定された型であればそのまま返し、異なれば NotificationError を返す。

        Args:
            value (Object): 確認対象の値
            specified_type (Object): 指定の型

        Returns:
            Object: 型を確認した値

        Raises:
            NotificationError: 型が一致しない場合に発生する

        Examples:
            >>> number = set_typed_variable(3, int)
            >>> number
            3
            >>> string = set_typed_variable('3', int)
            NotificationError: can only set int (not "str")
        '''
        if isinstance(value, specified_type):
            return value
        else:
            raise NotificationError(
                'can only set '
                f'{specified_type.__name__} '
                f'(not "{value.__class__.__name__}")'
            )

    # Main
    def notify(self):
        '''通知を行う関数

        実装は継承先のクラスで行う。

        Raises:
            NotImplementedError: 実装が行われていない場合に発生する
        '''
        raise NotImplementedError()


class OSSpecificNotification(BaseNotification):
    '''OS ごとの通知を行うクラス

    darwin(macOS) と Linux と Window をサポートしている。

    Attributes:
        system (str): 使用中の OS
    '''
    def __init__(self):
        '''コンストラクタ

        OS の判定を行う。
        '''
        self.system = platform.system()

    def darwin_notify(self):
        '''macOS 用の通知を行う関数

        Raises:
            NotImplementedError: 実装が行われていない場合に発生する
        '''
        raise NotImplementedError()

    def linux_notify(self):
        '''Linux 用の通知を行う関数

        Raises:
            NotImplementedError: 実装が行われていない場合に発生する
        '''
        raise NotImplementedError()

    def windows_notify(self):
        '''Windows 用の通知を行う関数

        Raises:
            NotImplementedError: 実装が行われていない場合に発生する
        '''
        raise NotImplementedError()

    def notify(self):
        '''通知を行う関数

        Raises:
            NotificationError: サポート外の OS を使用した場合に発生する
        '''
        if self.system == 'Darwin':
            self.darwin_notify()
        elif self.system == 'Linux':
            self.linux_notify()
        elif self.system == 'Windows':
            self.windows_notify()
        else:
            NotificationError(f'{self.system} is not supported system')


class MessageNotification(BaseNotification):
    '''メッセージを伴う通知を行うクラス

    デスクトップ通知や SNS など、メッセージを打ち込める場合に使用する。

    Attributes:
        message (str): メッセージ本文
    '''
    def __init__(self, message):
        '''コンストラクタ

        メッセージの設定を行う。

        Args:
            message (str): メッセージ本文
        '''
        self._message = None
        self.set_message(message)

    def get_message(self):
        return self._message

    def set_message(self, message):
        self._message = self.set_typed_variable(message, str)

    message = property(get_message, set_message)


class WebhookNotification(MessageNotification):
    '''Webhook による通知を行うクラス

    主に SNS 向けに Webhook を用いた通知を行う場合に使用する。

    Attributes:
        url (str): Webhook の URL
    '''
    def __init__(self, message, url):
        '''コンストラクタ

        Args:
            message (str): メッセージ本文
            url (str): Webhook の URL
        '''
        super().__init__(message)
        self._url = None
        self.set_url(url)

    def get_url(self):
        return self._url

    def set_url(self, url):
        self._url = self.set_typed_variable(url, str)

    url = property(get_url, set_url)


class TokenNotification(MessageNotification):
    '''トークンによる通知を行うクラス

    トークン認証の API を用いた通知を行う場合に使用する。

    Attributes:
        token (str): トークン
    '''
    def __init__(self, message, token):
        '''コンストラクタ

        Args:
            message (str): メッセージ本文
            token (str): トークン
        '''
        super().__init__(message)
        self._token = None
        self.set_token(token)

    def get_token(self):
        return self._token

    def set_token(self, token):
        self._token = self.set_typed_variable(token, str)

    token = property(get_token, set_token)


class BeepNotification(OSSpecificNotification):
    '''ビープ音による通知を行うクラス

    OS 標準のビープを用いた通知を行う場合に使用する。

    Attributes:
        times (int): 通知回数

    Examples:
        通常使用
        >>> bn = BeepNotification(3)
        >>> bn.notify()

        通知回数の変更
        >>> bn.times = 1
        >>> bn.notify()

        コマンドラインツール
        $ beep-notify [-h] [--times TIMES]
    '''
    def __init__(self, times):
        '''コンストラクタ

        Args:
            times (int): 通知回数
        '''
        super().__init__()
        self._times = None
        self.set_times(times)

    def get_times(self):
        return self._times

    def set_times(self, times):
        self._times = self.set_typed_variable(times, int)

    times = property(get_times, set_times)

    def darwin_notify(self):
        cmd = ['osascript', '-e', f'beep {self._times}']
        subprocess.run(cmd)

    def linux_notify(self):
        for _ in range(self._times):
            cmd = ['xkbbell']
            subprocess.run(cmd)
            time.sleep(0.5)

    def windows_notify(self):
        for _ in range(self._times):
            cmd = ['rundll32', 'user32.dll,MessageBeep']
            subprocess.run(cmd)
            time.sleep(0.5)


class CenterNotification(MessageNotification, OSSpecificNotification):
    '''デスクトップ通知を行うクラス

    macOS の通知センタ、 Linux のポップアップ通知、 Windows のトースト通知を行う。

    Attributes:
        title (str): タイトル
        subtitle (str): サブタイトル
        icon (str): アイコン
        sound (bool): 音の有無

    Examples:
        通常使用
        >>> cn = CenterNotification('本文', title='タイトル', subtitle='サブタイトル')
        >>> cn.notify()

        通知の変更
        >>> cn.message = '内容変更'
        >>> cn.notify()

        コマンドラインツール
        $ center-notify [-h] [--message MESSAGE] [--title TITLE]
                        [--subtitle SUBTITLE] [--nosound]
    '''
    def __init__(self, message, title=None, subtitle=None,
                 icon=None, sound=True):
        '''コンストラクタ

        Args:
            message(str): 本文
            title(str): タイトル
            subtitle(str): サブタイトル
            icon(str): アイコン
            sound(bool): 音の有無
        '''
        MessageNotification.__init__(self, message)
        OSSpecificNotification.__init__(self)
        self._title = None
        self._subtitle = None
        self._icon = None
        self._sound = None
        if title:
            self.set_title(title)
        if subtitle:
            self.set_subtitle(subtitle)
        if icon:
            self.set_icon(icon)
        if sound:
            self.set_sound(sound)

    def get_title(self):
        return self._title

    def set_title(self, title):
        self._title = self.set_typed_variable(title, str)

    title = property(get_title, set_title)

    def get_subtitle(self):
        return self._subtitle

    def set_subtitle(self, subtitle):
        self._subtitle = self.set_typed_variable(subtitle, str)

    subtitle = property(get_subtitle, set_subtitle)

    def get_icon(self):
        return self._icon

    def set_icon(self, icon):
        self._icon = self.set_typed_variable(icon, str)

    icon = property(get_icon, set_icon)

    def get_sound(self):
        return self._sound

    def set_sound(self, sound):
        self._sound = self.set_typed_variable(sound, bool)

    sound = property(get_sound, set_sound)

    def darwin_notify(self):
        _message = f'display notification \"{self._message}\"'
        _title = ''
        if self._title:
            _title += f'with title \"{self._title}\" '
        if self._subtitle:
            _title += f'subtitle \"{self._subtitle}\"'
        _sound = 'sound name \"\"' if self._sound else ''
        cmd = ['osascript', '-e', f'{_message} {_title} {_sound}']
        subprocess.run(cmd)

    def linux_notify(self):
        if self._title and self._subtitle:
            _title = f'{self._title} - {self._subtitle}'
        elif self._title:
            _title = self._title
        elif self._subtitle:
            _title = self._subtitle
        else:
            _title = ' '
        cmd = ['notify-send', _title, self._message]
        if self._icon:
            cmd.extend(['-i', self._icon])
        subprocess.run(cmd)

    def windows_notify(self):
        from win10toast import ToastNotifier
        toaster = ToastNotifier()
        if self._title and self._subtitle:
            _title = f'{self._title} - {self._subtitle}'
        elif self._title:
            _title = self._title
        elif self._subtitle:
            _title = self._subtitle
        else:
            _title = None
        toaster.show_toast(_title,
                           self._message,
                           icon_path=self._icon,
                           duration=5)


class SlackNotification(WebhookNotification):
    '''Slack による通知を行うクラス

    Slack API を用いて通知を行う。

    Examples:
        通常使用
        >>> sn = SlackNotification('本文', 'https://hooks.slack.com/xxx')
        >>> sn.notify()

        通知の変更
        >>> sn.message = '本文変更'
        >>> sn.notify()

        コマンドラインツール
        $ slack-notify [-h] [--message MESSAGE] url
    '''

    def notify(self):
        '''通知を行う関数

        '''
        data = {'text': self._message}
        requests.post(self._url, data=json.dumps(data))


class DiscordNotification(WebhookNotification):
    '''Discord による通知を行うクラス

    Discord Webhook を用いて通知を行う。

    Examples:
        通常使用
        >>> dn = DiscordNotification('本文', 'https://discordapp.com/xxx')
        >>> dn.notify()

        通知の変更
        >>> dn.message = '本文変更'
        >>> dn.notify()

        コマンドラインツール
        $ discord-notify [-h] [--message MESSAGE] url
    '''

    def notify(self):
        '''通知を行う関数

        '''
        data = {'content': self._message}
        requests.post(
            self._url,
            headers={'Content-Type': 'application/json'},
            data=json.dumps(data)
        )


class LineNotification(TokenNotification):
    '''LINE による通知を行うクラス

    LINE Notify を用いて通知を行う。

    Examples:
        通常使用
        >>> dn = DiscordNotification('本文', 'https://discordapp.com/xxx')
        >>> dn.notify()

        通知の変更
        >>> dn.message = '本文変更'
        >>> dn.notify()

        コマンドラインツール
        $ discord-notify [-h] [--message MESSAGE] url
    '''

    def __init__(self, message, token):
        '''コンストラクタ

        Args:
            message(str): メッセージ本文
            token(str): トークン
        '''
        super().__init__(message, token)
        self.URL = 'https://notify-api.line.me/api/notify'

    def notify(self):
        '''通知を行う関数

        '''
        headers = {'Authorization': f'Bearer {self._token}'}
        params = {'message': self._message}
        requests.post(
            self.URL,
            headers=headers,
            params=params
        )
