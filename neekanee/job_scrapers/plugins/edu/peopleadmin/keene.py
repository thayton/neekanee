from neekanee.jobscrapers.peopleadmin.PeopleAdminATS import PeopleAdminJobScraper

COMPANY = {
    'name': 'Keene State College',
    'hq': 'Keene, NH',

    'home_page_url': 'http://www.keene.edu',
    'jobs_page_url': 'https://jobs.usnh.edu/applicants/jsp/shared/index.jsp',

    'empcnt': [5001,10000]
}

class KeeneJobScraper(PeopleAdminJobScraper):
    def __init__(self):
        super(KeeneJobScraper, self).__init__(COMPANY)

    def update_hrSearch_form(self):
        ctl = self.br.form.find_control('di_20117')
        ctl.get(label='Keene State College').selected = True

def get_scraper():
    return KeeneJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
