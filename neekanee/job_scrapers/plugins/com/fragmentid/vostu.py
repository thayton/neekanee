import re, urlparse, json

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Vostu',
    'hq': 'Buenos Aires, Argentina',

    'home_page_url': 'http://www.vostu.com',
    'jobs_page_url': 'http://company.vostu.com/en/jobs/',

    'empcnt': [201,500]
}

class VostuJobScraper(JobScraper):
    def __init__(self):
        super(VostuJobScraper, self).__init__(COMPANY, return_usa_only=False)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        d = s.find('div', id='wrap')

        r1 = re.compile(r'^#\d+-\S+')
        r2 = re.compile(r'^\d+$')

        x = {'href': r1, 'id': r2}

        for a in d.findAll('a', attrs=x):
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
            fragid = urlparse.urlparse(job.url).fragment
            job_id = fragid.split('-')[0]

            self.br.open(job.url, data='job_id=%d' % int(job_id))

            j = self.br.response().read()
            d = json.loads(j)
            s = soupify(d['content'])
            l = self.parse_location(d['location'])

            if not l:
                continue

            job.location = l
            job.desc = get_all_text(s)
            job.save()

def get_scraper():
    return VostuJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
