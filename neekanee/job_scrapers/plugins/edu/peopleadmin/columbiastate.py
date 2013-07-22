from neekanee.jobscrapers.peopleadmin.peopleadmin3 import PeopleAdminJobScraper

COMPANY = {
    'name': 'Columbia State Community College',
    'hq': 'Columbia, TN',

    'home_page_url': 'http://www.columbiastate.edu',
    'jobs_page_url': 'https://jobs.tbr.edu',

    'empcnt': [201,500]
}

class ColumbiaStateJobScraper(PeopleAdminJobScraper):
    def __init__(self):
        super(ColumbiaStateJobScraper, self).__init__(COMPANY)

    def select_jobSearch_form(self):
        def select_form(form):
            return form.attrs.get('action', None) == '/postings/search'

        self.br.select_form(predicate=select_form)

    def update_jobSearch_form(self):
        ctl = self.br.form.find_control('642')
        ctl.get(label='Columbia State Community College').selected = True

    def submit_jobSearch_form(self):
        self.br.submit()

def get_scraper():
    return ColumbiaStateJobScraper()

if __name__:
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
