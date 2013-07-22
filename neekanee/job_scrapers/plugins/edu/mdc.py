import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Miami Dade College',
    'hq': 'Miami, FL',

    'home_page_url': 'http://www.mdc.edu',
    'jobs_page_url': 'https://wape.mdc.edu/MDCJobPositions/',

    'empcnt': [5001,10000]
}

class MdcJobScraper(JobScraper):
    def __init__(self):
        super(MdcJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)
        self.br.select_form('JobBrowser')

        ctl = self.br.form.find_control('PositionType')

        self.company.job_set.all().delete()

        for position_type in ctl.items[1:]:
            self.br.select_form('JobBrowser')
            self.br.form['PositionType'] = [position_type.name]
            self.br.submit('SearchBtn')

            s = soupify(self.br.response().read())
            t = s.find('table', id='PositionsList')

            r1 = re.compile(r'PostingDetails\d+_PositionTitle')
            r2 = re.compile(r'PostingDetails\d+_JobPostingDetails')
            r3 = re.compile(r'PostingDetails\d+_PositionID')

            for p in t.findAll('span', id=r1):
                d = p.findNext('table', id=r2)
                i = d.find('span', id=r3)

                job = Job(company=self.company)
                job.title = p.text
                job.url = urlparse.urljoin(self.br.geturl(), '?PositionIDList=%s' % i.text)
                job.location = self.company.location
                job.desc = get_all_text(d)
                job.save()

            self.br.back()

def get_scraper():
    return MdcJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
