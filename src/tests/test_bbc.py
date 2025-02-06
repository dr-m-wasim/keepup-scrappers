import os
import sys
testdir = os.path.dirname(__file__)
srcdir = '..'
sys.path.insert(0, os.path.abspath(os.path.join(testdir, srcdir)))
import yaml
from scrapy.http import HtmlResponse, Request
from keepup_scrappers.spiders.bbc_spider import BBCSpider

class TestbbcSpider:

    def setup_method(self):
        
        # sitekey and name intialization
        self.site_key = 'bbc'
        self.spider_name = 'bbc_spider'
        
        # initialization of spider
        self.spider = BBCSpider()
        # loading config file
        config_path = os.path.join(os.path.dirname(__file__), '..', 'keepup_scrappers', 'config', 'config.yaml')
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)

        # load site config
        self.site_config = self.config['sites']['bbc']
        self.spider.selectors = self.site_config['selectors']

    def test_spider_initialization(self):
        assert self.spider.site_key == self.site_key
        assert self.spider.name == self.spider_name
        assert self.spider.page_counter == 0
        assert self.spider.custom_settings['IMAGES_STORE'] == f'data/{self.site_key}/images/'

    def test_parse_method(self):
        
        with open(r'tests\test_data\bbc\listing_sample.json', 'r', encoding='utf-8') as f:
            html_content = f.read()    

        mock_response = HtmlResponse(
            url = self.spider.start_urls[0],
            body = html_content,
            encoding='utf-8',
        )

        results = list(self.spider.parse(mock_response))
   
        assert len(results) == 10  # 12 items + one next page request
        
        item = results[0].meta['item']
        assert item['title'] == 'Meteor Garden: Taiwanese star Barbie Hsu dies at 48'
        
        assert item['detail_url'] == 'https://www.bbc.com/news/articles/ckgy81rv22do'
        assert item['country'] == ['Asia']
        assert item['exerpt'] == ['She died from pneumonia after contracting influenza while on a vacation in Japan, local media report.']
        
   
    def test_parse_details_method(self):

        with open(r'tests\test_data\bbc\detail_sample (4).html', 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # example URL
        sample_url = "http://www.example.com/"
        request = Request(url = sample_url, meta = { 'item' : {}} )
        
        mock_response = HtmlResponse(
            url = sample_url,
            request = request,
            body = html_content,
            encoding = 'utf-8'
        )

        results = list(self.spider.parse_details(mock_response))
        assert len(results) == 1
        
        item = results[0]
        assert item['publication_date'] == '3 days ago'
        
        assert item['content'] == "Chinese fast fashion app Shein has relaunched in India five years after it was banned by Delhi, under a deal with Indian firm Reliance Retail. An official from Reliance Retail, who did not wish to be named, told the BBC the firm has entered a long-term licensing deal with the parent company to sell products manufactured and sourced in India on the platform. The group has not yet made an official announcement. Shein's re-entry to the Indian market comes with strict terms, which include saving all data within the country, India's Commerce Minister Piyush Goyal said in December. In 2020 India banned Shein and dozens of other Chinese apps including TikTok. It said this was in response to data security concerns and it followed a spike in tensions with China after clashes between the two countries' armies in a disputed Himalayan border area. The app was launched in India on Friday night and has so far been downloaded by more than 10,000 people. It is offering fashionwear for as little as 199 rupees ($2.30; £1.90). Shein is currently delivering to consumers only in the cities of Delhi, Mumbai and Bengaluru, but will soon offer services across India, according to a notification on the app. Over the last decade, Shein has gone from a little-known brand among older shoppers to one of the biggest fast fashion retailers globally. Today, it ships to customers in 150 countries across the world. Before the ban it became a big hit in India as it gave people a variety of options to buy trendy designs at an affordable price. The ban initially left a vacuum in the Indian market which was later filled by many local players. Experts say that with Shein India, Reliance Retail - owned by Indian billionaire Mukesh Ambani - is diversifying from its existing strategy of selling international brands through its flagship Ajio online retailer. The revival comes with strict conditions that give Reliance Retail full control over its operations and data while Shein will be a technological partner, Goyal told the Indian parliament in December. All customer and application data will be stored in India and Shein will not have any access rights, he said. Goyal also clarified that the app was banned in India, not the \"sale of Shein-branded products\". Shein will use India as a \"supply source for its global operations\" and will help Reliance Retail in \"building the network\" and training Indian garment manufacturers, as it aims to promote export of textile and garments from India, an official from Reliance Retail said. Shein's comeback under the deal with Reliance Retail is a rare exception to India's ban on more than 200 Chinese apps over the last five years. At the time, Indian officials said the ban followed many complaints against the apps for \"stealing and surreptitiously transmitting users' data in an unauthorised manner\". ByteDance's TikTok and popular combat and survival game PlayerUnknown's Battleground (PUBG) were also banned. However PubG was later rebranded and launched for the Indian market under the name Battlegrounds Mobile India (BGMI), which is held by Krafton India."