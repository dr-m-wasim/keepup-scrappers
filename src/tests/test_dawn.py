import os
import sys
testdir = os.path.dirname(__file__)
srcdir = '..'
sys.path.insert(0, os.path.abspath(os.path.join(testdir, srcdir)))
import yaml
from scrapy.http import HtmlResponse, Request
from keepup_scrappers.spiders.dawn_spider import DawnSpider

class TestdawnSpider:

    def setup_method(self):
        
        # sitekey and name intialization
        self.site_key = 'dawn'
        self.spider_name = 'dawn_spider'
        
        # initialization of spider
        self.spider = DawnSpider()
        
        # loading config file
        config_path = os.path.join(os.path.dirname(__file__), '..', 'keepup_scrappers', 'config', 'config.yaml')
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)

        # load site config
        self.site_config = self.config['sites']['dawn']
        self.spider.selectors = self.site_config['selectors']

    def test_spider_initialization(self):
        assert self.spider.site_key == self.site_key
        assert self.spider.name == self.spider_name
        #assert self.spider.page_counter == 1
        assert self.spider.custom_settings['IMAGES_STORE'] == f'data/{self.site_key}/images/'

    def test_parse_method(self):
        
        with open(r'D:\myenv\keepup-scrappers\src\tests\test_data\dawn\listing_sample.html', 'r', encoding='utf-8') as f:
            html_content = f.read()    

        mock_response = HtmlResponse(
            url = self.spider.start_urls[0],
            body = html_content,
            encoding='utf-8',
        )

        results = list(self.spider.parse(mock_response))
   
        assert len(results) == 228  # 12 items + one next page request
        
        item = results[0].meta['item']
        assert item['title'] == 'Alibaba releases AI model it claims surpasses DeepSeek-V3'
        
        assert item['detail_url'] == 'https://www.dawn.com/news/1888473/alibaba-releases-ai-model-it-claims-surpasses-deepseek-v3'
        
   
    def test_parse_details_method(self):

        with open(r'D:\myenv\keepup-scrappers\src\tests\test_data\dawn\detail_sample.html', 'r', encoding='utf-8') as f:
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
        assert item['publication_date'] == 'January 29, 2025'
        assert item['image_urls'][0] == 'https://i.dawn.com/primary/2025/01/29202159cee27f1.jpg'
        
        assert item['author'] == 'Reuters'
        assert item['content'] == "Chinese tech company Alibaba on Wednesday released a new version of its Qwen 2.5 artificial intelligence (AI) model that it claimed surpassed the highly acclaimed  -V3. The unusual timing of the Qwen 2.5-Max’s release, on the first day of the Lunar New Year when most Chinese people are off work and with their families, points to the pressure Chinese AI startup DeepSeek’s meteoric rise in the past three weeks has placed on not just overseas rivals, but also its domestic competition. “Qwen 2.5-Max outperforms … almost across the board GPT-4o, DeepSeek-V3 and Llama-3.1-405B,” Alibaba’s cloud unit said in an announcement posted on its official WeChat account, referring to OpenAI and Meta’s most advanced open-source AI models. The January 10 release of DeepSeek’s AI assistant, powered by the DeepSeek-V3 model, as well as the Jan 20 release of its R1 model, has   Silicon Valley and caused tech shares to plunge, with the Chinese startup’s purportedly low development and usage costs prompting investors to question huge spending plans by leading AI firms in the United States. But DeepSeek’s success has also led to a scramble among its domestic competitors to upgrade their own AI models. Two days after the release of DeepSeek-R1, TikTok owner ByteDance released an update to its flagship AI model, which it claimed outperformed Microsoft-backed OpenAI’s o1 in AIME, a benchmark test that measures how well AI models understand and respond to complex instructions. This echoed DeepSeek’s claim that its R1 model rivalled OpenAI’s o1 on several performance benchmarks."