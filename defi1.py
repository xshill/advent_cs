#!/usr/bin/env python3
import subprocess, re, urllib
args = "netcat workshop.dciets.com 8111".split(" ")
proc = subprocess.Popen(args, stdout=subprocess.PIPE)

while True:
    line = proc.stdout.readline().decode("ascii").strip()
    if line != '':
        match = re.match("What is the birth year of ([a-zA-z ]+) ?", line)
        if match is not None:
            name = match.group(1).strip()
            print(name)
        elif line != "Wrong" and line != "Timeout":
            pass
        else:
            pass
    else:
        break
