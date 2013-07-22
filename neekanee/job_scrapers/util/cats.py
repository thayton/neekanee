import re, urlparse

from jobscraper import JobScraper
from location import parse_location
from soupify import soupify, get_all_text

from neekanee_solr.models import *

class CatsJobScraper(JobScraper):
    def __init__(self, company_dict):
        company_dict['ats'] = 'CATS'
        super(CatsJobScraper, self).__init__(company_dict)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        r = re.compile(r'/careers/index\.php\?m=portal&a=details&jobOrderID=\d+')

        for a in s.findAll('a', href=r):
            t = a.findNext('td').text
            l = self.parse_location(t)

            if l is None:
                continue

            job = Job(company=self.company)
            job.title = a.text
            job.url = urlparse.urljoin(self.br.geturl(), a['href'])
            job.location = l
            jobs.append(job)

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            x = {'class': 'detailsJobDescription'}
            d = s.find('div', attrs=x)

            job.desc = get_all_text(d)
            job.save()
