import scrapy

from scrapy.loader import ItemLoader
from ..items import NordeaItem
from itemloaders.processors import TakeFirst


class NordeaSpider(scrapy.Spider):
	name = 'nordea'
	start_urls = ['https://www.nordea.com/no/presse-og-nyheter/nyheter-og-pressemeldinger/']

	def parse(self, response):
		post_links = response.xpath('//div[@class="grid-group landmark--palm list-all search-results listings__loadmore-item-container-js"]//h3/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		title = response.xpath('//h1/text()').get()
		description = response.xpath('//article//text()[normalize-space() and not(ancestor::small)]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//article/small/text()').get()
		if date:
			date = date.split()[0]

		item = ItemLoader(item=NordeaItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
