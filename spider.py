# coding: utf-8

import logging
import argparse
import importlib

ENGINES = {
    'nyt': 'http://nytimes.com',
    'dep': 'http://departures.com',
    'tmout': 'http://timeout.com',
}

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url",
                        dest="url",
                        help="Set page url for parsing places")
    parser.add_argument("-e", "--engine",
                        default='base',
                        dest="engine",
                        help="Set engine for parsing")
    arguments = parser.parse_args()
    domain = ENGINES.get(arguments.engine, '')
    engine = importlib.import_module('engines.%s' % arguments.engine)

    bot = engine.Spider(
        thread_number=2,
        config={
            'url': arguments.url,
            'domain': domain
        }
    )
    bot.run()
