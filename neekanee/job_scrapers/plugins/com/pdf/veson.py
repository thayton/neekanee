import re, urlparse, urllib

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text
from neekanee.txtextract.pdftohtml import pdftohtml

from neekanee_solr.models import *

COMPANY = {
    'name': 'Veson Nautical',
    'hq': 'Boston, MA',

    'home_page_url': 'http://www.veson.com',
    'jobs_page_url': 'http://www.veson.com/careers/current-openings/',

    'empcnt': [11,50]
}

class VesonJobScraper(JobScraper):
    def __init__(self):
        super(VesonJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        d = s.find('div', id='main')
        x = {'class': 'viewDescription'}
        r = re.compile(r'.*\.pdf')

        for v in d.findAll('div', attrs=x):
            t = v.a.contents[0]
            l = t.split('-')

            if len(l) > 1:
                l = self.parse_location(l[1])
            else:
                l = t.split('&ndash;')
                if len(l) > 1:
                    l = self.parse_location(l[1])
                else:
                    l = self.company.location
            
            x = v.findParent('div')
            a = x.find('a', href=r)

            if not a:
                continue

            job = Job(company=self.company)
            job.title = t
            job.location = l or self.company.location
            job.url = urlparse.urljoin(self.br.geturl(), urllib.quote(a['href'].strip(), ':/'))
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
    return VesonJobScraper()
