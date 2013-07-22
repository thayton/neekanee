import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text, get_mailto

from neekanee_solr.models import *

COMPANY = {
    'name': 'InfoStretch',
    'hq': 'Santa Clara, CA',

    'benefits': {'vacation': [(1,10)]},

    'home_page_url': 'http://www.infostretch.com',
    'jobs_page_url': 'http://www.infostretch.com/About/Current_Opportunities.php',

    'empcnt': [201,500]
}

class InfoStretchJobScraper(JobScraper):
    def __init__(self):
        super(InfoStretchJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        r = re.compile(r'^Location')

        for t in s.findAll(text=r):
            v = t.rsplit('-', 1)
            if len(v) < 2:
                v = t.rsplit('&ndash;', 1)
            if len(v) < 2:
                continue

            v = v[1]
            x = t.findNext('tr')
            r = re.compile(r'^javascript:eventdetails\(\'(\d+)\'')

            for a in x.findAll('a', attrs={'onclick': r}):
                m = re.search(r, a['onclick'])
                l = 'jobDescription.php?copening_id=' + m.group(1)

                job = Job(company=self.company)
                job.title = a.text
                job.url = urlparse.urljoin(self.br.geturl(), l)
                jobs.append(job)

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            t = s.find(text=re.compile(r'^Location -'))
            l = t.split('-', 1)[1]
            l = self.parse_location(l)
            t = t.findNext('tr')

            if not l:
                continue

            job.location = l
            job.desc = get_all_text(t)
            job.save()

def get_scraper():
    return InfoStretchJobScraper()
