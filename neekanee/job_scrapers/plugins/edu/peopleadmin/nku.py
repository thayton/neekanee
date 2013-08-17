from neekanee.jobscrapers.peopleadmin.peopleadmin3 import PeopleAdminJobScraper

COMPANY = {
    'name': 'Northern Kentucky University',
    'hq': 'Highland Heights, KY',

    'benefits': {
        'url': 'http://hr.nku.edu/benefits/index.php',
        'vacation': [(1,20),(10,25)],
        'holidays': 8,
        'tuition_assistance': True
    },

    'home_page_url': 'http://www.nku.edu',
    'jobs_page_url': 'https://jobs.nku.edu',

    'empcnt': [1001,5000]
}

def get_scraper():
    return PeopleAdminJobScraper(COMPANY)

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
