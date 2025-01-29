import os
import sys
testdir = os.path.dirname(__file__)
srcdir = '..'
sys.path.insert(0, os.path.abspath(os.path.join(testdir, srcdir)))
import yaml
from scrapy.http import HtmlResponse, Request
from keepup_scrappers.spiders.humenglish_spider import HumEnglishSpider

class TestIverifySpider:

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
        
        with open(r'D:\myenv\keepup-scrappers\src\tests\test_data\humenglish\listing_sample.html', 'r', encoding='utf-8') as f:
            html_content = f.read()    

        mock_response = HtmlResponse(
            url = self.spider.start_urls[0],
            body = html_content,
            encoding='utf-8',
        )

        results = list(self.spider.parse(mock_response))
   
        assert len(results) == 11  # 12 items + one next page request
        
        item = results[0].meta['item']
        assert item['title'] == 'Any truth behind the viral Kamala Harris disinformation claims?'
       
        assert item['detail_url'] == 'https://humenglish.com/world/fact-check-any-truth-behind-the-viral-kamala-harris-claims/'
        assert item['exerpt'] == 'Unfortunately, Harris is not alone in this — women in the public eye are more likely to be discredited by fake news and disinformation than men. This is known as “gendered disinformation.” '
        assert item['publication_date'] == 'Jul 26, 2024'
        assert item['image_urls'][0] == 'https://humenglish.com/wp-content/uploads/2024/07/69749756_403.jpg'

        
        
   
    def test_parse_details_method(self):

        with open(r'D:\myenv\keepup-scrappers\src\tests\test_data\humenglish\detail_sample.html', 'r', encoding='utf-8') as f:
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
        
        assert item['label'] == 'False'
        assert item['content'] == "WASHINGTON: United States (US) Vice President Kamala Harris is at the center of attention — and disinformation — now that Joe Biden has withdrawn from the presidential race. We looked into a few claims that have been making the rounds online. It will be a first in more ways than one if Kamala Harris becomes the next president of the United States: It would mark the first time a woman holds the post, and also the first time for a person of Jamaican and Indian heritage. The current vice president is not yet the official candidate of the Democratic Party, but since President Joe Biden withdrew from the presidential race on Sunday, she has been the favourite. Harris has become the target of a flurry of false allegations and disinformation, many of them old, many of them racist and many sexist. Unfortunately, Harris is not alone in this — women in the public eye are more likely to be discredited by fake news and disinformation than men. This is known as “gendered disinformation.” According to a 2016 study conducted by the Inter-Parliamentary Union, almost 42 per cent of women parliamentarians surveyed in some 40 countries reported having seen”extremely humiliating or sexually charged images” of themselves spread through social media. DW took a closer look at three key claims about Harris. According to some, the 59-year-old cannot become president of the US because of her origins. An X post that has garnered over 1 million views reads: “Reminder that Kamala Harris is not constitutionally eligible to be either President or Vice President and is currently illegally serving as VP.” False Harris’ US citizenship and eligibility were first called into question when she campaigned as Biden’s running mate four years ago. Now the false allegations are popping up once again. In principle, anyone born in the United States receives US citizenship. This is granted by section one of the fourteenth amendment to the US constitution: “All persons born or naturalised in the United States, and subject to the jurisdiction thereof, are citizens of the United States and of the State wherein they reside.” According to official information, Harris’ mother, Shyamala Gopalan, moved to the US from India at the age of 19 to enroll in a graduate program at the University of Berkeley in California, where she earned her PhD Harris’ Jamaican father, Donald J Harris, also earned his doctorate from Berkeley. Kamala Harris was born on October 20, 1964, in California, US. Harris’ birth certificatecan be found online. It was also included in an online article by the Californian daily newspaper in 2020, when the debate about Harris’ origins kicked off in earnest. The author of the article responded to a DW inquiry and said anybody in California could obtain copies of birth certificates for purposes of information, which is what he had done. Harris is thus a US citizen by birth and she fullfils the requirements needed to be elected (vice) president. “No Person except a natural born Citizen, or a Citizen of the United States, at the time of the Adoption of this Constitution, shall be eligible to the Office of President; neither shall any person be eligible to that Office who shall not have attained to the Age of thirty five Years, and been fourteen Years a Resident within the United States,” states Article II, Section 1 of the US Constitution. : “Today is today. And yesterday was today yesterday. Tomorrow will be today tomorrow. So live today, so the future today will be as the past today as it is tomorrow”: Harris appears to be saying these words in a video circulating on Telegram, X and other social media platforms. : Fake. Several aspects of the widely shared video are perplexing. Harris’ mouth movements and gestures often do not match what she is saying. The US vice president also appears to be slurring her words at times. The quality of the video is poor, which is typical when footage has been manipulated. A reverse image search shows that the video and its audio track have been circulating since May 2023, and also that it has been manipulated, possibly with the help of artificial intelligence. In the original footage, Harris is speaking about reproductive rights at an event at Howard University in 2023. In a video of Harris’ speech that can be found on Facebook, she starts speaking at minute 57. The fake video begins at timecode 01:01:08. The signs that people behind her are holding up read “Reproductive freedom,” as in some fake versions of Harris’ lectern, also providing clues as to the subject of Harris’ speech. A reverse image search with these elements in the image leads to media reports on the event at her former university. Many accounts have recently shared a screenshot together with an audio recording in which Harris describes Russia’s war in Ukraine in a very simple way: “Ukraine is a country in Europe. It’s next to another country called Russia. Russia is a bigger country. Russia is a powerful country. Russia has decided to invade a smaller country called Ukraine. So basically, that is wrong.” Many, including this X account, have made fun of Harris’ apparently limited understanding of Russia’s war in Ukraine on the basis of this simplistic description. Confusing This disinformation about Harris is also not new. A reverse image search brings up posts from 2022, and it is in March of that year, not long after Russia launched its full-scale invasion of Ukraine, that Harris actually said these words on the radio programme “The Morning Hustle.” Listening to the whole interview, it becomes clear why Harris used such simple wording. The presenter asks her specifically to break down the situation “in layman’s terms for people who don’t understand what’s going on.” Thus, in the posts circulating now, Harris’ words have been taken out of context and give the wrong impression, particularly if one considers her more detailed comments afterward."