#!/usr/bin/env python3
import sys

# https://stackoverflow.com/a/32353549/5411712
# helpful for accessing the information in pandas stdout/stderr 
class RedirectStdStreams(object):
    def __init__(self, stdout=None, stderr=None):
        self._stdout = stdout or sys.stdout
        self._stderr = stderr or sys.stderr

    def __enter__(self):
        self.old_stdout, self.old_stderr = sys.stdout, sys.stderr
        self.old_stdout.flush(); self.old_stderr.flush()
        sys.stdout, sys.stderr = self._stdout, self._stderr

    def __exit__(self, exc_type, exc_value, traceback):
        self._stdout.flush(); self._stderr.flush()
        sys.stdout = self.old_stdout
        sys.stderr = self.old_stderr


if __name__ == "__main__":
    from io import StringIO
    s = StringIO("some string buffer")
    print(s.read())
    s.seek(0)
    # demonstrate Redirect 
    # by writing "hello" to stdout via print
    # should overwrite "some s" with "hello\t" but keep rest of buffer
    with RedirectStdStreams(stdout=s):
        print("hello",end='\t')
    s.seek(0)
    print(s.read())

    # also works with text file
    log = open('log_RedirectStdStreams.txt', 'w') 
    with RedirectStdStreams(stdout=log):
        print("hello",end='\t')
