# coding: utf-8

import logging
import argparse
import importlib


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--hashtag",
                        dest="hashtag",
                        help="Set instagram hashtag for parsing media")
    parser.add_argument("-e", "--engine",
                        default='base',
                        dest="engine",
                        help="Set engine for parsing")
    arguments = parser.parse_args()
    engine = importlib.import_module('engines.%s' % arguments.engine)

    bot = engine.InstaSpider(
        thread_number=2,
        config={
            'hashtag': arguments.hashtag,
        }
    )
    bot.run()
