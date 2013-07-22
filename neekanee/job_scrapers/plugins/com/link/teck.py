import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Teck Resources Limited',
    'hq': 'Vancouver, Canada',

    'home_page_url': 'http://www.teck.com',
    'jobs_page_url': 'http://www.teck.com/Generic.aspx?PAGE=Teck+Site%2fCareers+Pages%2fCareer+Search+Results&portalName=tc',

    'empcnt': [5001,10000]
}

class TeckJobScraper(JobScraper):
    def __init__(self):
        super(TeckJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        r = re.compile(r'Generic\.aspx\?\S+PostingId=\d+')
        
        for a in s.findAll('a', href=r):
            tr = a.findParent('tr')
            td = tr.findAll('td')

            l = re.sub(r'[^-]+-', '', td[1].text)
            l = re.sub(r'near', '', l, flags=re.IGNORECASE)
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
            x = {'class': 'careersdetail-title'}
            t = s.find('td', attrs=x)
            t = t.findParent('table')

            job.desc = get_all_text(t)
            job.save()

def get_scraper():
    return TeckJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
