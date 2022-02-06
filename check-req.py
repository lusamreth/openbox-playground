#!/bin/python3

import os
import sys
import select

pwd = os.getcwd()
files_res = os.listdir(pwd)

req = [
    "header",
    "footer",
]

toXml = lambda f: "{}.xml".format(f)
required = list(map(toXml, req))

i = iter(range(len(files_res)))
files = dict(zip(files_res, i))


def check_req(files):
    leftover = []
    for p in required:
        if not p in files:
            leftover.append(p)
    return leftover


leftover = check_req(files)


def createMsg():

    msg = ""
    llen = len(leftover)
    for i, file in enumerate(leftover):
        msg += "-" + file
        if i != llen - 1 and llen > 1:
            msg += "\n"
    print("still require:")
    print(msg)


def createReq():
    for file in required:
        open(file, "+x")


def extract_std():
    print("Do you want to create these files?[Y/N]")
    std_input, _, _ = select.select([sys.stdin], [], [], 10)
    return std_input


def input_handler(userinput, callback):
    if userinput == "y":
        createReq()
    elif userinput == "n":
        print("Unable to glue in to rc.xml")
        exit(0)
    else:
        print("Answer is yes or no! Not anything else")
        callback()


def askIfcreate():
    std_input = extract_std()

    if std_input:
        userinput = sys.stdin.readline().strip().lower()
        input_handler(userinput, askIfcreate)
    else:
        print("Program timeout! exiting...")
        exit(0)

    userinput = sys.stdin.readline().strip()


if len(leftover) != 0:
    createMsg()
    askIfcreate()
