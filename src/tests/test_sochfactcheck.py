import os
import sys
testdir = os.path.dirname(__file__)
srcdir = '..'
sys.path.insert(0, os.path.abspath(os.path.join(testdir, srcdir)))
import yaml
from scrapy.http import HtmlResponse, Request
from keepup_scrappers.spiders.sochfactcheck_spider import SochFactCheckSpider

class TestSochFactCheckSpider:

    def setup_method(self):
        
        # sitekey and name intialization
        self.site_key = 'sochfactcheck'
        self.spider_name = 'sochfactcheck_spider'
        
        # initialization of spider
        self.spider = SochFactCheckSpider()
        # loading config file
        config_path = os.path.join(os.path.dirname(__file__), '..', 'keepup_scrappers', 'config', 'config.yaml')
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)

        # load site config
        self.site_config = self.config['sites']['sochfactcheck']
        self.spider.selectors = self.site_config['selectors']

    def test_spider_initialization(self):
        assert self.spider.site_key == self.site_key
        assert self.spider.name == self.spider_name
        assert self.spider.page_counter == 1
        assert self.spider.custom_settings['IMAGES_STORE'] == f'data/{self.site_key}/images/'

    def test_parse_method(self):
        
        with open(r'tests\test_data\sochfactcheck\listing_sample.json', 'r', encoding='utf-8') as f:
            html_content = f.read()    

        mock_response = HtmlResponse(
            url = self.spider.start_urls[0],
            body = html_content,
            encoding='utf-8',
        )

        results = list(self.spider.parse(mock_response))
   
        assert len(results) == 31  # 12 items + one next page request
        
        item = results[0].meta['item']
        assert item['title'] == 'Video showing Matiullah Jan’s expulsion from PMA debunked'
        assert item['publication_date'] == 'Dec 16, 2024'
        assert item['detail_url'] == 'https://www.sochfactcheck.com/video-showing-matiullah-jan-expulsion-from-pma-debunked/'
        assert item['image_urls'][0] == 'https://www.sochfactcheck.com/wp-content/uploads/2024/12/Untitled-design-1.png'
         
        
   
    def test_parse_details_method(self):

        with open(r'tests\test_data\sochfactcheck\detail_sample.html', 'r', encoding='utf-8') as f:
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
        #assert item['label'] == 'False'
        assert item['author'] == 'Editorial Team'
        assert item['content'] == "Claim : A video shows journalist Matiullah Jan in an army cadet’s uniform being stripped of his rank and discharged from the Pakistan Military Academy (PMA) due to poor character. Fact : The video does not show Matiullah Jan’s expulsion from the PMA. It is actually a digitally manipulated clip from Hum TV’s drama serial ‘Ehd-e-Wafa,’ with Jan’s face superimposed on the actor’s. On 28 November, X user @ImrankhanISP1 shared a video ( archive ) on X, writing, “مطیع اللہ جان اپنے گندے کاموں کا خمیازہ پہلے بھی بھگت چکا ہے مطیع اللہ جان کو پی ایم اے سے گندے کردار کی وجہ سے نکال دیا گیا تھا مگر افسوس کہ وہ آج بھی سبق نہیں سیکھا جھوٹ اور پروپیگنڈا کرنے والوں کا انجام ہمیشہ ایک جیسا ہوتا ہے” [Translated from Urdu: Matiullah Jan has suffered the consequences of his dirty deeds before Matiullah Jan was expelled from the PMA for his dirty character But unfortunately he has not learned the lesson even today The fate of liars and propagandists is always the same] Some social media users also shared a clip ( archive ) of a news segment of Suno News , a Pakistani broadcast news outlet, which featured a screenshot of the video alongside a discussion about Jan’s alleged expulsion. According to the Suno News segment, Matiullah Jan, Cadet No. 22801, joined the PMA’s 79th Long Course, was demoted to the 80th Long Course for poor performance and expelled in 1988 due to moral misconduct and a disreputable character. The segment also cited negative feedback allegedly attributed to his fellow cadets, including claims of dishonesty, uncooperative behaviour, and unreliability. Journalist, court reporter, and columnist Matiullah Jan was abducted on 25 November and charged with terrorism, according to a colleague and his lawyer, according to Reuters . Hours before he was picked up , Jan appeared on a TV show where he presented what he claimed were hospital records. These records contradicted the government’s denial that live ammunition was used by security forces to disperse the PTI protest at Islamabad’s D-Chowk or that any protesters were killed, according to Reuters . His lawyer Imaan Mazari said he had been charged with terrorism, drug peddling and attacking the police, the same report stated. It further added that the charges seen by Reuters alleged Jan had been under the influence of drugs at the time of the arrest. “The senior journalist was released from jail in a terrorism and narcotics case after an anti-terrorism court (ATC) in the federal capital approved his bail petition on Saturday, 30 November,” reported Geo News . Soch Fact Check conducted a reverse image search of keyframes of the video and was directed to an episode of Hum TV’s drama serial ‘Ehd-e-Wafa’. At 7:31 , a military cadet is shown being stripped of his rank and discharged from the PMA. Noting that the dialogue, actors, and layout of the entire scene match the clip in the claim, we concluded that this segment was digitally altered to superimpose Jan’s face onto an actor’s in the drama. Digitally altered videos often exhibit unnatural elements, such as the greyish-black hue visible on the edges of the altered video’s frames in contrast to the clear visuals in Hum TV’s stills. Additionally, the ISPR logo is blurred in the manipulated version. If this was genuine ISPR footage, the logo would remain unaltered. There are clear signs of digital manipulation in the clip. For instance, the Battalion Havildar Major’s (BHM) hands cut off midway while removing the badges on the uniform. Additionally, in scenes where the journalist’s face has been superimposed, we noticed other inconsistencies, such as the BHM’s hands appearing twice in some frames. Jan’s eyes also appear distorted during the removal of badges from his beret. Similarly, towards the end of the clip, his facial expressions remain static, while his face moves unnaturally, sometimes to the side and even beyond his beret. When the camera zooms out, the other actors’ faces are clearly visible and well-defined but Jan’s face appears blurred, making it difficult to distinguish his features. Soch Fact Check was unable to find the Suno News segment on their YouTube channel and did not receive a response to its request for comment. Several X users criticised the channel for airing the story against Jan. Jan himself has denied these allegations and asserted that the story was fabricated to tarnish his reputation. Soch Fact Check could not independently verify Jan’s academic record at the PMA. However, the claim appears suspicious as it coincided with the time of his arrest and when he revealed hospital records that were suppressed by government officials. The digitally manipulated video gained significant traction on X amassing over 200k views. It was shared here ( archive ) and here ( archive ). The Suno News segment, which features a clip from the altered video, was shared here , here , and here on Facebook. On Instagram, the news segment clip was shared here , here , here , and here . Conclusion : A video claiming to show senior journalist Matiullah Jan’s expulsion from the PMA is digitally manipulated. The original footage is from the drama serial ‘Ehd-e-Wafa,’ with Jan’s face superimposed on to an actor’s. Similar claims about the journalist apparently made in a segment aired by Suno News also included fake images of Jan in a uniform from the same altered video. – Background image in cover photo: Reuters To appeal against our fact-check, please send an email to appeals@sochfactcheck.com"