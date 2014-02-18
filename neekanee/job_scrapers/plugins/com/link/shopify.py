import re, urlparse, json

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text
from neekanee.urlutil import url_query_get

from neekanee_solr.models import *

COMPANY = {
    'name': 'Shopify',
    'hq': 'Ottawa, Canada',

    'home_page_url': 'http://www.shopify.com',
    'jobs_page_url': 'http://recruiting2.shopify.com/postings.js',

    'empcnt': [201,500]
}

class ShopifyJobScraper(JobScraper):
    def __init__(self):
        super(ShopifyJobScraper, self).__init__(COMPANY)
         
    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        d = self.br.response()
        j = json.loads(d.read())
        s = soupify(j['content'])
        x = {'class': 'job-list'}
        r = re.compile(r'\?posting=')

        for u in s.findAll('ul', attrs=x):
            for a in u.findAll('a', href=r):
                if not a.em:
                    continue

                l = self.parse_location(a.em.text)
                if not l:
                    continue

                p = url_query_get(a['href'], 'posting')
                u = urlparse.urljoin(self.br.geturl(), '/postings/' + p['posting'] + '.js')

                job = Job(company=self.company)
                job.title = a.contents[0]
                job.url = u
                job.location = l
                jobs.append(job)

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            
            d = self.br.response()
            j = json.loads(d.read())
            s = soupify(j['content'])
            d = s.find('div', id='application')
            d.extract()

            # change the URL so that when the user clicks on the link
            # they don't get the json version
            u = urlparse.urlparse(job.url)
            b = os.path.basename(u.path)
            i = b.split('.')[0]

            b = self.company.home_page_url
            u = b + '/careers?posting=' + i

            job.url = u
            job.desc = get_all_text(s)
            job.save()

def get_scraper():
    return ShopifyJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
