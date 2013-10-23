import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Westrich Pacific',
    'hq': 'Edmonton, Canada',

    'home_page_url': 'http://www.westrichpacific.com',
    'jobs_page_url': 'http://www.westrichpacific.com/index.php?/component/option,com_jobline/Itemid,15/',

    'empcnt': [11,50]
}

class WestrichPacificJobScraper(JobScraper):
    def __init__(self):
        super(WestrichPacificJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        x = {'class': 'jobtitle'}
        
        for td in s.findAll('td', attrs=x):
            job = Job(company=self.company)
            job.title = td.text
            job.url = urlparse.urljoin(self.br.geturl(), td.a['href'])
            job.location = self.company.location
            jobs.append(job)

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            d = s.find('div', id='jobline')
            t = s.find(text='Location')
            tr = t.findParent('tr')
            td = tr.findAll('td')

            l = self.parse_location(td[-1].text)
            if not l:
                continue

            job.location = l
            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return WestrichPacificJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
