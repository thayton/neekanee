import re, urlparse, urllib

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text
from neekanee.txtextract.pdftohtml import pdftohtml

from neekanee_solr.models import *

COMPANY = {
    'name': 'Wave Broadband',
    'hq': 'Seattle, WA',

    'home_page_url': 'http://www.wavebroadband.com',
    'jobs_page_url': 'http://www.wavebroadband.com/about/careers.php',

    'empcnt': [201,500],
}

class WaveBroadbandJobScraper(JobScraper):
    def __init__(self):
        super(WaveBroadbandJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        d = s.find('div', id='about_us_careers')
        r = re.compile(r'/jobs/Job Posting .*\.pdf$')
        x = re.compile(r' in (\w+, \w{2})$')

        for a in d.findAll('a', href=r):
            if not a.has_key('title'):
                continue

            m = re.search(x, a['title'])
            if not m:
                continue

            l = self.parse_location(m.group(1))
            if not l:
                continue

            job = Job(company=self.company)
            job.title = a.text
            job.url = urlparse.urljoin(self.br.geturl(), urllib.quote(a['href'], '/:'))
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
    return WaveBroadbandJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
