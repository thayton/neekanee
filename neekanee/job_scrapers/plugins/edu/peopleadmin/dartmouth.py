from neekanee.jobscrapers.peopleadmin.peopleadmin3 import PeopleAdminJobScraper

COMPANY = {
    'name': 'Dartmouth College',
    'hq': 'Hanover, NH',

    'benefits': {
        'url': 'http://jobs.dartmouth.edu/benefits/',
        'vacation': [(1,22)],
        'holidays': 8,
        'tuition_assistance': True
    },

    'home_page_url': 'http://www.dartmouth.edu',
    'jobs_page_url': 'https://searchjobs.dartmouth.edu',

    'empcnt': [1001,5000]
}

class DartmouthJobScraper(PeopleAdminJobScraper):
    def __init__(self):
        super(DartmouthJobScraper, self).__init__(COMPANY)

def get_scraper():
    return DartmouthJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
