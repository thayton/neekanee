from neekanee.jobscrapers.kenexa.kenexa import KenexaJobScraper

COMPANY = {
    'name': 'Synopsys',
    'hq': 'Mountain View, CA',

    'ats': 'Kenexa',
    'benefits': {
        'vacation': [(0,18)],
        'tuition_assistance': True
    },

    'home_page_url': 'http://www.synopsys.com',
    'jobs_page_url': 'https://sjobs.brassring.com/1033/ASP/TG/cim_home.asp?partnerid=25235&siteid=5359',

    'empcnt': [10001]
}

class SynopsysJobScraper(KenexaJobScraper):
    def __init__(self):
        super(SynopsysJobScraper, self).__init__(COMPANY)
        self.soupify_search_form = True

    def get_location_from_td(self, td):
        y = td[3].text.split(',')[0]
        return self.parse_location(y)
        
def get_scraper():
    return SynopsysJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
