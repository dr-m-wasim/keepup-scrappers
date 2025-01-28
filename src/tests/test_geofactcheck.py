import sys
import os
testdir = os.path.dirname(__file__)
srcdir = '..'
sys.path.insert(0, os.path.abspath(os.path.join(testdir, srcdir)))
import yaml
from scrapy.http import HtmlResponse, Request
from keepup_scrappers.spiders.GFC_spider import GFCSpider

class TestGFCSpider:

    def setup_method(self):
        # Site key and name initialization
        self.site_key = 'geofactcheck'
        self.spider_name = 'gfc_spider'
        #start_urls = ['https://www.geo.tv/category/geo-fact-check']

        # Initialization of spider
        self.spider = GFCSpider()

       # loading config file
        config_path = os.path.join(os.path.dirname(__file__), '..', 'keepup_scrappers', 'config', 'config.yaml')
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)

        # load site config
        self.site_config = self.config['sites']['geofactcheck']
        self.spider.selectors = self.site_config['selectors']

    def test_spider_initialization(self):
        assert self.spider.site_key == self.site_key
        assert self.spider.name == self.spider_name
        assert self.spider.page_counter == 1
        assert self.spider.custom_settings['IMAGES_STORE'] == f'data/{self.site_key}/images/'

    def test_parse_method(self):
        
        with open(r'D:\myenv\keepup-scrappers\src\tests\test_data\geofactcheck\listing_sample.html', 'r', encoding='utf-8') as f:
            html_content = f.read()    

        mock_response = HtmlResponse(
            url = self.spider.start_urls[0],
            body = html_content,
            encoding='utf-8',
        )

        results = list(self.spider.parse(mock_response))

        assert len(results) == 6  # 12 items + one next page request

        item = results[0].meta['item']
        assert item['title'] == 'Fact-check: NADRA has not removed Azad Jammu and Kashmir from ID cards'
        assert item['publication_date'] == 'Jan 27, 2025'
        assert item['detail_url'] ==  'https://www.geo.tv/latest/587573-fact-check-nadra-has-not-removed-azad-jammu-and-kashmir-from-id-cards'
        assert item['image_urls'][0] == 'https://www.geo.tv/assets/uploads/updates/2025-01-27/l_587573_121503_updates.jpg'
        assert item['author'] == 'Muhammad Binyameen Iqbal'

    def test_parse_details_method(self):

        with open(r'D:\myenv\keepup-scrappers\src\tests\test_data\geofactcheck\detail_sample.html', 'r', encoding='utf-8') as f:
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
        assert item['content'] == 'Social media is abuzz with claims that the National Database and Registration Authority (NADRA) has removed Azad Jammu and Kashmir (AJK) from the identity cards of its residents. These claims have sparked outrage, with many accusing NADRA of discriminating against the people of Kashmir. The claim is false. On January 18, a Facebook user posted: “The stubbornness of NADRA continues as it has removed AJK from the identity cards.” This post has been shared more than 90 times and liked 88 times to date. Identical claims were also shared , and . Both NADRA officials and representatives of the AJK government have refuted these claims, confirming that AJK has not been removed from the identity cards of its residents. Shabahat Ali, a spokesperson for NADRA, provided a press release to , dated January 19, which called the online allegations “baseless.” According to the press release, NADRA prints the phrase \"Resident of AJK [Azad Jammu and Kashmir] state\" in black on Smart Computerised National Identity Cards (CNICs) and in red on regular CNICs. It was also clarified that in order for a person’s CNIC to include “Resident of AJK,” the individual must submit a valid State Subject Certificate (Class 1, 2, or 3), issued by the AJK government. Without this certificate, the residency status cannot be printed on the identity card. From December 2024 to January 2025, NADRA has issued over 50,000 CNICs with the \"Resident of AJK\" status imprinted, disproving the claim that such information is being omitted. For the full press release, see : Additionally, Muhammad Mazhar Saeed, the information minister for AJK, also dismissed the claims, labeling them as \"completely fake news.\" He reiterated that in order to have AJK status printed on a CNIC, an individual must submit the required documentation, specifically the State Subject Certificate, as proof of residency in AJK. The claim that NADRA has removed \"Resident of AJK\" from the CNICs of Azad Jammu and Kashmir residents is false. Both NADRA and AJK government officials have confirmed that these rumors are entirely baseless and constitute misinformation.'
