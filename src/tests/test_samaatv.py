import os
import sys
testdir = os.path.dirname(__file__)
srcdir = '..'
sys.path.insert(0, os.path.abspath(os.path.join(testdir, srcdir)))
import yaml
from scrapy.http import HtmlResponse, Request
from keepup_scrappers.spiders.samaatv_spider import SamaaTVSpider

class TestsamaatvSpider:

    def setup_method(self):
        
        # sitekey and name intialization
        self.site_key = 'samaatv'
        self.spider_name = 'samaatv_spider'
        
        # initialization of spider
        self.spider = SamaaTVSpider()
        
        # loading config file
        config_path = os.path.join(os.path.dirname(__file__), '..', 'keepup_scrappers', 'config', 'config.yaml')
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)

        # load site config
        self.site_config = self.config['sites']['samaatv']
        self.spider.selectors = self.site_config['selectors']

    def test_spider_initialization(self):
        assert self.spider.site_key == self.site_key
        assert self.spider.name == self.spider_name
        assert self.spider.page_counter == 1
        assert self.spider.custom_settings['IMAGES_STORE'] == f'data/{self.site_key}/images/'

    def test_parse_method(self):
        
        with open(r'tests\test_data\samaatv\listing_sample (2).html', 'r', encoding='utf-8') as f:
            html_content = f.read()    

        mock_response = HtmlResponse(
            url = self.spider.start_urls[0],
            body = html_content,
            encoding='utf-8',
        )

        results = list(self.spider.parse(mock_response))
   
        assert len(results) == 25  # 12 items + one next page request
        
        item = results[0].meta['item']
        assert item['title'] == 'How US Congress is tackling threat of deepfakes'
        
        assert item['detail_url'] == 'https://www.samaa.tv/2087328512-how-us-congress-is-tackling-threat-of-deepfakes'
        assert item['image_urls'][0] == 'https://www.samaa.tv/images/sa-14.jpg'
        assert item['exerpt'] == 'Legislation in 2024 and 2025 aims to counter AI-generated deceptive content'
        
   
    def test_parse_details_method(self):

        with open(r'tests\test_data\samaatv\detail_sample (2).html', 'r', encoding='utf-8') as f:
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
        assert item['content'] == 'Deepfake technology, which uses artificial intelligence to create hyper-realistic but entirely fabricated videos and audio, has emerged as a growing concern in the digital world. From politicians being depicted making false statements to celebrities being exploited in non-consensual content, the potential for harm is vast. In response, the United States Congress has taken steps toward regulating and, in certain instances, banning the creation and distribution of deepfakes. Deepfakes have surged in popularity, as AI tools have become more sophisticated, making it increasingly difficult to distinguish between real and doctored media. According to a report from the Congressional Research Service, the use of deepfakes surged by over 100% between 2022 and 2024, with concerns rising over their influence in spreading disinformation and manipulating public opinion. The risks associated with this technology are especially alarming when considering its potential role in influencing elections, as seen in the heightened awareness surrounding deepfake political advertisements and fake news during recent elections. To curb the misuse of this powerful technology, US lawmakers have made significant strides in crafting legislation aimed at protecting individuals and institutions from malicious deepfake content. The DEEPFAKES Accountability Act of 2024 seeks to make it a federal crime to produce, distribute, or broadcast deceptive deepfakes without disclosure. This bill, introduced in Congress in late 2024, targets both the creators of such media and the platforms that host them without appropriate content moderation. One of the key provisions of the bill is the requirement for a watermark or clear labeling to identify AI-generated content, making it easier for viewers to distinguish between real and fake media. In addition, violators could face hefty fines and imprisonment, depending on the severity of the offense. Deepfakes have become a tool for political manipulation, with fake videos of candidates being used to mislead voters or tarnish reputations. In response, senators like Amy Klobuchar and Josh Hawley had proposed measures to ban the use of AI-generated content in political advertisements unless clearly disclosed. Another significant aspect of the legislative conversation centers on the non-consensual use of deepfake technology. Non-consensual deepfakes, particularly those involving explicit content, have raised ethical and legal concerns about privacy, consent, and harassment. The DEFIANCE Act of 2024, introduced by Senator Angus King, targets the creation of sexually explicit deepfakes, making it a punishable offense to create or distribute such content without the subject’s consent. This bill aims to provide victims with the ability to file lawsuits against perpetrators and seek financial damages. Legal experts note that this could set a precedent for future privacy laws in the digital age. Despite the progress made by US lawmakers, challenges remain in regulating deepfakes effectively. One of the major obstacles is the international nature of the internet. Deepfake creators often operate from countries with lax regulations, making enforcement difficult. Furthermore, the rapid development of AI technology means that new tools to generate deepfakes are constantly emerging, complicating efforts to stay ahead of the curve. As the US Congress continues to debate and refine its approach to deepfake legislation in 2025, the challenge will be striking a balance between protecting individuals from harm and allowing innovation in AI technology to flourish. With more legislation expected in the coming months, it is clear that the conversation around deepfakes is far from over. The next few years will be pivotal in shaping the future of digital media. If Congress succeeds in creating a robust legal framework for regulating deepfakes, it will help pave the way for a safer and more transparent digital world. However, technological advancements will require constant vigilance, as lawmakers work to address the evolving nature of AI-generated content.'
        assert item['publication_date'] == 'Feb 05, 2025'
        assert item['author'] == 'Waniya Kabir Ahmad'