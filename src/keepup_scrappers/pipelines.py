from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
from urllib.parse import urlparse
import os

class CustomImagesPipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None, *, item=None):
        # Extract the domain name to create subdirectories
        image_url = request.url
        domain = urlparse(image_url).netloc
        filename = os.path.basename(urlparse(image_url).path)
        return f'{domain}/{filename}'