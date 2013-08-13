import re, urlparse
from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Mandiant',
    'hq': 'Alexandria, VA',

    'home_page_url': 'https://www.mandiant.com',
    'jobs_page_url': 'https://www.mandiant.com/company/careers/',

    'empcnt': [11,50]
}

class MandiantJobScraper(JobScraper):
    def __init__(self):
        super(MandiantJobScraper, self).__init__(COMPANY)
        self.br.addheaders = [('User-agent', 
                               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.63 Safari/535.7')]

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        r = re.compile(r'^job-')
        z = {'class': 'job-loc'}
        x = {'id': r, 'data-target': re.compile(r'^job-\d+$')} 
        y = s.find('aside', id='job-locations')

        self.company.job_set.all().delete()

        for a in y.findAll('a', attrs=x):
            t = a['data-target']
            d = s.find('div', id=t)
            p = d.find('p', attrs=z)
            l = self.parse_location(p.text)

            if not l:
                continue

            b = os.path.dirname(a['href'])
            p = os.path.basename(b)
            b = os.path.dirname(b)

            job = Job(company=self.company)
            job.title = a.text
            job.url = urlparse.urljoin(self.br.geturl(), b + '/#' + p)
            job.location = l
            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return MandiantJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
