import re, urlparse, mechanize, urlutil

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Airvana Network Solutions',
    'hq': 'Chelmsford, MA',

    'ats': 'Taleo',

    'contact': 'recruiter@airvananetworksolutions.com',

    'home_page_url': 'http://www.airvananetworksolutions.com',
    'jobs_page_url': 'http://tbe.taleo.net/NA4/ats/careers/jobSearch.jsp?org=AIRVANA&cws=6',

    'empcnt': [501,1000]
}

# Like siteworx, akimeka, camber
# ATS = Taleo 
class AirvanaNetworkSolutionsJobScraper(JobScraper):
    def __init__(self):
        super(AirvanaNetworkSolutionsJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        #
        # soupify() to remove <script> tags since their
        # HTML is broken and makes mechanize choke
        #
        s = soupify(self.br.response().read()) 
        response = mechanize.make_response(s.prettify(),
                                           [("Content-Type", "text/html")],
                                           self.br.geturl(), 200, "OK")
        self.br.set_response(response)
        self.br.select_form('TBE_theForm')
        self.br.submit()

        s = soupify(self.br.response().read())
        r = re.compile(r'requisition\.jsp\?')

        for a in s.findAll('a', href=r):
            tr = a.findParent('tr')
            td = tr.findAll('td')

            l = self.parse_location(td[2].text)
            if l is None:
                continue

            job = Job(company=self.company)
            job.title = a.text
            job.url = urlparse.urljoin(self.br.geturl(), a['href'])
            job.url = urlutil.url_params_del(job.url)
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
            t = s.find('div', id='taleoContent')
            t = t.table

            job.desc = get_all_text(t)
            job.save()

def get_scraper():
    return AirvanaNetworkSolutionsJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
