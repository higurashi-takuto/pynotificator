import json
import platform
import subprocess
import time

import requests

from ._version import __version__   # noqa: F401


class NotificationError(Exception):
    '''Notification Error'''
    pass


class BaseNotification:
    '''Notification Superclass'''
    def set_typed_variable(self, value, specified_type):
        '''Check the type and return it.

        Args:
            value (Object): Value to check
            specified_type (Object): Specified type of value

        Returns:
            Object: Checked value

        Raises:
            NotificationError: When the types don’t match.

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
        '''Executing the notification

        Raises:
            NotImplementedError: When there is no implementation
        '''
        raise NotImplementedError()


class OSSpecificNotification(BaseNotification):
    '''OS-specific notifications

    Attributes:
        system (str): OS you are using
    '''
    def __init__(self):
        self.system = platform.system()

    def darwin_notify(self):
        '''Executing macOS notification

        Raises:
            NotImplementedError: When there is no implementation
        '''
        raise NotImplementedError()

    def linux_notify(self):
        '''Executing Linux notification

        Raises:
            NotImplementedError: When there is no implementation
        '''
        raise NotImplementedError()

    def windows_notify(self):
        '''Executing Windows notification

        Raises:
            NotImplementedError: When there is no implementation
        '''
        raise NotImplementedError()

    def notify(self):
        '''Executing the notification

        Raises:
            NotificationError: When you use an unsupported OS
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
    '''Notification with message

    Args:
        message (str): Message body
    '''
    def __init__(self, message):
        self._message = None
        self.set_message(message)

    def get_message(self):
        return self._message

    def set_message(self, message):
        self._message = self.set_typed_variable(message, str)

    message = property(get_message, set_message)
    '''str: Message body'''


class WebhookNotification(MessageNotification):
    '''Webhook notification

    Args:
        message (str): Message body
        url (str): Webhook URL
    '''
    def __init__(self, message, url):
        super().__init__(message)
        self._url = None
        self.set_url(url)

    def get_url(self):
        return self._url

    def set_url(self, url):
        self._url = self.set_typed_variable(url, str)

    url = property(get_url, set_url)
    '''str: Webhook URL'''


class TokenNotification(MessageNotification):
    '''Token notification

    Args:
        message (str): Message body
        token (str): Token
    '''
    def __init__(self, message, token):
        super().__init__(message)
        self._token = None
        self.set_token(token)

    def get_token(self):
        return self._token

    def set_token(self, token):
        self._token = self.set_typed_variable(token, str)

    token = property(get_token, set_token)
    '''str: Token'''


class BeepNotification(OSSpecificNotification):
    '''Beep notification

    Args:
        times (int): times of beep sound

    Examples:
        Usage
            >>> bn = BeepNotification(3)
            >>> bn.notify()

        Change the times of beep sound
            >>> bn.times = 1
            >>> bn.notify()

        Command Line Tools
            ``$ beep-notify [-h] [--times TIMES]``
    '''
    def __init__(self, times):
        super().__init__()
        self._times = None
        self.set_times(times)

    def get_times(self):
        return self._times

    def set_times(self, times):
        self._times = self.set_typed_variable(times, int)

    times = property(get_times, set_times)
    '''int: times of beep sound'''

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


class DesktopNotification(MessageNotification, OSSpecificNotification):
    '''Desktop Notification

    Args:
        message(str): Message body
        title(str): Title
        subtitle(str): Subtitle
        icon(str): Icon
        sound(bool): Presence of sound

    Examples:
        Usage
            >>> dn = DesktopNotification('Hello', title='PyNotificator')
            >>> dn.notify()

        Change the message body
            >>> dn.message = 'Change Body'
            >>> dn.notify()

        Command Line Tools
            ``$ desktop-notify [-h] [--message MESSAGE]
            [--title TITLE] [--subtitle SUBTITLE]
            [--nosound]``
    '''
    def __init__(self, message, title=None, subtitle=None,
                 icon=None, sound=True):
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

    def get_subtitle(self):
        return self._subtitle

    def set_subtitle(self, subtitle):
        self._subtitle = self.set_typed_variable(subtitle, str)

    def get_icon(self):
        return self._icon

    def set_icon(self, icon):
        self._icon = self.set_typed_variable(icon, str)

    def get_sound(self):
        return self._sound

    def set_sound(self, sound):
        self._sound = self.set_typed_variable(sound, bool)

    title = property(get_title, set_title)
    '''str: Title'''

    subtitle = property(get_subtitle, set_subtitle)
    '''str: Subtitle'''

    icon = property(get_icon, set_icon)
    '''str: Icon'''

    sound = property(get_sound, set_sound)
    '''bool: Presence of sound'''

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
    '''Slack Notification

    Examples:
        Usage
            >>> sn = SlackNotification('Hello', 'https://hooks.slack.com/xxx')
            >>> sn.notify()

        Change the message body
            >>> sn.message = 'Change Body'
            >>> sn.notify()

        Command Line Tools
            ``$ slack-notify [-h] [--message MESSAGE] url``
    '''

    def notify(self):
        '''Executing the notification'''
        data = {'text': self._message}
        requests.post(self._url, data=json.dumps(data))


class DiscordNotification(WebhookNotification):
    '''Discord Notification

    Examples:
        Usage
            >>> dn = DiscordNotification('Hello', 'https://discordapp.com/xxx')
            >>> dn.notify()

        Change the message body
            >>> dn.message = 'Change Body'
            >>> dn.notify()

        Command Line Tools
            ``$ discord-notify [-h] [--message MESSAGE] url``
    '''

    def notify(self):
        '''Executing the notification'''
        data = {'content': self._message}
        requests.post(
            self._url,
            headers={'Content-Type': 'application/json'},
            data=json.dumps(data)
        )


class LineNotification(TokenNotification):
    '''LINE Notification

    Args:
        message(str): Message body
        token(str): LINE Notify token

    Examples:
        Usage
            >>> ln = LineNotification('Hello', 'xxx')
            >>> ln.notify()

        Change the message body
            >>> ln.message = 'Change Body'
            >>> ln.notify()

        Command Line Tools
            ``$ line-notify [-h] [--message MESSAGE] token``
    '''

    def __init__(self, message, token):
        super().__init__(message, token)
        self.URL = 'https://notify-api.line.me/api/notify'

    def notify(self):
        '''Executing the notification'''
        headers = {'Authorization': f'Bearer {self._token}'}
        params = {'message': self._message}
        requests.post(
            self.URL,
            headers=headers,
            params=params
        )
