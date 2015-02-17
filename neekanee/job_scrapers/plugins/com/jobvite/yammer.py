import re, urllib, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Yammer',
    'hq': 'San Francisco, CA',

    'ats': 'Jobvite',

    'home_page_url': 'https://www.yammer.com',
    'jobs_page_url': 'https://hire.jobvite.com/CompanyJobs/Jobs.aspx?c=qI19Vfwx&jvresize=/wp-content/themes/roots/js/jobvite_frameresize.html',

    'empcnt': [51,200]
}

class YammerJobScraper(JobScraper):
    def __init__(self):
        super(YammerJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        # Acquired by Microsoft
        self.company.job_set.all().delete()

def get_scraper():
    return YammerJobScraper()
