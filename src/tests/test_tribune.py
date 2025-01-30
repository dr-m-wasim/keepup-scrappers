import os
import sys
testdir = os.path.dirname(__file__)
srcdir = '..'
sys.path.insert(0, os.path.abspath(os.path.join(testdir, srcdir)))
import yaml
from scrapy.http import HtmlResponse, Request
from keepup_scrappers.spiders.tribune_spider import tribuneSpider

class TestTribuneSpider:

    def setup_method(self):
        
        # sitekey and name intialization
        self.site_key = 'tribune'
        self.spider_name = 'tribune_spider'
        
        # initialization of spider
        self.spider = tribuneSpider()
        
        # loading config file
        config_path = os.path.join(os.path.dirname(__file__), '..', 'keepup_scrappers', 'config', 'config.yaml')
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)

        # load site config
        self.site_config = self.config['sites']['tribune']
        self.spider.selectors = self.site_config['selectors']

    def test_spider_initialization(self):
        assert self.spider.site_key == self.site_key
        assert self.spider.name == self.spider_name
        assert self.spider.page_counter == 1
        assert self.spider.custom_settings['IMAGES_STORE'] == f'data/{self.site_key}/images/'

    def test_parse_method(self):
        
        with open(r'tests\test_data\tribune\listing_sample.html', 'r', encoding='utf-8') as f:
            html_content = f.read()    

        mock_response = HtmlResponse(
            url = self.spider.start_urls[0],
            body = html_content,
            encoding='utf-8',
        )

        results = list(self.spider.parse(mock_response))
   
        assert len(results) == 51  # 12 items + one next page request
        
        item = results[0].meta['item']
        assert item['title'] == 'SZA shares emotional journey in India, praises Isha Foundation and Indian kids'
        
        assert item['detail_url'] == 'https://tribune.com.pk/story/2525005/sza-shares-emotional-journey-in-india-praises-isha-foundation-and-indian-kids'
        
        
        #assert item['author'] == 'CEJ'
   
    def test_parse_details_method(self):

        with open(r'tests\test_data\tribune\detail_sample.html', 'r', encoding='utf-8') as f:
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
        assert item['content'] == 'Grammy-winning artist SZA recently visited India to participate in a spiritual program at the Isha Foundation, led by Sadhguru. Known for her hit songs ‘Kill Bill’ and ‘All the Stars,’ the singer spent weeks at the foundation, engaging in the Samyama program, which she later described as a deeply transformative experience. In her Instagram posts, SZA shared that the program required complete disconnection—no phone, mirrors, or even eye contact—for over eight days. “Life is so profound and chaotic and beautiful. I have no words for my Samyama experience,” she wrote. Upon returning to her daily life, SZA expressed gratitude for the clarity and peace she gained, despite feeling initially overwhelmed. She thanked Sadhguru, the Isha volunteers, and the staff for their care, concluding her post with “Namaskaram.” Among the most emotional moments of her visit was a performance by children from Sadhguru Gurukulam Samskriti, a residential school emphasizing yoga, martial arts, music, dance, and academics. SZA shared a video of the children’s performance, describing it as “insane” and admitting it brought her to tears. “I’ve never seen such vibrant discipline,” she wrote, expressing her admiration for their talent and dedication. The performance left such an impact on SZA that she plans to incorporate the children’s audio into her music. “I’ve already sent it to my production team,” she revealed, showcasing how the experience has inspired her creatively. SZA concluded by thanking Radhe Jaggi, Sadhguru’s daughter, and the foundation’s team for an unforgettable experience. Her posts highlight the profound effect her time in India had on both her personal outlook and artistic vision, underscoring the transformative power of spiritual connection.   COMMENTS  Comments are moderated and generally will be posted if they are on-topic and not abusive.  For more information, please see our'

        assert item['publication_date'] == 'January 28, 2025'
        assert item['catagory'] == 'Pop Culture & Art'
        assert item['image_urls'][0] == 'https://i.tribune.com.pk/media/images/sza1717126588-0/sza1717126588-0.jpg'
