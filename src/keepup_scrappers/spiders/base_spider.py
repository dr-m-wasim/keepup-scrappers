import scrapy
import yaml
import os

class BaseSpider(scrapy.Spider):
    custom_settings = {}

    def __init__(self, site_key=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if not site_key:
            raise ValueError("You must provide a site_key to load configurations.")

        # Load the YAML configuration
        config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.yaml')
        
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)

        self.site_config = self.config['sites'][site_key]
        self.start_urls = self.site_config['start_urls']
        self.selectors = self.site_config['selectors']
        self.delay = self.site_config.get('delay', 2)  # 2 by default

        # Optionally set Scrapy's custom settings dynamically
        self.custom_settings.update({
            'DOWNLOAD_DELAY': self.delay
        })
       

    def parse(self, response):
        """
        Placeholder parse method. Child classes should override this.
        """
        raise NotImplementedError("Child spiders must implement the parse method.")