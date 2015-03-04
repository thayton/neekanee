import re, urlparse, json

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'SinnerSchrader',
    'hq': 'Hamburg, Germany',

    'home_page_url': 'http://www.sinnerschrader.com',
    'jobs_page_url': 'https://sinnerschrader.com/en/careers/',

    'empcnt': [201,500]
}

class SinnerSchraderJobScraper(JobScraper):
    def __init__(self):
        super(SinnerSchraderJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())

        r1 = re.compile(r'\bjobs--title\b')
        r2 = re.compile(r'\bjobs--location\b')

        x = {'class': r1}
        y = {'class': r2}

        for td1 in s.findAll('td', attrs=x):
            tr = td1.findParent('tr')
            td2 = tr.find('td', attrs=y)

            l = self.parse_location(td2.text)
            if not l:
                continue

            link = re.sub(r'\.', '', td1.text)
            link = '-'.join(link.lower().strip().split())

            job = Job(company=self.company)
            job.title = td1.text
            job.url = urlparse.urljoin(self.br.geturl(), '/en/job/' + link)
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
            x = {'class': 'post__main'}
            d = s.find('div', attrs=x)

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return SinnerSchraderJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
