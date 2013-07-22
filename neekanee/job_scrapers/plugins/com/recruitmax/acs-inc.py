import re, urlparse, mechanize

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'ACS',
    'hq': 'Columbia, MD',

    'ats': 'Taleo',
    'benefits': {'vacation': []},

    'home_page_url': 'http://www.acs-inc.com',
    'jobs_page_url': 'http://www.acs-inc.com/careeropportunities.aspx',

    'empcnt': [10001]
}

class AcsIncJobScraper(JobScraper):
    def __init__(self):
        super(AcsIncJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)
        self.br.follow_link(self.br.find_link(text='View employment opportunities'))
        self.br.select_form('txtjobsearch')
        self.br.submit()

        while True:
            s = soupify(self.br.response().read())
            for l in self.br.links(url_regex=re.compile(r'^Job_Profile.cfm\?')):
                a = s.find('a', href=l.url)
                t = a.findParent('td').findNext('td')

                if t.text.find('United States') == -1:
                    continue

                t = re.sub(r',\s*United States.*', '', t.text)
                t = self.parse_location(t)

                if not t:
                    continue

                job = Job(company=self.company)
                job.title = l.text
                job.location = t
                job.url = urlparse.urljoin(l.base_url, l.url)
                jobs.append(job)

            # Navigate to the next page
            i = s.find('img', alt='Next')
            if i is None:
                break

            a = i.parent
            l = urlparse.urljoin(l.base_url, a['href'])
            self.br.open(l)

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            t = s.find(text='Description').findParent('td')
            t = t.findNext('td')

            job.desc = get_all_text(t)
            job.save()

def get_scraper():
    return AcsIncJobScraper()
