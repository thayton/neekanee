import re, urllib, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Continuum',
    'hq': 'Newton, MA',

    'ats': 'Jobvite',

    'home_page_url': 'http://www.continuum.com',
    'jobs_page_url': 'http://hire.jobvite.com/CompanyJobs/Careers.aspx?c=q0c9Vfw0',

    'empcnt': [51,200]
}

class ContinuumJobScraper(JobScraper):
    def __init__(self):
        super(ContinuumJobScraper, self).__init__(COMPANY)

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
        d = { 'class': 'jvjoblink', 'href': '#' }
        r = re.compile(r"jvGoToPage\('Job Description','','(.*)'\)")

        for a in s.findAll('a', attrs=d):
            tr = a.findParent('tr')
            td = tr.findAll('td')
        
            l = self.parse_location(td[-1].text)
            if not l:
                continue

            m = re.search(r, a['onclick'])
            jobid = m.group(1)

            job = Job(company=self.company)
            job.title = a.text
            job.url = self.new_url(self.br.geturl(), jobid)
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
            f = s.find('form', attrs={'name': 'jvform'})

            job.desc = get_all_text(f)
            job.save()

def get_scraper():
    return ContinuumJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
