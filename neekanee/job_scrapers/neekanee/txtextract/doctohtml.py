import os
import sys
import StringIO

def doctohtml(data):
    """ 
    Convert Microsoft Word .doc into HTML. Write HTML back
    on stdout .
    """
    f = open('/tmp/data.doc', 'w')
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
            # java -jar /usr/local/bin/tika-app.jar -h /tmp/data.doc
            os.execlp('java', 'java', '-jar', '/usr/local/bin/tika-app.jar',  '-h', '/tmp/data.doc')
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
        os.unlink('/tmp/data.doc')
        sys.stderr.write("Exception: %s\n", e)
        sys.exit(1)
    
    os.unlink('/tmp/data.doc')
    return StringIO.StringIO(buf)

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        sys.stderr.write('usage: %s <doc-file>\n' % sys.argv[0])
        sys.exit(1)

    with open(sys.argv[1]) as f:
        s = doctohtml(f.read())
        print s.read()
        f.close()
