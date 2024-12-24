import scrapy, re
#from ..items import BookItem

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
            relative_url = book.css('h3 a ::attr(href)').get()
            if 'catalogue/' in relative_url:
                book_url = self.start_urls[0] + relative_url
            else:
                book_url = self.start_urls[0] + 'catalogue/' + relative_url
            yield response.follow(book_url, callback=self.parse_book_page)

        next_page = response.css('li.next a ::attr(href)').get()
        if next_page is not None:
            if 'catalogue/' in next_page:
                next_page_url = self.start_urls[0] + next_page
            else:
                next_page_url = self.start_urls[0] + 'catalogue/' + next_page
            yield response.follow(next_page_url, callback=self.parse)

    def parse_book_page(self, response):
        table_rows = response.css('table tr')

        # book_item = BookItem()
        # book_item['url'] = response.url
        # book_item['title'] = response.css('.product_main h1::text').get()
        # book_item['product_type'] = table_rows[1].css('td ::text').get()
        # book_item['price_excl_tax'] = table_rows[2].css('td ::text').get()
        # book_item['price_incl_tax'] = table_rows[3].css('td ::text').get()
        # book_item['tax'] = table_rows[4].css('td ::text').get()
        # book_item['availability'] = table_rows[5].css('td ::text').get()
        # book_item['num_reviews'] = table_rows[6].css('td ::text').get()
        # book_item['stars'] = response.css('p.star-rating').attrib['class']
        # book_item['category'] = response.xpath("//ul[@class='breadcrumb']/li[@class='active']/preceding-sibling::li[1]/a/text()").get()
        # book_item['description'] = response.xpath("//div[@id='product_description']/following-sibling::p/text()").get()
        # book_item['price'] = response.css('p.price_color ::text').get()
        # yield BookItem
        title = response.css('.product_main h1::text').get()
        category = response.xpath(
                "//ul[@class='breadcrumb']/li[@class='active']/preceding-sibling::li[1]/a/text()").get()
        price_excl_tax = table_rows[2].css('td ::text').get()
        price_incl_tax = table_rows[3].css('td ::text').get()
        tax = table_rows[4].css('td ::text').get()
        price = response.css('p.price_color ::text').get()
        availability = table_rows[5].css('td ::text').get()

        yield {
            'url': response.url,
            'title': title.strip(),
            'product_type': table_rows[1].css('td ::text').get(),
            'price_excl_tax': float(price_excl_tax[1:]),
            'price_incl_tax': float(price_incl_tax[1:]),
            'tax': float(tax[1:]),
            'availability': re.findall('(-?\d+(?:\.\d+)?)', availability)[0],
            'num_reviews': table_rows[6].css('td ::text').get(),
            'stars': response.css('p.star-rating').attrib['class'],
            'category': category.lower(),
            'description': response.xpath("//div[@id='product_description']/following-sibling::p/text()").get(),
            'price': float(price[1:])
        }
