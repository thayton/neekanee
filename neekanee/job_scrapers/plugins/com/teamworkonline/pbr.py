import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Professional Bull Riders',
    'hq': 'Pueblo, CO',

    'home_page_url': 'http://www.pbr.com',
    'jobs_page_url': 'http://pbrnow.teamworkonline.com/teamwork/jobs/default.cfm',

    'empcnt': [51,200]
}

class PbrJobScraper(JobScraper):
    def __init__(self):
        super(PbrJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        r = re.compile(r'/jobs/jobs\.cfm/')
        x = re.compile(r'\(([^)]+)\)$')
        y = re.compile(r'^#\d+$')

        self.company.job_set.all().delete()

        for n in s.findAll('a', href=r):
            u = urlparse.urljoin(self.br.geturl(), n['href'])
            self.br.open(u)
            z = soupify(self.br.response().read())

            for a in z.findAll('a', href=y):
                m = re.search(x, a.text)
                l = self.parse_location(m.group(1))

                if not l:
                    continue

                job = Job(company=self.company)
                job.title = a.text
                job.url = urlparse.urljoin(self.br.geturl(), a['href'])
                job.location = l

                u = {'name': a['href'][1:]}
                v = z.find('a', attrs=u)
                u = {'class': re.compile(r'JobDescriptionDisplay')}
                v = v.findNext('div', attrs=u)

                job.desc = get_all_text(v)
                job.save()

            self.br.back()


def get_scraper():
    return PbrJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
