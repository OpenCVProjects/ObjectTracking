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
    f = open ('resultados.txt','w')

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

                print("Area: ", cv2.contourArea(contour))
                f.write("Area: ")
                f.write(str(cv2.contourArea(contour)))
                print("\n")

                (x, y, w, h) = cv2.boundingRect(contour)
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)

                print("Y", y)
                route.append(y)
                print ("Recorrido: ", route)

                f.write("Y: ")
                f.write(str(y))
                f.write("\n")
                f.write("Recorrido: ")
                f.write(str(route))
                f.write("\n")

                if y > 140 and y < 181 and len(route) >= 3 :
                    print ("Recorrido Final: ", route)
                    f.write("------------------------------- RECORRIDO FINAL: ")
                    f.write(str(route))
                    f.write("\n")
                    padentro = getRoute(route)
                    print("++++++++++PA DENTRO", str(padentro))
                    f.write("++++++++++PA DENTRO")
                    f.write(str(padentro))
                    f.write("\n")
                    if getRoute(route):
                        print("Sube")
                        f.write("*-*-*-*--*-*-*-*-*-*-*- SUBE")
                        f.write("\n")
                        counter = counter + 1
                        route = []
                    else:
                        print("baja")
                        f.write("*-*-*-*--*-*-*-*-*-*-*- BAJA")
                        f.write("\n")
                        counter = counter - 1
                        route = []


            print ("Contador", counter)
            self.lcdNumber.display(counter)
            f.write("*-*-*-*--*-*-*-*-*-*-*- CONTADOR *-*-*-*--*-*-*-*-*-*-*-")
            f.write("\n")
            f.write(str(counter))
            f.write("\n")

            time.sleep(0.5)

            cv2.imshow("Frame", frame)
            cv2.moveWindow("Frame", 270, 350)

            cv2.imshow("Thresh Delta", thresh_frame)
            cv2.moveWindow("Thresh Delta", 700, 350)

            key = cv2.waitKey(1)
            if key == ord('q'):
                break

    video.release()
    cv2.destroyAllWindows

if __name__ == "__main__":
    counterPeople()
