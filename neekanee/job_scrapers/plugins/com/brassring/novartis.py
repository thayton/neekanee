from neekanee.jobscrapers.kenexa.kenexa import KenexaJobScraper

COMPANY = {
    'name': 'Novartis',
    'hq': 'Cambridge, MA',

    'ats': 'Kenexa',

    'home_page_url': 'http://www.novartis.com',
    'jobs_page_url': 'https://sjobs.brassring.com/2057/ASP/TG/cim_home.asp?partnerid=13617&siteid=5260',

    'empcnt': [10001]
}

class NovartisJobScraper(KenexaJobScraper):
    def __init__(self):
        super(NovartisJobScraper, self).__init__(COMPANY)
        self.soupify_search_form = True

    def update_frmAgent_form(self):
        #
        # Set field to limit results to USA only and allow all languages
        #
        self.br.form.new_control('hidden', 'Question20146__FORMTEXT27',   {'value':''})
        self.br.form.new_control('hidden', 'GTGLanguageList',             {'value':''})
        self.br.form.fixup()

        self.br.form.set_all_readonly(False)
        self.br.form['Question20146__FORMTEXT27'] = 'AnswerName&=|USA=X|%%%AnswerValue&=|US=X|%%%GDEAnswerValue&=|=X|???'
        self.br.form['GTGLanguageList'] = 'All'

    def get_title_from_td(self, td):
        return td[2].text

    def get_location_from_td(self, td):
        y = td[4].text.strip() 
        if y != 'USA':
            return None

        return self.parse_location(td[5].text)

def get_scraper():
    return NovartisJobScraper()
