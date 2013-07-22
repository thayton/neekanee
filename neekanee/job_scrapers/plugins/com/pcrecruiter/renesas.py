import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Renesas',
    'hq': 'Santa Clara, CA',

    'home_page_url': 'http://am.renesas.com',
    'jobs_page_url': 'http://www.pcrecruiter.net/pcrbin/regmenu.exe?uid=Renesas%20Electronics%20America%20Inc.Renesastechnologyamericainc',

    'empcnt': [501,1000]
}

class RenasasJobScraper(JobScraper):
    def __init__(self):
        super(RenasasJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)
        self.br.select_form('mainsearch')
        self.br.submit()

        s = soupify(self.br.response().read())
        t = s.find('table', id='reg5_table9')
        r = re.compile(r'^/pcrbin/reg5\.aspx\?')

        for a in t.findAll('a', href=r):
            tr = a.findParent('tr')
            td = tr.findAll('td')

            l = self.parse_location(td[1].text)
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
            t = s.find('table', id='reg5_table20')

            job.desc = get_all_text(t)
            job.save()

def get_scraper():
    return RenasasJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
