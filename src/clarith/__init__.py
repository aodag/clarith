import logging
import sys

from cliff.app import App
from cliff.commandmanager import CommandManager

__version__ = '0.1'


class ClarithApp(App):
    def __init__(self):
        super(ClarithApp, self).__init__(
            description='clarith app',
            version=__version__,
            command_manager=CommandManager('clarith.commands'),
            )


def main(argv=sys.argv[1:]):
    app = ClarithApp()
    return app.run(argv)

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))