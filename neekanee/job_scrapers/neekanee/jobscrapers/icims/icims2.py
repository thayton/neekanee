import re, time, urlparse, mechanize

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

class IcimsJobScraper(JobScraper):
    def __init__(self, company_dict):
        super(IcimsJobScraper, self).__init__(company_dict)
        self.use_company_location = False

    def scrape_job_links(self, urls):
        jobs = []

        if not isinstance(urls, list):
            urls = [ urls ]

        for url in urls:
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
                    l = None

                    if self.use_company_location:
                        l = self.company.location
                    elif hasattr(self, 'get_location_from_div'):
                        l = self.get_location_from_div(d)
                    elif p and len(p.text.strip()) == 0:
                        p = p.meta['content']
                        l = self.parse_location(p)
                    elif p:
                        l = self.parse_location(p.text)
                    
                    if not l and not hasattr(self, 'get_location_from_desc'):
                        continue

                    job = Job(company=self.company)
                    job.title = d.a.text
                    job.url = urlparse.urljoin(self.br.geturl(), d.a['href'])

                    if l:
                        job.location = l

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

            if hasattr(self, 'get_location_from_desc'):
                l = self.get_location_from_desc(d)
                if not l:
                    continue
                job.location = l

            job.desc = get_all_text(d)
            job.save()
