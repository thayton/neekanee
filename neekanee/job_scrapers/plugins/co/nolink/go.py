import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': '.CO Internet',
    'hq': 'Bogota, Columbia',

    'home_page_url': 'http://www.go.co',
    'jobs_page_url': 'http://www.go.co/company/team/careers',

    'empcnt': [11,50]
}

class CoJobScraper(JobScraper):
    def __init__(self):
        super(CoJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        r = re.compile(r'^views_slideshow_cycle_div_job_openings-panel_pane_\d+_\d+$')
        x = {'id': r}
        y = {'class': 'location'}

        self.company.job_set.all().delete()

        for d in s.findAll('div', attrs=x):
            p = s.find('span', attrs=y)
            p = p.div.text.split(';')[0]
            l = self.parse_location(p)

            if not l:
                continue

            job = Job(company=self.company)
            job.title = d.h3.text
            job.url = self.br.geturl()
            job.location = l
            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return CoJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
