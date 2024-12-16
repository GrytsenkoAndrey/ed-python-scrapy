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

        next_page = response.css('li.next a ::attr(href)').get()

        if next_page is not None:
            if 'catalogue/' in next_page:
                next_page_url = self.start_urls[0] + next_page
            else:
                next_page_url = self.start_urls[0] + 'catalogue/' + next_page
            yield response.follow(next_page_url, callback=self.parse)
