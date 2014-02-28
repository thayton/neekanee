import re, urlparse, mechanize

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text
from django.utils.encoding import smart_str, smart_unicode

from neekanee_solr.models import *


COMPANY = {
    'name': 'Intuit',
    'hq': 'Mountain View, CA',

    'home_page_url': 'http://www.intuit.com',
    'jobs_page_url': 'http://jobs.intuit.com/searches.aspx?keyword=advanced+search&jobtitlekeyword=filter%20by%20job%20title&locationkeyword=filter%20by%20job%20location&dateKeyword=&categoryKeyword=&issearchpaging=True&isdate=True&pagenumber=',

    'empcnt': [5001, 10000]
}

class IntuitJobScraper(JobScraper):
    def __init__(self):
        super(IntuitJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        pageno = 1
        u = url + '%d' % pageno
        pageno += 1

        self.br.open(u)
        
        while True:
            s = soupify(self.br.response().read())
            r = re.compile(r'^search_result_link_\d+$')

            for a in s.findAll('a', id=r):
                tr = a.findParent('tr')
                td = tr.findAll('td')

                if len(td[1].text.strip()) == 0:
                    continue

                l = self.parse_location(td[1].text)
                if not l:
                    continue

                job = Job(company=self.company)
                job.title = a.text
                job.url = urlparse.urljoin(self.br.geturl(), a['href'])
                job.location = l
                jobs.append(job)
                
            f = lambda x: x.name == 'a' and x.text == '%d' % pageno
            a = s.find(f)

            if not a:
                break

            u = url + '%d' % pageno
            pageno += 1

            self.br.open(u)

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            x = {'class': 'jobDesc'}
            d = s.find('div', attrs=x)
            
            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return IntuitJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
