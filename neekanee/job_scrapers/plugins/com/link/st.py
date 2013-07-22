import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'STMicroelectronics',
    'hq': 'Geneva, Switzerland',

    'home_page_url': 'http://www.st.com',
    'jobs_page_url': 'http://jobs.st.com/HROnline/HROnlineJobReq.nsf/JobReqAllWeb?SearchView&Query=((NOT%20[Empl_Class]=I))&JFEnd&SearchOrder=3&SearchMax=199&Count=50&Start=1',

    'empcnt': [10001]
}

class StJobScraper(JobScraper):
    def __init__(self):
        super(StJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        x = self.br.response().read()
        t = x.find('document openJob('
        r = re.compile(r"openJob\('([A-Z0-9]+)'\)")

        for a in s.findAll('a', href=r):
            tr = a.findParent('tr')
            td = tr.findAll('td')

            l = td[3].text + ', ' + td[2].text
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
            x = {'class': 'miscpage jobs'}
            a = s.find('article', attrs=x)
            d = a.findParent('div')

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return StJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
