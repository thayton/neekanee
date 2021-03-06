#!/usr/bin/env python

"""
TODO: Make the url a command line parameter instead of having to manually change url
"""

import os, sys, mechanize, logging, glob
from job_scraper_engine import JobScraperEngine

url = 'http://www.neekanee.com/load_jobs/'

if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.stderr.write('usage: %s <plugins-dir> <results-dir>\n' % sys.argv[0])
        sys.exit(1)

    engine = JobScraperEngine(plugin_dir=sys.argv[1], results_dir=sys.argv[2])
    engine.load_plugins()
    engine.run()

    os.system('cat /var/log/neekanee/job_scraper_engine.log | ssh -l thayton thayton.webfactional.com sendmail todd.hayton@gmail.com')
    os.system('cat /var/log/neekanee/neekanee_geocoder.log  | ssh -l thayton thayton.webfactional.com sendmail todd.hayton@gmail.com')

    logger = logging.getLogger('neekanee.scrape_jobs')

    for file in glob.glob('%s/*.json' % sys.argv[2]):
        with open(file) as f:
            br = mechanize.Browser()
            br.open(url)
            br.select_form('upload_jobs')
            br.add_file(filename=file, file_object=f)
            try:
                br.submit()
            except:
                logger.exception("Error loading jobs for %s: %s:" % (file, sys.exc_info()[0]))
                pass
            else:
                logger.info("Server response for %s upload: %s" % (file, br.response().read()))

