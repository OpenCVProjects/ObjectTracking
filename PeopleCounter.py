import cv2
import time

def nothing(x):
    pass

#Creates a window with the differents trackbar
def controlBoard():
    cv2.namedWindow("Control Window")
    cv2.createTrackbar("Threshold Min", "Control Window", 30, 255, nothing)
    cv2.createTrackbar("Threshold Max", "Control Window", 255, 255, nothing)
    cv2.moveWindow("Control Window", 270, 150)

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

def counterPeople(self):

    #Saves the first frame
    first_frame = None

    #Number of people inside the classroom
    counter = 0

    #Travel followed by a person
    route = []

    video = cv2.VideoCapture("../video.wmv")

    min_value_threshold = any
    max_value_threshold = any

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
                if cv2.contourArea(contour) < 10100:
                    continue

                (x, y, w, h) = cv2.boundingRect(contour)
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)

                route.append(y)

                if y > 140 and y < 181 and len(route) >= 3 :
                    if getRoute(route):
                        counter = counter + 1
                        route = []
                    else:
                        counter = counter - 1
                        route = []

            self.lcdNumber.display(counter)

            cv2.imshow("Frame", frame)
            cv2.moveWindow("Frame", 270, 350)

            cv2.imshow("Thresh Delta", thresh_frame)
            cv2.moveWindow("Thresh Delta", 700, 350)

            key = cv2.waitKey(1)
            if key == ord('q'):
                break

    video.release()
    cv2.destroyAllWindows
