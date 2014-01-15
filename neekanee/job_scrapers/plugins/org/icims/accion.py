from neekanee.jobscrapers.icims.icims2 import IcimsJobScraper

COMPANY = {
    'name': 'Accion',
    'hq': 'Boston, MA',

    'ats': 'icims',

    'home_page_url': 'http://www.accion.org',
    'jobs_page_url': 'https://jobs-accion.icims.com/jobs/intro?in_iframe=1',

    'empcnt': [51,200]
}

class AccionJobScraper(IcimsJobScraper):
    def __init__(self):
        super(AccionJobScraper, self).__init__(COMPANY)

    def get_location_from_div(self, div):
        y = {'itemprop': 'address'}
        p = div.find('span', attrs=y)
        l = '-'.join(['%s' % x['content'] for x in p.findAll('meta')])

        return self.parse_location(l)
        
def get_scraper():
    return AccionJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
