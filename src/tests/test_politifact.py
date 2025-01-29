import os
import sys
testdir = os.path.dirname(__file__)
srcdir = '..'
sys.path.insert(0, os.path.abspath(os.path.join(testdir, srcdir)))
import yaml
from scrapy.http import HtmlResponse, Request
from keepup_scrappers.spiders.politifact_spider import PolitifactSpider

class TestIverifySpider:

    def setup_method(self):
        
        # sitekey and name intialization
        self.site_key = 'politifact'
        self.spider_name = 'politifact_spider'
        
        # initialization of spider
        self.spider = PolitifactSpider()
        
        # loading config file
        config_path = os.path.join(os.path.dirname(__file__), '..', 'keepup_scrappers', 'config', 'config.yaml')
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)

        # load site config
        self.site_config = self.config['sites']['politifact']
        self.spider.selectors = self.site_config['selectors']

    def test_spider_initialization(self):
        assert self.spider.site_key == self.site_key
        assert self.spider.name == self.spider_name
        assert self.spider.page_counter == 1
        assert self.spider.custom_settings['IMAGES_STORE'] == f'data/{self.site_key}/images/'

    def test_parse_method(self):
        
        with open(r'D:\myenv\keepup-scrappers\src\tests\test_data\politifact\listing_sample.html', 'r', encoding='utf-8') as f:
            html_content = f.read()    

        mock_response = HtmlResponse(
            url = self.spider.start_urls[0],
            body = html_content,
            encoding='utf-8',
        )

        results = list(self.spider.parse(mock_response))
   
        assert len(results) == 31  # 12 items + one next page request
        
        item = results[0].meta['item']
        assert item['title'] == '“President Trump just announced full nationwide concealed carry reciprocity.”'
       
        assert item['detail_url'] == 'https://www.politifact.com/factchecks/2025/jan/29/facebook-posts/no-trump-didnt-expand-conceal-carry-reciprocity-th/'
        
        assert item['label'] == 'false'
        
   
    def test_parse_details_method(self):

        with open(r'D:\myenv\keepup-scrappers\src\tests\test_data\politifact\detail_sample.html', 'r', encoding='utf-8') as f:
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
        assert item['author'] == "Ciara O'Rourke"
        assert item['publication_date'] == 'January 29, 2025'
        #assert item['image_urls'][0] == '[]'


        assert item['content'] == "U.S. Rep. Richard Hudson, R-N.C., and 169 co-sponsors reintroduced a bill Jan. 3 that would expand concealed carry permit rights in the United States. But a recent Facebook post jumps the gun by claiming President Donald Trump has enabled anyone with such a permit to legally carry a firearm in any other state that allows concealed carry. \"BREAKING NEWS,\" a Jan. 25 Facebook said. \"President Trump just announced FULL nationwide concealed carry reciprocity.\" The post includes an image of Trump signing a document, surrounded by smiling lawmakers. This post was flagged as part of Meta’s efforts to combat false news and misinformation on its News Feed. (Read more about our , which owns Facebook, Instagram and Threads.) , the proposed , would allow people who have a concealed carry permit in one state to carry that concealed firearm in other states that have such laws. Concealed carry is legal in some form in all 50 states, either by permit or automatically for those who are eligible in states that allow \"constitutional carry\" or \"permitless carry,\" Andrew Willinger, executive director of the Duke Center for Firearms Law, said. Some states already honor concealed carry permits from other states. Some do not. Trump during his 2024 presidential campaign to sign concealed carry reciprocity legislation. \"Your Second Amendment does not end at the state line,\" Trump . Trump made and broke a . Willinger told PolitiFact that although Trump has said he would sign the proposed legislation if it passes the House and Senate, \"I’m not aware of any executive action by President Trump related to concealed carry permitting or reciprocity.\" The image in the Facebook post is old. It , signing a policy directive that directed NASA to return to the moon. We rate claims Trump expanded concealed carry reciprocity False."