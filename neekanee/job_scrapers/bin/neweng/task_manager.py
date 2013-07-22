#!/usr/bin/env python

import os
import sys
import time
import random
import socket
import select
import signal
import logging

from datetime import datetime, timedelta

MAX_TASK_RUN_TIME = timedelta(hours=2)
SELECT_WAIT_TIME = float(1.0)
MAX_NUM_TASKS = 5

#
# SIGCHLD signal handler writes to one end of this socket pair
# and we monitor the other end to detect when tasks complete
#
sockets = socket.socketpair(socket.AF_UNIX, socket.SOCK_DGRAM)

def sigchld(signo, frame):
    ''' 
    Write the pid of the process that died to socket. Receiving
    end will use this to track completed processes.
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
            else:
                break

class TaskProc:
    ''' task must implement a "run()" method '''
    def __init__(self, pid=None, task=None, logfile='job_scraper_engine.log'):
        self.pid = pid
        self.task = task
        self.launch_time = None
        self.logger = logging.getLogger('neekanee')
        self.logger.setLevel(logging.DEBUG)

        fh = None
        for handler in self.logger.handlers:
            if isinstance(handler, logging.FileHandler):
                fh = handler

        if not fh:
            fh = logging.FileHandler(filename=logfile, mode='w')
            fh.setLevel(logging.DEBUG)

            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            fh.setFormatter(formatter)

            self.logger.addHandler(fh)
        
class TaskManager(object):
    def __init__(self, tasks=[], max_num_tasks=MAX_NUM_TASKS, max_task_run_time=MAX_TASK_RUN_TIME):
        self.tasks = tasks
        self.procs = {}
        self.max_num_tasks = max_num_tasks
        self.max_task_run_time = max_task_run_time

        signal.signal(signal.SIGCHLD, sigchld)

    def set_task_list(self, tasks):
        self.tasks = tasks

    def run(self):
        while len(self.tasks) > 0 or len(self.procs) > 0:
            self.launch_tasks()
            self.wait_for_tasks()
            self.kill_hung_tasks()

    def launch_tasks(self):
        while len(self.tasks) > 0 and len(self.procs) < self.max_num_tasks:
            task = self.get_next_task(self.tasks)
            if task is not None:
                self.tasks.remove(task)
                self.launch_task(task)
            else:
                break

    def launch_task(self, task):
        try:
            pid = os.fork()
        except os.OSError, e:
            sys.stderr.write('Fork failed: %s\n' %  e.strerror)
            raise

        if pid == 0: # child
            task.run()
            os._exit(0)
        else: # parent
            self.logger.info('Creating task for task %s (pid %d)' % (task, pid))
            proc = TaskProc(pid, task)
            proc.launch_time = datetime.now()

            self.procs[pid] = proc
            self.task_launched(task, pid)

    def task_launched(self, task, pid):
        ''' Override in derived class '''
        pass

    def wait_for_tasks(self, timeout=SELECT_WAIT_TIME):
        '''
        When sockets[0] becomes readable, it means that a task has finished.
        We can read the pid of the process used to run the task from sockets[0]
        '''
        while True:
            try:
                r,w,e = select.select([sockets[0]], [], [], timeout)
            except select.error, e:
                if e[0] == os.errno.EINTR: # WTF, e has no errno attrib
                    continue
                else:
                    sys.stderr.write('select failed: %s\n' % e)
                    raise
            else:
                break

        if len(r) > 0:
            pid = int(sockets[0].recv(16))
            if self.procs.has_key(pid):
                self.task_completed(self.procs[pid].task, pid)
                del self.procs[pid]

    def task_completed(self, task):
        ''' Override in derived class. Not called if task is killed '''
        pass

    def kill_hung_tasks(self):
        now = datetime.now()
        for pid, proc in self.procs.items():
            delta = now - proc.launch_time
            if delta > self.max_task_run_time:
                try:
                    self.logger.warning('Killing hung task %d' % int(pid))
                    os.kill(pid, signal.SIGKILL)
                except OSError, e:
                    if e.errno != os.errno.ESRCH:
                        raise
                else:
                    sys.stderr.write('* %02d:%02d:%02d killed %d => delta: %s\n' % \
                                         (now.hour, now.minute, now.second, pid, delta))

    def stop(self):
        for pid, proc in self.procs.items():
            try:
                os.kill(pid, signal.SIGKILL)
            except OSError, e:
                if e.errno != os.errno.ESRCH:
                    raise
