# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os
from urllib import request
from scrapy.pipelines.images import ImagesPipeline
from qiche import settings


class QichePipeline:
    def __init__(self):
        self.path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'images')
        if not os.path.exists(self.path):
            os.mkdir(self.path)

    def process_item(self, item, spider):
        title = item['title']
        urls = item['urls']
        title_path = os.path.join(self.path, title)
        if not os.path.exists(title_path):
            os.mkdir(title_path)
        for url in urls:
            image_name = url.split('_')[-1]
            request.urlretrieve(url, os.path.join(title_path, image_name))
        return item

class QicheImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        request_objs = super(QicheImagesPipeline, self).get_media_requests(item, info)
        for request_obj in request_objs:
            request_obj.item = item
        return request_objs

    def file_path(self, request, response=None, info=None):
        path = super(QicheImagesPipeline, self).file_path(request, response, info)
        title = request.item.get('title')
        images_store = settings.IMAGES_STORE
        title_path = os.path.join(images_store, title)
        if not os.path.exists(title_path):
            os.mkdir(title_path)
        name = path.replace('full/', '')
        images_path = os.path.join(title_path, name)
        return images_path
