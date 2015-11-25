# -*- coding:utf-8 -*-

# Title: WordPressChecker
# Date: 16/01/2015
# Author: Spire
# Version: 1.0

import sys
import requests
from bs4 import BeautifulSoup

argc = len(sys.argv)
argv = sys.argv

__IFILE__ = "./list.txt"
__OFILE__ = "./results.txt"

class Finder:
    def __init__(self, iFile = __IFILE__, oFile = __OFILE__):
        self.iFile = str(iFile)
        self.oFile = str(oFile)

    def run(self):
        print "\nRunning with this file: \"" + self.iFile + "\"..."

        with open(self.iFile) as f:
            urls = f.readlines()

        i = 1
        for url in urls:
            try:
                r = requests.get(url.lower().rstrip())
            except requests.exceptions.RequestException as e:
                print "\n[ERROR] " + str(e)
                print "\nPlease check " + self.iFile
                sys.exit(1)
            else:
                if i == 1:
                    f = open(self.oFile, "w")
                    f.write("")

                f = open(self.oFile, "a")

                start = "\n----------------------------------------\nWebsite: " + r.url + "\nStatus code: " + str(r.status_code) + "\n"
                f.write(start)
                print start

                html = BeautifulSoup(r.text)

                if html.find("meta", {"name" : "generator"}) is None:
                    fail = "[FAIL] Not running under WordPress"
                    f.write(fail)
                    print fail
                else:
                    success = "[OK] Version: " + str(html("meta", {"name" : "generator"})[0].get("content"))
                    f.write(success)
                    print success

                end = "\n----------------------------------------\n"
                f.write(end)
                print end

                if i >= len(urls):
                    print "Checking done \o/\nLogs here: " + self.oFile
                i += 1

        f.close()

def usage():
    print "\n\n------------------------- WordPressChecker 1.0 -------------------------\n\n"
    print "Usage: wpchecker.py [input file] [output file]\n"
    print "input file: websites list (default value: \"" + __IFILE__ + "\")"
    print "output file: scan results (default value: \"" + __OFILE__ + "\")"

def main():
    if argc == 1:
        finder = Finder()
    elif argc == 2:
        finder = Finder(argv[1])
    elif argc == 3:
        finder = Finder(argv[1], argv[2])
    elif argv > 3:
        usage()
        sys.exit(0)
    else:
        finder = Finder()

    finder.run()

if __name__ == '__main__':
    main()