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

class SetOfDetection:
    def __init__(self):
        self.set = []

    def append(self, detection):
        if isinstance(detection, Detection):
            self.set.append(detection)

    def delete(self, index):
        self.set.pop(index)

    def getNumberOfDetection(self):
        self.set.__len__

    def display(self):
        for detection in self.set:
            detection.display()

    def getSize(self):
        return len(self.set)

    def getDetection(self, i):
        return self.set[i]

class Detection:
    def __init__(self):
        self.dictionary = {}
        self.dictionary["frame"] = 0
        self.dictionary["id"] = -1
        self.dictionary["bb_left"] = 0.0
        self.dictionary["bb_top"] = 0.0
        self.dictionary["bb_height"] = 0.0
        self.dictionary["bb_width"] = 0.0

    def fill(self, frame, id, bb_left, bb_top, bb_width, bb_height):
        self.dictionary["frame"] = int(frame)
        self.dictionary["id"] = int(id)
        self.dictionary["bb_left"] = float(bb_left)
        self.dictionary["bb_top"] = float(bb_top)
        self.dictionary["bb_height"] = float(bb_height)
        self.dictionary["bb_width"] = float(bb_width)

    def assignId(self, id):
        self.dictionary["id"] = int(id)

    def get(self):
        return self.dictionary

    def display(self):
        print(self.dictionary["frame"], self.dictionary["bb_left"],
        self.dictionary["bb_top"], self.dictionary["bb_height"],
        self.dictionary["bb_width"])