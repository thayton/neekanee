import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Community Wealth Ventures',
    'hq': 'Washington, DC',

    'home_page_url': 'http://www.communitywealth.com',
    'jobs_page_url': 'https://www.smartrecruiters.com/CommunityWealthVentures/',

    'empcnt': [11,50]
}

class CommunityWealthJobScraper(JobScraper):
    def __init__(self):
        super(CommunityWealthJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        x = {'class': 'cs_table'}
        y = {'title': True}
        t = s.find('table', attrs=x)        

        for a in t.findAll('a', attrs=y):
            tr = a.findParent('tr')
            td = tr.findAll('td')

            if a != td[0].a:
                continue

            job = Job(company=self.company)
            job.title = a.text
            job.url = urlparse.urljoin(self.br.geturl(), a['href'])
            job.location = self.company.location
            jobs.append(job)

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            x = {'class': 'jobAdWrapper'}
            d = s.find('div', attrs=x)

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return CommunityWealthJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
