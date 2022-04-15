import scrapy
from ..items import Mobile
import copy

class FlipkartScraper(scrapy.Spider):
  name = "flipkart_scraper"
  headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.2840.71 Safari/539.36'}
  no_of_pages = 10000
  # page_no = 0

  def start_requests(self):
    urls = [
      "https://www.flipkart.com/search?q=samsung%20mobile&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off"
    ] # Change this URL

    for url in urls:
      yield scrapy.Request(url = url, callback = self.parse, headers = self.headers)

  def parse(self, response):
    self.logger.info("------------------- Inside Parse ----------------------------")
    self.no_of_pages -= 1
    # self.page_no += 1

    # mobiles = response.xpath('//*[@id="container"]/div/div[3]/div[1]/div[2]/div[contains(@class, "_1AtVbE")]/div/div/div/a').xpath("@href").getall()
    mobiles = response.xpath('//a[@class="_1fQZEK"]').xpath("@href").getall()

    self.logger.info(mobiles)
    # mobiles = [mobiles[0]]

    for mobile in mobiles:
      mobileUrl = response.urljoin(mobile)
      self.logger.info("Going to Mobile individual page")
      yield scrapy.Request(url = mobileUrl, callback = self.parse_mobile, headers = self.headers)

    if(self.no_of_pages > 0):
      # next_page_all_href = response.xpath("//div[@class='_2zg3yZ']/nav[@class='_1ypTlJ']/a[@class='_3fVaIS']").xpath("@href").getall()
      next_page_url = response.xpath('//a[@class="_1LKTO3"]').xpath("@href").getall()

      if next_page_url:
        next_page_url = response.urljoin(next_page_url[-1])
        self.logger.info("Going to Mobiles list next page")
        yield scrapy.Request(url = next_page_url, callback = self.parse, headers = self.headers)
      else:
        self.logger.info("------------------- parse end ----------------------------")

  def parse_mobile(self, response):

    self.logger.info("------------------- Inside parse_mobile ----------------------------")

    product_details = {}
    product_details['name'] = response.xpath("//span[@class='B_NuCI']//text()").get().strip()
    product_details['price'] = response.xpath("//div[contains(@class, '_16Jk6d')]//text()").get().strip()

    next_page_url = response.xpath('//div[contains(@class, "JOpGWq")]/a').xpath("@href").get()

    if next_page_url:
      next_page_url = response.urljoin(next_page_url)
      self.logger.info(next_page_url)
      self.logger.info(product_details)

      request = scrapy.Request(url=next_page_url, callback=self.parse_reviews, headers=self.headers, cb_kwargs=product_details)

      self.logger.info("Going to All Reviews page")
      yield request
    else:
      self.logger.info("------------------- parse_mobile end ------------------------------------")


  def parse_reviews(self, response, **product_details):

    self.logger.info("------------------- inside parse_reviews ----------------------------")

    params = copy.deepcopy(product_details)

    reviews = response.xpath('//div[contains(@class, "_27M-vq")]')
    self.logger.info(f"Reviews length {len(reviews)}")

    # reviews = [reviews[0]]

    for review in reviews:
      params['title'] = review.xpath('.//p[contains(@class, "_2-N8zT")]//text()').get().strip()

      text_list = review.xpath('.//div[contains(@class, "t-ZTKy")]/div/div//text()').getall()
      params['review'] = '\n'.join(text_list)

      params['rating'] = review.xpath('.//div[contains(@class, "_3LWZlK")]/text()').get().strip()

      votes = review.xpath('.//span[contains(@class, "_3c3Px5")]/text()').getall()

      params['likes'] = votes[0].strip()
      params['dislikes'] = votes[1].strip()

      self.logger.info("Saving field values")
      yield Mobile(**params)

    next_page_url = response.xpath('//a[contains(@class, "_1LKTO3")]').xpath("@href").getall()

    if next_page_url:
      next_page_url = response.urljoin(next_page_url[-1])

      request = scrapy.Request(url=next_page_url, callback=self.parse_reviews, headers=self.headers, cb_kwargs=product_details)

      self.logger.info("Going to next review page")
      yield request
    else:
      self.logger.info("------------------- parse_reviews end -----------------------")
