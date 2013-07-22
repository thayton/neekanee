import re, urlparse
from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify

from neekanee_solr.models import *

COMPANY = {
    'name': 'LabKey Software',
    'hq': 'Seattle, WA',

    'home_page_url': 'http://www.labkey.com',
    'jobs_page_url': 'http://www.labkey.com/company/careers',

    'empcnt': [11,50]
}

class LabKeyJobScraper(JobScraper):
    def __init__(self):
        super(LabKeyJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        r = re.compile(r'^/company/careers#')

        self.company.job_set.all().delete()

        for a in s.findAll('a', href=r):
            l = a.text.rsplit(',', 1)
            l = self.parse_location(l[1])

            if not l:
                continue

            job = Job(company=self.company)
            job.title = a.text
            job.url = urlparse.urljoin(self.br.geturl(), a['href'])
            job.location = l
            job.desc = ''

            i = a['href'].find('#')
            x = {'name' : a['href'][i+1:]}
            x = s.find('a', attrs=x)
            x = x.next

            while x:
                name = getattr(x, 'name', None)
                if name == 'hr':
                    break
                elif name is None:
                    job.desc += x
                x = x.next

            job.save()

def get_scraper():
    return LabKeyJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
