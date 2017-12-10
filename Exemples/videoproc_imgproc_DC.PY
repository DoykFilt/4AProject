import numpy as np
import cv2
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt


# Callback vide....
def nothing(x):
    pass

# Callback slider for T
def callback1(x):
    T = x


def imgproc(imgc, imgp):

    #imgc = cv2.medianBlur(imgc, 5)

    #filtering with kernel
    kernel1 = np.ones((9, 9), np.float32) / 25
    imgc = cv2.filter2D(imgc, -1, kernel1)
    imgp = cv2.filter2D(imgp, -1, kernel1)

    # Sobel
    #imgtemp = cv2.Sobel(imgc, cv2.CV_64F, 1, 0, ksize=3)
    #imgc = cv2.Sobel(imgtemp, cv2.CV_64F, 0, 1, ksize=3)
    #imgc = cv2.add(imgc,imgtemp)

    # Laplacien
    # imgc = cv2.Laplacian(imgc, cv2.CV_64F)

    #Canny
    #imgc = cv2.Canny(imgc, 100, 200)

    #soustraction
    imgc = cv2.absdiff(imgc,imgp)

    # Binarisation
    ret, imgc = cv2.threshold(imgc, 127, 255, cv2.THRESH_BINARY)
    kernel2 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))
    cv2.erode(imgc, kernel2, imgc, iterations=2)
    cv2.dilate(imgc, kernel2, imgc, iterations=2)

    #analysis of the conttours
    imgc, contours, hierarchy = cv2.findContours(imgc, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #cv2.drawContours(frame, contours, -1, (255, 0, 0), 3)    # -1 = tous au lieu de donner un numero de contours

    density = 0
    for cnt in contours :
        #cv2.drawContours(frame, [cnt], 0, (0, 255, 0), -1)
        density = density + cv2.contourArea(cnt)

    return imgc, density

def countDescriptorMatchings(img1, img2, matchThreshold):
    #cv2.imshow("img1", img1)
    #cv2.imshow("img2", img2)
    
    #print(type(img1),type(img2))
    # Initiate SIFT detector
    sift = cv2.xfeatures2d.SIFT_create()
    
    # find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(img1,None)
    kp2, des2 = sift.detectAndCompute(img2,None)

    if des1 is not None and des2 is not None:
        # BFMatcher with default params
        bf = cv2.BFMatcher()
        matches = bf.knnMatch(des1,des2, k=2)

        # Apply ratio test
        good = []
        for m,n in matches:
            if m.distance < matchThreshold*n.distance:
                good.append([m])

        # cv2.drawMatchesKnn expects list of lists as matches.
        img3 = cv2.drawMatchesKnn(img1,kp1,img2,kp2,good,img2, flags=2)

        cv2.imshow("img3", img3)
        cv2.waitKey(20)
        return len(good)
    else:
        return 0
    
   

def chooseImageFromDescriptors(lstImages, matchThreshold):
    
    if len(lstImages)<2:
        return None
    
    listCountMatching = []
    for ind in range(len(lstImages)-1):
        listCountMatching.append(countDescriptorMatchings(lstImages[ind],lstImages[ind+1], matchThreshold))

    indMax = np.argmax(listCountMatching)
    #print (listCountMatching, indMax)
    return lstImages[indMax]
        
    
    

# cap = cv2.VideoCapture('C:\\house.avi')
cap = cv2.VideoCapture('data/starwars.mp4')

T=10000
duration = 30
cpt = 0
matchThreshold = 0.0005

#Creation fenetre Affichage Result
cv2.namedWindow('Input', cv2.WINDOW_AUTOSIZE | cv2.WINDOW_GUI_EXPANDED)
cv2.namedWindow('Result', cv2.WINDOW_AUTOSIZE | cv2.WINDOW_GUI_EXPANDED)
cv2.createTrackbar("Threshold","Result",T,99999,callback1)

#Creation image vide
#blank_image = np.zeros((10,10,3), np.uint8)
#blank_image[:,0:0.5*width] = (255,0,0)      # (B, G, R)
#blank_image[:,0.5*width:width] = (0,255,0)
#cv2.imshow('Result',blank_image)

lstImages=[]
while (True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    if ret == True:
        # Our operations on the frame come here
        cpt = cpt + 1

        #First Frame cannot be processed but histogram is shown
        if (cpt > 1):
            # Update frame succession
            previous = gray.copy()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Next frame processing
            imgshow, intensity = imgproc(gray, previous)

            # Display the initial and resulting frames
            cv2.imshow('Input', frame)
            cv2.imshow('Result', imgshow)

            # Gestion IHM
            T = cv2.getTrackbarPos('Threshold', 'Result')

            #Display Textual results
            if (intensity > T):
                duration = 200
                #cv2.displayOverlay("Result", "CUT :" + str(intensity), 10)
                #cv2.displayStatusBar("Result", "CUT :" + str(intensity))
                average = chooseImageFromDescriptors(lstImages, matchThreshold)
                cv2.imwrite("summary//" + str(cpt) + ".png",average)
                lstImages = []
                lstImages.append(frame)
            else:
                #average = cv2.addWeighted(average,0.5,frame,0.5,0)
                lstImages.append(frame)
                duration = 30
                


        else:
            #Draw color histogram of first frame
            #color = ('b', 'g', 'r')
            #for i, col in enumerate(color):
            #    histr = cv2.calcHist([frame], [i], None, [256], [0, 256])
            #    plt.plot(histr, color=col)
            #    plt.xlim([0, 256])
            plt.get_current_fig_manager().window.setGeometry(10,500,200,200)
            plt.show(block=False,)

            # Show and converted first frame
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            cv2.imshow('Input', frame)
            cv2.moveWindow('Input', 10, 10)

            # Adapt Threshold to Frame size
            height, width, channels = frame.shape
            T = int((height * width) / 8)
            cv2.setTrackbarPos('Threshold', 'Result', T)

            average = frame.copy()

    else:
        print('video ended')
        break

    if cv2.waitKey(duration) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
