import re, urllib, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text
from neekanee.urlutil import url_query_add

from neekanee_solr.models import *

COMPANY = {
    'name': 'Guavus',
    'hq': 'San Mateo, CA',

    'ats': 'Jobvite',

    'home_page_url': 'http://www.guavus.com',
    'jobs_page_url': 'http://hire.jobvite.com/CompanyJobs/Jobs.aspx?c=qOo9Vfw0&jvresize=http://www.guavus.com/wp-content/themes/guavus/FrameResize.html',

    'empcnt': [201,500]
}

class GuavusJobScraper(JobScraper):
    def __init__(self):
        super(GuavusJobScraper, self).__init__(COMPANY)

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
        r = re.compile(r'/careers/\?jvi=(\w+,Job)$')
        x = { 'class': 'jvjoblink', 'href': r }

        for a in s.findAll('a', attrs=x):
            p = a.parent.span
            l = self.parse_location(p.text)

            if not l:
                continue

            m = re.search(r, a['href'])
            i = {'j': m.group(1), 'k':'Job'}
            u = url_query_add(self.br.geturl(), i.items())

            job = Job(company=self.company)
            job.title = a.text
            job.url = u
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
    return GuavusJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
