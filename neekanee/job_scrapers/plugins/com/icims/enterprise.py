from neekanee.jobscrapers.icims.icims2 import IcimsJobScraper

COMPANY = {
    'name': 'Enterprise Rent-A-Car',
    'hq': 'St. Louis, MO',

    'ats': 'icims',

    'home_page_url': 'http://www.enterprise.com',
    'jobs_page_url': 'https://us-erac.icims.com/jobs/intro?in_iframe=1',

    'empcnt': [10001]
}

class EnterpriseJobScraper(IcimsJobScraper):
    def __init__(self):
        super(EnterpriseJobScraper, self).__init__(COMPANY)

    def get_location_from_div(self, div):
        x = {'itemprop': 'address'}
        d = div.find(attrs=x)
        l = d.text
        d = div.findAll('div')
        l += '-' + d[-1].contents[-1].strip()
        return self.parse_location(l)

def get_scraper():
    return EnterpriseJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
