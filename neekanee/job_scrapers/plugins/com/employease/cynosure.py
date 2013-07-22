import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Cynosure',
    'hq': 'Westford, MA',

    'home_page_url': 'http://www.cynosure.com',
    'jobs_page_url': 'http://www.cynosure.com/about-us/careers.php',
    'jobs_page_domain': 'eease.com',

    'empcnt': [501,1000]
}

class BottomlineJobScraper(JobScraper):
    def __init__(self):
        super(BottomlineJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []
        job_links = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        r = re.compile(r'home.eease.com/recruit/\?id=\d+')

        for a in s.findAll('a', href=r):
            url = urlparse.urljoin(self.br.geturl(), a['href'])

            if url in job_links:
                continue
            else:
                job_links.append(url)

            h = a.findPrevious('hr')
            f = lambda x: x.name == 'strong' and re.search(r'Location', x.text)
            g = h.findNext(f)
            if not g:
                continue

            l = self.parse_location(g.nextSibling)
            if not l:
                continue

            job = Job(company=self.company)
            job.url = url
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
            f = s.find('form')
            t = f.table
            x = {'class': 'postingTitle'}
            p = f.find('span', attrs=x)

            if not p:
                continue

            job.title = p.text
            job.desc = get_all_text(t)
            job.save()

def get_scraper():
    return BottomlineJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
