# PyNotificator

[HomePage](https://higurashi-takuto.github.io/pynotificator/) / [Documentation](https://pynotificator.readthedocs.io/en/latest/) / [PyPI](https://pypi.org/project/pynotificator/)

## Quick Start

### Installation

Install with pip.
```
$ pip install pynotificator
```

If you are using Windows, you need an option: `pip install pynotificator[win]`.

### Python and Command Line Tools

You can use command line tools.

#### Beep
```
# Python
from pynotificator import BeepNotification
bn = BeepNotification(3)
bn.notify()

# Command Line Tools
$ beep-notify -t 3
```

#### Desktop
```
# Python
from pynotificator import DesktopNotification
dn = DesktopNotification('Hello', title='PyNotificator', subtitle='Notify')
dn.notify()

# Command Line Tools
$ desktop-notify -m Hello -t PyNotificator -s Notify
```

#### Slack
```
# Python
from pynotificator import SlackNotification
sn = SlackNotification('PyNotificator', 'https://hooks.slack.com/services/xxx')
sn.notify()

# Command Line Tools
$ slack-notify -m PyNotificator https://hooks.slack.com/services/xxx
```

#### Discord
```
# Python
from pynotificator import DiscordNotification
dn = DiscordNotification('PyNotificator', 'https://discordapp.com/api/webhooks/xxx')
dn.notify()

# Command Line Tools
$ discord-notify -m PyNotificator https://discordapp.com/api/webhooks/xxx
```

#### LINE
```
# Python
from pynotificator import LineNotification
ln = LineNotification('PyNotificator', 'xxx')
ln.notify()

# Command Line Tools
$ line-notify -m PyNotificator xxx
```

## License
[MIT License](https://raw.githubusercontent.com/higurashi-takuto/pynotificator/master/LICENSE)

## Author
[higurashi-takuto](https://hgrs.me/)
