import re, urlparse, mechanize

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text
from neekanee.urlutil import url_query_filter, url_query_get

from neekanee_solr.models import *

COMPANY = {
    'name': 'Inditex',
    'hq': 'Arteixo, Spain',

    'home_page_url': 'http://www.inditex.com',
    'jobs_page_url': 'http://www.joinfashioninditex.com/joinfashion/en/vacancy-search',

    'empcnt': [10001]
}

class InditexJobScraper(JobScraper):
    def __init__(self):
        super(InditexJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        pageno = 2

        self.company.job_set.all().delete()

        while True:
            s = soupify(self.br.response().read())
            x = {'class': 'main'}
            d = s.find('div', attrs=x)
            r = re.compile(r'^/joinfashion/en/retail-offer\?id=\d+')
    
            for a in d.findAll('a', href=r):
                l = a.contents[-1].strip()
                l = self.parse_location(l)
    
                if not l:
                    continue
    
                job = Job(company=self.company)
                job.title = a.contents[0]
                job.url = urlparse.urljoin(self.br.geturl(), a['href'])
                job.url = url_query_filter(job.url, 'id')
                job.location = l
                jobs.append(job)

            ul = s.find('ul', attrs={'class': 'pages '})
            t = ul.find('a', text='%d' % pageno)

            if not t:
                break

            a = t.parent
            u = urlparse.urljoin(self.br.geturl(), a['href'])

            self.br.open(u)

            pageno += 1

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            id = url_query_get(job.url, 'id')['id']
            r = re.compile(r'/vacancies/view/%d' % int(id))

            self.br.open(job.url)
            self.br.follow_link(self.br.find_link(url_regex=r))

            s = soupify(self.br.response().read())
            d = s.find('div', id='main')

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return InditexJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
