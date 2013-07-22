import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Bottomline Technologies',
    'hq': 'Portsmouth, NH',

    'home_page_url': 'http://www.bottomline.com',
    'jobs_page_url': 'http://www.bottomline.com/about/careers.html',

    'empcnt': [501,1000]
}

class BottomlineJobScraper(JobScraper):
    def __init__(self):
        super(BottomlineJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        t = s.find('table', attrs={'class': 'content'})
        r = re.compile(r'home.eease.com/recruit/\?id=\d+')

        for a in t.findAll('a', href=r):
            tr = a.findParent('tr')
            td = tr.findAll('td')

            l = td[-1].text.split(' or ')[0]
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
            f = s.find('form')
            t = f.table

            job.desc = get_all_text(t)
            job.save()

def get_scraper():
    return BottomlineJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
