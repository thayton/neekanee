import re, time, urlparse, mechanize

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

class IcimsJobScraper(JobScraper):
    def __init__(self, company_dict):
        super(IcimsJobScraper, self).__init__(company_dict)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)
        self.br.select_form('searchForm')
        self.br.submit()

        pageno = 1 # page numbers start at 0

        z = re.compile(r'iCIMS_JobListingRow')
        x = {'class': z}
        y = {'itemprop': 'address'}

        while True:
            s = soupify(self.br.response().read())

            for d in s.findAll('div', attrs=x):
                p = d.find('span', attrs=y)
                l = self.parse_location(p.text)

                if not l:
                    continue

                job = Job(company=self.company)
                job.title = d.a.text
                job.url = urlparse.urljoin(self.br.geturl(), d.a['href'])
                jobs.append(job)

            # Navigate to the next page
            try:
                r = re.compile(r'/jobs/search\?pr=' + str(pageno))
                pageno += 1
                self.br.follow_link(self.br.find_link(url_regex=r))
            except mechanize.LinkNotFoundError:
                break

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            r = re.compile(r'iCIMS_JobPage')
            x = {'class': r}
            d = s.find('div', attrs=x)

            job.desc = get_all_text(d)
            job.save()
