import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Partners in Health',
    'hq': 'Boston, MA',

    'ats': 'Taleo',

    'home_page_url': 'http://www.pih.org',
    'jobs_page_url': 'http://tbe.taleo.net/NA1/ats/careers/jobSearch.jsp?org=PIH&cws=1',

    'empcnt': [51,200]
}

class PihJobScraper(JobScraper):
    def __init__(self):
        super(PihJobScraper, self).__init__(COMPANY)
        self.geocoder.return_usa_only = False

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)
        self.br.select_form('TBE_theForm')
        self.br.submit()

        s = soupify(self.br.response().read())
        d = s.find('div', id='content')
        r = re.compile(r'/ats/careers/requisition\.jsp\?org=PIH')

        for a in d.findAll('a', href=r):
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
            d = s.find('div', id='content')
            r = re.compile(r'Location:')
            t = d.findAll(text=r)

            if len(t) > 1:
                if t[1].parent.name == 'strong':
                    l = t[1].findNext(text=True)
                else:
                    l = d.findAll(text=r)[1].parent.contents[-1]
            else:
                l = t[0].split('Location:')[1]

            l = self.parse_location(l)
            
            if l is None:
                continue

            job.location = l
            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return PihJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
