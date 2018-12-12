import re
from typing import List

import scrapy
from scrapy.http import Response


class BulletinSpider(scrapy.Spider):
    name = 'bulletin'

    start_urls = ['http://bulletin.uga.edu/CoursesHome.aspx']

    # download_delay = 0.1
    start = 'http://bulletin.uga.edu/CoursesHome.aspx'

    def parse(self, response: Response):
        for subject in response.css('select#ddlAllPrefixes > option ::attr(value)').extract():
            # Skip over "Select a Prefix" option.
            if subject == '-1':
                continue
            yield scrapy.FormRequest(
                self.start,
                formdata={
                    'ddlAllPrefixes':    subject,
                    '__VIEWSTATE':       response.css('input#__VIEWSTATE::attr(value)').extract_first(),
                    '__EVENTVALIDATION': response.css('input#__EVENTVALIDATION::attr(value)').extract_first()
                },
                callback=self.parse_subjects
            )

    def parse_subjects(self, response: Response):
        for course in response.css('select#ddlAllCourses > option ::attr(value)').extract():
            # Skip over "Select a Course" option.
            if course == '-1':
                continue
            # Skip over options that aren't "All Courses". Could remove this to get more detailed information.
            if course != '0':
                continue
            yield scrapy.FormRequest(
                self.start,
                formdata={
                    'ddlAllCourses':     course,
                    '__VIEWSTATE':       response.css('input#__VIEWSTATE::attr(value)').extract_first(),
                    '__EVENTVALIDATION': response.css('input#__EVENTVALIDATION::attr(value)').extract_first()
                },
                callback=self.parse_result
            )

    course_id = re.compile(r'Course ID:\n(.*?)\n')
    credit_hours = re.compile(r'Course ID:\n(?:.*?)\n\. (.*?)\n')
    course_title = re.compile(r'Course Title:\n(.*?)\n')
    course_description = re.compile(r'Course\nDescription:\n(.*?)\n')
    athena_title = re.compile(r'Athena Title:\n(.*?)\n')
    duplicate_credit = re.compile(r'Duplicate Credit:\n(.*?)\n')
    period = re.compile(r'Semester Course\nOffered:\n(.*?)\n')
    nontraditional = re.compile(r'Nontraditional Format:\n(.*?)\n')
    grading_system = re.compile(r'Grading System:\n(.*?)\n')

    def parse_result(self, response: Response):
        def try_search(pattern, string):
            try:
                return re.search(pattern, string).group(1).strip()
            except AttributeError:
                return None

        for course_table in response.css("table.courseresultstable"):
            course_info: List = course_table.css("td.courseinfo ::text").extract()

            if len(course_info) == 0:
                continue

            joined = '\n'.join(course_info) + '\n'

            joined.replace('\r', ' ')

            result = {
                'course_id':          try_search(self.course_id, joined),
                'credit_hours':       try_search(self.credit_hours, joined),
                'course_title':       try_search(self.course_title, joined),
                'course_description': try_search(self.course_description, joined),
                'athena_title':       try_search(self.athena_title, joined),
                'duplicate_credit':   try_search(self.duplicate_credit, joined),
                'period':             try_search(self.period, joined),
                'nontraditional':     try_search(self.nontraditional, joined),
                'grading_system':     try_search(self.grading_system, joined),
            }
            yield result


if __name__ == '__main__':
    from scrapy.cmdline import execute

    execute()
