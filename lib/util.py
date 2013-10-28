import subprocess, sys

def run(cmd, returncode=False, echo=True, **kargs):
    """ Executes a shell command and prints out STDOUT / STDERROR, exits on failure by default """
    
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, **kargs)
    if echo:
        print "$ %s" % cmd
    
    while True:
        out = process.stdout.read(1)
        if out == '' and process.poll() != None:
            break
        if out != '':
            sys.stdout.write(out)
            sys.stdout.flush()

    if returncode:
        return process.returncode
    else:
        if process.returncode != 0:
            print "Something went wrong! returncode=%s" % process.returncode
            sys.exit(1)