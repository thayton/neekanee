import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text
from neekanee.urlutil import url_query_filter

from neekanee_solr.models import *

COMPANY = {
    'name': 'MathWorks',
    'hq': 'Natick, MA',

    'home_page_url': 'http://www.mathworks.com',
    'jobs_page_url': 'http://www.mathworks.com/company/jobs/opportunities/search?',

    'empcnt': [1,10]
}

class MathWorksJobScraper(JobScraper):
    def __init__(self):
        super(MathWorksJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        while True:
            s = soupify(self.br.response().read())
            d = s.find('div', id='results_container')
            r = re.compile(r'/company/jobs/opportunities/\S+')

            for a in d.findAll('a', href=r):
                tr = a.findParent('tr')
                l = self.parse_location(tr.span.text)

                if not l:
                    continue

                job = Job(company=self.company)
                job.title = a.text
                job.url = urlparse.urljoin(self.br.geturl(), a['href'])
                job.location = l
                jobs.append(job)

            x = {'class': 'next_page pagination '}
            a = s.find('a', attrs=x)
            if not a:
                break

            u = urlparse.urljoin(self.br.geturl(), a['href'])
            self.br.open(u)

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            d = s.find('div', id='content_container')

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return MathWorksJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
