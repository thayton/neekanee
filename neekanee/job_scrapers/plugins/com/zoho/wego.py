import re, urlparse, mechanize

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text
from neekanee.urlutil import url_query_add, url_set_path

from neekanee_solr.models import *

COMPANY = {
    'name': 'Wego.com',
    'hq': 'Singapore, Singapore',

    'home_page_url': 'http://www.wego.com',
    'jobs_page_url': 'https://recruit.zoho.com/ats/Portal.na?digest=XjGeD*20vV5dni33tNU8fAP8IddWmSvNAr7XrH.cV*c-',

    'empcnt': [51,200]
}

class WegoJobScraper(JobScraper):
    def __init__(self):
        super(WegoJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        while True:
            s = soupify(self.br.response().read())
            r = re.compile(r'^/ats/Portal.na\?\S+wid=\d+')

            for a in s.findAll('a', href=r):
                tr = a.findParent('tr')
                td = tr.findAll('td')
            
                l = td[1].text + ', ' + td[2].text
                l = self.parse_location(l)

                if not l:
                    continue

                job = Job(company=self.company)
                job.title = a.text
                job.url = urlparse.urljoin(self.br.geturl(), a['href'])
                job.location = l
                jobs.append(job)

            t = s.find(text=re.compile(r'^Next '))
            if not t:
                break

            a = t.parent
            r = re.compile(r"filterRecord\('(\d+)', '', '(\d+)', '(\d+)'")
            m = re.search(r, a['href'])

            # https://recruit.zoho.com/ats/Widget.na?digest=XjGeD*20vV5dni33tNU8fAP8IddWmSvNAr7XrH.cV*c-&wid=227503000000052038&start=11&recordperpage=10
            i = {'wid': m.group(1), 'start': m.group(2), 'recordperpage': m.group(3)}
            u = url_set_path(self.br.geturl(), '/ats/Widget.na')
            u = url_query_add(u, i.items())
            self.br.open(u)

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            x = {'class': 'job-opening-form-values'}
            d = s.find('div', attrs=x)

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return WegoJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
