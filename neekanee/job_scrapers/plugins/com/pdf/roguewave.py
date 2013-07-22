import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text, get_mailto
from neekanee.txtextract.pdftohtml import pdftohtml

from neekanee_solr.models import *

COMPANY = {
    'name': 'Rogue Wave',
    'hq': 'Boulder, CO',

    'contact': 'staffing@roguewave.com',
    'benefits': {'vacation': []},

    'home_page_url': 'http://www.roguewave.com',
    'jobs_page_url': 'http://www.roguewave.com/company/careers.aspx',

    'empcnt': [51,200]
}

class RogueWaveJobScraper(JobScraper):
    def __init__(self):
        super(RogueWaveJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        f = lambda x: x.name == 'h2' and x.text == 'Current Openings:'
        h = s.find(f)
        u = h.nextSibling.nextSibling
        r = re.compile(r'^/documents\.aspx\?Command=Core_Download&EntryId=\d+')

        for a in u.findAll('a', href=r):
            job = Job(company=self.company)
            job.title = a.text
            job.url = urlparse.urljoin(self.br.geturl(), a['href'])

            l = self.company.location
            m = re.search(r'\((.*)\)', a.parent.contents[-1])

            if m:
                l = self.parse_location(m.group(1))

            if not l:
                continue

            job.location = l
            jobs.append(job)

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            d = self.br.response().read()
            s = soupify(pdftohtml(d))

            job.desc = get_all_text(s.html.body)
            job.save()
        
def get_scraper():
    return RogueWaveJobScraper()
