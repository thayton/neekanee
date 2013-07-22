import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Parrot',
    'hq': 'Paris, France',

    'home_page_url': 'http://www.parrot.com',
    'jobs_page_url': 'http://recrute.parrot.com/en/offres.php',

    'empcnt': [501,1000]
}

class ParrotJobScraper(JobScraper):
    def __init__(self):
        super(ParrotJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        r = re.compile(r'^details-offre\.php\?id=\d+$')
        x = {'class': 'list-jobs'}
        t = s.find('table', attrs=x)
        y = {'class': 'td-city'}
        
        for a in t.findAll('a', href=r):
            if a.parent['class'] != 'td-mission':
                continue

            tr = a.findParent('tr')
            td = tr.find('td', attrs=y)

            l = self.parse_location(td.text)
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
            x = {'class': 'wrapper'}
            n = s.find('section', id='section-2')

            job.desc = get_all_text(n)
            job.save()

def get_scraper():
    return ParrotJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
