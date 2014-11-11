import re, urlparse, mechanize, urlutil, json

from HTMLParser import HTMLParser
from BeautifulSoup import BeautifulSoup

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'BAE Systems',
    'hq': 'London, UK',

    'home_page_url': 'http://www.baesystems.com',
    'jobs_page_url': 'http://www.baesystems.jobs/search-jobs.php',

    'empcnt': [10001]
}

class BaeSystemsJobScraper(JobScraper):
    def __init__(self):
        super(BaeSystemsJobScraper, self).__init__(COMPANY)
        self.geocoder.return_usa_only = False

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = BeautifulSoup(self.br.response().read())
        r = re.compile(r'searchdata = (\[.*}]);')
        m = re.search(r, s.prettify())
        s = json.loads(m.group(1))

        for j in s:
            u = HTMLParser().unescape(j['job_url'])
            u = soupify(u)

            l = j['city'] + ', ' + j['state'] + j['country']
            l = self.parse_location(l)

            if not l:
                continue

            job = Job(company=self.company)
            job.title = j['title_advertising']
            job.url = urlparse.urljoin(self.br.geturl(), u.a['href'])
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
            x = {'class': 'job_description'}
            d = s.find('div', attrs=x)
            d = d.parent

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return BaeSystemsJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
