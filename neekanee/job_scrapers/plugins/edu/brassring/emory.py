from neekanee.jobscrapers.kenexa.kenexa import KenexaJobScraper

COMPANY = {
    'name': 'Emory University',
    'hq': 'Atlanta, GA',

    'ats': 'Kenexa',

    'benefits': {
        'url': 'http://hr.emory.edu/careers/benefits.html',
        'vacation': [],
        'holidays': 12,
        'tuition_assistance': True
    },

    'home_page_url': 'http://www.emory.edu',
    'jobs_page_url': 'https://sjobs.brassring.com/1033/ASP/TG/cim_home.asp?partnerid=25066&siteid=5043',

    'gctw_chronicle': True,

    'empcnt': [10001]
}

class EmoryJobScraper(KenexaJobScraper):
    def __init__(self):
        super(EmoryJobScraper, self).__init__(COMPANY)

    def get_title_from_td(self, td):
        return td[3].text

def get_scraper():
    return EmoryJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
