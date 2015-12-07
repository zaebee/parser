# coding: utf-8

from base import BaseSpider


class Spider(BaseSpider):
    """ departures.com parser """

    selectors = [
        'views-field views-field-field-slide-title h1.field-content'
    ]
    next_slide_selectors = '.slide-text a'

    def task_page(self, grab, task):
        print 'Initial page', task.url
        for selector in self.selectors:
            elements = grab.doc.tree.cssselect(selector)
            if len(elements):
                for elem in elements:
                    print 'Place title:', elem.text
                    place = {
                        'url': elem.get('href'),
                        'title': elem.text,
                    }
                    url = GOOGLE_PLACE_URL % (place['title'], GOOGLE_API_KEY)
                    yield Task('google_place', url=url, place=place)

