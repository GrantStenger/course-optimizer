# Import Dependencies
import scrapy
import re

# Define Spider
class CoursesSpider(scrapy.Spider):

    # Constants
    name = 'courses'
    allowed_domains = ['catalogue.usc.edu']
    url = 'http://catalogue.usc.edu/content.php?catoid=8&catoid=8&navoid=2389&' \
          + 'filter%5B27%5D=-1&filter%5B29%5D=&filter%5Bcourse_type%5D=-1&' \
          + 'filter%5Bkeyword%5D=&filter%5B32%5D=1&filter%5Bcpage%5D={}&' \
          + 'filter%5Bitem_type%5D=3&filter%5Bonly_active%5D=1&' \
          + 'filter%5B3%5D=1#acalog_template_course_filter'

    def __init__(self):
        super().__init__()

    def start_requests(self):
        yield scrapy.Request(url=self.url.format(1), dont_filter=True,
            callback=self.parse_first_page)

    def parse_first_page(self, response):
        last_page_number = int(response.css('td.block_content_outer').xpath(
            './table[1]//table[2]//tr[last()]/td/a[last()]/text()').get())

        for i in range(1, last_page_number + 1):
            request = scrapy.Request(url=self.url.format(i), callback=self.parse_page)
            yield request

    def parse_page(self, response):
        all_rows = response.css('td.block_content_outer').xpath('./table[1]//table[2]//tr')
        for row in all_rows:
            if len(row.xpath('.//td')) == 2:
                course_url = row.xpath('.//td[2]/a/@href').get()
                yield response.follow(url=course_url, callback=self.parse_course)

    def parse_course(self, response):
        title = response.css('#course_preview_title::text').get().strip()
        prefix = title.split()[0]
        enroll_in = response.css('#course_preview_title').xpath(
            './following-sibling::text()[contains(., "Enroll in")]')
        if len(enroll_in) == 0:
            units = self.parse_units(response)
            description = self.parse_description(response)
            prerequisities_elems = response.css('td.block_content').xpath(
                './/em[contains(text(),"Prerequisite")]/following-sibling::a')
            prerequisities = []
            for req in prerequisities_elems:
                prerequisities.append(req.xpath('text()').get())
            yield {
                'prefix': prefix,
                'title': title,
                'units': units,
                'description': description,
                'prerequisities': prerequisities
            }
        else:
            path = response.css('#course_preview_title').xpath('./following-sibling::a/@href').get()
            if path:
                request = scrapy.Request(url='http://catalogue.usc.edu/'+path,
                        callback=self.parse_enrolled_in_course)
                request.meta['title'] = title
                request.meta['prefix'] = prefix
                yield request

    def parse_enrolled_in_course(self, response):
        units = self.parse_units(response)
        description = self.parse_description(response)
        prerequisities_elems = response.css('td.block_content').xpath(
            './/em[contains(text(),"Prerequisite")]/following-sibling::a')
        prerequisities = []
        for req in prerequisities_elems:
            prerequisities.append(req.xpath('text()').get())
        yield {
            'prefix': response.meta['prefix'],
            'title': response.meta['title'],
            'units': units,
            'description': description,
            'prerequisities': prerequisities
        }

    def parse_units(self, response):
        # Some units are in p tag and some or not... First try to find
        # units in p tag (if the p tag was found) and then if units
        # were not found look in the sibling text.
        units = -1
        units_p = response.css('#course_preview_title').xpath(
                './following-sibling::p/text()').get()
        if units_p:
            units = self.find_units(units_p)
        if units == -1:
            units_str = response.css('#course_preview_title').xpath(
                './following-sibling::text()[1]').get()
            units = self.find_units(units_str)
        return units

    def find_units(self, units_string):
        units = re.search(r'(?<=Units: )\d', units_string)
        if units:
            units = int(units.group(0))
        return units

    def parse_description(self, response):
        x = response.css('#course_preview_title').xpath('./following-sibling::text()')
        longest = ''
        if len(x) != 0:
            longest = x[0].get()
            for item in x:
                if len(item.get()) > len(longest):
                    longest = item.get()
        return longest.strip()
