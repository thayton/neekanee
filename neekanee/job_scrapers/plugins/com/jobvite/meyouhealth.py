import re, urllib, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'MeYou Health',
    'hq': 'Boston, MA',

    'ats': 'Jobvite',

    'home_page_url': 'http://meyouhealth.com',
    'jobs_page_url': 'http://hire.jobvite.com/Jobvite/Jobs.aspx?b=nFEJyfwk',

    'empcnt': [11,50]
}

class MeYouHealthJobScraper(JobScraper):
    def __init__(self):
        super(MeYouHealthJobScraper, self).__init__(COMPANY)

    def new_url(self, url, jobid):
        u = urlparse.urlparse(url)
        l = urlparse.parse_qsl(u.query)
        x = [ (k,v) for (k,v) in l if k == 'c' ]

        x.append(('page', 'Job Description'))
        x.append(('j',     jobid))

        u = list(u)
        u[4] = urllib.urlencode(x)
        u = urlparse.urlunparse(u)

        return u

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        x = {'name': 'JobList'}
        i = s.find('input', attrs=x)
        t = i.findNext('table')
        r = re.compile(r'Job\.aspx\?')

        for a in t.findAll('a', href=r):
            p = a.findNext('span')
            l = self.parse_location(p.text)

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
            t = s.find('table', id='maintable')

            job.desc = get_all_text(t)
            job.save()

def get_scraper():
    return MeYouHealthJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
