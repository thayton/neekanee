import re, urlparse, mechanize

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'CACI International',
    'hq': 'Arglinton, VA',

    'home_page_url': 'http://www.caci.com',
    'jobs_page_url': 'http://careers.caci.com/search?q',

    'empcnt': [10001]
}

class CaciJobScraper(JobScraper):
    def __init__(self):
        super(CaciJobScraper, self).__init__(COMPANY, return_usa_only=False)

    def scrape_job_links(self, url):
        jobs = []

        pageno = 2
        self.br.open(url)

        while True:
            s = soupify(self.br.response().read())
            t = s.find('table', id='searchresults')
            r = re.compile(r'^/job/\S+/\d+/$')

            for a in t.findAll('a', href=r):
                tr = a.findParent('tr')

                p = tr.find('span', attrs={'class': 'jobLocation'})
                l = self.parse_location(p.text)
                
                if not l:
                    continue

                job = Job(company=self.company)
                job.title = a.text
                job.url = urlparse.urljoin(self.br.geturl(), a['href'])
                job.location = l
                jobs.append(job)

            try:
                x = re.compile(r'Page %d' % pageno)
                self.br.follow_link(self.br.find_link(text_regex=x))
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
            x = {'class': 'jobDisplayShell'}
            d = s.find('div', attrs=x)

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return CaciJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
