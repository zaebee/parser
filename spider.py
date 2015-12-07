# coding: utf-8
import urllib
import csv
import logging
import argparse

from grab.spider import Spider, Task

GOOGLE_PLACE_URL = 'https://maps.googleapis.com/maps/api/place/textsearch/json?query=%s&key=%s'
GOOGLE_API_KEY = 'AIzaSyBysqUovlPKigIp5bmNYcEygcrrvXl9tYA'


class BaseSpider(Spider):
    selectors = [
        'div.slideshow .feature-item__text h3 a',
        'div.medium_list .feature-item__column h3 a',
        'div.small_list .feature-item__column h3 a'
    ]

    def prepare(self):
        # Prepare the file handler to save results.
        # The method `prepare` is called one time before the
        # spider has started working
        filename = self.config.get('url', 'result.txt')
        self.result_file = csv.writer(open(filename, 'w'))

        # This counter will be used to enumerate found images
        # to simplify image file naming
        self.result_counter = 0

    def task_generator(self):
        url = self.config.get('url')
        if url:
            yield Task('page', url=url)

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

    def task_google_place(self, grab, task):
        print 'Google place id search result for %s' % task.place['title']
        data = grab.response.json
        if data.get('status') == 'OK':
            results = data.get('results', [])
            if len(results) == 1: ## one place
                self.result_file.writerow([
                    task.place['url'].encode('utf-8'),
                    task.place['title'].encode('utf-8'),
                    results[0].get('place_id')
                ])
                # Increment place counter
                self.result_counter += 1
            elif len(results) > 1:
                pass
                ## TODO find google api place if results more then 1
                ## yield Task('place_detail', url=task.place['url'], place=place)

    def task_place_detail(self, grab, task):
        print 'Find place detail lat, lon params for %s' % task.place['title']
        map = grab.doc.tree.cssselect('[data-module="map"]')
        if len(map):
            params = map[0].attrib('data-params')
            params = json.loads(params) ## get lat, lon attrs


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url",
                        dest="url",
                        help="Set page url for parsing places")
    arguments = parser.parse_args()

    bot = BaseSpider(
        thread_number=2,
        config={
            'url': arguments.url
        }
    )
    bot.run()
