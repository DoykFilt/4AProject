import sys

from SetOfDetection import *
from Parser import Parser

def main(args=sys.argv):
    parser = Parser()
    args.pop(0)
    for arg in args:
        parser.setpath(arg)
        set = parser.parse()
        set.display()
    parser.closeParser()

if __name__ == "__main__":
    sys.exit(main())