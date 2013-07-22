import re, urlparse, webcli

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'International Atomic Energy Agency',
    'hq': 'Vienna, Austria',

    'home_page_url': 'http://www.iaea.org',
    'jobs_page_url': 'https://recruitment.iaea.org/phf/p_vacancies.asp',

    'empcnt': [1001,5000]
}

class IaeaJobScraper(JobScraper):
    def __init__(self):
        super(IaeaJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        d = s.find('div', id='content')
        x = {'class': 'vnList'}
        t = d.find('table', attrs=x)
        r = re.compile(r'/vacancies/p/\d{4}/\d{4}_\d+\.html$')

        for a in t.findAll('a', href=r):
            job = Job(company=self.company)
            job.title = a.text
            job.url = urlparse.urljoin(self.br.geturl(), a['href'])
            jobs.append(job)

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            d = s.find('div', id='vnBody')
            t = d.find(text='Duty Station:')

            if not t:
                continue

            tr = t.findParent('tr')
            td = tr.findAll('td')

            l = self.parse_location(td[-1].text)

            if not l:
                continue

            job.location = l
            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return IaeaJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
