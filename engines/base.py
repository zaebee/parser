# -*- coding: utf-8 -*-

import csv
from datetime import datetime
from grab.spider import Spider, Task
from instagram.models import Media


class InstaSpider(Spider):
    API_ACCESS_TOKEN = '2887062364.edc9621.8c1d23b875374cebb765da67b96e022c'
    API_TAGS_URL = 'https://api.instagram.com/v1/tags/%s/media/recent?count=%s&access_token=%s'
    COUNT = 100

    def prepare(self):
        # Prepare the file handler to save results.
        # The method `prepare` is called one time before the
        # spider has started working
        hashtag = self.config.get('hashtag')
        date = datetime.now().strftime('%Y%m%d%H%M')
        filename = '%s_%s.csv' % (date, hashtag)

        self.result_file = csv.writer(open(filename, 'w'))
        self.base_url = self.API_TAGS_URL % (hashtag, self.COUNT, self.API_ACCESS_TOKEN)

        # This counter will be used to enumerate found media
        # to simplify media file naming
        self.result_counter = 0

    def task_generator(self):
        yield Task('hashtag', url=self.base_url)

    def task_hashtag(self, grab, task):
        data = grab.doc.json
        status_code = data.get('meta', {}).get('code')
        next_url = data.get('pagination', {}).get('next_url')

        if next_url:
            yield Task('hashtag', url=next_url)
        for element in data.get('data'):
            media = Media.object_from_dictionary(element)
            self.result_file.writerow([
                media.id,
                media.link,
                media.like_count,
                media.caption,
            ])
            # Increment saved media counter
            self.result_counter += 1
