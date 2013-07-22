import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'VolunteerMatch',
    'hq': 'San Francisco, CA',

    'home_page_url': 'http://www.volunteermatch.com',
    'jobs_page_url': 'http://www.volunteermatch.org/careers/index.jsp',

    'empcnt': [11,50]
}

class VolunteerMatchJobScraper(JobScraper):
    def __init__(self):
        super(VolunteerMatchJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        r = re.compile(r'^#')
        x = {'class': 'read_more', 'href': r}
        d = s.find('div', id='maininfo')
        d.extract()

        self.company.job_set.all().delete()

        for a in s.findAll('a', attrs=x):
            job = Job(company=self.company)
            job.title = a.text
            job.url = urlparse.urljoin(self.br.geturl(), a['href'])
            job.location = self.company.location

            x = d.find(attrs={'name' : a['href'][1:]})
            v = x.findNext('div', attrs={'class': 'subitem'})

            if len(v.text.strip()) == 0:
                continue

            job.desc = get_all_text(v)
            job.save()

def get_scraper():
    return VolunteerMatchJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
