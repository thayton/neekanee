from neekanee.jobscrapers.apply2jobs.apply2jobs import Apply2JobsJobScraper

COMPANY = {
    'name': 'Brunswick',
    'hq': 'Lake Forest, IL',

    'home_page_url': 'http://www.brunswick.com',
    'jobs_page_url': 'https://www.brunswickcareers.apply2jobs.com/ProfExt/index.cfm?fuseaction=mExternal.showSearchInterface',

    'empcnt': [10001]
}

class BrunswickJobScraper(Apply2JobsJobScraper):
    def __init__(self):
        super(BrunswickJobScraper, self).__init__(COMPANY)

    def get_location_from_td(self, td):
        l = td[-3].text + ', ' + td[-4].text
        return self.parse_location(l)

def get_scraper():
    return BrunswickJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
