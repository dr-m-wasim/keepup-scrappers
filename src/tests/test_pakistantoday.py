import os
import sys
testdir = os.path.dirname(__file__)
srcdir = '..'
sys.path.insert(0, os.path.abspath(os.path.join(testdir, srcdir)))
import yaml
from scrapy.http import HtmlResponse, Request
from keepup_scrappers.spiders.pakistantoday_spider import PakistanTodaySpider
import re

class TestpakistantodaySpider:

    def setup_method(self):
        
        # sitekey and name intialization
        self.site_key = 'pakistantoday'
        self.spider_name = 'pakistantoday_spider'
        
        # initialization of spider
        self.spider = PakistanTodaySpider()
        # loading config file
        config_path = os.path.join(os.path.dirname(__file__), '..', 'keepup_scrappers', 'config', 'config.yaml')
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)

        # load site config
        self.site_config = self.config['sites']['pakistantoday']
        self.spider.selectors = self.site_config['selectors']

    def test_spider_initialization(self):
        assert self.spider.site_key == self.site_key
        assert self.spider.name == self.spider_name
        assert self.spider.page_counter == 1
        assert self.spider.custom_settings['IMAGES_STORE'] == f'data/{self.site_key}/images/'

    import re

    def test_parse_method(self):
        with open(r'tests\test_data\pakistantoday\listing_sample (2).json', 'r', encoding='utf-8') as f:
            html_content = f.read()

        # Clean the HTML content to remove invalid control characters
        html_content = re.sub(r'[\x00-\x1F\x7F]', '', html_content)  # Remove non-printable characters

        mock_response = HtmlResponse(
            url=self.spider.start_urls[0],
            body=html_content,
            encoding='utf-8',
        )

        results = list(self.spider.parse(mock_response))

    # Continue with your assertions

   
        #assert len(results) == 32 # 12 items + one next page request
        
        item = results[0].meta['item']
        assert item['title'] == "Saudi Arabia’s new airlines commences flight operations to Pakistan"
        assert item['image_urls'][0] == 'https://www.pakistantoday.com.pk/wp-content/uploads/2025/02/Flyadeal-218x150.jpg'
        assert item['detail_url'] == 'https://www.pakistantoday.com.pk/2025/02/01/saudi-arabias-new-airlines-commences-flight-operations-to-pakistan/'
        assert item['exerpt'] == 'KARACHI: Saudi Arabia’s new airlines, Flyadeal, has commenced its flight operations to Pakistan.\r\n\r\nAccording to a PAA spokesperson, the first Flyadeal flight, F3...'
        
        #assert item['author'] == 'CEJ'
   
    def test_parse_details_method(self):

        with open(r'tests\test_data\pakistantoday\detail_sample (2).html', 'r', encoding='utf-8') as f:
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
        assert item['content'] == "LAHORE: The identification of 13 Pakistani nationals who perished in the Morocco boat tragedy has been completed, according to diplomatic sources. The accident, which occurred on January 2 after the vessel departed from Mauritania, claimed the lives of at least 50 people, including 66 Pakistanis onboard. The Pakistani embassy in Morocco, in coordination with local authorities, shared fingerprint data and photographs with the National Database and Registration Authority (NADRA) to verify the victims’ identities. Officials have now released the names of the deceased: Although early reports indicated that 44 Pakistani nationals had died in the tragedy, only 13 bodies were recovered. Moroccan authorities rescued 36 people from the ill-fated vessel. In response to the tragedy, Pakistani Prime Minister Shehbaz Sharif directed strict action against human traffickers and officials involved in facilitating illegal migration. Authorities have already dismissed 35 officials for their roles in smuggling operations. Eight survivors of the accident, aged between 21 and 41, returned to Pakistan today aboard Qatar Airways flight QR614 and are being questioned by officials. They include Muhammad Afzal, Muhammad Adeel, Irfan Ahmed, Arsalan Shamil, Ghulam Mustafa, Badram Muhiuddin, Mujahid Ali, and Tasbeeh Ahmed Shamil. These survivors hail from various districts, including Sheikhupura, Sialkot, Mandi Bahauddin, Gujarat, and Jhelum. Another group of seven survivors from districts such as Gujranwala and Hafizabad arrived in Pakistan last night. The boat tragedy underscores the dangers faced by migrants and the urgency to address human trafficking networks that operate across multiple regions, including Senegal, Mauritania, and Morocco."

        assert item['publication_date'] == 'February 4, 2025'
        assert item['author'] == 'Monitoring Report'
       
        