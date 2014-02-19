from neekanee.jobscrapers.apply2jobs.apply2jobs import Apply2JobsJobScraper

COMPANY = {
    'name': 'Brocade',
    'hq': 'San Jose, CA',

    'home_page_url': 'http://www.brocade.com',
    'jobs_page_url': 'https://www.brocade.apply2jobs.com/ProfExt/index.cfm?fuseaction=mExternal.showSearchInterface',

    'empcnt': [1001,5000]
}

class BrocadeJobScraper(Apply2JobsJobScraper):
    def __init__(self):
        super(BrocadeJobScraper, self).__init__(COMPANY)

    def get_location_from_td(self, td):
        l = ', '.join(['%s' % x.text for x in td[3:0:-1]])
        return self.parse_location(l)


def get_scraper():
    return BrocadeJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
