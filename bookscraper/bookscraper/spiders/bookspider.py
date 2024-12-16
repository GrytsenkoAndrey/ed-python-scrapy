import scrapy
#from bookscraper.bookscraper.items import BookItem

class BooksSpider(scrapy.Spider):
    name = 'books'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['https://books.toscrape.com/']
    # custom_settings = {
    #     'FEEDS': { 'data.csv': { 'format': 'csv'}}
    # }

    #def start_requests(self):
    #    url = 'https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html'

    def parse(self, response, **kwargs):
        books = response.css('article.product_pod')

        for book in books:
            yield{
                'name': book.css('h3 a::text').get(),
                'price': book.css('.product_price .price_color::text').get(),
                'url': book.css('h3 a').attrib['href']
            }
