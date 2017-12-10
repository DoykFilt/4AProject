#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      thiba
#
# Created:     10/12/2017
# Copyright:   (c) thiba 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from SetOfDetection import *

class Parser:
    def __init__(self):
        self.path = ""
        self.file = None

    def setpath(self, path):
        self.path = path
        if self.file != None:
            self.file.close()
        self.file = open(path, "r")

    def closeParser(self):
        if self.file != None:
            self.file.close()

    def parse(self):
        if self.file != None:
            file_content = self.file.read()
            file_content = file_content.split("\n")
            setOfDetection = SetOfDetection()
            del file_content[-1]
            for line in file_content:
                detection = Detection()
                tab = line.split(",")
            #In line :frame, id, bb_left, bb_top, bb_width, bb_height, x, y, z
                detection.fill(tab[0], tab[2], tab[3], tab[4], tab[5])
                setOfDetection.append(detection)
            return setOfDetection
        return None


