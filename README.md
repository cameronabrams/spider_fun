# FrySpider -- scrapes all of John Fry's official emails

> Cameron F. Abrams, cfa22@drexel.edu


### Usage

First, run the spider using ``scrapy`` to generate the JSON output

```
scrapy runspider fry_spider.py -O fry.json
```

Now, run ``analyze.py`` to generate the word cloud:

```
python analyze.py -f fry.json
```
