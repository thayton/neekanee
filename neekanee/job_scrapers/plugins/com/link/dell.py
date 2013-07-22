import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Dell',
    'hq': 'Round Rock, TX',

    'home_page_url': 'http://www.dell.com',
    'jobs_page_url': 'http://jobs.dell.com/careers/',

    'empcnt': [10001]
}

class DellJobScraper(JobScraper):
    def __init__(self):
        super(DellJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        while True:
            s = soupify(self.br.response().read())
            d = s.find('div', id='conteinerForSearchResults')
            r = re.compile(r'^jobs_list_link_\d+$')

            for a in d.findAll('a', id=r):
                tr = a.findParent('tr')
                td = tr.findAll('td')

                if len(td[1].text.strip()) == 0:
                    continue

                l = self.parse_location(td[1].text)
                if not l:
                    continue

                job = Job(company=self.company)
                job.title = a.text
                job.url = urlparse.urljoin(self.br.geturl(), a['href'])
                job.location = l
                jobs.append(job)

            n = s.find('a', id='jobs_next_page_link')

            if not n:
                break

            u = urlparse.urljoin(self.br.geturl(), n['href'])

            self.br.open(u)

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            x = {'class': 'box jobDesc'}
            d = s.find('div', attrs=x)
            
            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return DellJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
