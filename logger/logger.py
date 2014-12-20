import sys
import os
from datetime import datetime


class Logger():

    displayed_levels = [
#         'error',
#         'warn',
#         'info',
#         'debug',
#         'trace'
    ]

    hidden_categories = [
        # 'start_client',
        # 'client',
        # 'server'
    ]

    @staticmethod
    def error(msg, parameters=None, category='main'):
        Logger.log('error', msg, parameters, category)

    @staticmethod
    def warn(msg, parameters=None, category='main'):
        Logger.log('warn', msg, parameters, category)

    @staticmethod
    def info(msg, parameters=None, category='main'):
        Logger.log('info', msg, parameters, category)

    @staticmethod
    def debug(msg, parameters=None, category='main'):
        Logger.log('debug', msg, parameters, category)

    @staticmethod
    def trace(msg, parameters=None, category='main'):
        Logger.log('trace', msg, parameters, category)

    @staticmethod
    def log(level, msg, parameters, category='main'):
        if level in Logger.displayed_levels and category not in Logger.hidden_categories:
            if parameters is not None:
                msg = msg % parameters
            now = datetime.now()
            sys.stdout.write(
                '[%s] [%s] [%s] [%s]: %s\n' % (now, os.getpid(), level.upper(), category, msg)
            )

    def __init__(self):
        raise Exception('Static class')