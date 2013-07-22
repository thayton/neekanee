import re, urlparse, urlutil

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Citizen Schools',
    'hq': 'Boston, MA',

    'ats': 'Taleo',

    'home_page_url': 'http://www.citizenschools.org',
    'jobs_page_url': 'http://tbe.taleo.net/NA6/ats/careers/jobSearch.jsp?org=CITIZENSCHOOLS&cws=2',

    'empcnt': [201,500]
}

class CitizenSchoolsJobScraper(JobScraper):
    def __init__(self):
        super(CitizenSchoolsJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)
        self.br.select_form('TBE_theForm')
        self.br.submit()

        r = re.compile(r'/ats/careers/requisition\.jsp')
        s = soupify(self.br.response().read())
        d = s.find('div', id='taleoContent')

        for a in d.findAll('a', href=r):
            job = Job(company=self.company)
            job.title = a.text
            job.url = urlparse.urljoin(self.br.geturl(), a['href'])
            job.url = urlutil.url_params_del(job.url)
            jobs.append(job)

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            d = s.find('div', id='taleoContent')
            t = d.find(text='Location:').findParent('tr')
            l = t.findAll('td')[1].text
            r = re.compile(r'&#40;(.*?)&#41;')
            m = re.search(r, l)

            if not m:
                continue

            l = self.parse_location(m.group(1))

            if not l:
                continue

            job.location = l
            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return CitizenSchoolsJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
