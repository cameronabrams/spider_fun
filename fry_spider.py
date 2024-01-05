import scrapy

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        # "https://drexel.edu/president/messages/message/2023/April/summer-fridays-and-july-3-closure/",
        "https://drexel.edu/president/messages/message/",
    ]

    def parse(self, response):
        article=response.css("article.content-news")
        if article is not None and article.xpath("//h1/text()").get() is not None:
            yield {
                'title':article.xpath("//h1/text()").get(),
                'date':article.css("span.date::text").get(),
                'body':article.xpath("//p/text()").extract()
            }
        years=response.css("ul.year-guide")
        for yearstruct in years.css("li"):
            articles=yearstruct.css("ul.highlighted-articles")
            for article in articles.css("li.highlighted-article"):
                for href in article.css('a::attr(href)'):
                    yield response.follow(href, self.parse)