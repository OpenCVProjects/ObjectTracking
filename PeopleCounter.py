import cv2, time

first_frame = None

video = cv2.VideoCapture("../video.wmv")

contador = 0
sentido = 0
entra = False

if video.isOpened() == False:
    print("Error: Fallo al abrir el video")

while video.isOpened():
    check, frame = video.read()

    if check == True:
        status  = 0

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray,(21, 21), 0)

        if first_frame is None:
            first_frame = gray
            continue

        delta_frame = cv2.absdiff(first_frame, gray)

        thresh_frame = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]

        thresh_frame = cv2.dilate(thresh_frame, None, iterations=2)

        (_,cnts,_) = cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        img = cv2.line(frame,(0,210),(200,210),(0,255,0),4)

        for contour in cnts:
            if cv2.contourArea(contour) < 15000:
                continue

            status = 1
            (x, y, w, h) = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)
            # sentido.append(x)

            print("Sentido", sentido)
            print("Y", y)
            if y < sentido:
                print("sale")
                entra = False
            else:
                print("entra")
                entra = True

            sentido = y
            print ("Entrar: ", entra)
            if y > 140 and y < 170:
                if entra:
                    print("Sube")
                    contador = contador + 1
                    entra = False
                    sentido = 180
                else:
                    print("baja")
                    contador = contador - 1
                    entra = True
                    sentido = 0

            # print("X", x)
            # print("Y", y)

        # print("sentido Final", sentido)
        print ("Contador", contador)

        time.sleep(1/10)
        cv2.imshow("Frame", frame)

        cv2.imshow("Thresh Delta", thresh_frame)

        key = cv2.waitKey(1)
        if key == ord('q'):
            break

        # print status

video.release()
cv2.destroyAllWindows
