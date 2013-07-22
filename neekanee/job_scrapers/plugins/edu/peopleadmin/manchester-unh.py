from neekanee.jobscrapers.peopleadmin.PeopleAdminATS import PeopleAdminJobScraper

COMPANY = {
    'name': 'University of New Hampshire at Manchester',
    'hq': 'Manchester, NH',

    'home_page_url': 'http://manchester.unh.edu',
    'jobs_page_url': 'https://jobs.usnh.edu/applicants/jsp/shared/index.jsp',

    'empcnt': [1001,5000]
}

class JobScraper(PeopleAdminJobScraper):
    def __init__(self):
        super(JobScraper, self).__init__(COMPANY)

    def update_hrSearch_form(self):
        ctl = self.br.form.find_control('di_20117')
        ctl.get(label='University of New Hampshire (Manchester Campus)').selected = True

def get_scraper():
    return JobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
