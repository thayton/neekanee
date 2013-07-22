import re, urlparse, mechanize

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text
from neekanee.urlutil import url_query_del

from neekanee_solr.models import *

COMPANY = {
    'name': 'Thermo Fisher Scientific',
    'hq': 'Waltham, MA',

    'home_page_url': 'http://www.thermofisher.com',
    'jobs_page_url': 'https://careers.thermofisher.com/joblist.html?erpc=alljobs',

    'empcnt': [10001]
}

class ThermoFisherJobScraper(JobScraper):
    def __init__(self):
        super(ThermoFisherJobScraper, self).__init__(COMPANY, return_usa_only=False)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        while True:
            s = soupify(self.br.response().read())
            x = {'name': 'newjoblist'}
            f = s.find('form', attrs=x)
            r = re.compile(r'^viewjob\.html\?')

            for a in f.findAll('a', href=r):
                tr = a.findParent('tr')
                td = tr.findAll('td')

                l = td[3].text.split(',')[0]
                l = self.parse_location(l)

                if not l:
                    continue

                job = Job(company=self.company)
                job.title = a.text
                job.url = urlparse.urljoin(self.br.geturl(), a['href'])
                job.url = url_query_del(job.url, 'JServSessionIdroot')
                job.location = l
                jobs.append(job)

            try:
                x = re.compile(r'^Next.+Page$')
                self.br.follow_link(self.br.find_link(text_regex=x))
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
            d = s.find('div', id='container')
            t = d.find('td', attrs={'class': 'tablebackgroundcolor'})

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return ThermoFisherJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
