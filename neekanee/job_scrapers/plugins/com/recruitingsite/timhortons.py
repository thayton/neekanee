import re, urlparse, mechanize

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Tim Hortons',
    'hq': 'Oakville, ON',

    'home_page_url': 'http://www.timhortons.com',
    'jobs_page_url': 'http://www.recruitingsite.com/csbsites/timhortons/english/Search.asp',

    'empcnt': [1001,5000]
}

class TimHortonsJobScraper(JobScraper):
    def __init__(self):
        super(TimHortonsJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)
        self.br.select_form('search')
        self.br.submit()

        pageno = 2

        while True:
            s = soupify(self.br.response().read())
            r = re.compile(r'^JobDescription\.asp\?JobNumber=\d+$')
        
            for a in s.findAll('a', href=r):
                tr = a.findParent('tr')
                td = tr.findAll('td')
            
                l = self.parse_location(td[-2].text)
                if not l:
                    continue

                job = Job(company=self.company)
                job.title = a.text
                job.url = urlparse.urljoin(self.br.geturl(), a['href'])
                job.location = l
                jobs.append(job)

            f = lambda x: x.name == 'a' and x.text == 'Next'
            a = s.find(f)

            if not a:
                break

            self.br.select_form('main')
            self.br.form.set_all_readonly(False)
            self.br.form['StartPage'] = '%d' % pageno
            self.br.form['SortOrder'] = '-1'
            self.br.submit()

            pageno += 1

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            d = s.find('div', id='realLunchBreak')

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return TimHortonsJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
