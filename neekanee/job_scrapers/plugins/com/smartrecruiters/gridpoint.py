import re, urllib, urlparse, mechanize

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text, get_mailto

from neekanee_solr.models import *

COMPANY = {
    'name': 'GridPoint',
    'hq': 'Arlington, VA',

    'home_page_url': 'http://www.gridpoint.com',
    'jobs_page_url': 'http://www.smartrecruiters.com/Gridpoint/',

    'empcnt': [51,200]
}

class GridPointJobScraper(JobScraper):
    def __init__(self):
        super(GridPointJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        pageno = 1

        while True:
            s = soupify(self.br.response().read())
            t = s.find('table', attrs={'class': 'cs_table'})
            r = re.compile(r'/Gridpoint/\d+-\S+')

            for a in t.findAll('a', href=r):
                tr = a.findParent('tr')
                td = a.findParent('td')

                if td != tr.td:
                    continue

                job = Job(company=self.company)
                job.title = a.text
                job.url = urlparse.urljoin(self.br.geturl(), a['href'])
                jobs.append(job)

            # Navigate to next page
            a = s.find('a', attrs={'class': 'next'})
            if not a:
                break

            f = a.findParent('form')
            n = f.input.nextSibling
            n = ' '.join(n.split())

            if 'of %d' % pageno == n:
                break
            else:
                pageno += 1

            u = urlparse.urljoin(self.br.geturl(), a['href'])
            self.br.open(u)

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            d = s.find('div', attrs={'class': 'jobAdWrapper'})
            l = d.find('span', attrs={'class': 'jobAdLocation'})
            l = self.parse_location(l.text)

            if not l:
                continue

            job.location = l
            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return GridPointJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
