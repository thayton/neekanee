from neekanee.jobscrapers.kenexa.kenexa import KenexaJobScraper

COMPANY = {
    'name': 'Duke University',
    'hq': 'Durham, NC',

    'ats': 'Kenexa',

    'benefits': {
        'url': 'http://www.hr.duke.edu/benefits/index.php',
        'vacation': [(0,15)],
        'holidays': 13,
        'tuition_assistance': True
    },

    'home_page_url': 'http://www.duke.edu',
    'jobs_page_url': 'https://sjobs.brassring.com/1033/ASP/TG/cim_home.asp?partnerid=25017&siteid=5172',

    'gctw_chronicle': True,

    'empcnt': [10001]
}

class DukeJobScraper(KenexaJobScraper):
    def __init__(self):
        super(DukeJobScraper, self).__init__(COMPANY)

    def get_location_from_td(self, td):
        y = td[4].text
        if y.find(',') == -1:
            y += ', NC'

        return self.parse_location(y)

def get_scraper():
    return DukeJobScraper()
