import re, urlparse, mechanize

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text
from neekanee.urlutil import url_query_filter

from neekanee_solr.models import *

COMPANY = {
    'name': 'Cartera Commerce',
    'hq': 'Lexington, MA',

    'ats': 'Hirebridge',

    'home_page_url': 'http://www.cartera.com',
    'jobs_page_url': 'http://www.hirebridge.com/jobseeker2/Searchjobresults.asp?cid=6671',

    'empcnt': [201,500]
}

class CarteraJobScraper(JobScraper):
    def __init__(self):
        super(CarteraJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)
    
        s = soupify(self.br.response().read())
        r = re.compile(r'^viewdetail\.asp\?joblistid=\d+')

        for a in s.findAll('a', href=r):
            tr = a.findParent('tr')
            td = tr.findAll('td')

            l = self.parse_location(td[2].text)
            if not l:
                continue

            job = Job(company=self.company)
            job.title = a.text
            job.url = urlparse.urljoin(self.br.geturl(), a['href'])
            job.url = url_query_filter(job.url, ['joblistid', 'cid'])
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
            t = s.find('table', attrs={'class': 'InteriorPage'})

            job.desc = get_all_text(t)
            job.save()

def get_scraper():
    return CarteraJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
