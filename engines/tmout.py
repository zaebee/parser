# coding: utf-8

from base import BaseSpider


class Spider(BaseSpider):
    """ timeout.com parser """

    selectors = [
        'div.slideshow .feature-item__text h3 a',
        'div.medium_list .feature-item__column h3 a',
        'div.small_list .feature-item__column h3 a'
    ]
