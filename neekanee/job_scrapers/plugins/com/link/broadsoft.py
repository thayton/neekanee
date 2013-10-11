import re, urllib2, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'BroadSoft',
    'hq': 'Gaithersburg, MD',

    'home_page_url': 'http://www.broadsoft.com',
    'jobs_page_url': 'http://apply.broadsoft.com/careers/careers.aspx',

    'empcnt': [201,500]
}

class BroadSoftJobScraper(JobScraper):
    def __init__(self):
        super(BroadSoftJobScraper, self).__init__(COMPANY)
        
    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)
        self.br.follow_link(self.br.find_link(text_regex=re.compile(r'Current Open Positions')))

        s = soupify(self.br.response().read())

        for a in s.findAll('a', attrs={'class': 'JobLink'}):
            tr = a.findParent('tr')
            td = tr.findAll('td')

            l = td[-1].text
            f = l.lower()

            if f.startswith('mult'):
                l = l[len('mult')+1:]
                l = l.split(',')[0]

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
            s.footer.extract()

            [ b.extract() for b in s.findAll('body') ]

            job.desc = get_all_text(s.html)
            job.save()

def get_scraper():
    return BroadSoftJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
