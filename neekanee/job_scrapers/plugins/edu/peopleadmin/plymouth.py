from neekanee.jobscrapers.peopleadmin.PeopleAdminATS import PeopleAdminJobScraper

COMPANY = {
    'name': 'Plymouth State University',
    'hq': 'Plymouth, NH',

    'home_page_url': 'http://www.plymouth.edu',
    'jobs_page_url': 'https://jobs.usnh.edu/applicants/jsp/shared/index.jsp',

    'empcnt': [201,500]
}

class PlymouthJobScraper(PeopleAdminJobScraper):
    def __init__(self):
        super(PlymouthJobScraper, self).__init__(COMPANY)

    def update_hrSearch_form(self):
        ctl = self.br.form.find_control('di_20117')
        ctl.get(label='Plymouth State University').selected = True

def get_scraper():
    return PlymouthJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
