import re, urlparse, mechanize

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'iDirect',
    'hq': 'Herndon, VA',

    'ats': 'submit4jobs',

    'home_page_url': 'http://www.idirect.net',
    'jobs_page_url': 'http://idirect.submit4jobs.com',

    'empcnt': [201,500]
}

class iDirectJobScraper(JobScraper):
    def __init__(self):
        super(iDirectJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        r = re.compile(r'^index\.cfm\?fuseaction=\d+\.viewjobdetail')
        x = {'class': 'joblink', 'href': r}
        
        s = soupify(self.br.response().read())

        for a in s.findAll('a', attrs=x):
            tr = a.findParent('tr')
            td = tr.findAll('td')

            l = self.parse_location(td[-2].text)
            if l is None:
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
            x = {'name': 'applyonline'}
            f = s.find('form', attrs=x)

            job.desc = get_all_text(f)
            job.save()

def get_scraper():
    return iDirectJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
