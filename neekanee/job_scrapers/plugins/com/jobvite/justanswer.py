import re, urllib, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'JustAnswer',
    'hq': 'San Francisco, CA',

    'ats': 'Jobvite',

    'home_page_url': 'http://www.justanswer.com',
    'jobs_page_url': 'http://hire.jobvite.com/CompanyJobs/Careers.aspx?k=JobListing&c=qEY9Vfwq&jvresize=http%3a%2f%2fww2.justanswer.com%2fframeresize.htm&v=1',

    'empcnt': [51,200]
}

class JustAnswerJobScraper(JobScraper):
    def __init__(self):
        super(JustAnswerJobScraper, self).__init__(COMPANY)
        self.br.addheaders = [('User-agent', 
                               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.63 Safari/535.7')]

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        r = re.compile('/careers\?jvi=')
        v = {'class': 'jvcontent'}
        d = s.find('div', attrs=v)

        for a in d.findAll('a', href=r):
            job = Job(company=self.company)
            job.title = a.text
            job.url = a['href']
            jobs.append(job)
        
        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            f = s.find('iframe', id='jobviteframe')
            x = job.url.find('jvi=')+4
            j = '&j=' + job.url[x:]
            l = f['src'] + j + '&k=Job'

            self.br.open(l)

            s = soupify(self.br.response().read())
            d = s.find('div', attrs={'class': 'jvcontent'})
            x = {'class': 'job_info'}
            p = d.find('p', attrs=x)
            l = p.text.split('&mdash;')[1]
            l = self.parse_location(l)

            if not l:
                continue

            job.location = l
            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return JustAnswerJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
