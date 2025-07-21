from pathlib import Path
import scrapy

class BachhoaxanhSpider(scrapy.Spider):
    name = "winmart"
    
    async def start(self): 
        prod_name = getattr(self, "prod_name")
        if prod_name is None:
            raise ValueError("prod_name must be provided")
        start_urls = [f"https://winmart.vn/search/{prod_name}"]
        yield scrapy.Request(url=start_urls[0], callback=self.parse, meta={"playwright": True, "playwright_page_options": {
            "timeout": 60000,  # Increase timeout to 60 seconds
            "wait_until": "networkidle",  # Wait until network is idle
        }})
        
    def parse(self, response):
        # products = response.xpath("/html/body/div[1]/div[1]/div/div[2]/main")
        products = response.xpath("/html/body/div[1]/div[1]/div/div[2]/div/div[2]/div[2]/div[2]/div/div")
        print("Result: ", len(products), " products found:")
        for product in products:
            # Extract product details
            p_name = product.css("div.product-card-two__Title-sc-1lvbgq2-6::text").get()
            p_price = str(product.css("div.product-card-two__Price-sc-1lvbgq2-9::text").get())[:-2]
            p_per = product.xpath("./div/div[2]/text()").get()
            p_url = product.css("a::attr(href)").get()
            p_img = product.css("img.product-image::attr(src)").get()
            print("Product: ", {
                "name": p_name.strip() if p_name else "N/A",
                "price": p_price.strip() if p_price else "N/A",
                "per": p_per if p_per else "N/A",
                "url": response.urljoin(p_url) if p_url else "N/A",
                "img": response.urljoin(p_img) if p_img else "N/A"
            })
            yield {
                "name": p_name.strip() if p_name else "N/A",
                "price": p_price.strip() if p_price else "N/A",
                "per": p_per if p_per else "N/A",
                "url": response.urljoin(p_url) if p_url else "N/A",
                "img": response.urljoin(p_img) if p_img else "N/A"
            }