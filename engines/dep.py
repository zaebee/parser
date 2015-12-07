# coding: utf-8

import urlparse
from base import BaseSpider, Task


class Spider(BaseSpider):
    """ departures.com parser """

    selectors = [
        '.views-field.views-field-field-slide-title h1.field-content'
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
                        'url': task.url,
                        'title': elem.text,
                    }
                    url = self.GOOGLE_PLACE_URL % (place['title'], self.GOOGLE_API_KEY)
                    yield Task('google_place', url=url, place=place)

            next_slide = grab.doc.tree.cssselect(self.next_slide_selectors)
            if len(next_slide):
                next_slide = next_slide[0]
                url = urlparse.urljoin(self.domain, next_slide.get('href'))
                yield Task('page', url=url)
