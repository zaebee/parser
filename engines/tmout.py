# coding: utf-8

import json
from base import BaseSpider


class Spider(BaseSpider):
    """ timeout.com parser """

    selectors = [
        'div.slideshow .feature-item__text h3 a',
        'div.medium_list .feature-item__column h3 a',
        'div.medium_list .feature-item__column h3',
        'div.small_list .feature-item__column h3 a'
    ]

    def task_place_detail(self, grab, task):
        print 'Find place detail lat, lng params for %s' % task.place['title']
        map = grab.doc.tree.cssselect('[data-module="map"]')
        if len(map):
            params = map[0].get('data-params')
            params = json.loads(params) ## get lat, lng attrs
            lat = params.get('lat')
            lng = params.get('lng')
            google_data = task.google_data
            results = [r for r in google_data
                      if '%.2f' % r['geometry']['location']['lat'] == '%.2f' % lat
                      and '%.2f' % r['geometry']['location']['lng'] == '%.2f' % lng
                     ]
            for result in results:
                self.result_file.writerow([
                    task.place['title'].encode('utf-8'),
                    results[0].get('place_id')
                ])
                # Increment place counter
                self.result_counter += 1
