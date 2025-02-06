import os
import sys
testdir = os.path.dirname(__file__)
srcdir = '..'
sys.path.insert(0, os.path.abspath(os.path.join(testdir, srcdir)))
import yaml
from scrapy.http import HtmlResponse, Request
from keepup_scrappers.spiders.humenglish_spider import HumEnglishSpider

class TesthumenglishSpider:

    def setup_method(self):
        
        # sitekey and name intialization
        self.site_key = 'humenglish'
        self.spider_name = 'humenglish_spider'
        
        # initialization of spider
        self.spider = HumEnglishSpider()
        # loading config file
        config_path = os.path.join(os.path.dirname(__file__), '..', 'keepup_scrappers', 'config', 'config.yaml')
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)

        # load site config
        self.site_config = self.config['sites']['humenglish']
        self.spider.selectors = self.site_config['selectors']

    def test_spider_initialization(self):
        assert self.spider.site_key == self.site_key
        assert self.spider.name == self.spider_name
        assert self.spider.page_counter == 1
        assert self.spider.custom_settings['IMAGES_STORE'] == f'data/{self.site_key}/images/'

    def test_parse_method(self):
        
        with open(r'tests\test_data\humenglish\listing_sample (2).html', 'r', encoding='utf-8') as f:
            html_content = f.read()    

        mock_response = HtmlResponse(
            url = self.spider.start_urls[0],
            body = html_content,
            encoding='utf-8',
        )

        results = list(self.spider.parse(mock_response))
   
        assert len(results) == 11 # 12 items + one next page request
        
        item = results[0].meta['item']
        assert item['title'] == "G-B declares three-day mourning, public holiday over demise of Aga Khan IV"
        assert item['image_urls'][0] == 'https://humenglish.com/wp-content/uploads/2025/02/Aga-Khan-IV.jpg'
        assert item['detail_url'] == 'https://humenglish.com/latest/g-b-declares-three-day-mourning-public-holiday-over-demise-of-aga-khan-iv/'
        assert item['exerpt'] == 'The Government of Gilgit-Baltistan decides to observe a three-day mourning from February 5 to 7, 2025, over the passing of His Highness Aga Khan IV.'
        
        #assert item['author'] == 'CEJ'
   
    def test_parse_details_method(self):

        with open(r'tests\test_data\humenglish\detail_sample (2).html', 'r', encoding='utf-8') as f:
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
        assert item['content'] == 'GILGIT: The Gilgit-Baltistan government on Wednesday declared a three-day mourning period across the region and a holiday on Thursday over the demise of the spiritual leader of the Shia Imami Ismaili Muslims Prince Shah Karim Al-Husseini, Aga Khan IV. The 49th hereditary imam or spiritual leader of the world’s 15 million Ismailis passed away in Lisbon on Tuesday aged 88, leaving his followers in mourning across the world. A large number of Ismailis live in Gilgit-Baltistan with a majority of Hunza and Ghizer belonging to the community. “The Government of Gilgit-Baltistan has decided to observe a three-day mourning from February 5 to 7, 2025, over the passing of His Highness Aga Khan IV, spiritual leader of the Ismaili community. During this period, the national flag will remain at half-mast across Gilgit-Baltistan,” reads a statement issued by information department G-B. In a separate notification, the General Administration Department declared a public holiday on February 6. All government offices will remain closed on Thursday in this regard. As the news of his demise spread early Wednesday in the region, the Ismaili community and many others were left in deep sorrow and disbelief. People gathered in large numbers in the community centers, known as jamat khana, to offer prayers and pay their respects to the late Aga Khan IV. The overall mood of the region was somber and markets were deserted. Condolences poured in soon after news of Aga Khan’s death spread. G-B Chief Minister Gulbar Khan, Governor Mehdi Shah, former CMs Khalid Khursheed, Hafiz Hafeezur Rehman, Imamia Masjid Gilgit Khateeb Agha Rahat Hussain Alhussaini, and many other political, social and religious leaders expressed grief over death on Aga Khan IV. According to the Ismaili community’s website, his successor as the 50th Shia Imami Ismaili Imam has been “designated in conformity with the historical Shia Imami Ismaili tradition and practice of nass”. Instructions for the followers published on the website said the designation made by Shah Karim is recorded in his will, which is to be read in Lisbon in the presence of his family and senior international Ismaili leaders. A date has not been announced. “In the Ismaili tradition, the word refers to the transfer of the Imamat from one Imam to the next by explicit designation. It is believed that just as the Prophet Muhammad (SAW) was divinely designated by Allah, the Prophet, through divine support or inspiration, designated Imam Ali as his legatee (wasi) and successor at Ghadir Khumm,” reads the instructions. Thus, according to Ismaili tradition, Imamat is seen as a prerogative bestowed by Allah upon a chosen person from the progeny of the Prophet. Before his death, and through divine support or inspiration, the Imam designates his successor from among his male progeny or a more distant descendant. For the Shia Ismailis, is the formal act of an Imam designating his successor, continuing the Imamat in the line of Imams directly descended from Prophet Muhammad through Hazrat Ali and Hazrat Fatima, and through the lineage of Imam Husayn and his progeny in perpetuity.'

        assert item['publication_date'] == '6 Minutes ago'
       
        assert item['author'] == 'Tanveer Abbas'
        