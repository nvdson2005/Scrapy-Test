from pathlib import Path
import scrapy

class BachhoaxanhSpider(scrapy.Spider):
    name = "winmart"
    
    async def start(self): 
        start_urls = [f"https://winmart.vn/"]
        yield scrapy.Request(url=start_urls[0], callback=self.parse, meta={"playwright": True})
        
    def parse(self, response):
        # products = response.xpath("/html/body/div[1]/div[1]/div/div[2]/main")
        products = response.xpath("/html/body/div[1]/div[1]/div/div[2]/main/div/div[3]/div/div[2]/div")
        print("Result: ", products.get())