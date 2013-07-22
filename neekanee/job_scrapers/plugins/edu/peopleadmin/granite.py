from neekanee.jobscrapers.peopleadmin.PeopleAdminATS import PeopleAdminJobScraper

COMPANY = {
    'name': 'Granite State College',
    'hq': 'Concord, NH',

    'home_page_url': 'http://www.granite.edu',
    'jobs_page_url': 'https://jobs.usnh.edu/applicants/jsp/shared/index.jsp',

    'empcnt': [51,200]
}

class GraniteJobScraper(PeopleAdminJobScraper):
    def __init__(self):
        super(GraniteJobScraper, self).__init__(COMPANY)

    def update_hrSearch_form(self):
        ctl = self.br.form.find_control('di_20117')
        ctl.get(label='Granite State College').selected = True

def get_scraper():
    return GraniteJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
