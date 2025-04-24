from typing import Iterable

import scrapy
from scrapy import Request

from ..items import ImgItem

class DownloadImagesSpider(scrapy.Spider):
    name = "download_images"
    raw_urls = []

    def __init__(self, file_name, *args, **kwargs):
        super(DownloadImagesSpider, self).__init__(*args, **kwargs)
        self.file_name = file_name

    def start_requests(self) -> Iterable[Request]:
        print(self.file_name)
        if not self.file_name == "":
            with open(self.file_name) as f:
                for line in f:
                    if not line.strip():
                        continue

                    if line.split(',')[1].startswith("http"):
                        self.raw_urls.append(line.split(',')[1])

            yield Request("temp_url")

    def parse(self, response):
        item = ImgItem()
        item['image_urls'] = self.raw_urls
        yield item


