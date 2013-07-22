import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text, get_mailto

from neekanee_solr.models import *

COMPANY = {
    'name': 'Apps Associates',
    'hq': 'Westford, MA',

    'home_page_url': 'http://www.appsassociates.com',
    'jobs_page_url': 'http://www.appsassociates.com/careers.php',

    'empcnt': [201,500]
}

class AppsAssociatesJobScraper(JobScraper):
    def __init__(self):
        super(AppsAssociatesJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        l = {
            'usa': self.parse_location('Acton, MA'),
            'germany': self.parse_location('Dortmund, Germany'),
            'netherlands': self.parse_location('Eindhoven, Netherlands'),
            'india': self.parse_location('Hyderabad, India')
        }

        s = soupify(self.br.response().read())
        r = re.compile(r'^careers-([^.]+)\.php$')

        self.company.job_set.all().delete()

        for a in s.findAll('a', href=r):
            m = re.search(r, a['href'])
            if not l.has_key(m.group(1)):
                continue

            l = self.parse_location(l[m.group(1)])
            if not l:
                continue

            u = urlparse.urljoin(self.br.geturl(), a['href'])
            self.br.open(u)

            z = soupify(self.br.response().read())
            d = z.find('div', id='accordion')

            for h in d.findAll('h3'):
                v = h.findNextSibling('div')
                job = Job(company=self.company)
                job.title = h.text
                job.url = self.br.geturl()
                job.desc = get_all_text(v)
                job.location = l
                job.save()

def get_scraper():
    return AppsAssociatesJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
