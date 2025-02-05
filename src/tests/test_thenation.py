import os
import sys
testdir = os.path.dirname(__file__)
srcdir = '..'
sys.path.insert(0, os.path.abspath(os.path.join(testdir, srcdir)))
import yaml
from scrapy.http import HtmlResponse, Request
from keepup_scrappers.spiders.thenation_spider import TheNationSpider

class TestthenationSpider:

    def setup_method(self):
        
        # sitekey and name intialization
        self.site_key = 'thenation'
        self.spider_name = 'thenation_spider'
        
        # initialization of spider
        self.spider = TheNationSpider()
        
        # loading config file
        config_path = os.path.join(os.path.dirname(__file__), '..', 'keepup_scrappers', 'config', 'config.yaml')
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)

        # load site config
        self.site_config = self.config['sites']['thenation']
        self.spider.selectors = self.site_config['selectors']

    def test_spider_initialization(self):
        assert self.spider.site_key == self.site_key
        assert self.spider.name == self.spider_name
        #assert self.spider.page_counter == 1
        assert self.spider.custom_settings['IMAGES_STORE'] == f'data/{self.site_key}/images/'

    def test_parse_method(self):
        
        with open(r'tests\test_data\thenation\listing_sample (2).json', 'r', encoding='utf-8') as f:
            html_content = f.read()    

        mock_response = HtmlResponse(
            url = self.spider.start_urls[0],
            body = html_content,
            encoding='utf-8',
        )

        results = list(self.spider.parse(mock_response))
   
        assert len(results) == 37  # 12 items + one next page request
        
        item = results[0].meta['item']
        assert item['title'] == 'GulAhmed lawn collection 2025 – exclusive summer lawn online'
        
        assert item['detail_url'] == 'https://www.nation.com.pk/05-Feb-2025/gulahmed-lawn-collection-2025-exclusive-summer-lawn-online'
        assert item['image_urls'][0] == 'https://www.nation.com.pk/digital_images/medium/2025-02-05/gulahmed-lawn-collection-2025-exclusive-summer-lawn-online-1738727610-9927.jpg'
        #assert item['exerpt'] == 'Legislation in 2024 and 2025 aims to counter AI-generated deceptive content'
        
   
    def test_parse_details_method(self):

        with open(r'tests\test_data\thenation\detail_sample (2).html', 'r', encoding='utf-8') as f:
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
        assert item['content'] == "The wait is finally over! GulAhmed’s much-anticipated lawn collection 2025 has arrived, launching exclusively online on February 4th. This year, it’s all about vibrant hues, delicate embroideries, and effortless elegance. With over 250 stunning lawn dress designs, this summer collection 2025 promises something for every fashion-forward woman. The collection is divided into 10 uniquely curated lookbooks, each an ode to timeless craftsmanship blended with contemporary aesthetics. From to silk kaftans and printed cotton saris, every piece is designed to elevate your summer wardrobe with breezy sophistication. This season, step into a world of color with Chunri lawn suits featuring mesmerizing printed and embroidered designs. A fusion of heritage and modernity, these unstitched lawn ensembles reimagine classic in vibrant hues, making them a must-have for your summer wardrobe. For those who adore timeless elegance, the Premium Luxury Collection is pure indulgence. Think exquisite embroidered swiss voile, silk, and schiffli lawn dresses that exude grace. Whether it's a 3-piece embroidered lawn suit for an intimate evening or a delicately embroidered jacquard ensemble for a festive gathering, this collection is where sophistication meets style. Nothing says summer like delicate florals, and GulAhmed’s Floral World prints are a fresh take on botanical elegance. Soft pastel-hued lawn dress designs adorned with artistic detailing ensure you stay effortlessly chic while embracing the lightness of the season. Rooted in heritage yet modern in appeal, the Dhoop Kinare Collection encapsulates effortless sophistication. Crafted from the finest fabrics, each design is an ode to refined femininity—perfect for warm summer days and breezy evenings. From 2-piece unstitched lawn suits perfect for casual chic styling to ensembles ideal for statement-making moments, GulAhmed has left no stone unturned in curating a collection that defines summer 2025 fashion. If you’re a fan of delicate craftsmanship, the Timeless Allure Collection is your calling. These regal ensembles transport you to a world of mystic gardens where every thread weaves a tale of grandeur. Meanwhile, the Tribute to Mothers Collection pays homage to the love and care of generations past, with fabrics that embody warmth, devotion, and heritage. GulAhmed introduces an innovative twist to summer fashion with Bamboo Fabric Lawn Dresses—a sustainable, breathable, and UV-protective fabric that ensures you stay cool and comfortable throughout the season. These lawn 2025 designs are long-lasting, wrinkle-resistant, and quick-drying, making them a perfect blend of practicality and style. This lawn dress design 2025 collection is more than just clothing—it’s an experience. From printed and embroidered lawn to chiffon, jacquard, and chikankari, each fabric choice enhances the beauty of summer dressing. Get ready to indulge in the ultimate summer fashion affair. Shop the exclusively online at and be the first to embrace the season’s hottest trends!"
        assert item['publication_date'] == 'February 05, 2025'
        assert item['author'] == 'Areeba Haroon'