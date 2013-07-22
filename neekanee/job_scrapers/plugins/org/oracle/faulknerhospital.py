import re, urlparse, mechanize

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Faulkner Hospital',
    'hq': 'Boston, MA',

    'home_page_url': 'http://www.faulknerhospital.org',
    'jobs_page_url': 'http://careers.brighamandwomensfaulkner.org/boston',

    'empcnt': [51,200]
}

class FaulknerJobScraper(JobScraper):
    def __init__(self):
        super(FaulknerJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        while True:
            s = soupify(self.br.response().read())
            d = s.find('div', id='divMain')
            x = {'class': 'info-table'}
            t = d.find('table', attrs=x)
            r = re.compile(r'jobs_list_link_\d+')

            for a in t.findAll('a', id=r):
                tr = a.findParent('tr')
                td = tr.find('td', attrs={'class': 'location'})
            
                l = self.parse_location(td.text)
                if not l:
                    continue
                        
                job = Job(company=self.company)
                job.title = a.text
                job.url = urlparse.urljoin(self.br.geturl(), a['href'])
                job.location = l
                jobs.append(job)

            # Navigate to the next page
            try:
                f = lambda x: dict(x.attrs).has_key('id') and dict(x.attrs)['id'] == 'jobs_next_page_link'
                n = self.br.find_link(predicate=f)
                self.br.follow_link(n)
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
            x = {'class': 'box jobDesc'}
            d = s.find('div', attrs=x)

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return FaulknerJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
