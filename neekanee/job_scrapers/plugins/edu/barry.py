import re, urlparse, json

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text
from BeautifulSoup import BeautifulSoup

from neekanee_solr.models import *

COMPANY = {
    'name': 'Barry University',
    'hq': 'Miami Shores, FL',

    'benefits': {
        'url': 'http://www.barry.edu/humanresources/benefits/Default.htm',
        'vacation': [(0,25)],
        'holidays': 11
    },

    'home_page_url': 'http://www.barry.edu',
    'jobs_page_url': 'http://www.barry.edu/human-resources/job-postings.html',

    'empcnt': [1001,5000]
}

class BarryJobScraper(JobScraper):
    def __init__(self):
        super(BarryJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = BeautifulSoup(self.br.response().read())
        t = s.find(text=re.compile(r'var jsonJobPosting ='))
        p = t.findParent('script')
        b = p.text.find('{')
        e = t.find('};')
        t = p.text[b:e]
        d = json.loads(t)

        self.company.job_set.all().delete()

        for j in d['data']:
            job = Job(company=self.company)
            job.title = j['title']
            job.url = urlparse.urljoin(self.br.geturl(), 'preview.aspx?jobposting_id=' + j['jobposting_id'])
            job.location = self.company.location
            job.desc = ' '.join(['%s' % v.replace('<br/>', '') for v in j.values()])
            job.save()

def get_scraper():
    return BarryJobScraper()
