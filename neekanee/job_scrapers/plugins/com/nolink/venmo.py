import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Venmo',
    'hq': 'Philadelphia PA',

    'contact': 'jobs@venmo.com',
    'benefits': {'vacation': []},

    'home_page_url': 'http://www.venmo.com',
    'jobs_page_url': 'https://venmo.com/info/jobs',

    'empcnt': [1,10]
}

class VenmoJobScraper(JobScraper):
    def __init__(self):
        super(VenmoJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        a = { 'class': 'm_twenty_b gray_top_dotted_divider p_ten_t' }

        for d in s.findAll('div', attrs=a):
            job = Job(company=self.company)
            job.title = d.div.text
            job.url = urlparse.urljoin(self.br.geturl(), d.a['href'])
            job.location = self.company.location
            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return VenmoJobScraper()

