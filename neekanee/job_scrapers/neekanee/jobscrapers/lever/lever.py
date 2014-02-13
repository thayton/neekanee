import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

class LeverJobScraper(JobScraper):
    def __init__(self, company_dict):
        super(LeverJobScraper, self).__init__(company_dict)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        x = {'class': 'posting-title'}
        y = {'class': re.compile(r'sort-by-location')}

        for a in s.findAll('a', attrs=x):
            p = a.parent.find('span', attrs=y)
            if not p:
                continue

            l = self.parse_location(p.text)
            if not l:
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
            x = {'class': 'content'}
            d = s.find('div', attrs=x)

            job.desc = get_all_text(d)
            job.save()
