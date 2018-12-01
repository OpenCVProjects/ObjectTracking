import cv2, time

first_frame = None

video = cv2.VideoCapture("../video.wmv")

contador = 0
sentido = 0
entra = False
recorrido = []

f = open ('resultados.txt','w')

if video.isOpened() == False:
    print("Error: Fallo al abrir el video")

while video.isOpened():
    check, frame = video.read()
    if check == True:
        status  = 0

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray,(9, 9), 0)

        if first_frame is None:
            first_frame = gray
            continue

        delta_frame = cv2.absdiff(first_frame, gray)

        thresh_frame = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]

        thresh_frame = cv2.dilate(thresh_frame, None, iterations=2)

        (_,cnts,_) = cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        img = cv2.line(frame,(0,210),(200,210),(0,255,0),4)

        for contour in cnts:
            if cv2.contourArea(contour) < 10100:
                continue

            print("Area: ", cv2.contourArea(contour))
            f.write("Area: ")
            f.write(str(cv2.contourArea(contour)))
            print("\n")

            (x, y, w, h) = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)

            print("Sentido", sentido)
            print("Y", y)
            recorrido.append(y)
            print ("Recorrido: ", recorrido)

            f.write("Sentido: ")
            f.write(str(sentido))
            f.write("\n")
            f.write("Y: ")
            f.write(str(y))
            f.write("\n")
            f.write("Recorrido: ")
            f.write(str(recorrido))
            f.write("\n")

            if y < sentido:
                print("sale")
                entra = False
            else:
                print("entra")
                entra = True

            sentido = y
            print ("Entrar: ", entra)
            f.write("******** ENTRAR :")
            f.write(str(entra))
            f.write("\n")
            if y > 140 and y < 181 and len(recorrido) >= 3 :
                print ("Recorrido Final: ", recorrido)
                f.write("------------------------------- RECORRIDO FINAL: ")
                f.write(str(recorrido))
                f.write("\n")
                if entra:
                    print("Sube")
                    f.write("*-*-*-*--*-*-*-*-*-*-*- SUBE")
                    f.write("\n")
                    contador = contador + 1
                    entra = False
                    sentido = 180
                    recorrido = []
                else:
                    print("baja")
                    f.write("*-*-*-*--*-*-*-*-*-*-*- BAJA")
                    f.write("\n")
                    contador = contador - 1
                    entra = True
                    sentido = 0
                    recorrido = []

        print ("Contador", contador)
        f.write("*-*-*-*--*-*-*-*-*-*-*- CONTADOR *-*-*-*--*-*-*-*-*-*-*-")
        f.write("\n")
        f.write(str(contador))
        f.write("\n")

        time.sleep(0.53)
        cv2.imshow("Frame", frame)

        cv2.imshow("Thresh Delta", thresh_frame)

        key = cv2.waitKey(1)
        if key == ord('q'):
            break

video.release()
cv2.destroyAllWindows
