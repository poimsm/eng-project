class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class console(object):
    @staticmethod
    def info(msg):
        print(bcolors.BOLD + '[INFO] ' + msg + bcolors.ENDC)

    @staticmethod
    def debug(msg):
        print(bcolors.OKBLUE + '[DEBUG] ' + msg + bcolors.ENDC)

    @staticmethod
    def warning(msg):
        print(bcolors.WARNING + '[WARNING] ' + msg + bcolors.ENDC)

    @staticmethod
    def error(msg):
        print(bcolors.FAIL + '[ERROR] ' + msg + bcolors.ENDC)


def unique(sequence):
    result = []
    for item in sequence:
        if item not in result:
            result.append(item)
    return result
