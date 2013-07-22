from neekanee.jobscrapers.apply2jobs.apply2jobs import Apply2JobsJobScraper

COMPANY = {
    'name': 'Intermedix',
    'hq': 'Fort Lauderdale, FL',

    'home_page_url': 'http://www.intermedix.com',
    'jobs_page_url': 'https://www1.apply2jobs.com/Intermedix/ProfExt/index.cfm?fuseaction=mExternal.showSearchInterface',

    'empcnt': [501,1000]
}

class IntermedixJobScraper(Apply2JobsJobScraper):
    def __init__(self):
        super(IntermedixJobScraper, self).__init__(COMPANY)

    def get_location_from_td(self, td):
        l = td[-2].text + ', ' + td[-1].text
        return self.parse_location(l)

def get_scraper():
    return IntermedixJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
