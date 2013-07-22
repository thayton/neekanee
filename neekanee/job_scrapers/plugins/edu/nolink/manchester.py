import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify

from neekanee_solr.models import *

COMPANY = {
    'name': 'Manchester College',
    'hq': 'North Manchester, IN',

    'benefits': {
        'vacation': [(1,10),(6,15),(16,20)],
        'holidays': 12,
        'sick_days': 10,
        'tuition_assistance': True
    },

    'home_page_url': 'http://www.manchester.edu',
    'jobs_page_url': 'http://www.manchester.edu/OHR/',

    'gctw_chronicle': True,

    'empcnt': [201,500]
}

class ManchesterJobScraper(JobScraper):
    def __init__(self):
        super(ManchesterJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        r = re.compile(r'^#')

        links = [ 'facultypositions.htm',
                  'staffpositions.htm',
                  'pharmacypositions.htm' ]

        self.company.job_set.all().delete()

        for l in links:
            self.br.open(urlparse.urljoin(self.br.geturl(), l))
            s = soupify(self.br.response().read())

            for a in s.findAll('a', href=r):
                job = Job(company=self.company)
                job.title = a.text
                job.url = urlparse.urljoin(self.br.geturl(), a['href'])
                job.location = self.company.location
                job.desc = ''

                x = s.find(attrs={'name' : a['href'][1:]})

                if not x:
                    continue

                x = x.next

                while x and getattr(x, 'name', None) != 'hr':
                    if hasattr(x, 'name') is False: 
                        job.desc += x
                    x = x.next

                job.save()

def get_scraper():
    return ManchesterJobScraper()
