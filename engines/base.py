# coding: utf-8

import json
import urllib
import csv
import urlparse

from grab.spider import Spider, Task


class BaseSpider(Spider):
    GOOGLE_PLACE_URL = 'https://maps.googleapis.com/maps/api/place/textsearch/json?query=%s&key=%s'
    GOOGLE_API_KEY = 'AIzaSyBysqUovlPKigIp5bmNYcEygcrrvXl9tYA'
    GOOGLE_API_KEY = 'AIzaSyDMPRPS4ALxQVBoNrqApWBY1x2YQPjzpsg'
    selectors = []

    def prepare(self):
        # Prepare the file handler to save results.
        # The method `prepare` is called one time before the
        # spider has started working
        filename = self.config.get('url')
        filename = filename.strip('/').replace('/', '-')
        self.result_file = csv.writer(open(filename, 'w'))
        self.domain = self.config.get('domain')
        self.base_url = self.config.get('url')

        # This counter will be used to enumerate found images
        # to simplify image file naming
        self.result_counter = 0

    def task_generator(self):
        if self.base_url and self.domain:
            url = urlparse.urljoin(self.domain, self.base_url)
            yield Task('page', url=url)

    def task_page(self, grab, task):
        print 'Initial page', task.url
        for selector in self.selectors:
            elements = grab.doc.tree.cssselect(selector)
            if len(elements):
                for elem in elements:
                    print 'Place title:', elem.text.strip()
                    place = {
                        'url': elem.get('href'),
                        'title': elem.text.strip(),
                    }
                    url = self.GOOGLE_PLACE_URL % (place['title'], self.GOOGLE_API_KEY)
                    yield Task('google_place', url=url, place=place)

    def task_google_place(self, grab, task):
        print 'Google place id search result for %s' % task.place['title']
        data = grab.response.json
        if data.get('status') == 'OK':
            results = data.get('results', [])
            if len(results) == 1: ## one place
                self.result_file.writerow([
                    task.place['title'].encode('utf-8'),
                    results[0].get('place_id')
                ])
                # Increment place counter
                self.result_counter += 1
            elif len(results) > 1:
                ## TODO find google api place if results more then 1
                url = urlparse.urljoin(self.domain, task.place['url'])
                yield Task('place_detail', url=url, place=task.place, google_data=results)

    def task_place_detail(self, grab, task):
        print 'Find place detail lat, lng params for %s' % task.place['title']
