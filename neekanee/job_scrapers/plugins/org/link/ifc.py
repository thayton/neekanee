import re, urlparse, urllib

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'International Finance Corporation',
    'hq': 'Washington, DC',

    'home_page_url': 'http://www.ifc.org',
    'jobs_page_url': 'http://www1.ifc.org/wps/wcm/connect/careers_ext_content/ifc_external_corporate_site/ifc+careers/career+opportunities',

    'empcnt': [1001,5000]
}

class IfcJobScraper(JobScraper):
    def __init__(self):
        super(IfcJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        d = s.find('div', id='CareerOpportunities')
        s = soupify(d.textarea.text)

        # From the JavaScript source
        u = '/wps/wcm/connect/Careers_Ext_Content/IFC_External_Corporate_Site/IFC Careers/Career Opportunities/CareerOpportunityPlaceHolder?JobReqNo='
        u = urlparse.urljoin(self.br.geturl(), u)

        for j in s.findAll('jobs'):
            l = self.parse_location(j.find('descr200').text)
            if not l:
                continue

            job = Job(company=self.company)
            job.title = j.find('posting-title').text
            job.url = urllib.quote(u + j.find('job-req-num').text, '/:?=')
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
            d = s.find('div', id='CareerOpportunities')
            d = soupify(d.textarea.text)

            job.desc = get_all_text(d.find('job-details'))
            job.save()

def get_scraper():
    return IfcJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
