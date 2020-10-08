import scrapy
import os
import shutil


class GamasutraSpider(scrapy.Spider):
    name = "gama"
    main_address = 'https://www.gamasutra.com'

    def start_requests(self):
        url = self.main_address + '/updates?page='
        for i in range(1, 500):
            temp_url = url + str(i)
            yield scrapy.Request(url=temp_url, callback=self.parse)

    def parse(self, response):
        os.makedirs('./saved', exist_ok=True)

        for res in response.xpath("//*[@class='feed_item']/a/@href"):
            cur_url = res.get()
            if cur_url[0] == '/':
                cur_url = self.main_address + cur_url

            print("getting : " + cur_url)
            yield scrapy.Request(url=cur_url, callback=self.parse_article)



    def parse_article(self, response):
        page_name = response.url.split("/")[-1].replace('?', '').replace('=', '').replace('.php', '')
        filename = 'raw-%s.html' % page_name
        print("saving : " + filename)
        with open(filename, 'wb') as f:
            f.write(response.body)
        shutil.move(filename, './saved/' + filename)