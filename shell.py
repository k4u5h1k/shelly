#!/usr/bin/env python3

import os
import re
import sys
import platform
import signal
import shutil
import socket
import time
import subprocess
import shlex
from datetime import datetime

from scripts.cow import cow

if not sys.platform.startswith('win'): # Chat issues in windows so disabling temporarily
    try:
        import readline
        readline.parse_and_bind("tab: complete")
    except:
        print("readline not installed, installing manually")

        if sys.platform.startswith('win'):
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyreadline"])
            import readline
            readline.parse_and_bind("tab: complete")


script_loc = os.path.dirname(os.path.realpath(__file__))
histfile = open(os.path.join(script_loc,'.pysh_history'),'a+')

if sys.platform.startswith('win'):
    USER = 'USERNAME'

    # This makes ansi escape codes work in cmd magically (O_O)
    os.system('color')

else:
    USER = 'USER'

# up = '\x1b[A'
# down = '\x1b[B'
# left = '\x1b[D'
# right = '\x1b[C'

reset = '\033[0m'
red = '\033[31m'
green = '\033[32m'
yellow = '\033[33m'
blue = '\033[34m'
purple = '\033[35m'
cyan = '\033[36m'

def cowsay(string):
    cow(string)


def cd(path):
    if os.path.isdir(path):
        os.chdir(path)
    if os.path.isfile(dirname):
        print(f"{red}That is a file not directory {user}!{reset}")
    else:
        print(f"{red}{dirname} is not a valid directory!{reset}")


def pwd():
    print(os.getcwd())


def whoami():
    print(os.getenv(USER))


def ls(dirname=None):

    if dirname is None:
        ls = os.listdir(os.curdir)
    else:
        if os.path.isdir(dirname):
            ls = os.listdir(dirname)
        elif os.path.isfile(dirname):
            print(f"{red}That is a file not directory {user}!{reset}")
        else:
            print(f"{red}{dirname} is not a valid directory!{reset}")

    max_file_len = max(len(name) for name in ls) + 5

    # I want list in three columns (neat stonk)
    counter = 0
    for obj in ls:
        print(obj.ljust(max_file_len),end="")
        counter+=1
        if counter%3==0 or counter == len(ls):
            print()
dir = ls


def clear():
    # Got this using clear | hexdump -C
    print("\x1b\x5b\x48\x1b\x5b\x32\x4a", end="")    
cls = clear


def diff(file1, file2):


def touch(filename):
    if not os.path.exists(filename):
        open(filename, 'a').close()
    else:
        print(f"{red}file already exists{reset}")


def rm(filename):
    if os.path.exists(filename):
        os.remove(filename)
    else:
        print(f"{red}Not a valid file path!{reset}")


def mkdir(path):
    if not os.path.isdir(path):
        os.mkdir(path)
    else:
        print(f"{red}Not a valid/free directory path!{reset}")


def cat(filename):
    if os.path.exists(filename):
        with open(filename) as handle:
            for line in handle:
                print(line.strip())
    else:
        print(f"{red}File does not exist!{reset}")


def history():
    histfile.seek(0)
    lines = histfile.readlines()
    for counter,command in enumerate(lines):
        print(f"{(str(counter)+'.').ljust(3)} {command.rstrip()}")


def kill(pid):
    os.kill(pid, signal.SIGSTOP)


def df():
    st = os.statvfs("/")
    free = st.f_bavail * st.f_frsize
    total = st.f_blocks * st.f_frsize
    used = (st.f_blocks - st.f_bfree) * st.f_frsize

    print("Total: %d GiB" % (total // (2**30)))
    print("Used: %d GiB" % (used // (2**30)))
    print("Free: %d GiB" % (free // (2**30)))


def echo(toprint=None):
    if toprint==None:
        print('Usage: echo <string to print>')
    else:
        print(toprint)


def sleep(secs=None):
    if secs==None:
        print('Usage: sleep <seconds>')
    else:
        time.sleep(secs)


def hostname():
    print(socket.gethostname())


def date():
    print(datetime.now().strftime("%a %b %d %H:%M:%S %Y"))


def cp(source=None, destination=None):
    if source==None or destination==None:
        print('Usage: cp <source> <destination>')
    elif os.path.isfile(source):
        shutil.copy(source, destination)


def mv(source, destination):
    if source==None or destination==None:
        print('Usage: mv <source> <destination>')
    elif os.path.isfile(source):
        shutil.move(source, destination)


def run(filename=None,**kwargs):
    try:
        if filename==None:
            print('Usage: run <filename>')
        else:
            with open(filename, "rb") as source_file:
                code = compile(source_file.read(), filename, "exec")
            exec(code, kwargs)
    except:
        return


def chat():
    run(os.path.join(script_loc,'scripts','irc_client.py'))

def colorswitch():
    global userColor, dirColor, symbolColor
    available = [ "red",
                "green",
                "yellow",
                "blue",
                "purple",
                "cyan"]

    toprint = "\n".join([ f"{red}red{reset}",
                f"{green}green{reset}",
                f"{yellow}yellow{reset}",
                f"{blue}blue{reset}",
                f"{purple}purple{reset}",
                f"{cyan}cyan{reset}"])

    print(f'Available Colors: \n{toprint}')
    user = input('Username color: ').lower()
    directory = input('Directory color: ').lower()
    symbol = input('Prompt symbol color: ').lower()
    if user in available and directory in available and symbol in available:
        userColor = globals()[user]
        dirColor = globals()[directory]
        symbolColor = globals()[symbol]
    else:
        print(f'{red}One of more inputs were invalid!{reset}')
    

def help():
    global available
    max_comm_len = max(len(func) for func in available) + 5
    print('Available Commands:')

    # I want list in five columns (neat stonk)
    counter = 0
    for obj in available:
        print(obj.ljust(max_comm_len),end="")
        counter+=1
        if counter%5==0 or counter == len(available):
            print()
    print(f'{yellow}+ Any python3 one-liners {reset}')


# DEFINE YOUR FUNCTIONS ABOVE THIS LINE
# =====================================

# This will make available = ['cd', 'pwd', ... with all functions above next line]
available = []
local_locals = list(locals().items()).copy()
for key, value in local_locals:
    if callable(value) and value.__module__ == __name__:
        available.append(key)

userColor = cyan
dirColor = green
symbolColor = purple

def runShell():
    cwd = os.getcwd()
    dirname = os.path.split(cwd)[-1]
    user = os.getenv(USER)
    PS1 = f"{userColor}{user}{reset} {dirColor}{dirname}{reset} {symbolColor}${reset} "

    # func_cleanup = re.compile(f"({'|'.join(available)})")

    command = input(PS1)
    histfile.write(command+'\n')

    # possible_types = {1: 'Python', 2: 'Shell', 3: 'Invalid'}

    old_stdout = sys.stdout
    try:
        sys.stdout = None 
        splitted = shlex.split(command)
        if splitted[0] in available:
            command_type = 2
            if len(splitted) == 1:
                command += '()'
            else:
                splitted.insert(1,"(")
                splitted.append(")")
                start_quote = lambda word: word.startswith("'") or word.startswith('"')
                end_quote = lambda word: word.endswith("'") or word.endswith('"')
                sawQuote = False
                for i in range(2,len(splitted)-1):
                    word = splitted[i]

                    if not sawQuote and not (start_quote(word) or end_quote(word)):
                        splitted[i]="'"+splitted[i]+"'"
                        word = splitted[i]

                    elif start_quote(word):
                        sawQuote=True

                    if end_quote(word) and i!=len(splitted)-2:
                        splitted[i]+=","
                        sawQuote = False

                    
                command = ''.join(splitted[:2])+' '.join(splitted[2:-1])+splitted[-1]
        elif exec(command) is None:
            command_type = 1
    except:
        command_type = 3
    sys.stdout = old_stdout

    if command == 'exit' or command == 'quit':
        raise KeyboardInterrupt
    elif command_type == 3:
        print(f"{red}Invalid command {user}!{reset}")
    else:
        try:
            exec(command)
        except Exception as err:
            print(f'{red}Invalid command {user}!{reset}')
            print(f'{red}{err}{reset}')

try:
    while True:
        runShell()

except (KeyboardInterrupt, EOFError, ValueError):
    histfile.close()
    print()
    print(yellow+"Exiting cleanly"+reset)
    print()
    sys.exit(1)
