import re, urlparse, mechanize

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Scotiabank',
    'hq': 'Toronto, Canada',

    'home_page_url': 'http://www.scotiabank.com',
    'jobs_page_url': 'http://jobs.scotiabank.com/careers/',

    'empcnt': [10001]
}

class ScotiabankJobScraper(JobScraper):
    def __init__(self):
        super(ScotiabankJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        while True:
            s = soupify(self.br.response().read())
            x = {'class': 'jobTitle'}

            for td in s.findAll('td', attrs=x):
                tr = td.findParent('tr')

                l = tr.find('td', attrs={'class': 'location'})
                l = self.parse_location(l.text)

                if not l:
                    continue

                job = Job(company=self.company)
                job.title = td.text
                job.url = urlparse.urljoin(self.br.geturl(), td.a['href'])
                job.location = l
                jobs.append(job)

            try:
                self.br.follow_link(self.br.find_link(text='Next page'))
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
            x = {'class': 'job-details'}
            d = s.find('div')

            job.desc = get_all_text(d)
            job.save()
    
def get_scraper():
    return ScotiabankJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
