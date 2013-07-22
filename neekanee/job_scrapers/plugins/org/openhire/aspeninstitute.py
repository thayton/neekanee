import re, urlparse, mechanize

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'The Aspen Institute',
    'hq': 'Washington, DC',

    'ats': 'OpenHire',
    'benefits': {'vacation': []},

    'home_page_url': 'http://www.aspeninstitute.org',
    'jobs_page_url': 'http://www.aspeninstitute.org/about',

    'empcnt': [51,200]
}

class AspenInstituteJobScraper(JobScraper):
    def __init__(self):
        super(AspenInstituteJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        def work_link(link):
            for k,v in link.attrs:
                if k == 'title' and v == 'Work for the Institute':
                    return True
            return False

        self.br.open(url)
        self.br.follow_link(self.br.find_link(predicate=work_link))
        self.br.follow_link(self.br.find_link(text='All Posted Jobs'))

        s = soupify(self.br.response().read())
        r = re.compile(r'^/epostings/submit\.cfm\?fuseaction=app.jobinfo&jobid=\d+')
        x = {'class': 'cssAllJobListPositionHref', 'href': r}

        for a in s.findAll('a', attrs=x):
            l = a.parent.contents[-1]
            l = re.sub(r',\s+US.*', '', l)
            l = self.parse_location(l)

            if not l:
                continue

            job = Job(company=self.company)
            job.title = a.text
            job.location = l
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
            f = s.find('form', id='applyJob')

            job.desc = get_all_text(f)
            job.save()

def get_scraper():
    return AspenInstituteJobScraper()
