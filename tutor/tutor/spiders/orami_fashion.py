import scrapy


class OramiFashionSpider(scrapy.Spider):
    name = 'orami_fashion'
    allowed_domains = ['orami.co.id']
    start_urls = ['https://www.orami.co.id/shopping/category/fashion']

    def parse(self, response):
        # data = {
        #     "page": 2
        # }

        return scrapy.FormRequest(
            url="https://www.orami.co.id/shopping/category/fashion?page=2",
            callback=self.after_load_form
        )

    def after_load_form(self, response):
        # get detail product
        detail_product: List[Selector] = response.css(".jsx-3196085131 .jsx-3196085131 a")
        for detail in detail_product:
            href = detail.attrib.get("href")
            yield response.follow(href, callback=self.parse_detail)

        #yield{"title": response.css("title::text").get()}

    def parse_detail(self, response):
        #yield {"title":response.css("title::text").get()}
        image = response.xpath("//meta[@property='og:image']/@content")[0].extract()
        title = response.css(".prod-detail-title::text").get()

        return {
            'image': image,
            'title': title
        }