import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text, get_mailto

from neekanee_solr.models import *

COMPANY = {
    'name': 'AcademicWorks',
    'hq': 'Austin, TX',

    'home_page_url': 'http://www.academicworks.com',
    'jobs_page_url': 'http://www.academicworks.com/company/careers/',

    'empcnt': [1,10]
}

class AcademicWorksJobScraper(JobScraper):
    def __init__(self):
        super(AcademicWorksJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())

        x = {'class': 'tab-title-wrapper'}
        d = s.find('div', attrs=x)

        x = {'class': re.compile(r'tab-content-wrapper')}
        w = s.find('div', attrs=x)

        x = {'class': re.compile(r'tab-title')}
        y = {'class': re.compile(r'tab-content')}

        self.company.job_set.all().delete()

        for h4 in d.findAll('h4', attrs=x):
            i = d.index(h4)
            tab_content_list = w.findAll('div', attrs=y)
            tab_content = tab_content_list[i]

            job = Job(company=self.company)
            job.title = h4.text
            job.url = self.br.geturl()
            job.location = self.company.location
            job.desc = get_all_text(tab_content)
            job.save()

def get_scraper():
    return AcademicWorksJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
