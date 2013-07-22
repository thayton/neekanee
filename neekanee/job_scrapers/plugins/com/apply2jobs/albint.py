from neekanee.jobscrapers.apply2jobs.apply2jobs import Apply2JobsJobScraper

COMPANY = {
    'name': 'Albany Engineered Composites',
    'hq': 'Rochester, NH',

    'home_page_url': 'http://www.albint.com',
    'jobs_page_url': 'https://www1.apply2jobs.com/albint/ProfExt/index.cfm?fuseaction=mExternal.showSearchInterface',

    'empcnt': [501,1000]
}

class AlbintJobScraper(Apply2JobsJobScraper):
    def __init__(self):
        super(AlbintJobScraper, self).__init__(COMPANY)

    def get_location_from_td(self, td):
        return self.parse_location(td[-1].text)

def get_scraper():
    return AlbintJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
