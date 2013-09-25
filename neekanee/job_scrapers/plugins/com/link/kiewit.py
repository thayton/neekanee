import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Kiewit',
    'hq': 'Omaha, NE',

    'home_page_url': 'http://www.kiewit.com',
    'jobs_page_url': 'http://kiewitjobs.com/careers/',

    'empcnt': [10001]
}

class KiewitJobScraper(JobScraper):
    def __init__(self):
        super(KiewitJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        x = re.compile(r'^jobs_list_link_\d+$')
        y = {'class': 'location'}

        while True:
            s = soupify(self.br.response().read())
            d = s.find('div', id='SearchResultsConteiner')

            for a in d.findAll('a', id=x):
                tr = a.findParent('tr')
                td = tr.find('td', attrs=y)

                l = self.parse_location(td.text)
                if not l:
                    continue

                job = Job(company=self.company)
                job.title = a.text
                job.url = urlparse.urljoin(self.br.geturl(), a['href'])
                job.url = job.url.encode('utf8')
                job.location = l
                jobs.append(job)

            a = s.find('a', id='jobs_next_page_link')
            if not a:
                break

            u = urlparse.urljoin(self.br.geturl(), a['href'])
            self.br.open(u)

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            try:
                self.br.open(job.url)
            except:
                continue

            s = soupify(self.br.response().read())
            x = {'class': 'box jobDesc'}
            d = s.find('div', id='jobDesc')

            if not d:
                continue

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return KiewitJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
