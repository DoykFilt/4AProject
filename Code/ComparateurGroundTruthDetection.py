#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      thiba
#
# Created:     18/12/2017
# Copyright:   (c) thiba 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import sys
import cv2
import time
from Parser import Parser

def getImagePath(pathDossier, nImage):
    numeroImage = "%d" % nImage
    while len(numeroImage) != 6:
        numeroImage = "0" + numeroImage
    return pathDossier + "\\" + numeroImage + ".jpg"

def getSetsofDetections(pathDetection, pathGT):
    parser = Parser()

    parser.setpath(pathDetection)
    set1 = parser.parse()
    parser.setpath(pathGT)
    set2 = parser.parse()

    parser.closeParser()
    return set1, set2

def main(args=sys.argv):
    #Le nombre d'image en premier et le dossier en deuxième
    nbrImages = int(args[1])
    pathDossier = args[2]
    #Les detections en 3 et les ground truth en 4
    setOfDetections, setOfGT = getSetsofDetections(args[3], args[4])

    for nImage in range(1, nbrImages):
        imageGroundTruth = cv2.imread(getImagePath(pathDossier, nImage), cv2.IMREAD_COLOR)
        imageDetection = cv2.imread(getImagePath(pathDossier, nImage), cv2.IMREAD_COLOR)

        #On ajoute tout les triangles par image
        for i in range(0, setOfDetections.getSize()):
            detectionDico = setOfDetections.getDetection(i).get()
            if int(detectionDico["frame"]) == nImage:
                cv2.rectangle(imageDetection, (int(detectionDico["bb_left"]), int(detectionDico["bb_top"])),
                            (int(detectionDico["bb_left"] + detectionDico["bb_width"]), int(detectionDico["bb_top"] + detectionDico["bb_height"])),
                            (200, 200, 200));
        for i in range(0, setOfGT.getSize()):
            detectionDico = setOfGT.getDetection(i).get()
            if int(detectionDico["frame"]) == nImage:
                cv2.rectangle(imageGroundTruth, (int(detectionDico["bb_left"]), int(detectionDico["bb_top"])),
                            (int(detectionDico["bb_left"] + detectionDico["bb_width"]), int(detectionDico["bb_top"] + detectionDico["bb_height"])),
                            (detectionDico["id"], detectionDico["id"], detectionDico["id"]), int(5));

        imageGroundTruth = cv2.resize(imageGroundTruth, (800, 600))
        imageDetection = cv2.resize(imageDetection, (800, 600))

        cv2.imshow('groundTruth', imageGroundTruth)
        cv2.imshow('detections', imageDetection)
        cv2.waitKey(1);

if __name__ == "__main__":
    sys.exit(main())




