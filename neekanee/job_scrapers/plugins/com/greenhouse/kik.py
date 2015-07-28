import re, urlparse, mechanize, urllib

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text, extract_form_fields

from neekanee_solr.models import *

COMPANY = {
    'name': 'Kik Interactive',
    'hq': 'Waterloo, Canada',

    'ats': 'COMPAS',

    'home_page_url': 'http://kik.com',
    'jobs_page_url': 'http://kik.mycompas.com/corp/consol_careers/careers_source.aspx',

    'empcnt': [11,50]
}

# XXX similar to com/sendouts/cummins.py
class KikJobScraper(JobScraper):
    def __init__(self):
        super(KikJobScraper, self).__init__(COMPANY)
        self.br.addheaders = [('User-agent', 
                               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.63 Safari/535.7'),
                              ('Referrer',
                               'http://minerva.mycompas.com/corp/careers/minerva/careers_source.aspx'),]


    def get_job_cmp(self):
        def cmp(job1, job2):
            qs1 = urlparse.parse_qs(job1.url_data)
            qs2 = urlparse.parse_qs(job2.url_data)

            return job1.url == job2.url and qs1['__EVENTTARGET'] == qs2['__EVENTTARGET']

        return cmp

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        d = s.find('div', id='divresults')
        r = re.compile(r'WebForm_PostBackOptions\("(\S+)"')

        for a in d.findAll('a', href=r):
            tr = a.findParent('tr')
            td = tr.findAll('td')
        
            l = self.parse_location(td[-1].text)
            if not l:
                continue

            f = s.find('form', attrs={'name': 'form1'})
            m = re.search(r, a['href'])

            x = extract_form_fields(f)
            x['__EVENTTARGET'] = m.group(1)

            if x.has_key('btntranssearch'):
                del x['btntranssearch']

            job = Job(company=self.company)
            job.title = a.text
            job.url = urlparse.urljoin(self.br.geturl(), f['action'])
            job.url_data = urllib.urlencode(x)
            job.location = l
            jobs.append(job)

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list, use_job_cmp=True)
        new_jobs = self.new_job_listings(job_list, use_job_cmp=True)

        for job in new_jobs:
            self.br.open(job.url)

            def get_postingid(query):
                d = urlparse.parse_qs(query)
                return d['__EVENTTARGET'][0]

            self.br.select_form('form1')
            self.br.set_all_readonly(False)
            self.br.form['__EVENTTARGET'] = get_postingid(job.url_data)
            self.br.form['__EVENTARGUMENT'] = ''

            ctl = self.br.form.find_control(name='btntranssearch')

            self.br.form.controls.remove(ctl)
            self.br.submit()

            v = soupify(self.br.response().read())
            d = v.find('div', id='divshowdesc')

            job.desc = get_all_text(d)
            job.save()

            self.br.back()

def get_scraper():
    return KikJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
