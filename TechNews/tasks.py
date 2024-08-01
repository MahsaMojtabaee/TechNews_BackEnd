from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from my_scraper.my_scraper.spiders.final_spider import FinalSpider
from celery import shared_task


@shared_task
def crawl():
    settings = get_project_settings()
    process = CrawlerProcess(settings)
    process.crawl(FinalSpider)
    process.start()
