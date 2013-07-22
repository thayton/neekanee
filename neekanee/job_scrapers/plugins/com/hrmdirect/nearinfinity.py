import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Near Infinity',
    'hq': 'Reston, VA',

    'ats': 'hrmdirect',

    'home_page_url': 'http://www.nearinfinity.com',
    'jobs_page_url': 'http://nearinfinity.hrmdirect.com/employment/openings.php',

    'gptwcom_entrepreneur': True,

    'empcnt': [51,200]
}

class NearInfinityJobScraper(JobScraper):
    def __init__(self):
        super(NearInfinityJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        t = s.find('table', attrs={'class': 'reqResultTable'})
        r = re.compile(r'^job-opening\.php\?req=\d+&#job')

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
            x = {'class': 'reqResult'}
            d = s.find('div', attrs=x)
            t = d.find('td', text='Location:')
            
            if not t:
                continue

            tr = t.findParent('tr')
            td = tr.findAll('td')
            
            l = self.parse_location(td[-1].text)

            if not l:
                continue

            job.desc = get_all_text(d)
            job.location = l
            job.save()

def get_scraper():
    return NearInfinityJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
