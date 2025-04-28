import scrapy
from keepup_scrappers.spiders.base_spider import BaseSpider
from keepup_scrappers.items import AryNewsItem
from scrapy.selector import Selector
import re
import json

class AryNewsSpider(BaseSpider):
    
    name = 'arynews_spider'
    site_key = 'arynews'
    page_counter = 1
    custom_settings = {
            "IMAGES_STORE": f'data/{site_key}/images/',
            "FEEDS": {
                f"data/{site_key}/data.json": {
                    "format": "json",
                    "encoding": "utf8",
                    "indent": 4,
                }
            },
            "DOWNLOAD_DELAY": 3,
            'ROBOTSTXT_OBEY': False,
        }
    
    def __init__(self, *args, **kwargs):
        # Pass site_key to the base class
        kwargs['site_key'] = self.site_key
        super().__init__(*args, **kwargs)

    def get_payload_headers(self, page_no):
        
        payload = {
            "action": "td_ajax_block",
            "td_atts": '{"modules_on_row":"50%","modules_gap":"10","modules_category":"above","show_excerpt":"eyJwb3J0cmFpdCI6Im5vbmUiLCJhbGwiOiJub25lIn0=","show_btn":"none","ajax_pagination":"load_more","hide_audio":"yes","limit":"9","image_width":"eyJwaG9uZSI6IjEwMCIsImFsbCI6IjQwIn0=","image_floated":"eyJwaG9uZSI6Im5vX2Zsb2F0IiwiYWxsIjoiZmxvYXRfbGVmdCJ9","meta_padding":"eyJhbGwiOiIwIDAgMCAzMHB4IiwibGFuZHNjYXBlIjoiMCAwIDAgMjVweCIsInBvcnRyYWl0IjoiMCAwIDAgMjBweCIsInBob25lIjoiMjVweCAwIDAgMCJ9","image_radius":"10","image_height":"eyJwaG9uZSI6IjExMCIsImFsbCI6IjUwIn0=","meta_info_horiz":"","modules_category_margin":"eyJhbGwiOiIwIiwicG9ydHJhaXQiOiIwIn0=","show_cat":"none","show_author":"none","show_com":"none","show_review":"none","show_date":"none","art_title":"eyJhbGwiOiIxMHB4IDAiLCJwb3J0cmFpdCI6IjZweCAwIiwibGFuZHNjYXBlIjoiOHB4IDAifQ==","f_title_font_family":"downtown-sans-serif-font_global","f_title_font_size":"eyJhbGwiOiIyMiIsImxhbmRzY2FwZSI6IjI4IiwicG9ydHJhaXQiOiIyNCIsInBob25lIjoiMzIifQ==","f_title_font_line_height":"1.2","f_title_font_weight":"900","f_title_font_transform":"undefined","title_txt":"#000000","title_txt_hover":"#444444","modules_category_padding":"eyJhbGwiOiIwIiwicG9ydHJhaXQiOiIwIn0=","f_cat_font_family":"downtown-sans-serif-font_global","f_cat_font_size":"eyJhbGwiOiIxNSIsImxhbmRzY2FwZSI6IjE0IiwicG9ydHJhaXQiOiIxMyJ9","f_cat_font_line_height":"1.2","f_cat_font_weight":"700","f_cat_font_transform":"","cat_bg":"rgba(255,255,255,0)","cat_bg_hover":"rgba(255,255,255,0)","cat_txt":"#edb500","author_txt":"undefined","author_txt_hover":"undefined","art_excerpt":"eyJwb3J0cmFpdCI6IjZweCAwIDAgMCIsImFsbCI6IjAifQ==","f_ex_font_family":"downtown-sans-serif-font_global","f_ex_font_size":"eyJhbGwiOiIxNSIsImxhbmRzY2FwZSI6IjE0IiwicG9ydHJhaXQiOiIxMyJ9","f_ex_font_line_height":"1.4","f_ex_font_weight":"500","ex_txt":"#666666","meta_info_align":"center","all_modules_space":"eyJhbGwiOiIyMCIsInBvcnRyYWl0IjoiMTAiLCJsYW5kc2NhcGUiOiIxNSIsInBob25lIjoiMzAifQ==","tdc_css":"eyJhbGwiOnsibWFyZ2luLWJvdHRvbSI6IjAiLCJkaXNwbGF5IjoiIn0sImxhbmRzY2FwZSI6eyJkaXNwbGF5IjoiIn0sImxhbmRzY2FwZV9tYXhfd2lkdGgiOjExNDAsImxhbmRzY2FwZV9taW5fd2lkdGgiOjEwMTksInBvcnRyYWl0Ijp7ImRpc3BsYXkiOiIifSwicG9ydHJhaXRfbWF4X3dpZHRoIjoxMDE4LCJwb3J0cmFpdF9taW5fd2lkdGgiOjc2OCwicGhvbmUiOnsiZGlzcGxheSI6IiJ9LCJwaG9uZV9tYXhfd2lkdGgiOjc2N30=","pag_h_bg":"#b20000","pag_a_bg":"var(--downtown-menu-bg)","modules_cat_border":"0","modules_category_radius":"50","f_cat_font_style":"undefined","f_cat_font_spacing":"undefined","cat_txt_hover":"#000000","f_title_font_style":"undefined","f_title_font_spacing":"undefined","f_meta_font_family":"downtown-sans-serif-font_global","f_meta_font_size":"eyJhbGwiOiIxMyIsInBvcnRyYWl0IjoiMTIifQ==","f_meta_font_line_height":"1","f_meta_font_style":"undefined","f_meta_font_weight":"500","f_meta_font_transform":"capitalize","f_meta_font_spacing":"undefined","date_txt":"#666666","f_ex_font_style":"undefined","f_ex_font_transform":"undefined","f_ex_font_spacing":"undefined","excl_txt":"Locked","excl_margin":"-4px 5px 0 0","excl_padd":"eyJhbGwiOiI1cHggOHB4IiwibGFuZHNjYXBlIjoiNHB4IDZweCIsInBvcnRyYWl0IjoiM3B4IDVweCIsInBob25lIjoiNHB4IDZweCJ9","excl_color_h":"#ffffff","excl_bg":"var(--downtown-menu-bg-light)","excl_bg_h":"var(--downtown-menu-bg-light)","f_excl_font_family":"downtown-sans-serif-font_global","f_excl_font_size":"eyJhbGwiOiIxMSIsImxhbmRzY2FwZSI6IjEwIiwicG9ydHJhaXQiOiIxMCIsInBob25lIjoiMTAifQ==","f_excl_font_line_height":"1.1","f_excl_font_transform":"uppercase","pag_border_width":"0","pag_space":"eyJhbGwiOiIyNSIsInBvcnRyYWl0IjoiMjAifQ==","f_pag_font_family":"downtown-sans-serif-font_global","f_pag_font_weight":"500","f_btn_font_family":"downtown-sans-serif-font_global","all_excl_border_style":"","h_effect":"shadow","modules_border_size":"1px 1px 1px 1px","modules_border_style":"dashed","modules_border_color":"#d1d1d1","m_radius":"10px","m_padding":"&#x60;","ad_loop_repeat":"6","video_popup":"","modules_divider":"","image_size":"td_1920x0","image_alignment":"71","ad_loop_full":"","category_id":51,"block_type":"tdb_loop","separator":"","custom_title":"","custom_url":"","block_template_id":"","title_tag":"","mc1_tl":"","mc1_title_tag":"","mc1_el":"","offset":"","open_in_new_window":"","post_ids":"-585371","include_cf_posts":"","exclude_cf_posts":"","sort":"","installed_post_types":"","ajax_pagination_next_prev_swipe":"","ajax_pagination_infinite_stop":"","review_source":"","container_width":"","modules_divider_color":"#eaeaea","hide_image":"","show_favourites":"","fav_size":"2","fav_space":"","fav_ico_color":"","fav_ico_color_h":"","fav_bg":"","fav_bg_h":"","fav_shadow_shadow_header":"","fav_shadow_shadow_title":"Shadow","fav_shadow_shadow_size":"","fav_shadow_shadow_offset_horizontal":"","fav_shadow_shadow_offset_vertical":"","fav_shadow_shadow_spread":"","fav_shadow_shadow_color":"","video_icon":"","video_rec":"","spot_header":"","video_rec_title":"- Advertisement -","video_rec_color":"","video_rec_disable":"","autoplay_vid":"yes","show_vid_t":"block","vid_t_margin":"","vid_t_padding":"","video_title_color":"","video_title_color_h":"","video_bg":"","video_overlay":"","vid_t_color":"","vid_t_bg_color":"","f_vid_title_font_header":"","f_vid_title_font_title":"Video pop-up article title","f_vid_title_font_settings":"","f_vid_title_font_family":"","f_vid_title_font_size":"","f_vid_title_font_line_height":"","f_vid_title_font_style":"","f_vid_title_font_weight":"","f_vid_title_font_transform":"","f_vid_title_font_spacing":"","f_vid_title_":"","f_vid_time_font_title":"Video duration text","f_vid_time_font_settings":"","f_vid_time_font_family":"","f_vid_time_font_size":"","f_vid_time_font_line_height":"","f_vid_time_font_style":"","f_vid_time_font_weight":"","f_vid_time_font_transform":"","f_vid_time_font_spacing":"","f_vid_time_":"","meta_width":"","meta_margin":"","meta_space":"","meta_info_border_size":"","meta_info_border_style":"","meta_info_border_color":"#eaeaea","meta_info_border_radius":"","art_btn":"","modules_extra_cat":"","author_photo":"","author_photo_size":"","author_photo_space":"","author_photo_radius":"","show_modified_date":"","time_ago":"","time_ago_add_txt":"ago","time_ago_txt_pos":"","review_space":"","review_size":"2.5","review_distance":"","excerpt_col":"1","excerpt_gap":"","excerpt_middle":"","excerpt_inline":"","show_audio":"block","art_audio":"","art_audio_size":"1.5","btn_title":"","btn_margin":"","btn_padding":"","btn_border_width":"","btn_radius":"","pag_padding":"","pag_border_radius":"","prev_tdicon":"","next_tdicon":"","pag_icons_size":"","f_header_font_header":"","f_header_font_title":"Block header","f_header_font_settings":"","f_header_font_family":"","f_header_font_size":"","f_header_font_line_height":"","f_header_font_style":"","f_header_font_weight":"","f_header_font_transform":"","f_header_font_spacing":"","f_header_":"","f_pag_font_title":"Pagination text","f_pag_font_settings":"","f_pag_font_size":"","f_pag_font_line_height":"","f_pag_font_style":"","f_pag_font_transform":"","f_pag_font_spacing":"","f_pag_":"","f_title_font_header":"","f_title_font_title":"Article title","f_title_font_settings":"","f_title_":"","f_cat_font_title":"Article category tag","f_cat_font_settings":"","f_cat_":"","f_meta_font_title":"Article meta info","f_meta_font_settings":"","f_meta_":"","f_ex_font_title":"Article excerpt","f_ex_font_settings":"","f_ex_":"","f_btn_font_title":"Article read more button","f_btn_font_settings":"","f_btn_font_size":"","f_btn_font_line_height":"","f_btn_font_style":"","f_btn_font_weight":"","f_btn_font_transform":"","f_btn_font_spacing":"","f_btn_":"","mix_color":"","mix_type":"","fe_brightness":"1","fe_contrast":"1","fe_saturate":"1","mix_color_h":"","mix_type_h":"","fe_brightness_h":"1","fe_contrast_h":"1","fe_saturate_h":"1","m_bg":"","shadow_shadow_header":"","shadow_shadow_title":"Module Shadow","shadow_shadow_size":"","shadow_shadow_offset_horizontal":"","shadow_shadow_offset_vertical":"","shadow_shadow_spread":"","shadow_shadow_color":"","all_underline_height":"","all_underline_color":"#000","cat_border":"","cat_border_hover":"","meta_bg":"","com_bg":"","com_txt":"","rev_txt":"","shadow_m_shadow_header":"","shadow_m_shadow_title":"Meta info shadow","shadow_m_shadow_size":"","shadow_m_shadow_offset_horizontal":"","shadow_m_shadow_offset_vertical":"","shadow_m_shadow_spread":"","shadow_m_shadow_color":"","audio_btn_color":"","audio_time_color":"","audio_bar_color":"","audio_bar_curr_color":"","btn_bg":"","btn_bg_hover":"","btn_txt":"","btn_txt_hover":"","btn_border":"","btn_border_hover":"","nextprev_border_h":"","pag_text":"","pag_h_text":"","pag_a_text":"","pag_bg":"","pag_border":"","pag_h_border":"","pag_a_border":"","ad_loop":"","ad_loop_title":"- Advertisement -","ad_loop_color":"","f_ad_font_header":"","f_ad_font_title":"Ad title text","f_ad_font_settings":"","f_ad_font_family":"","f_ad_font_size":"","f_ad_font_line_height":"","f_ad_font_style":"","f_ad_font_weight":"","f_ad_font_transform":"","f_ad_font_spacing":"","f_ad_":"","ad_loop_disable":"","el_class":"","td_column_number":1,"header_color":"","td_ajax_preloading":"","td_ajax_filter_type":"","td_filter_default_txt":"","td_ajax_filter_ids":"","color_preset":"","border_top":"","css":"","class":"tdi_66","tdc_css_class":"tdi_66","tdc_css_class_style":"tdi_66_rand_style"}',
            "td_block_id": "tdi_66",
            "td_column_number": "1",
            "td_current_page": str(page_no),
            "block_type": "tdb_loop",
            "td_filter_value": "", 
            "td_user_action": "",
            "td_magic_token": "269894e1ea"
        }

        return payload
    
    def start_requests(self):     
        payload = self.get_payload_headers(self.page_counter)

        yield scrapy.FormRequest(url = self.start_urls[0], 
                                 formdata = payload,
                                 method='POST', 
                                 callback = self.parse)


    def parse(self, response):

        data = json.loads(response.text)
        html_content = data.get('td_data', '')
        html_selector = Selector(text=html_content)

        for index, post in enumerate(html_selector.css(self.selectors['single_post'])):

            if not post:  
                self.logger.info("No more posts. Stopping scraper.")
                return
            item = AryNewsItem()
            
            item['title'] = post.css(self.selectors['post_title']).get(default='').strip()
            item['detail_url'] = post.css(self.selectors['post_link']).get(default='').strip()
            # image_url = post.css(self.selectors['post_image']).get(default='')
            # image_url = re.search(r'url\((.*?)\)', image_url).group(1)
            # #item['image_urls'] = [response.urljoin(image_url)] if image_url else []
            
            yield scrapy.Request(
                url = item['detail_url'],
                callback = self.parse_details,
                meta = {'item': item},
                errback = self.handle_error,
            )

        self.logger.info(f"Page {self.page_counter} completed")
        self.page_counter += 1
        payload = self.get_payload_headers(self.page_counter)

        yield scrapy.FormRequest(
            url=self.start_urls[0],
            formdata=payload,
            callback=self.parse,
            errback=self.handle_error,
        )

    def parse_details(self, response):
        item = response.meta['item']
        item['publication_date'] = response.css(self.selectors['post_date']).get(default='')
        item['author'] = response.css(self.selectors['author']).get(default='').strip()
        item['exerpt']  = response.css(self.selectors['exerpt']).get(default='').strip()
        content_paragraphs = response.css(self.selectors['content']).getall()
        item['content'] = ' '.join([p.strip() for p in content_paragraphs if p.strip()])

        yield item

    def handle_error(self, failure):
        self.logger.error(f"Request Failed: {failure.request.url}")