import sys, atexit, datetime, hashlib


class Logger:
    """
    Logger class that allows to write lines to the console and/or a file.
    """

    def __init__(self, logfile=None, console=sys.stderr, level=1):
        """

        :param logfilename: The name of a file to log to. If none then messages are not written to a file
        :param console: Whether to write messages to the console. The default is to write to sys.stderr, but you can
        specify sys.stdout or None instead.
        :param level: What types of message to log. 0 = everything, 1 = WARNING and ERROR, 2 = ERROR only
        """
        self.console = console
        self.level = 0
        self.infos = 0
        self.warnings = 0
        self.errors = 0
        if logfile:
            self.logfile = open(logfile, 'w')
            self.closed = False
        else:
            self.logfile = None
            self.closed = True
        atexit.register(self.close)
        x = datetime.datetime.now()
        self.log('Initialising logging at level {} at {}'.format(level, x), level=0)
        self.level = level


    def close(self):
        if self.logfile and not self.closed:
            self.logfile.close()
            self.closed = True

    def log(self, *args, level=0, **kwargs):
        """
        Log output to STDERR and/or the specified log file
        :param args: arguments to log
        :param level: 0 = INFO, 1 = WARNING, 2 = ERROR
        :param kwargs: kwargs to send to the print() statement
        :return:
        """

        if level == 0:
            self.infos += 1
        elif level == 1:
            self.warnings += 1
        elif level == 2:
            self.errors += 1

        if level >= self.level:
            if level == 0:
                key = 'INFO:'
            elif level == 1:
                key = 'WARNING:'
            elif level == 2:
                key = 'ERROR:'
            else:
                key = None
            if self.console:
                print(key, *args, file=self.console, **kwargs)
            if self.logfile:
                print(key, *args, file=self.logfile, **kwargs)

    def get_num_messages(self):
        return self.infos, self.warnings, self.errors

def gen_sha256(file):
    sha256_hash = hashlib.sha256()
    with open(file, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def main():

    log = Logger(logfile='logfile.log', level=1)

    log.log('a', 'b', 'c', level=0)
    log.log('foo', 'bar', 'baz')
    log.log('foo', 99, 'apples', level=2)


if __name__ == "__main__":
    main()
