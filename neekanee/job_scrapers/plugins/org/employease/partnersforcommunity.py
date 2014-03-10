import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Partners for Community',
    'hq': 'Springfield, MA',

    'home_page_url': 'http://www.partnersforcommunity.org',
    'jobs_page_url': 'http://www.partnersforcommunity.org/default/index.cfm/job-opportunities/',

    'empcnt': [11,50]
}

class PartnersForCommunityJobScraper(JobScraper):
    def __init__(self):
        super(PartnersForCommunityJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        r = re.compile(r'^/default/index\.cfm/job-opportunities/[A-Z]+\d+$')
        d = s.find('div', id='content2')

        for a in d.findAll('a', href=r):
            l = a.text.split('-')[0]
            l = ','.join(l.split(',')[1:])
            l = re.sub(r'\(.*', '', l)
            l = self.parse_location(l)

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
            r = re.compile(r'home\.eease\.adp\.com/recruit/\?id=\d+$')
            
            self.br.follow_link(self.br.find_link(url_regex=r))

            s = soupify(self.br.response().read())
            f = s.find('form', id='Container0')

            job.desc = get_all_text(f)
            job.save()

def get_scraper():
    return PartnersForCommunityJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
