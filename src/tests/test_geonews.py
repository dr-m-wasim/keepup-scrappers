import os
import sys
testdir = os.path.dirname(__file__)
srcdir = '..'
sys.path.insert(0, os.path.abspath(os.path.join(testdir, srcdir)))
import yaml
from scrapy.http import HtmlResponse, Request
from keepup_scrappers.spiders.geonews_spider import GNSpider

class TestGNSpider:

    def setup_method(self):
        
        # sitekey and name intialization
        self.site_key = 'geonews'
        self.spider_name = 'gn_spider'
        
        # initialization of spider
        self.spider = GNSpider()
        
        # loading config file
        config_path = os.path.join(os.path.dirname(__file__), '..', 'keepup_scrappers', 'config', 'config.yaml')
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)

        # load site config
        self.site_config = self.config['sites']['geonews']
        self.spider.selectors = self.site_config['selectors']

    def test_spider_initialization(self):
        assert self.spider.site_key == self.site_key
        assert self.spider.name == self.spider_name
        #assert self.spider.page_counter == 1
        assert self.spider.custom_settings['IMAGES_STORE'] == f'data/{self.site_key}/images/'

    def test_parse_method(self):
        
        with open(r'D:\myenv\keepup-scrappers\src\tests\test_data\geonews\listing_sample.html', 'r', encoding='utf-8') as f:
            html_content = f.read()    

        mock_response = HtmlResponse(
            url = self.spider.start_urls[0],
            body = html_content,
            encoding='utf-8',
        )

        results = list(self.spider.parse(mock_response))
   
        assert len(results) == 59  # 12 items + one next page request
        
        item = results[0].meta['item']
        assert item['title'] == '50 Cent to fight legal dispute over alleged SUV assault'
        
        assert item['detail_url'] == 'https://www.geo.tv/latest/587786-50-cent-to-fight-legal-dispute-over-alleged-suv-assault'
        
   
    def test_parse_details_method(self):

        with open(r'D:\myenv\keepup-scrappers\src\tests\test_data\geonews\detail_sample.html', 'r', encoding='utf-8') as f:
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
        assert item['image_urls'][0] == 'https://www.geo.tv/assets/uploads/updates/2025-01-28/587786_8903706_updates.jpg'
        #assert item['label'] == 'False'
        assert item['author'] == 'Web Desk'
        assert item['publication_date'] == 'January 28, 2025'
        assert item['content'] == "Rapper 50 Cent addressed a legal dispute Monday involving a photographer, Guadalupe De Los Santos, who filed a lawsuit in Los Angeles Superior Court.  De Los Santos claims the rapper ordered him to be knocked off his electric scooter using a car door following a book signing at The Grove in LA on September 11, 2022. According to  , represented by renowned attorney Gloria Allred, De Los Santos alleges that a member of 50 Cent's entourage caused the incident, leaving him injured and unable to work. Moreover, the photographer, who was capturing professional shots of the rapper, stated in legal documents that the SUV's passenger door was deliberately opened, striking his left side and damaging his scooter. Additionally, De Los Santos claims the incident resulted in significant medical expenses and loss of income, prompting his pursuit of damages. As per the publication, 50 Cent, whose real name is Curtis Jackson, denied the allegations through his legal team, asserting he had not been served with the lawsuit.  Furthermore, his attorney stated, \"If and when such a frivolous claim is filed and served, Mr. Jackson’s legal team will swiftly move to dismiss it and seek maximum sanctions.” It is worth mentioning that the rapper took to Instagram to address the case humorously, sharing past photos of himself with Allred and writing, \"Gloria, you should know better, chase a different ambulance.\" He also dismissed the allegations as an attempt to extort money, while adding, \"Gloria, you’re not gonna get any money from me that way, but if you call me, I’ll take you to dinner. LOL.\""