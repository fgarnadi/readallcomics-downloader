import scrapy
from scrapy.pipelines.images import ImagesPipeline


class ComicImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        yield scrapy.Request(item["image_url"])

    def file_path(self, request, response=None, info=None, *, item=None):
        return "{title}/{page}.{extension}".format(extension="jpg", **item)


class ReadallcomicsSpider(scrapy.Spider):
    name = "readallcomics"
    base_url = "https://readallcomics.com/category/{category}/"

    def __init__(self, *args, **kwargs):
        super(ReadallcomicsSpider, self).__init__(*args, **kwargs)
        self.start_urls = [self.base_url.format(category=self.category)]

    @classmethod
    def update_settings(cls, settings):
        super(ReadallcomicsSpider, cls).update_settings(settings)
        pipeline_name = ComicImagesPipeline.__module__
        pipeline_name += "." + ComicImagesPipeline.__name__
        settings["ITEM_PIPELINES"][pipeline_name] = 1

    def parse(self, response):
        for chapter_url in response.css("ul.list-story a::attr(href)"):
            yield scrapy.Request(chapter_url.get(), callback=self.parse_chapter)

    def parse_chapter(self, response):
        page = 1
        title = response.css("div>span>strong::text").extract_first().replace(" ", "_")
        for img in response.xpath("//img[not(parent::div[@id='logo'])]"):
            yield {
                "image_url": img.xpath("@src").extract_first(),
                "page": page,
                "title": title,
            }

            page += 1
