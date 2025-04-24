import scrapy
import re
import json
import csv

class IndexSpider(scrapy.Spider):
    name = "index_spider"

    start_urls = ["your_url"]

    def parse(self, response):
        data = re.findall("let jsonEditions =(.+?);\n", response.body.decode("utf-8"), re.S)

        data[0] = data[0].replace(u"\u221e", '00')

        editions = []
        if data:
            editions = json.loads(data[0])

        csv_data = []
        for edition in editions["main"]:
            csv_data.append({
                "id": edition["id"],
                "image_path": "https:" + edition["icon"] if len(edition["icon"]) > 0 else '',
                "edition": edition["acronym"],
                "release": edition["dtrelease"],
                "search_term": "card=edid=" + edition["id"] + "%20ed=" + edition["acronym"],
                "file_name": edition["icon"].split("/")[-1] if len(edition["icon"].split("/")) > 0 else ''
            })

        if len(editions['main']) > 0:
            try:
                with open("extracted/index/editions.csv", 'x', newline='', encoding='utf-8') as file:
                    fieldnames = ['id', 'image_path', 'edition', 'release', 'search_term', 'file_name']
                    writer = csv.DictWriter(file, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(csv_data)
            except FileExistsError:
                with open("extracted/index/editions.csv", 'w', newline='', encoding='utf-8') as file:
                    fieldnames = ['id', 'image_path', 'edition', 'release', 'search_term', 'file_name']
                    writer = csv.DictWriter(file, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(csv_data)

