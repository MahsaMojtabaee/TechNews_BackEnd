import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time
from ..items import NewsItem


class FinalSpider(scrapy.Spider):
    name = 'scrape'
    start_urls = ['https://www.zoomit.ir/archive/']
    current_page = 1
    max_page=3
    count = 0
    base_url = 'https://www.zoomit.ir/archive/'
    current_url = 'https://www.zoomit.ir/archive/?pageNumber={}'

    def __init__(self, *args, **kwargs):
        super(FinalSpider, self).__init__(*args, **kwargs)

        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-browser-side-navigation')
        options.add_argument('--disable-infobars')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--disable-web-security')
        options.add_argument('--disable-site-isolation-trials')
        options.add_argument('--disable-setuid-sandbox')
        options.add_argument('--disable-service-workers')
        chrome_driver_path = 'C:/Users/mojta/Desktop/chromedriver-win64/chromedriver.exe'
        self.driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)
        self.wait = WebDriverWait(self.driver, 10)

    def __del__(self):
        self.driver.quit()

    def parse(self, response):
        if self.current_page < self.max_page:
            self.driver.get(response.url)
            self.logger.info(f'Current response URL: {response.url}')
            try:
                main_div = self.wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div.flex__Flex-le1v16-0.cVZflE")))
                a_elements = self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a.bzMtyO')))
                links = [a.get_attribute('href') for a in a_elements]
            except Exception as e:
                self.logger.error(f'Error receiving the first data: {e}')
                return

            self.logger.info(f'Links: {links}')
            yield scrapy.Request(links[0], callback=self.parse_content, meta={'links': links})


    def parse_content(self, response):
        self.driver.get(response.url)
        links = response.meta.get('links')
        links.remove(response.url)
        print(f'length of links is {len(links)}')
        print(f'in the link the links are {links}')
        items = NewsItem()
        try:
            div_element_tags = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div.flex__Flex-le1v16-0.kDyGrB'))
            )
            p_elements = self.wait.until(
                EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, 'p.ParagraphElement__ParagraphBase-sc-1soo3i3-0'))
            )

        except Exception as e:
            print(f'Error waiting for div element: {e}')

        try:
            a_tags = self.wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div_element_selector a')))
            tags = [a.text for a in a_tags]
        except Exception as e:
            self.logger.error(f'Error extracting tags: {e}')
            tags = []

        try:
            h1_title = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'h1'))).text
        except Exception as e:
            self.logger.error(f'Error getting title: {e}')
            h1_title = 'No title found'

        paragraphs = [p.text for p in p_elements]
        body = '\n'.join(paragraphs)

        items['resources'] = response.url
        items['title'] = h1_title
        items['tags'] = tags
        items['body'] = body
        yield items

        if len(links) > 0:
            yield scrapy.Request(url=links[0], callback=self.parse_content, meta={'links':links})

        if self.current_page < 3:
            self.current_page += 1
            next_page = self.current_url.format(self.current_page)
            print(f'next page is {next_page}')
            yield scrapy.Request(next_page, callback=self.parse)

        # if len(links) <= 0:
        #     if self.current_page < 3:
        #         self.current_page += 1
        #         next_page = self.current_url.format(self.current_page)
        #         self.logger.info(f'Next page URL: {next_page}')
        #         yield scrapy.Request(url=next_page, callback=self.parse)
        #     else:
        #         yield None
        # else:
        #     yield scrapy.Request(url=links[0], callback=self.parse_content, meta={'links':links})
