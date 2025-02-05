import os
import sys
testdir = os.path.dirname(__file__)
srcdir = '..'
sys.path.insert(0, os.path.abspath(os.path.join(testdir, srcdir)))
import yaml
from scrapy.http import HtmlResponse, Request
from keepup_scrappers.spiders.dailytimes_spider import DailyTimesSpider

class TestdailytimesSpider:

    def setup_method(self):
        
        # sitekey and name intialization
        self.site_key = 'dailytimes'
        self.spider_name = 'dailytimes_spider'
        
        # initialization of spider
        self.spider = DailyTimesSpider()
        # loading config file
        config_path = os.path.join(os.path.dirname(__file__), '..', 'keepup_scrappers', 'config', 'config.yaml')
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)

        # load site config
        self.site_config = self.config['sites']['dailytimes']
        self.spider.selectors = self.site_config['selectors']

    def test_spider_initialization(self):
        assert self.spider.site_key == self.site_key
        assert self.spider.name == self.spider_name
        assert self.spider.page_counter == 1
        assert self.spider.custom_settings['IMAGES_STORE'] == f'data/{self.site_key}/images/'

    def test_parse_method(self):
        
        with open(r'tests\test_data\dailytimes\listing_sample.html', 'r', encoding='utf-8') as f:
            html_content = f.read()    

        mock_response = HtmlResponse(
            url = self.spider.start_urls[0],
            body = html_content,
            encoding='utf-8',
        )

        results = list(self.spider.parse(mock_response))
   
        assert len(results) == 11  # 12 items + one next page request
        
        item = results[0].meta['item']
        assert item['title'] == 'PML-N Mushahid Hussain says Nawaz not suited for PM Office in ‘hybrid plus’ system'
        
        assert item['detail_url'] == 'https://dailytimes.com.pk/1158965/pml-n-mushahid-hussain-says-nawaz-not-suited-for-pm-office-in-hybrid-plus-system/'
        assert item['image_urls'][0] == 'https://dailytimes.com.pk/assets/uploads/2019/05/27/Mushahid-Hussain-Syed-150x150.jpg'
        assert item['exerpt'] == 'PML-N Senator Mushahid Hussain Syed has reportedly advised the party’s leader, Nawaz Sharif, to consider pursuing the presidency instead of the prime minister’s office in the current “hybrid plus” system. In an interview with a private news channel, Senator Mushahid expressed concerns about the suitability of Nawaz Sharif for the role of prime minister and […]'
        
   
    def test_parse_details_method(self):

        with open(r'tests\test_data\dailytimes\detail_sample.html', 'r', encoding='utf-8') as f:
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
        assert item['publication_date'] == 'January 8, 2024'
        assert item['author'] == 'Web Desk'
        assert item['content'] == "PML-N Senator Mushahid Hussain Syed has reportedly advised the party’s leader, Nawaz Sharif, to consider pursuing the presidency instead of the prime minister’s office in the current “hybrid plus” system. In an interview with a private news channel, Senator Mushahid expressed concerns about the suitability of Nawaz Sharif for the role of prime minister and suggested that the presidency, with its significance as the supreme commander of the military, would be a more fitting position for him. Highlighting the frequent changes in prime ministers over the last few years, Senator Mushahid recommended that Nawaz Sharif step back and allow another party member to take on the role of prime minister. He further proposed the idea of a national government, citing his belief that no single party would be able to secure a simple majority in the upcoming elections scheduled for February 8. Addressing the concept of the “mother of all deals,” Senator Mushahid acknowledged certain political maneuvers, such as bringing individuals into power and later ousting them, and the necessity of making deals as required. He stressed the importance of reconciliation and cooperation among the major political parties, specifically mentioning PML-N, PTI, and PPP as national parties with distinct bases of support. Senator Mushahid underlined the significance of considering the national interest in politics, particularly pointing out the challenges faced by the PTI in Khyber Pakhtunkhwa (KP) due to its proximity to Afghanistan and strained ties with the Afghan government. He emphasized the need for collaboration among political parties and bridging the gap between the elite and the general public in the current political landscape."