"""
Параметры вывода текста
"""

bcolors = {'RED': '\033[31m', 'GREEN': '\033[32m', 'YELLOW': '\033[33m',
           'BLUE': '\033[34m', 'MAGENDA': '\033[35m', 'CYAN': '\033[36m',
           'BOLD': '\033[1m', 'UNDERLINE': '\033[4m', 'NEGATIVE': '\033[7m',
           'ENDC': '\033[0m'}

def red(str, end='\n'):
    print(f"{bcolors['RED']}{str}{bcolors['ENDC']}", end=end)


def green(str, end='\n'):
    print(f"{bcolors['GREEN']}{str}{bcolors['ENDC']}", end=end)


def yellow(str, end='\n'):
    print(f"{bcolors['YELLOW']}{str}{bcolors['ENDC']}", end=end)


def blue(str, end='\n'):
    print(f"{bcolors['BLUE']}{str}{bcolors['ENDC']}", end=end)


def magenda(str, end='\n'):
    print(f"{bcolors['MAGENDA']}{str}{bcolors['ENDC']}", end=end)


def cyan(str, end='\n'):
    print(f"{bcolors['CYAN']}{str}{bcolors['ENDC']}", end=end)


def bold(str, end='\n'):
    print(f"{bcolors['BOLD']}{str}{bcolors['ENDC']}", end=end)


def under_line(str, end='\n'):
    print(f"{bcolors['UNDERLINE']}{str}{bcolors['ENDC']}", end=end)


def negative(str, end='\n'):
    print(f"{bcolors['NEGATIVE']}{str}{bcolors['ENDC']}", end=end)


def colored_input(prompt):
    return input(f"{bcolors['CYAN']}{prompt}{bcolors['ENDC']}")
