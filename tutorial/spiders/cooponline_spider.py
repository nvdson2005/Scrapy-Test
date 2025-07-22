from  pathlib import Path
import scrapy

class CoopOnlineSpider(scrapy.Spider):
    name = "cooponline"
    
    async def start(self):
        prod_name = getattr(self, "prod_name")
        if prod_name is None:
            raise ValueError("prod_name must be provided")
        start_urls = [f"https://cooponline.vn/search?router=productListing&query={prod_name}"]
        yield scrapy.Request(url=start_urls[0], callback=self.parse, meta={"playwright": True, "playwright_page_options": {
            "timeout": 90000,  # Increase timeout to 60 seconds
            "wait_until": "networkidle",  # Wait until network is idle
        }})
    
    def parse(self, response):
        products = response.css("div.css-1y2krk0 div.css-13w7uog")
        print("Result:", len(products), " products found.")
        for product in products:
            p_url = product.css("a::attr(href)").get()
            p_img = product.css("img::attr(src)").get()
            p_name = product.css("h3.css-1xdyrhj::text").get()
            p_price = str(product.css("div.att-product-detail-latest-price::text").get())[:-2]
            p_per = str(product.css("div.css-1f5a6jh::text").get())[13:]
            print("Product: ", {
                "name": p_name.strip() if p_name else "N/A",
                "price": p_price.strip() if p_price else "N/A",
                "per": p_per.strip() if p_per else "N/A",
                "url": response.urljoin(p_url) if p_url else "N/A",
                "img": response.urljoin(p_img) if p_img else "N/A"
            })
            yield  {
                "name": p_name.strip() if p_name else "N/A",
                "price": p_price.strip() if p_price else "N/A",
                "per": p_per.strip() if p_per else "N/A",
                "url": response.urljoin(p_url) if p_url else "N/A",
                "img": response.urljoin(p_img) if p_img else "N/A"
            }