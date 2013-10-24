import re, urlparse, mechanize

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'SuccessFactors',
    'hq': 'San Francisco, CA',

    'home_page_url': 'http://www.successfactors.com',
    'jobs_page_url': 'http://jobs.successfactors.com/search',

    'empcnt': [1001,5000]
}

class SuccessFactorsJobScraper(JobScraper):
    def __init__(self):
        super(SuccessFactorsJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        pageno = 2

        while True:
            s = soupify(self.br.response().read())
            r = re.compile(r'^/job/[^/]+/\d+/$$')
            t = s.find('table', id='searchresults')
            x = {'class': 'jobLocation'}

            for a in t.findAll('a', href=r):
                tr = a.findParent('tr')
                sp = tr.find('span', attrs=x)

                l = self.parse_location(sp.text)
                if not l:
                    continue

                job = Job(company=self.company)
                job.title = a.text
                job.url = urlparse.urljoin(self.br.geturl(), a['href'])
                job.location = l
                jobs.append(job)

            try:
                self.br.follow_link(self.br.find_link(text='Page %d' % pageno))
                pageno += 1
                break
            except mechanize.LinkNotFoundError:
                break

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            x = {'class': 'jobDisplay'}
            d = s.find('div', attrs=x)

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return SuccessFactorsJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
