import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text, get_mailto

from neekanee_solr.models import *

COMPANY = {
    'name': 'NetSuite',
    'hq': 'San Mateo, CA',

    'contact': 'careers@netsuite.com',

    'home_page_url': 'http://www.netsuite.com',
    'jobs_page_url': 'http://www.netsuite.com/portal/career/openings.shtml',

    'empcnt': [1001,5000]
}

class NetSuiteJobScraper(JobScraper):
    def __init__(self):
        super(NetSuiteJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        d = s.find('div', attrs={'class': 'content '})
        r = re.compile(r'^/portal/career/openings-[a-z]{2}\.shtml')
        x = re.compile(r'^/portal/common/career/\S+\.shtml$')

        for a in d.findAll('a', href=r):
            country = a.text
            u = urlparse.urljoin(self.br.geturl(), a['href'])

            self.br.open(u)

            z = soupify(self.br.response().read())
            v = z.find('div', attrs={'class': 'content '})

            for a in v.findAll('a', href=x):
                l = a.findAllNext(text=True, limit=2)
                if len(l) != 2:
                    continue

                m = re.search(r'\((.*)\)', l[1])
                if m is None:
                    continue

                l = m.group(1)
                l = l.split('/', 1)[0] + ', ' + country
                l = self.parse_location(l)
        
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
            try:
                self.br.open(job.url)
            except:
                continue

            s = soupify(self.br.response().read())
            d = s.find('div', id='contentcontainer')

            if not d:
                continue

            x = {'class': 'content '}
            d = d.find('div', attrs=x)

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return NetSuiteJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
