import scrapy
import re
import json

class LigaIndexSpider(scrapy.Spider):
    name = "index_spider"

    start_urls = ["your_url"]

    def parse(self, response):
        data = re.findall("let jsonEditions =(.+?);\n", response.body.decode("utf-8"), re.S)

        data[0] = data[0].replace(u"\u221e", '00')

        editions = []
        if data:
            editions = json.loads(data[0])

        for edition in editions["main"]:
            yield {
                "id": edition["id"],
                "image": "https:" + edition["icon"],
                "edition": edition["acronym"],
                "release": edition["dtrelease"],
                "searchTerm": "card=edid=" + edition["id"] + "%20ed=" + edition["acronym"]
            }

