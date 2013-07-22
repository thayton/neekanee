#!/usr/bin/env python

"""
Front-end for running multiple job scraping plugins and writing the 
JSON-encoded results to files. Plugins which return 0 jobs and plugins
which generate exceptions are logged so that they can be debugged later.

The list of files generated containing scraped jobs is contained in results[].

Plugins are scheduled to run in a random order. This is done to lessen
the chance of scheduling two or more plugins, that both scrape jobs off 
of the same applicant tracking system (taleo, jobvite) at the same time.
"""
import os
import re
import sys
import json
import logging
import random


from loader import PluginLoader
from urlparse import urlparse
from datetime import date

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../../../')))
sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../../')))

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from neekanee_solr.models import *

def last_scrape_time(plug):
    try:
        company = Company.objects.get(home_page_url=plug.COMPANY['home_page_url'])
    except:
        return 1

    if company.last_scrape_time is not None:
        return company.last_scrape_time.toordinal()
    else:
        return 1

class ProgressReport:
    def __init__(self, tot=1):
        self.cur = 1
        self.tot = tot

    def update(self):
        self.cur += 1

    def report(self, company, logger=None):
        if not logger:
            print "%d/%d" % (self.cur, self.tot)
            print "%s\n%s\n%s" % ('-' * 15, company, '-' * 15)
        else:
            logger.info("%d/%d" % (self.cur, self.tot))

class JobsPageScraper:
    def __init__(self, plugin_dir, results_dir, max_plugins_to_run=10, logfile='jobs_page_scraper.log'):
        self.plugin_dir = plugin_dir
        self.results_dir = results_dir
        self.already_ran = self.plugins_already_run(results_dir)
        self.max_plugins_to_run = max_plugins_to_run
        self.nojobs = []
        self.exceptions = []
        self.pldr = PluginLoader()
        self.prog = None
        self.results = [] # List of file names containing JSON-encoded jobs

        random.seed()

        self.logger = logging.getLogger('neekanee')
        self.logger.setLevel(logging.DEBUG)

        fh = logging.FileHandler(filename=logfile, mode='w')
        fh.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)

        self.logger.addHandler(fh)

    def load_plugins(self):
        """
        Load plugins into memory and then order them by last_scrape_time such that
        oldest plugins get run. Then randomly shuffle the plugins so that plugins
        that run consecutively are less lakely to hit the same site (eg. avoid back-
        to-back runs of taleo, kenexa, etc. plugins so that their site's bandwidth
        doesn't get a suddent spike).
        """
        self.pldr.load_plugins([self.plugin_dir])
        self.pldr.plugins.sort(key=last_scrape_time)
        self.pldr.plugins = self.pldr.plugins[:self.max_plugins_to_run]

        random.shuffle(self.pldr.plugins)

        self.logger.info('loaded %d plugins' % len(self.pldr.plugins))
        self.prog = ProgressReport(len(self.pldr.plugins))

    def run_plugins(self):
        """
        Launch plugins. 
        """
        for plug in self.pldr.plugins:
            self.run_plugin(plug)
            self.save_company_jobs(plug)
            self.prog.update()

    def run_plugin(self, plug):
        self.logger.info('running plugin %s' % plug)
        self.prog.report(plug.COMPANY['name'], self.logger)

        job_scraper = plug.get_scraper()

        try:
            job_scraper.scrape_jobs()
        except Exception, e:
            self.exceptions.append('%s' % plug)
            self.logger.warning('plugin %s generated exception: %s' % (plug, e))
            sys.stderr.write("Exception: %s\n" % e)
            sys.exc_clear()

        if job_scraper.company.job_set.count() == 0:
            self.nojobs.append('%s' % plug)
            self.logger.warning('plugin %s has 0 jobs' % plug)

        job_scraper.company.last_scrape_time = date.today()
        job_scraper.company.save()

    def save_company_jobs(self, plug):
        """
        Save job results for company c to disk. Filename will be the name
        of the plugin prefixed with the TLD. For example, for com/viasat.py
        the filename will be com-viasat.json.
        """
        try:
            company = Company.objects.get(home_page_url=plug.COMPANY['home_page_url'])
        except ObjectDoesNotExist:
            return

        num_jobs = company.job_set.count()
        if num_jobs == 0:
            return

        file = self.make_plug_filename(plug)
        path = '%s/%s.json' % (self.results_dir, file)

        try:
            f = open(path, 'w')
            f.write(json.dumps(company.dict(), indent=4))
            f.close()
        except Exception, e:
            sys.stderr.write("Exception: %s\n" % e)
            sys.exc_clear()

        self.logger.info('Saved %d jobs for company %s to file %s' % (num_jobs, company.name, path))
        self.results.append(path)

    def plugins_already_run(self, dir):
        """
        Return a list of plugins that have already been run. If a 
        plugin has a .json file in the results directory then we 
        assume it's already been run.
        """
        return [ os.path.splitext(x)[0] \
                     for x in os.listdir(dir) if x.endswith('.json') ]

    def make_plug_filename(self, plug):
        """
        Return the filename we'll use to store results for a given plugin.
        """
        # bu.py for bu.edu => edu-bu
        netloc = urlparse(plug.COMPANY['home_page_url']).netloc
        tld = netloc.rsplit('.', 1)[1]

        filename = tld + '-' + plug.__name__
        return filename

if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.stderr.write('usage: %s <plugins-dir> <results-dir>\n' % sys.argv[0])
        sys.exit(1)

    scraper = JobsPageScraper(plugin_dir=sys.argv[1], results_dir=sys.argv[2])
    scraper.load_plugins()
    scraper.run_plugins()
