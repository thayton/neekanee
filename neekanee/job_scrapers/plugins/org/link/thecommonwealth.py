import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text, get_mailto
from neekanee.urlutil import url_query_filter

from neekanee_solr.models import *

COMPANY = {
    'name': 'The Commonwealth',
    'hq': 'London, England',

    'home_page_url': 'http://thecommonwealth.org',
    'jobs_page_url': 'http://thecommonwealth.org/jobs',

    'empcnt': [51,200]
}

class CommonWealthJobScraper(JobScraper):
    def __init__(self):
        super(CommonWealthJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        r = self.br.response().read()
        b = r[r.find('<body'):]
        s = soupify(b)

        r = re.compile(r'\bview-job-vacancies\b')
        x = {'class': r}
        d = s.find('div', attrs=x)
        r = re.compile(r'^/jobs/[^/]+$')

        for a in d.findAll('a', href=r):
            job = Job(company=self.company)
            job.title = a.text
            job.url = urlparse.urljoin(self.br.geturl(), a['href'])
            jobs.append(job)

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            r = self.br.response().read()
            b = r[r.find('<body'):]
            s = soupify(b)

            r = re.compile(r'^node-\d+$')
            d = s.find('div', id=r)
            f = lambda x: x.name == 'strong' and x.text == 'Location:'
            t = d.find(f)
            if not t:
                continue

            l = self.parse_location(t.nextSibling)
            if not l:
                continue

            job.location = l
            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return CommonWealthJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
