import csv
import json
import re
from typing import Iterable

import scrapy
from scrapy import Request


class EditionSpider(scrapy.Spider):
    name = "edition_spider"
    start_urls = ["your_url"]

    def start_requests(self) -> Iterable[Request]:
        with open("extracted/index/editions.csv") as f:
            for line in f:
                if not line.strip():
                    continue

                if line.split(',')[4].startswith("card="):
                    yield Request(self.start_urls[0] + line.split(',')[4])

    def get_correct_path(self, path):
        if len(path) > 0:
            if path.startswith("//"):
                return path.replace("//", "repo_url", 1)
            elif path.startswith("/"):
                return path.replace("/", "repo_url", 1)
            else:
                return path
        else:
                return path

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
                    "image_path": self.get_correct_path(card["sP"]) if "sP" in card else '',
                    "i18n_name": card["nPT"] if "nPT" in card else '',
                    "lowPrice": card["precoMenor"],
                    "highPrice": card["precoMaior"],
                    "number": card["sN"],
                    "file_name": self.get_correct_path(card["sP"]).split("/")[8] if "sP" in card and len(self.get_correct_path(card["sP"]).split("/")) > 7 else ''
                })

        if len(cards) > 0 and len(csv_data) > 0:
            try:
                with open("extracted/" + cards[0]["sSigla"] + "_cards.csv", 'x', newline='', encoding='utf-8') as file:
                    fieldnames = ['name', 'image_path', 'i18n_name', 'lowPrice', 'highPrice', 'number', 'file_name']
                    writer = csv.DictWriter(file, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(csv_data)
            except FileExistsError:
                with open("extracted/" + cards[0]["sSigla"] + "_cards.csv", 'w', newline='', encoding='utf-8') as file:
                    fieldnames = ['name', 'image_path', 'i18n_name', 'lowPrice', 'highPrice', 'number', 'file_name']
                    writer = csv.DictWriter(file, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(csv_data)

