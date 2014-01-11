from neekanee.jobscrapers.icims.icims2 import IcimsJobScraper

COMPANY = {
    'name': 'Jacobs Technology',
    'hq': 'Tullahoma, TN',

    'ats': 'icims',

    'home_page_url': 'http://www.jacobstechnology.com',
    'jobs_page_url': 'https://jacobsexternal-jacobstechnology.icims.com/jobs/intro?in_iframe=1',

    'empcnt': [1001,5000]
}

class JacobsJobScraper(IcimsJobScraper):
    def __init__(self):
        super(JacobsJobScraper, self).__init__(COMPANY)

    def get_location_from_desc(self, d):
        x = {'itemprop': 'address'}
        p = d.find('span', attrs=x)
        m = '-'.join(['%s' % x['content'] for x in p.findAll('meta')])
        l = self.parse_location(m)
        return l

def get_scraper():
    return JacobsJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
