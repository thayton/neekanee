from neekanee.jobscrapers.apply2jobs.apply2jobs import Apply2JobsJobScraper

COMPANY = {
    'name': 'Lucasfilm',
    'hq': 'San Francisco, CA',

    'home_page_url': 'http://www.lucasfilm.com',
    'jobs_page_url': 'https://www.lucasfilm.apply2jobs.com/ProfExt/index.cfm?fuseaction=mExternal.showSearchInterface',

    'empcnt': [1001,5000]
}

class LucasfilmJobScraper(Apply2JobsJobScraper):
    def __init__(self):
        super(LucasfilmJobScraper, self).__init__(COMPANY)

    def get_location_from_td(self, td):
        l = td[-1].text + ', ' + td[-2].text
        l = self.parse_location(l)
        return l

def get_scraper():
    return LucasfilmJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
