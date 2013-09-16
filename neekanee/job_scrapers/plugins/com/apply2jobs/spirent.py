from neekanee.jobscrapers.apply2jobs.apply2jobs import Apply2JobsJobScraper

COMPANY = {
    'name': 'Spirent',
    'hq': 'Germantown, MD',

    'ats': 'VirtualEdge',

    'home_page_url': 'http://www.spirent.com',
    'jobs_page_url': 'https://www.spirent.apply2jobs.com/index.cfm',

    'empcnt': [1001,5000]
}

class SpirentJobScraper(Apply2JobsJobScraper):
    def __init__(self):
        super(SpirentJobScraper, self).__init__(COMPANY)

    def get_location_from_td(self, td):
        l = '-'.join(['%s' % x.text for x in td[2:5]])
        return self.parse_location(l)

def get_scraper():
    return SpirentJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()

