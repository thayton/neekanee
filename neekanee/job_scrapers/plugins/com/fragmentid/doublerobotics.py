import re, urlparse
from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify

from neekanee_solr.models import *

COMPANY = {
    'name': 'Double Robotics',
    'hq': 'Sunnyvale, CA',

    'home_page_url': 'http://www.doublerobotics.com',
    'jobs_page_url': 'http://www.doublerobotics.com/jobs.html',

    'empcnt': [11,50]
}

class DoubleRoboticsJobScraper(JobScraper):
    def __init__(self):
        super(DoubleRoboticsJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        x = {'role': 'main'}
        d = s.find('div', attrs=x)
        x = {'class': 'section'}
        d = d.find('div', attrs=x)
        r = re.compile(r'^#\S+')
        d.extract()

        self.company.job_set.all().delete()

        for a in d.findAll('a', href=r):
            job = Job(company=self.company)
            job.title = a.text
            job.url = urlparse.urljoin(self.br.geturl(), a['href'])
            job.location = self.company.location
            job.desc = ''

            x = d.find('a', attrs={'name' : a['href'][1:]})
            x = x.findNext('h4').next

            while x:
                name = getattr(x, 'name', None)
                if name == 'h4':
                    break
                elif name is None:
                    job.desc += x
                x = x.next

            job.save()

def get_scraper():
    return DoubleRoboticsJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
