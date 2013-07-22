import re, urlparse, mechanize

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Edmunds.com',
    'hq': 'Santa Monica, CA',

    'home_page_url': 'http://www.edmunds.com',
    'jobs_page_url': 'http://jobs.edmunds.com/search/',

    'empcnt': [201,500]
}

class EdmundsJobScraper(JobScraper):
    def __init__(self):
        super(EdmundsJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        pageno = 2

        while True:
            s = soupify(self.br.response().read())
            t = s.find('table', id='searchresults')
            x = {'class': 'jobTitle'}
            y = {'class': 'jobLocation'}

            for p in s.findAll('span', attrs=x):
                if not p.a:
                    continue

                tr = p.findParent('tr')

                l = tr.find('span', attrs=y)
                l = self.parse_location(l.text)

                if not l:
                    continue

                job = Job(company=self.company)
                job.title = p.a.text
                job.url = urlparse.urljoin(self.br.geturl(), p.a['href'])
                job.location = l
                jobs.append(job)

            try:
                self.br.follow_link(self.br.find_link(text='Page %d' % pageno))
                pageno += 1
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
    return EdmundsJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
