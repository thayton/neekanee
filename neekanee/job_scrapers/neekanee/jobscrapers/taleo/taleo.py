import re, urlparse, urlutil

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

class TaleoJobScraper(JobScraper):
    def __init__(self, company_dict):
        super(TaleoJobScraper, self).__init__(company_dict)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)
        self.br.select_form('TBE_theForm')
        self.br.submit()

        s = soupify(self.br.response().read())
        r = re.compile(r'requisition\.jsp(;jsessionid=[^?]+)?\?')

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

            if hasattr(self, 'get_location_from_s'):
                job.location = self.get_location_from_s(s)
                if not job.location:
                    continue

            if hasattr(self, 'get_desc_from_s'):
                job.desc = self.get_desc_from_s(s)
            else:
                t = s.find('div', id='taleoContent')
                if t:
                    t = t.table
                else:
                    x = {'role': 'presentation'}
                    t = s.find('table', attrs=x)

                job.desc = get_all_text(t)

            job.save()
