# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from pathlib import PurePosixPath

from scrapy.pipelines.images import ImagesPipeline
from scrapy.utils.httpobj import urlparse_cached


class DownloadImagePipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None, *, item=None):
        url_raw = request.url
        url_raw.replace("https://", "", 1)

        split = url_raw.split("/")

        if split[6] == 'ed':
            return "logos/" + PurePosixPath(urlparse_cached(request).path).name
        elif split[6] == 'cd':
            return "cards/" + split[7] + "/" + PurePosixPath(urlparse_cached(request).path).name
        else:
            return PurePosixPath(urlparse_cached(request).path).name
