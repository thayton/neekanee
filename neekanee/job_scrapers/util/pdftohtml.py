import os
import sys
import StringIO

def pdftohtml(data):
    """ Convert PDF data into HTML. Write HTML back
    on stdout """
    f = open('/tmp/data.pdf', 'w')
    f.write(data)
    f.close()

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
            os.execlp('pdftotext', 'pdftotext', '-htmlmeta', '/tmp/data.pdf', '-')
        else: # parent 
            os.close(w)

            buf = ''
            while True:
                c = os.read(r, 1)
                if c == '':
                    break
                buf += c

            os.close(r)
            os.waitpid(pid, 0)

    except OSError, e:
        os.unlink('/tmp/data.pdf')
        sys.stderr.write("Exception: %s\n", e)
        sys.exit(1)
    
    os.unlink('/tmp/data.pdf')
    return StringIO.StringIO(buf)
