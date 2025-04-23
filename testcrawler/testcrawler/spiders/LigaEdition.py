import csv
import json
import re
from typing import Iterable

import scrapy
from scrapy import Request


class LigaEditionSpider(scrapy.Spider):
    name = "edition_spider"
    start_urls = ["your_url"]

    def start_requests(self) -> Iterable[Request]:
        with open("editions.csv") as f:
            for line in f:
                if not line.strip():
                    continue

                if line.split(',')[4].startswith("card="):
                    yield Request(self.start_urls[0] + line.split(',')[4])

    def parse(self, response):
        raw_data = re.findall("var cardsjson =(.+?);\n", response.body.decode("utf-8"), re.S)

        cards = []
        if raw_data:
            if len(raw_data) > 0:
                cards = json.loads(raw_data[0])

        csv_data = []
        for card in cards:
            if "nEN" in card:
                csv_data.append({
                    "name": card["nEN"].replace(u'\u221e', 'oo', 1),
                    "image": card["sP"].replace('//', "https://repositorio.sbrauble.com/", 1) if "sP" in card else '',
                    "lowPrice": card["precoMenor"],
                    "highPrice": card["precoMaior"],
                    "number": card["sN"]
                })

        if len(cards) > 0 and len(csv_data) > 0:
            try:
                with open("extracted/" + cards[0]["sSigla"] + "_cards.csv", 'x', newline='', encoding='utf-8') as file:
                    fieldnames = ['name', 'image', 'lowPrice', 'highPrice', 'number']
                    writer = csv.DictWriter(file, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(csv_data)
            except FileExistsError:
                with open("extracted/" + cards[0]["sSigla"] + "_cards.csv", 'w', newline='', encoding='utf-8') as file:
                    fieldnames = ['name', 'image', 'lowPrice', 'highPrice', 'number']
                    writer = csv.DictWriter(file, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(csv_data)

