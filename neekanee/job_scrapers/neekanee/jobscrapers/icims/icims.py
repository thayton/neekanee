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

        pageno = 2
        r = re.compile(r'jobs/\d+/([^/]+/)?job')

        while True:
            s = soupify(self.br.response().read())

            for a in s.findAll('a', href=r):
                tr = a.findParent('tr')
                td = tr.findAll('td')

                job = Job(company=self.company)
                job.location = self.company.location

                if hasattr(self, 'get_title_from_td'):
                    job.title = self.get_title_from_td(td)
                else:
                    job.title = a.text

                if hasattr(self, 'get_location_from_td'):
                    y = self.get_location_from_td(td)
                    if y is None:
                        continue

                    job.location = y

                job.url = urlparse.urljoin(self.br.geturl(), a['href'])
                jobs.append(job)

            # Navigate to the next page
            try:
                x = re.compile(r'/jobs/search\?pr=' + str(pageno))
                pageno += 1
                self.br.follow_link(self.br.find_link(url_regex=x))
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
            x = {'class': 'iCIMS_MainTable iCIMS_JobPage'}
            t = s.find('table', attrs=x)

            job.desc = get_all_text(t)
            job.save()
