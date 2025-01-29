import os
import sys
testdir = os.path.dirname(__file__)
srcdir = '..'
sys.path.insert(0, os.path.abspath(os.path.join(testdir, srcdir)))
import yaml
from scrapy.http import HtmlResponse, Request
from keepup_scrappers.spiders.pakiverify_spider import PakIverifySpider

class TestIverifySpider:

    def setup_method(self):
        
        # sitekey and name intialization
        self.site_key = 'pakiverify'
        self.spider_name = 'pakiverify_spider'
        
        # initialization of spider
        self.spider = PakIverifySpider()
        
        # loading config file
        config_path = os.path.join(os.path.dirname(__file__), '..', 'keepup_scrappers', 'config', 'config.yaml')
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)

        # load site config
        self.site_config = self.config['sites']['pakiverify']
        self.spider.selectors = self.site_config['selectors']

    def test_spider_initialization(self):
        assert self.spider.site_key == self.site_key
        assert self.spider.name == self.spider_name
        assert self.spider.page_counter == 1
        assert self.spider.custom_settings['IMAGES_STORE'] == f'data/{self.site_key}/images/'

    def test_parse_method(self):
        
        with open(r'tests/test_data/iverify/listing_sample.html', 'r', encoding='utf-8') as f:
            html_content = f.read()    

        mock_response = HtmlResponse(
            url = self.spider.start_urls[0],
            body = html_content,
            encoding='utf-8',
        )

        results = list(self.spider.parse(mock_response))
   
        assert len(results) == 13  # 12 items + one next page request
        
        item = results[0].meta['item']
        assert item['title'] == 'Viral video does not show Saudi minister getting scared by crackers upon arrival at Riyadh’s Chinese embassy'
        assert item['publication_date'] == 'January 15, 2025'
        assert item['detail_url'] == 'https://pak.i-verify.org/viral-video-does-not-show-saudi-minister-getting-scared-by-crackers-upon-arrival-at-riyadhs-chinese-embassy/'
        assert item['image_urls'][0] == 'https://pak.i-verify.org/wp-content/uploads/2025/01/image-23.jpg'
        assert item['label'] == 'False'
        assert item['author'] == 'CEJ'
   
    def test_parse_details_method(self):

        with open(r'tests/test_data/iverify/details_sample.html', 'r', encoding='utf-8') as f:
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
        assert item['content'] == 'False FACT-CHECKED Posts from multiple users on social media platforms since January 6, 2025, shared a video, claiming it showed Saudi Arabia’s defence minister being scared by crackers during a visit to the Chinese embassy. However, the video is from a 2019 mock military drill in Kuwait. Claim Video of Saudi defence minister getting scared, fleeing due to crackers at his arrival at Riyadh’s Chinese embassy Rating Justification The iVerify Pakistan team investigated this content and determined that it is . To reach the conclusion, iVerify Pakistan conducted the reverse image and a keyword search to find the original source. Posts from multiple users on social media platforms since January 6, 2025, shared a video, claiming it showed Saudi Arabia’s defence minister being scared by crackers during a visit to the Chinese embassy. However, the video is from a mock military drill in Kuwait. On Jan 15, the iVerify Pakistan team was alerted by the public about a video circulating on the messaging platform WhatsApp featuring a man in traditional Saudi attire with a white keffiyeh headdress with the claim that he was the country’s defence minister who was spooked by crackers going off during a visit to the Chinese embassy. The message was accompanied by the caption: “The Saudi defence minister visited the Chinese embassy in Riyadh but the Chinese Embassy did not inform him that crackers would be set off to welcome him.” The video and the same caption were shared across other social media platforms, including Facebook , , and , as well as on X , , and . A fact-check was initiated to determine the veracity of the claim due to its virality and keen public interest in the affairs of Saudi Arabia and China. A reverse image search yielded a on an Arabic YouTube channel dated December 12, 2024, titled: “Training of the royal guard at the exhibition grounds … This is how situations are handled when gunfire is directed at prominent figures.” A Jan 5 was also found with the caption: “Amiri guards shows how they handle when a VIP is shot. Gulf Defence and AVSON exhibition on December 12, 2019. A keyword search for “Gulf Defence Exhibition 2019” yielded a video of the same scene from another angle on X by Saudi-based outlet with the following caption: “Gulf Defence and Aerospace Exhibition | Amiri Guards Mock Military Show” on December 12, 2019. Highlights from the exhibition were also on the official Instagram account of Kuwait’s army, including the clip of the scene with the following caption: “Part of the Amiri Guard Authority’s show that was implemented during the fifth Gulf Defence and Aviation Exhibition, which was held during the period from December 10-12, 2019 at the Mishref Exhibition Grounds.” The Amiri Guard is an elite protection unit of Qatar’s military. The Gulf Defence and Aviation Exhibition is a leading bi-annual defence, security and military . Its fifth edition was held in December 2019 at the Kuwait International Fair Grounds in the Mishref neighbourhood. It is pertinent to note that the same video with the same and different captions was shared across social media platforms periodically in the past and was fact-checked by credible outlets such as and . The claim that a video shows the Saudi defence minister recoiling in fear and fleeing after crackers go off to welcome him at the Chinese embassy in Riyadh is . The video is from a mock military drill in Kuwait during the Gulf Defence and Aviation Exhibition held in December 2019. Evidence and References December 12, 2019, X post: December 11, 2019, Kuwait army Instagram post:'