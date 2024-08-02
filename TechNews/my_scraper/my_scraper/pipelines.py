import sys
import os
import django
from asgiref.sync import sync_to_async

sys.path.append(r'E:\Roshan\TechNews')
os.environ['DJANGO_SETTINGS_MODULE'] = 'TechNews.settings'

django.setup()

from news.models import News, Tag

import logging


class MyScraperPipeline:
    # @sync_to_async
    def process_item(self, item, spider):
        # Extract fields from the item
        title = item.get('title')
        body = item.get('body')
        tags = item.get('tags')
        resources = item.get('resources')
        print(f"title: {title} ({type(title)})")
        print(f"body: {body} ({type(body)})")
        print(f"tags: {tags} ({type(tags)})")
        print(f"resources: {resources} ({type(resources)})")

        if not all([title, body, tags, resources]):
            spider.logger.error(f"Missing fields in item: {item}")
            return

        news = News.objects.all()
        print(news)
        news_item, created = News.objects.update_or_create(
            title=title,
            defaults={
                'body': body,
                'resources': resources,
            }
        )
        for tag_name in tags:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            news_item.tags.add(tag)
            tag.save()
        news_item.save()
        return item

