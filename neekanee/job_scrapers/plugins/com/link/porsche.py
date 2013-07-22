import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Porsche',
    'hq': 'Atlanta, GA',

    'home_page_url': 'http://www.porsche.com',
    'jobs_page_url': 'http://content2.us.porsche.com/prod/pag/jobs.nsf/usaenglish/jobs_joblocator?OpenDocument&result&market=usaenglish&jobkinds=',

    'empcnt': [5001,10000]
}

class PorscheJobScraper(JobScraper):
    def __init__(self):
        super(PorscheJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        r = re.compile(r'openJob\(\'([^\']+)')

        for a in s.findAll('a', href=r):
            tr = a.findParent('tr')
            td = tr.findAll('td')

            l = self.parse_location(td[-1].text)
            if not l:
                continue

            m = re.search(r, a['href'])
            b = '/prod/company/JobOffers.nsf/usaenglish/%s?OpenDocument' % m.group(1)
            u = urlparse.urljoin(self.br.geturl(), b)

            job = Job(company=self.company)
            job.title = a.text
            job.url = u
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
            x = {'class': 'content'}
            d = s.find('div', attrs=x)

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return PorscheJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
