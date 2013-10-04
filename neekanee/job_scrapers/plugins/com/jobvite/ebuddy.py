import re, urllib, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'eBuddy',
    'hq': 'Amsterdam, Netherlands',

    'ats': 'Jobvite',

    'home_page_url': 'http://www.ebuddy.com',
    'jobs_page_url': 'http://hire.jobvite.com/Jobvite/Jobs.aspx?b=nKE7mlwH',

    'empcnt': [51,200]
}

class EbuddyJobScraper(JobScraper):
    def __init__(self):
        super(EbuddyJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        r = re.compile(r'Jobvite/Job\.aspx\?')

        for a in s.findAll('a', href=r):
            if a.parent.name != 'b':
                continue

            tr = a.findParent('tr')
            td = tr.findAll('td')

            l = td[0].findAll('span')[1]
            l = self.parse_location(l.text)

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
            f = s.find('form', attrs={'name': 'Form1'})

            job.desc = get_all_text(f)
            job.save()

def get_scraper():
    return EbuddyJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
