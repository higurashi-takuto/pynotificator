import json
import platform
import subprocess
import time

import requests


class NotificationError(Exception):
    pass


class BaseNotification:
    def set_typed_variable(self, value, specified_type):
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
        raise NotImplementedError()


class OSSpecificNotification(BaseNotification):
    '''
    OSSpecificNotification:
        OS ごとの通知
    '''
    def __init__(self):
        self.system = platform.system()

    # macOS 用の通知
    def darwin_notify(self):
        raise NotImplementedError()

    # Linux 用の通知
    def linux_notify(self):
        raise NotImplementedError()

    # Windows 用の通知
    def windows_notify(self):
        raise NotImplementedError()

    # 通知の実行
    def notify(self):
        if self.system == 'Darwin':
            self.darwin_notify()
        elif self.system == 'Linux':
            self.linux_notify()
        elif self.system == 'Windows':
            self.windows_notify()
        else:
            NotificationError(f'{self.system} is not supported system')


class MessageNotification(BaseNotification):
    '''
    MessageNotification:
        メッセージを打ち込める通知
    引数:
        message(str): 本文
    '''
    def __init__(self, message):
        self._message = None
        self.set_message(message)

    # message のプロパティ用
    def get_message(self):
        return self._message

    def set_message(self, message):
        self._message = self.set_typed_variable(message, str)

    message = property(get_message, set_message)


class WebhookNotification(MessageNotification):
    '''
    WebhookNotification:
        Webhook による通知
    引数:
        message(str): 本文
        url(str): Webhook の URL
    '''
    def __init__(self, message, url):
        super().__init__(message)
        self._url = None
        self.set_url(url)

    # url のプロパティ用
    def get_url(self):
        return self._url

    def set_url(self, url):
        self._url = self.set_typed_variable(url, str)

    url = property(get_url, set_url)


class TokenNotification(MessageNotification):
    '''
    TokenNotification:
        Token による通知
    引数:
        message(str): 本文
        token(str): トークン
    '''
    def __init__(self, message, token):
        super().__init__(message)
        self._token = None
        self.set_token(token)

    # token のプロパティ用
    def get_token(self):
        return self._token

    def set_token(self, token):
        self._token = self.set_typed_variable(token, str)

    token = property(get_token, set_token)


class BeepNotification(OSSpecificNotification):
    '''
    BeepNotification:
        ビープ音による通知
    引数:
        times(int): ビープ音の回数
    '''
    def __init__(self, times):
        super().__init__()
        self._times = None
        self.set_times(times)

    # times のプロパティ用
    def get_times(self):
        return self._times

    def set_times(self, times):
        self._times = self.set_typed_variable(times, int)

    times = property(get_times, set_times)

    # 通知の実行
    def darwin_notify(self):
        cmd = ['osascript', '-e', f'beep {self._times}']
        subprocess.run(cmd)

    def linux_notify(self):
        for _ in range(self._times):
            cmd = ['xkbbell']
            time.sleep(0.5)
            subprocess.run(cmd)


class CenterNotification(MessageNotification):
    '''
    CenterNotification:
        通知センターによる通知
    引数:
        message(str): 本文
        title(str): タイトル
        subtitle(str): サブタイトル
        sound(bool): 音の有無
    '''
    def __init__(self, message, title=None, subtitle=None, sound=True):
        super().__init__(message)
        self._title = None
        self._subtitle = None
        self._sound = None
        if title:
            self.set_title(title)
        if subtitle:
            self.set_subtitle(subtitle)
        if sound:
            self.set_sound(sound)

    # title のプロパティ用
    def get_title(self):
        return self._title

    def set_title(self, title):
        self._title = self.set_typed_variable(title, str)
        # タイトルとサブタイトルの両方がないといけないため、
        # 片方だけ設定された場合、もう一方を空白にする
        if not self._subtitle:
            self._subtitle = ' '

    title = property(get_title, set_title)

    # subtitle のプロパティ用
    def get_subtitle(self):
        return self._subtitle

    def set_subtitle(self, subtitle):
        self._subtitle = self.set_typed_variable(subtitle, str)
        # タイトルとサブタイトルの両方がないといけないため、
        # 片方だけ設定された場合、もう一方を空白にする
        if not self._title:
            self._title = ' '

    subtitle = property(get_subtitle, set_subtitle)

    # sound のプロパティ用
    def get_sound(self):
        return self._sound

    def set_sound(self, sound):
        self._sound = self.set_typed_variable(sound, bool)

    sound = property(get_sound, set_sound)

    # 通知の実行
    def notify(self):
        _message = f'display notification \"{self._message}\"'
        _title = \
            f'with title \"{self._title}\" subtitle \"{self._subtitle}\"' \
            if self._title and self._subtitle else ''
        _sound = 'sound name \"\"' if self._sound else ''
        cmd = ['osascript', '-e', f'{_message} {_title} {_sound}']
        subprocess.run(cmd)


class SlackNotification(WebhookNotification):
    '''
    SlackNotification:
        Slack による通知
    引数(WebhookNotification):
        message(str): 本文
        url(str): Incoming Webhook の URL
    '''
    # 通知の実行
    def notify(self):
        data = {'text': self._message}
        requests.post(self._url, data=json.dumps(data))


class DiscordNotification(WebhookNotification):
    '''
    DiscordNotification:
        Discord による通知
    引数(WebhookNotification):
        message(str): 本文
        url(str): Discord の Webhook の URL
    '''
    # 通知の実行
    def notify(self):
        data = {'content': self._message}
        requests.post(
            self._url,
            headers={'Content-Type': 'application/json'},
            data=json.dumps(data)
        )


class LineNotification(TokenNotification):
    '''
    LineNotification:
        Line による通知
    引数:
        message(str): 本文
        token(str): LINE Notify のトークン
    '''
    def __init__(self, message, token):
        super().__init__(message, token)
        self.URL = 'https://notify-api.line.me/api/notify'

    # 通知の実行
    def notify(self):
        headers = {'Authorization': f'Bearer {self._token}'}
        params = {'message': self._message}
        requests.post(
            self.URL,
            headers=headers,
            params=params
        )
