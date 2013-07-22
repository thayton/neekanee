import re, urlparse, urllib

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'United Nations Development Programme',
    'hq': 'New York, NY',

    'home_page_url': 'http://www.undp.org',
    'jobs_page_url': 'http://jobs.undp.org/cj_view_jobs.cfm',

    'empcnt': [10001]
}

class UndpJobScraper(JobScraper):
    def __init__(self):
        super(UndpJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        r = re.compile(r'^cj_view_job\.cfm\?cur_job_id=\d+$')

        for a in s.findAll('a', href=r):
            tr = a.findParent('tr')
            td = tr.findAll('td')

            l = self.parse_location(td[-2].text)
            if not l:
                continue

            job = Job(company=self.company)
            job.title = a.text
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
            x = {'class': 'job'}
            t = s.find('td', attrs=x)
            t = t.findParent('table')

            job.desc = get_all_text(t)
            job.save()

def get_scraper():
    return UndpJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
