import os
import sys
import signal
import StringIO

def sigchld(signo, frame):
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
            if pid <= 0:
                break

def pdftohtml(data):
    """ 
    Convert PDF data into HTML. Write HTML back
    on stdout 
    """
    f = open('/tmp/data.pdf', 'w')
    f.write(data)
    f.close()

    signal.signal(signal.SIGCHLD, sigchld)

    #
    #   parent    child
    #   r <------ w (stdout) 
    #
    r,w = os.pipe()
    try:
        pid = os.fork()
        if pid == 0: # child 
            os.dup2(w, 1)
            os.close(r)
            os.close(w)
            #os.execlp('pdftotext', 'pdftotext', '-htmlmeta', '/tmp/data.pdf', '-')
            # java -jar /usr/local/bin/tika-app-1.1.jar -h /tmp/data.pdf
            os.execlp('java', 'java', '-jar', '/usr/local/bin/tika-app-1.4.jar',  '-h', '/tmp/data.pdf')
        else: # parent 
            os.close(w)

            buf = ''
            while True:
                try:
                    c = os.read(r, 1)
                except OSError, e:
                    if e.errno == os.errno.EINTR:
                        continue
                    else:
                        raise

                if c == '':
                    break
                buf += c

            os.close(r)

    except OSError, e:
        os.unlink('/tmp/data.pdf')
	raise
    
    os.unlink('/tmp/data.pdf')
    return StringIO.StringIO(buf)
