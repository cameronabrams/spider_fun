# Author: Cameron F. Abrams, <cfa22@drexel.edu>
#
# FrySpider: scrapes all content of John Fry's official emails to the Drexel Community
# and dumps to a JSON file
#
import scrapy

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        "https://drexel.edu/president/messages/message/",
    ]

    def parse(self, response):
        article=response.css("article.content-news")
        if article is not None and article.xpath("//h1/text()").get() is not None:
            yield {
                'title':article.xpath("//h1/text()").get(),
                'date':article.css("span.date::text").get(),
                'body':article.xpath("//p/text()").extract(),
                'links':article.xpath("//p/a/text()").extract(),
            }
        years=response.css("ul.year-guide")
        for yearstruct in years.css("li"):
            articles=yearstruct.css("ul.highlighted-articles")
            for article in articles.css("li.highlighted-article"):
                for href in article.css('a::attr(href)'):
                    yield response.follow(href, self.parse)