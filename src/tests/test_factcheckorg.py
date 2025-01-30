import os
import sys
testdir = os.path.dirname(__file__)
srcdir = '..'
sys.path.insert(0, os.path.abspath(os.path.join(testdir, srcdir)))
import yaml
from scrapy.http import HtmlResponse, Request
from keepup_scrappers.spiders.factcheckorg_spider import FactcheckorgSpider

class TestfactcheckorgSpider:

    def setup_method(self):
        
        # sitekey and name intialization
        self.site_key = 'factcheckorg'
        self.spider_name = 'factcheckorg_spider'
        
        # initialization of spider
        self.spider = FactcheckorgSpider()
        # loading config file
        config_path = os.path.join(os.path.dirname(__file__), '..', 'keepup_scrappers', 'config', 'config.yaml')
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)

        # load site config
        self.site_config = self.config['sites']['factcheckorg']
        self.spider.selectors = self.site_config['selectors']

    def test_spider_initialization(self):
        assert self.spider.site_key == self.site_key
        assert self.spider.name == self.spider_name
        assert self.spider.page_counter == 1
        assert self.spider.custom_settings['IMAGES_STORE'] == f'data/{self.site_key}/images/'

    def test_parse_method(self):
        
        with open(r'tests\test_data\factcheckorg\listing_sample.html', 'r', encoding='utf-8') as f:
            html_content = f.read()    

        mock_response = HtmlResponse(
            url = self.spider.start_urls[0],
            body = html_content,
            encoding='utf-8',
        )

        results = list(self.spider.parse(mock_response))
   
        assert len(results) == 11  # 12 items + one next page request
        
        item = results[0].meta['item']
        assert item['title'] == 'Trump Order Didn’t Reverse All of Biden’s Measures to Lower Drug Costs'
        assert item['publication_date'] == 'January 28, 2025'
        assert item['detail_url'] == 'https://www.factcheck.org/2025/01/trump-order-didnt-reverse-all-of-bidens-measures-to-lower-drug-costs/'
        assert item['image_urls'][0] == 'https://cdn.factcheck.org/UploadedFiles/Biden-IRA-720-x-307-200x200.png'
         
        
   
    def test_parse_details_method(self):

        with open(r'tests\test_data\factcheckorg\detail_sample.html', 'r', encoding='utf-8') as f:
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
        assert item['author'] == 'Alan Jaffe'
        assert item['content'] == "President Donald Trump rescinded an executive order issued by former President Joe Biden aimed at finding new models for lowering drug costs. Trump’s action didn’t affect the caps on seniors’ drug costs or Medicare price negotiations that Biden signed into law. But social media posts have wrongly claimed otherwise. , in August 2022 then-President Joe Biden signed the sweeping into law, which included several measures aimed at reducing prescription drug costs for Medicare beneficiaries. The law required the federal government to negotiate the price of some Medicare drugs, capped monthly insulin copays at $35, capped seniors’ out-of-pocket costs at $2,000 a year for Medicare’s prescription drugs and made vaccines free. To further curb medical costs, in October 2022 Biden executive order 14087, “Lowering Prescription Drug Costs for Americans,” which directed the secretary of Health and Human Services to “consider whether to select for testing by the [Center for Medicare and Medicaid Innovation] new health care payment and delivery models that would lower drug costs and promote access to innovative drug therapies for beneficiaries enrolled in the Medicare and Medicaid programs.” On his first day in office, President Donald Trump, in an supported by his predecessor, Biden’s executive order. Trump’s revocation of Biden’s 2022 order ends the testing of three new models to lower drug costs. But it doesn’t reverse the Inflation Reduction Act provisions, contrary to some social media posts. Experts also told us there isn’t much of a direct impact from Trump’s action, since the new models hadn’t been implemented yet. But social media posts have exaggerated the impact. wrongly claimed Trump “just reversed all the cost caps Biden negotiated for anyone on Medicare or Medicaid, over 120 MILLION Americans.” claimed, “Trump has rolled back a Biden order that mandated negotiations to the lower cost of drugs for people using Medicare and Medicaid,” wrongly linking Trump’s action to price negotiations under the Inflation Reduction Act. “Medicare had just announced 15 more drugs whose prices they were going to bring down in negotiations with Big Pharma,” the post said. Rescinding Biden’s order has not “reversed all the cost caps Biden negotiated” through the IRA. In fact, Trump’s action “is unlikely to change anything directly,” a professor of health policy at Vanderbilt University Medical Center, told us. Biden’s executive order in 2022 included several ways to possibly lower prescription drug costs beyond what was included in the Inflation Reduction Act, explained deputy director of the Program on Medicare Policy at KFF, a nonpartisan healthy policy research organization. “There were three ideas that were floated in that executive order,” Cubanski told us in a phone interview. One idea was to create a list, referred to as the “$2 drug model,” which would give beneficiaries access to a set of low-cost generic drugs for common conditions at a flat copay of $2 available through Medicare Part B plans. “The idea was basically to encourage more utilization of these lower-cost medications,” Cubanski said. A second model was “designed to facilitate greater access through Medicaid programs to expensive cell and gene therapies” through multistate purchasing agreements, Cubanski said. “They are right now really difficult to purchase on an individual need because of the expense of these medications.” The third model was called the “accelerating clinical evidence model. It was engineered I think to encourage pharmaceutical companies who had had their drugs approved by the FDA … to move more quickly through the confirmatory clinical trials that are needed in order to get full approval from the FDA,” Cubanski explained. The accelerated approvals would make some drugs available to patients faster and at a lower price. “The bottom line is that none of these models were actually in the implementation stage. They were in development,” she said. “So they weren’t off and running.” On the one hand, Cubanski said, “you can look at Trump’s action to rescind Biden’s executive order as not really being all that meaningful, because they’re not pulling back on much that actively happened to lower drug costs under these three models. Savings haven’t yet materialized for people on Medicare or for states or for others who may have been able to benefit from these models.” But, Cubanski added, “if President Trump is abandoning these efforts, I think that signals that he’s walking away from these specific efforts to reduce prescription drug prices.” The president’s action, however, is “not so broad as to cancel out other provisions in the Inflation Reduction Act that are part of laws and have already been implemented,” Cubanski said. Dusetzina, the Vanderbilt health policy professor, said Trump’s revocation of Biden’s order may indicate Trump’s interest in “more efforts to roll back these policies in the future. But the changes to date aren’t likely to directly impact patients.” Congress.gov. Deputy director, Program on Medicare Policy, KFF. Phone interview with FactCheck.org. 27 Jan 2025. . Professor of health policy, Vanderbilt University Medical Center. Email to FactCheck.org. 27 Jan 2025. Joseph R. Biden Jr. Executive Order 14087. Federal Register. 14 Oct 2022. Lovelace, Berkeley Jr. NBC News. 21 Jan 2025. Robertson, Lori. FactCheck.org. Updated 18 Aug 2022. White House. Executive Order. 20 Jan 2025."