from sys import argv
from os import system

if '-n' not in argv:
    system('clear')
else:
    for _ in range(argv.count('-n')):
        argv.remove('-n')

try:
    switch = argv[1]
except:
    switch = '-e'
try:
    value = argv[2:]
except:
    value = []

if not switch.startswith('-'):
    value.insert(0,switch)
    switch = '-e'