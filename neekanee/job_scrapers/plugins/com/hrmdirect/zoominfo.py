import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'ZoomInfo',
    'hq': 'Columbia, MD',

    'ats': 'hrm direct',

    'benefits': {
        'url': 'http://www.zoominfo.com/business/about/careers.html#2',
        'vacation': [(0,17)],
        'tuition_assistance': True
    },

    'home_page_url': 'http://www.zoominfo.com',
    'jobs_page_url': 'http://zoominfo.hrmdirect.com/employment/job-openings.php?search=true&nohd',

    'empcnt': [51,200]
}

class ZoomInfoJobScraper(JobScraper):
    def __init__(self):
        super(ZoomInfoJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        x = {'class': 'reqResultTable'}
        t = s.find('table', attrs=x)
        r = re.compile(r'^job-opening\.php\?req=\d+')

        for a in t.findAll('a', href=r):
            tr = a.findParent('tr')
            td = tr.findAll('td')

            l = td[-3].text + ', ' + td[-2].text
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
            x = {'class': 'reqResult'}
            d = s.find('div', attrs=x)

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return ZoomInfoJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
