from pathlib import Path
import scrapy

class BachhoaxanhSpider(scrapy.Spider):
    name = "bachhoaxanh"
    
    async def start(self): 
        prod_name = getattr(self, "prod_name")
        if prod_name is None:
            raise ValueError("prod_name must be provided")
        start_urls = [f"https://www.bachhoaxanh.com/tim-kiem?key={prod_name}"]
        yield scrapy.Request(url=start_urls[0], callback=self.parse, meta={"playwright": True, "playwright_page_options": {
            "timeout": 60000,  # Increase timeout to 60 seconds
            "wait_until": "networkidle",  # Wait until network is idle
        }})
        
    def parse(self, response):
        products = response.xpath("/html/body/div[1]/div/div[2]/div/main/div/div[2]/div")
        print("Result: ", len(products), " products found.")
        for product in products:
            # Extract product details
            p_name = product.css("h3::text").get()
            p_price = product.css("div.product_price::text").get()
            p_per = str(product.css("div.product_price div::text").get())[1:]
            p_url = product.css("a::attr(href)").get()
            p_img = product.css("img::attr(src)").get()
            print("Product: ", {
                "name": p_name.strip() if p_name else "N/A",
                "price": p_price.strip() if p_price else "N/A",
                "per": p_per.strip() if p_per else "N/A",
                "url": response.urljoin(p_url) if p_url else "N/A",
                "img": response.urljoin(p_img) if p_img else "N/A"
            })
            yield {
                "name": p_name.strip() if p_name else "N/A",
                "price": p_price.strip() if p_price else "N/A",
                "per": p_per.strip() if p_per else "N/A",
                "url": response.urljoin(p_url) if p_url else "N/A",
                "img": response.urljoin(p_img) if p_img else "N/A"
            }
        # if next_page:
        #     yield scrapy.Request(url=next_page, callback=self.parse)
        # else:
        #     self.logger.info("No more pages to scrape.")