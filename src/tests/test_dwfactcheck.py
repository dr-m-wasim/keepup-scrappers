import os
import sys
testdir = os.path.dirname(__file__)
srcdir = '..'
sys.path.insert(0, os.path.abspath(os.path.join(testdir, srcdir)))
import yaml
from scrapy.http import HtmlResponse, Request
from keepup_scrappers.spiders.dwfactcheck_spider import DWfactcheckSpider

class TestbrecorderSpider:

    def setup_method(self):
        
        # sitekey and name intialization
        self.site_key = 'dwfactcheck'
        self.spider_name = 'dwfactcheck_spider'
        
        # initialization of spider
        self.spider = DWfactcheckSpider()
        # loading config file
        config_path = os.path.join(os.path.dirname(__file__), '..', 'keepup_scrappers', 'config', 'config.yaml')
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)

        # load site config
        self.site_config = self.config['sites']['dwfactcheck']
        self.spider.selectors = self.site_config['selectors']

    def test_spider_initialization(self):
        assert self.spider.site_key == self.site_key
        assert self.spider.name == self.spider_name
        #assert self.spider.page_counter == 1
        assert self.spider.custom_settings['IMAGES_STORE'] == f'data/{self.site_key}/images/'

    def test_parse_method(self):
        
        with open(r'tests\test_data\dwfactcheck\listing_sample.html', 'r', encoding='utf-8') as f:
            html_content = f.read()    

        mock_response = HtmlResponse(
            url = self.spider.start_urls[0],
            body = html_content,
            encoding='utf-8',
        )

        results = list(self.spider.parse(mock_response))
   
        assert len(results) == 51  # 12 items + one next page request
        
        item = results[0].meta['item']
        assert item['title'] == "Fact check: Deportation misinformation in Germany"
        
        #assert item['detail_url'] == 'https://www.dw.com/en/fact-check-can-trump-technically-take-back-panama-canal/a-71364492'
        assert item['image_urls'][0] == 'https://static.dw.com/image/70095464_800.jpg'
        #assert item['image_urls'][0] == 'https://www.dw.com/en/fact-check/t-56584214/page-1' #confusing why in place of image url used page url??
        assert item['exerpt'] == "Donald Trump has promised to \"take back\" the \"foolish gift\" that was the Panama Canal. DW explains where he's wrong."
        assert item['category'] == 'Politics'
        assert item['publication_date'] == '01/22/2025'
   
    def test_parse_details_method(self):

        with open(r'tests\test_data\dwfactcheck\detail_sample.html', 'r', encoding='utf-8') as f:
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
        
        assert item['author'] == 'Anwar Ashraf'
        assert item['label'] == 'False'
        assert item['content'] == "is back in the , and he started his term with the announcing a series of sweeping that he says are going to take to \"make America great again.\" He reiterated his interest in \"taking back\" the Panama Canal in Central America. The waterway connects the Atlantic and the Pacific oceans and is one of the most important shipping routes for global trade. The United States oversaw the canal's construction in the early 20th century and controlled it until the end of 1999. In his speech at the Capitol, Trump said: \"We have been treated very badly by this foolish gift that should have never been made, and Panama's promise to us has been broken. The purpose of our deal and the spirit of our treaty has been totally violated.\" False. The transfer of power over the Panama Canal from the United States to was not seen as \"a gift,\" as Trump claimed, but the result of lengthy negotiations. The United States transferred control under the terms of what is known as the Torrijos-Carter treaties — named for General Omar Torrijos, then the commander of Panama's National Guard, and . The two agreements were signed by both countries on September 7, 1977. The mentions that the US control over the canal would end on December 31, 1999 (Article 2, paragraph 2). The other treaty, known as the , states in Article 5 that \"after the termination of the Panama Canal Treaty, only the Republic of Panama shall operate the Canal and maintain military forces, defense sites and military installations within its national territory.\" Trump's claim that the \"purpose of our deal\" was violated is also incorrect. According to Article 4 of the Panama Canal Treaty, both governments committed to ensuring the canal's protection and defense during the transfer of power. The Neutrality Treaty guaranteed the permanent neutrality of the Panama Canal, which would remain accessible to all nations in both times of peace and war. Carla Martinez Machain, a political science professor at the University at Buffalo, confirmed to DW that this neutrality remains intact: \"Any ship from any country wishing to transit the canal has the right to do so after paying a fee.\" Furthermore, Panama agreed that the United States would retain the right to defend the canal if it were ever threatened by a foreign aggressor. \"Neither one (none) of those terms has been violated. So, I am not sure why Mr. Trump thinks the agreement has been violated,\" said Martinez Machain. To view this video please enable JavaScript, and consider upgrading to a web browser that Trump said, \"China is operating the Panama Canal. And we didn't give it to China. We gave it to Panama.\" False Donald Trump often claimed that operates This is false. As previously mentioned, Panama has owned and administered the canal since December 31, 1999, when the United States handed over control. The Panama Canal Authority, a federal government agency, operates and manages the waterway. \"The accusations that China is running the canal are unfounded,\" Ricaurte Vasquez Moralez, the head of the Panama Canal Authority, recently told the . Panama's President Jose Raul Mulino has also the presence of Chinese forces. \"There are no Chinese soldiers in the canal, for the love of God,\" he said in December 2024. China has also categorically denied claims that it controls the canal. Chinese Foreign Ministry spokesperson Mao Ning said in a in December that the country has \"always supported the people of Panama in their just cause for sovereignty over the canal.\" While there are no indications of China controlling the canal, the country is in construction projects. Experts have raised concerns about two ports in the Panama Canal that have long been operated by a subsidiary of Hong Kong-based . China is the second-largest customer of the Panama Canal after the US. But the company manages ports rather than owning them, said Martínez Machain, the University of Buffalo professor. \"They're not making the decisions on who gets to go through the canal or not, they're not making the decisions on who gets charged, what to go through the canal? They don't own the canal. They don't own the ports.\" Trump said in his inaugural speech, \"The United States ... lost 38,000 lives in the building of the Panama Canal.\" False France began construction of the Panama Canal before the US took over in the early 20th century. The of the Panama Canal Authority estimates that 25,000 people died during its construction. However, \"according to hospital records, 5,609 lives were lost from disease and accidents during the American construction era.\" The US Centers for Disease Control and Prevention (CDC) has noted that most deaths were due to diseases. \"During the effort to build the canal in the 1880s, more than 22,000 workers from France died, many from malaria and yellow fever, before the etiologies of these tropical diseases were understood,\" the CDC states on its . According to the CDC, more than 55,000 people were employed during the US construction period. Matthew Parker, author of \"Hell's Gorge: The Battle to Build the Panama Canal,\" recently told the that nearly all those who died during the US construction period were from Barbados. \"And only about 300 were Americans,\" he said."