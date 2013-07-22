import re, urlparse, mechanize

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'American Express',
    'hq': 'New York, NY',

    'home_page_url': 'http://www.americanexpress.com',
    'jobs_page_url': 'http://jobs.americanexpress.com/group/?inav=SearchJobs',

    'empcnt': [10001]
}

class AmericanExpressJobScraper(JobScraper):
    def __init__(self):
        super(AmericanExpressJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        def select_form(form):
            return form.attrs.get('id', None) == 'search-form'

        self.br.open(url)
        self.br.select_form(predicate=select_form)
        self.br.submit()

        r = re.compile(r'^/job/[\w-]+/\d+/')

        pageno = 2

        while True:
            s = soupify(self.br.response().read())

            for a in s.findAll('a', href=r):
                tr = a.findParent('tr')
                td = tr.findAll('td')

                l = self.parse_location(td[1].text)
                
                if l is None:
                    l = self.company.location

                job = Job(company=self.company)
                job.title = a.text
                job.url = urlparse.urljoin(self.br.geturl(), a['href'])
                job.location = l
                jobs.append(job)

            # Navigate to the next page
            try:
                p = r'Page ' + str(pageno) + ' \(\d+ -'
                pageno += 1
                a = s.find('a', attrs={'title': re.compile(p)})
                if a is None:
                    break
                n = self.br.find_link(url=a['href'])
                self.br.follow_link(n)
            except mechanize.LinkNotFoundError:
                break
        
        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            a = {'class': 'jobDisplay'}
            d = s.find('div', attrs=a)

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return AmericanExpressJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
    print job_scraper.serialize()
