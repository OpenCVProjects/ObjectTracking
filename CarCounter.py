import cv2
import time
import numpy as np


min_value_threshold = any
max_value_threshold = any

def nothing(x):
    pass

#Creates a window with the differents trackbar
def controlBoard():
    cv2.namedWindow("Control Window")
    cv2.createTrackbar("Threshold Min", "Control Window", 30, 255, nothing)
    cv2.createTrackbar("Threshold Max", "Control Window", 255, 255, nothing)
    # cv2.moveWindow("Control Window", 270, 150)

#Prepare a frame to work with it
def preparareFrame(first_frame, gray):
    delta_frame = cv2.absdiff(first_frame, gray)
    thresh_frame = cv2.threshold(delta_frame, min_value_threshold, max_value_threshold, cv2.THRESH_BINARY)[1]
    thresh_frame = cv2.dilate(thresh_frame, None, iterations=2)
    return thresh_frame

#Gets if a people go in or go out
def getRoute(route):
    pos = route[0]
    goIn = True
    for i in route:
        if i >= pos:
            goIn = True
        else:
            goIn = False
        pos = i
    return goIn

def counterPeople():

    #Saves the first frame
    first_frame = None

    #Number of people inside the classroom
    # counter = 0
    counter1 = 0
    # counter2 = 0
    # counter3 = 0
    # counter4 = 0
    # counter5 = 0

    #Travel followed by a person
    # route = []

    video = cv2.VideoCapture("../rotonda.MOV")


    controlBoard()

    if video.isOpened() == False:
        print("Error: Fallo al abrir el video")


    while video.isOpened():
        global min_value_threshold
        global max_value_threshold

        min_value_threshold = cv2.getTrackbarPos("Threshold Min", "Control Window")
        max_value_threshold = cv2.getTrackbarPos("Threshold Max", "Control Window")

        check, frame = video.read()
        if check == True:
            status  = 0

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray,(9, 9), 0)

            if first_frame is None:
                first_frame = gray
                continue

            thresh_frame = preparareFrame(first_frame, gray)

            (_,cnts,_) = cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            for contour in cnts:
                if cv2.contourArea(contour) < 4000 or cv2.contourArea(contour) > 19000:
                    continue

                (x, y, w, h) = cv2.boundingRect(contour)
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)

                x = x + w/2
                y = y + h/2

                # print("X", x)
                # print("Y", y)

                route.append(y)

                # if ( (x > 599 and x <= 606) and ( y >= 473 and y < 600)  ):
                #     counter = counter + 1
                #     print(cv2.contourArea(contour))

                if ( (x > 616 and x <= 623) and ( y >= 473 and y < 600)  ):
                    counter1 = counter1 + 1

                # if ( (x > 630 and x <= 637) and ( y >= 473 and y < 600)  ):
                #     counter2 = counter2 + 1
                #
                # if ( (x > 640 and x <= 647) and ( y >= 473 and y < 600)  ):
                #     counter3 = counter3 + 1
                #
                # if ( (x > 650 and x <= 657) and ( y >= 473 and y < 600)  ):
                #     counter4 = counter4 + 1
                #
                # if ( (x > 760 and x <= 767) and ( y >= 473 and y < 600)  ):
                #     counter5 = counter5 + 1

                # if x > 500 and x < 600: and len(route) >= 3 :
                #     if getRoute(route):
                #         counter = counter + 1
                #         route = []
                #     else:
                #         counter = counter - 1
                #         route = []

            # self.lcdNumber.display(counter1)

            # width, height = frame.shape[:2]
            # print ("Width: ", width)
            # print ("height: ", height)
            # height = np.size(image, 0)
            # width = np.size(image, 1)
            # print ("Width: ", frame)
            # print ("height: ", frame)

            # frame = cv2.line(frame,(600,600),(600,400),(0,255,0),4)
            #
            # frame = cv2.line(frame,(620,600),(620,400),(0,255,0),4)
            # frame = cv2.line(frame,(635,600),(635,400),(0,255,0),4)
            # frame = cv2.line(frame,(645,600),(645,400),(0,255,0),4)
            # frame = cv2.line(frame,(655,600),(655,400),(0,255,0),4)
            # frame = cv2.line(frame,(765,600),(765,400),(0,255,0),4)
            cv2.imshow("Frame", frame)
            # cv2.moveWindow("Frame", 270, 350)

            cv2.imshow("Thresh Delta", thresh_frame)
            # cv2.moveWindow("Thresh Delta", 700, 350)

            # time.sleep(0.59)

            # print ("C", counter)
            print ("c1", counter1)
            # print ("C2", counter2)
            # print ("C3", counter3)
            # print ("C4", counter4)
            # print ("C5", counter5)


            key = cv2.waitKey(1)
            if key == ord('q'):
                break

    video.release()
    cv2.destroyAllWindows

if __name__ == "__main__":
    counterPeople()
