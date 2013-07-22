from neekanee.jobscrapers.kenexa.kenexa import KenexaJobScraper

COMPANY = {
    'name': 'Yale University',
    'hq': 'New Haven, CT',

    'ats': 'Kenexa',

    'benefits': {
        'url': 'http://www.yale.edu/hronline/benefits/index.html',
        'vacation': [(1,10),(5,15),(10,20),(20,25)],
        'holidays': 16,
        'sick_days': 12,
        'tuition_assistance': True
    },

    'home_page_url': 'http://www.yale.edu',
    'jobs_page_url': 'https://sjobs.brassring.com/1033/ASP/TG/cim_home.asp?partnerid=25053&siteid=5248',

    'empcnt': [10001]
}

class YaleJobScraper(KenexaJobScraper):
    def __init__(self):
        super(YaleJobScraper, self).__init__(COMPANY)

    def get_title_from_td(self, td):
        return td[5].text

    def update_frmAgent_form(self):
        self.br.form.set_all_readonly(False)
        self.br.form['Question27935__FORMDATE1'] = 'AnswerName&=|=X|%%%AnswerValue&=|=X|%%%GDEAnswerValue&=|=X|???'

def get_scraper():
    return YaleJobScraper()
