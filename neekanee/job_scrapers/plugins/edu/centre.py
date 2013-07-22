import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Centre College',
    'hq': 'Danville, KY',

    'home_page_url': 'http://www.centre.edu',
    'jobs_page_url': 'http://www.centre.edu/human_resources/jobs.html',

    'empcnt': [201,500]
}

class CentreJobScraper(JobScraper):
    def __init__(self):
        super(CentreJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        r = re.compile(r'window\.open\(\'(http://www\.mycareernetwork\.com/clientResumeMgr/\?cid=\d+&first=true)\'')
        a = s.find('a', attrs={'onclick': r})
        m = re.search(r, a['onclick'])

        self.br.open(m.group(1))

        s = soupify(self.br.response().read())
        r = re.compile(r'JobSearchDetails\.aspx\?JobID=\d+')

        for a in s.findAll('a', href=r):
            job = Job(company=self.company)
            job.title = a.text
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
            d = s.find('div', id='content')
            x = {'class': 'JobDetailsJobTitle'}
            p = d.findAll('span', attrs=x)
            l = self.parse_location(p[-2].text)
            
            if not l:
                continue

            job.location = l
            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return CentreJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
