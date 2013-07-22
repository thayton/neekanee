import re, urlparse, mechanize

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Arbor Networks',
    'hq': 'Chelmsford, MA',

    'home_page_url': 'http://www.arbornetworks.com',
    'jobs_page_url': 'http://jobs.danaher.com/go/jobs-with-arbor-networks/333688/',

    'empcnt': [201,500]
}

class ArborJobScraper(JobScraper):
    def __init__(self):
        super(ArborJobScraper, self).__init__(COMPANY, return_usa_only=False)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        pageno = 2

        while True:
            s = soupify(self.br.response().read())
            t = s.find('table', id='searchresults')
            x = {'class': 'jobTitle'}
            r = re.compile(r'/jobs/\S+')

            for p in t.tbody.findAll('span', attrs=x):
                tr = p.findParent('tr')
                td = tr.find('td', attrs={'class': 'colLocation'})

                l = self.parse_location(td.text)
                if not l:
                    continue

                job = Job(company=self.company)
                job.title = p.text
                job.url = urlparse.urljoin(self.br.geturl(), p.a['href'])
                job.location = l
                jobs.append(job)

            try:
                self.br.follow_link(self.br.find_link(text='Page %d' % pageno))
                pageno += 1
            except mechanize.LinkNotFoundError:
                break

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            x = {'class': 'jobDisplay'}
            d = s.find('div', attrs=x)

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return ArborJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
