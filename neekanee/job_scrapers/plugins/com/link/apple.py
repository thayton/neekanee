import re, urlparse, mechanize, urlutil, urllib, json, time

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Apple',
    'hq': 'Cupertino, CA',

    'home_page_url': 'http://www.apple.com',
    'jobs_page_url': 'https://jobs.apple.com/us/search?',

    'empcnt': [10001]
}

class AppleJobScraper(JobScraper):
    def __init__(self):
        super(AppleJobScraper, self).__init__(COMPANY)
        self.br.addheaders = [('User-agent', 
                               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36'),
                              ('Accept-Language', 'en-US,en;q=0.8'),
                              ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')]

    def scrape_job_links(self, url):
        jobs = []

        pageno = 0

        data_orig = { 'searchRequestJson': '{"searchString":"","jobType":1,"filters":{"locations":null,"retailJobSpecs":null,"businessLine":null,"jobFunctions":null,"languageSkills":null},"sortBy":"req_open_dt","sortOrder":"1","pageNumber":"%d"}',
                 'csrfToken': 'null',
                 'clientOffset': '-300'
               }

        data = data_orig.copy()
        data['searchRequestJson'] = data['searchRequestJson'] % pageno
        pageno += 1

        data = urllib.urlencode(data)
        resp = mechanize.Request('https://jobs.apple.com/us/search/search-result', data)

        r = mechanize.urlopen(resp)

        while True:
            s = soupify(r.read())
            if not s.requisition:
                break

            for r in s.findAll('requisition'):
                j = int(r.jobid.text)
                job = Job(company=self.company)
                job.title = r.postingtitle.text
                job.url = self.company.jobs_page_url + 'job=%d&openJobId=%d' % (j, j)
                jobs.append(job)

            # Next page
            data = data_orig.copy()
            data['searchRequestJson'] = data['searchRequestJson'] % pageno
            pageno += 1

            data = urllib.urlencode(data)
            resp = mechanize.Request('https://jobs.apple.com/us/search/search-result', data)

            r = mechanize.urlopen(resp)
                
        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            # Time delay so we don't hit their servers too hard
            # NeekaneeBrowser() usually handles this for us but here
            # we're creating requests manually
            time.sleep(2)

            u = 'https://jobs.apple.com/us/requisition/detail.json'
            m = re.search(r'job=(\d+)', job.url)

            data = { 'requisitionId': m.group(1),
                     'reqType':       'REQ',
                     'clientOffset':  '-300'
            }
            data = urllib.urlencode(data)

            resp = mechanize.Request(u, data)

            r = mechanize.urlopen(resp)
            j = json.loads(r.read())

            d = '\n'.join(['%s' % x for x in j['reqTextFields'].values()])
            r = j['requisitionInfo']
            l = [r['locationName'], r.get('stateAbbr', ''), r['countryCode']]
            l = ', '.join(['%s' % x for x in l if x])
            l = self.parse_location(l)
                         
            if not l:
                continue

            job.location = l
            job.desc = d
            job.save()

def get_scraper():
    return AppleJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
