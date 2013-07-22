import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text, get_mailto

from neekanee_solr.models import *

COMPANY = {
    'name': 'OwnLocal',
    'hq': 'Pflugerville, TX',

    'benefits': {'vacation': []},

    'home_page_url': 'http://ownlocal.com',
    'jobs_page_url': 'http://ownlocal.com/company/jobs/',

    'empcnt': [1,10]
}

class OwnLocalJobScraper(JobScraper):
    def __init__(self):
        super(OwnLocalJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        d = s.find('div', id='subnav')
        r = re.compile(r'^#')
        v = {'class': 'left'}

        self.company.job_set.all().delete()

        for li in d.ul.findAll('li', attrs=v):
            title = li.a.text.lower().strip()
            if title.startswith('recruiters'):
                continue

            job = Job(company=self.company)
            job.title = li.a.text
            job.url = urlparse.urljoin(self.br.geturl(), li.a['href'])
            job.location = self.company.location

            x = s.find('div', id=li.a['href'][1:])
            x.extract()

            job.desc = get_all_text(x)
            job.save()


def get_scraper():
    return OwnLocalJobScraper()
