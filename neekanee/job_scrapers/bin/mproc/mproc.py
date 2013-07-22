#!/usr/bin/env python

import os
import sys
import time
import random
import socket
import select
import signal

from job_scraper import JobScraper
from datetime import datetime, timedelta

MAX_RUNNING_TIME = timedelta(seconds=15)
SELECT_WAIT_TIME = 1
MAX_NUM_SCRAPERS = 3

# singleton
sockets = socket.socketpair(socket.AF_UNIX, socket.SOCK_DGRAM)

def sigchld(signo, frame):
    ''' 
    Write the pid of the process that died to socket. Receiving
    end will use this track completed processes.
    '''
    while True:
        try:
            (pid, exit_status) = os.waitpid(-1, os.WNOHANG)
        except OSError, e:
            if e.errno == os.errno.ECHILD:
                break
            else:
                sys.stderr.write('Waitpid failed: %s' % e.strerror)
                raise
        else:
            if pid > 0:
                sockets[1].send('%d' % pid)

class JobScraperProc:
    def __init__(self, pid=None, job_scraper=None):
        self.pid = pid
        self.job_scraper = job_scraper
        self.launch_time = None
        
class JobScraperEngine:
    def __init__(self, job_scrapers=[]):
        self.job_scrapers = job_scrapers
        self.procs = {}
        self.domains_being_scraped = []

        signal.signal(signal.SIGCHLD, sigchld)

    def run(self):
        while len(self.job_scrapers) > 0 or len(self.procs) > 0:
            self.launch_scrapers()
            self.wait_for_scrapers()
            self.kill_hung_scrapers()

    def launch_scrapers(self):
        while len(self.job_scrapers) > 0 and len(self.procs) < MAX_NUM_SCRAPERS:
            job_scraper = self.get_next_job_scraper()
            if job_scraper is not None:
                self.launch_scraper(job_scraper)
            else:
                break

    def wait_for_scrapers(self, timeout=SELECT_WAIT_TIME):
        '''
        When sockets[0] becomes readable, it means that a scraper has finished.
        We can read the pid of the completed scraper process from sockets[0]
        '''
        while True:
            try:
                r,w,e = select.select([sockets[0]], [], [], timeout)
            except select.error, e:
                if e[0] != os.errno.EINTR: # WTF, e has no errno attrib
                    sys.stderr.write('select failed: %s\n' % v)
                    raise
            else:
                break

        if len(r) > 0:
            pid = int(sockets[0].recv(16))

            job_scraper = self.procs[pid].job_scraper
            self.domains_being_scraped.remove(job_scraper.domain)

            del self.procs[pid]

    def get_next_job_scraper(self):
        for job_scraper in self.job_scrapers:
            if job_scraper.domain not in self.domains_being_scraped:
                self.job_scrapers.remove(job_scraper)
                return job_scraper

        return None

    def stop(self):
        pass

    def launch_scraper(self, job_scraper):
        try:
            pid = os.fork()
        except os.OSError, e:
            sys.stderr.write('Fork failed: %s\n' %  e.strerror)
            raise

        if pid == 0: # child
            job_scraper.run()
            sys.exit(0)
        else: # parent
            proc = JobScraperProc(pid, job_scraper)
            proc.launch_time = datetime.now()

            self.procs[pid] = proc

            if job_scraper.domain not in self.domains_being_scraped:
                self.domains_being_scraped.append(job_scraper.domain)

    def kill_hung_scrapers(self):
        now = datetime.now()
        for pid, proc in self.procs.items():
            delta = now - proc.launch_time
            if delta > MAX_RUNNING_TIME:
                try:
                    os.kill(pid, signal.SIGKILL)
                except OSError, e:
                    if e.errno != os.errno.ESRCH:
                        raise
                else:
                    sys.stderr.write('* %02d:%02d:%02d killed %d => delta: %s\n' % \
                                         (now.hour, now.minute, now.second, pid, delta))


if __name__ == '__main__':
    random.seed()

    engine = JobScraperEngine()

    engine.job_scrapers.append(JobScraper('www.tenablesecurity.com', 'adp.com'))
    engine.job_scrapers.append(JobScraper('www.blurb.com',           'adp.com'))
    engine.job_scrapers.append(JobScraper('www.edgewave.com',        'adp.com'))

    engine.job_scrapers.append(JobScraper('www.akimeka.com',         'taleo.com'))
    engine.job_scrapers.append(JobScraper('www.camber.com',          'taleo.com'))
    engine.job_scrapers.append(JobScraper('www.qualys.com',          'taleo.com'))

    engine.job_scrapers.append(JobScraper('www.debix.com',           'debix.com'))
    engine.job_scrapers.append(JobScraper('www.ember.com',           'ember.com'))
    engine.job_scrapers.append(JobScraper('www.extole.com',          'extole.com'))

    engine.job_scrapers.append(JobScraper('www.gwu.com',             'peopleadmin.com'))
    engine.job_scrapers.append(JobScraper('www.gmu.com',             'peopleadmin.com'))
    engine.job_scrapers.append(JobScraper('www.jsu.com',             'peopleadmin.com'))

    engine.run()

