import re, urlparse, mechanize

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text
from neekanee.urlutil import url_query_del

from neekanee_solr.models import *

COMPANY = {
    'name': 'Thermo Fisher Scientific',
    'hq': 'Waltham, MA',

    'home_page_url': 'http://www.thermofisher.com',
    'jobs_page_url': 'http://jobs.thermofisher.com',

    'empcnt': [10001]
}

class ThermoFisherJobScraper(JobScraper):
    def __init__(self):
        super(ThermoFisherJobScraper, self).__init__(COMPANY, return_usa_only=False)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        r = re.compile(r'/job-detail/[^/]+/\d+/$')
        x = {'class': 'jobslink', 'href': r}
        y = {'class': re.compile(r'joblocation')}

        for a in s.findAll('a', attrs=x):
            d = a.find('div', attrs=y)
            l = self.parse_location(d.get('title', d.text))
            if not l:
                continue

            job = Job(company=self.company)
            job.title = a.span.text
            job.url = urlparse.urljoin(self.br.geturl(), a['href'])
            job.location = l
            jobs.append(job)

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            a = s.find('article', id='job-details')

            job.desc = get_all_text(a)
            job.save()

def get_scraper():
    return ThermoFisherJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
