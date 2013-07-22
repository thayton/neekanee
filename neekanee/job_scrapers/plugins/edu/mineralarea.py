import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Mineral Area College ',
    'hq': 'Park Hills, MO',

    'benefits': {'vacation': []},

    'home_page_url': 'http://www.mineralarea.edu',
    'jobs_page_url': 'http://www.mineralarea.edu/employmentOpportunities/',

    'gctw_chronicle': True,

    'empcnt': [201,500]
}

class MineralAreaJobScraper(JobScraper):
    def __init__(self):
        super(MineralAreaJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        r = re.compile(r'EmploymentDetails\.aspx\?EmploymentID=\d+')

        links = [ 'mineralAreaCollegeEmployment.aspx',
                  'graduateEmployment.aspx',
                  'studentEmployment.aspx']
              
        for l in links:
            self.br.open(urlparse.urljoin(url, l))
            s = soupify(self.br.response().read())

            for a in s.findAll('a', href=r):
                job = Job(company=self.company)
                job.title = a.text
                job.url = urlparse.urljoin(self.br.geturl(), a['href'])
                jobs.append(job)

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            t = s.find('table', id='Table2')
            l = t.find(text='Location:').findNext('span')
            l = self.parse_location(l.text + ', MO')

            if not l:
                continue

            job.location = l
            job.desc = get_all_text(t)
            job.save()

def get_scraper():
    return MineralAreaJobScraper()
