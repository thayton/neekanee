import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Telecom Italia',
    'hq': 'Milano, Italy',

    'home_page_url': 'http://www.telecomItalia.com',
    'jobs_page_url': 'http://www.telecomitalia.com/tit/en/career/per-candidarti/opportunita.html',

    'empcnt': [10001]
}

class TelecomItaliaJobScraper(JobScraper):
    def __init__(self):
        super(TelecomItaliaJobScraper, self).__init__(COMPANY, return_usa_only=False)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        x = {'class': 'table-inner'}
        d = s.find('div', attrs=x)
        r = re.compile(r'/en/career/')

        for a in d.table.findAll('a', href=r):
            tr = a.findParent('tr')
            td = tr.findAll('td')
            
            l = self.parse_location(td[-3].text)
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
            d = s.find('div', id='ti-content')

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return TelecomItaliaJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
