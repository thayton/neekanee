from neekanee.jobscrapers.apply2jobs.apply2jobs import Apply2JobsJobScraper

COMPANY = {
    'name': 'Konica Minolta Business Solutions',
    'hq': 'Ramsey, NJ',

    'home_page_url': 'http://kmbs.konicaminolta.us',
    'jobs_page_url': 'https://www.kmbs.apply2jobs.com/ProfExt/index.cfm?fuseaction=mExternal.showSearchInterface',

    'empcnt': [5001,10000]
}

class KonicaMinoltaJobScraper(Apply2JobsJobScraper):
    def __init__(self):
        super(KonicaMinoltaJobScraper, self).__init__(COMPANY)

    def get_location_from_td(self, td):
        l = td[1].text + ', ' + td[2].text
        return self.parse_location(l)

def get_scraper():
    return KonicaMinoltaJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
