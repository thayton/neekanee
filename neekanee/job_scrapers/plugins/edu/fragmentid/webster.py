import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify

from neekanee_solr.models import *

COMPANY = {
    'name': 'Webster University',
    'hq': 'St. Louis, MO',

    'home_page_url': 'http://www.webster.edu',
    'jobs_page_url': 'http://webster.edu/human-resources/job-opportunities.html',

    'empcnt': [1001,5000]
}

class WebsterJobScraper(JobScraper):
    def __init__(self):
        super(WebsterJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        x = {'class': 'schedule'}
        r = re.compile(r'^#')
        m = self.parse_location('St. Louis, MO')

        self.company.job_set.all().delete()

        for t in s.findAll('table', attrs=x):
            h = t.findAll('th')
            y = [h.index(x) for x in h if re.search(r'Location', x.text, re.I)]
            f = lambda y,td: len(y) == 0 and m or self.parse_location(td[y[0]].text)

            for a in t.findAll('a', href=r):
                tr = a.findParent('tr')
                td = tr.findAll('td')

                job = Job(company=self.company)
                job.title = a.text
                job.url = urlparse.urljoin(self.br.geturl(), a['href'])
                job.location = f(y,td)
                job.desc = ''

                x = s.find(attrs={'name' : a['href'][1:]})
                x = x.next

                while x and getattr(x, 'name', None) != 'hr':
                    if hasattr(x, 'name') is False: 
                        job.desc += x
                    x = x.next

                job.save()
                break

def get_scraper():
    return WebsterJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
