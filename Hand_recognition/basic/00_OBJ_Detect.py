import pyautogui   # control mouse
import time        # 
import cv2         # camera vision
import mediapipe as mp # modulo di riconoscimento -> check


image_captured = cv2.VideoCapture(0)  # apri camera al canale 0, il canale dipende a seconda del dispositivo
mphands = mp.solutions.hands          # utilizza il modulo Mediapipe per trovare le mani
hands = mphands.Hands(max_num_hands=1,min_detection_confidence=0.5, min_tracking_confidence=0.2)

mpDraw = mp.solutions.drawing_utils   # trova i punti di flessione della mano e li mostra sullo schermo

counter = 0

last_ten = []
xs = []
ys = []

x_counter = 0
y_counter = 0


while True:                                             # LOOP


    success, img_right = image_captured.read()          # trova l'immagine a specchio

    img = cv2.flip(img_right,1)                         # ruota l'immagine orizzontalmente

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)       # cambia i valori del colore -> perchè?

    results = hands.process(imgRGB)                     # trova la mano con il modulo di computer vision

    #print(results.multi_hand_landmarks)
    
    if results.multi_hand_landmarks:                   # se la mano viene individuata
        

        for handLms in results.multi_hand_landmarks:   # per ogni mano che viene individuata

            mpDraw.draw_landmarks(img, handLms, mphands.HAND_CONNECTIONS) # unisci i punti di flessione all'interno della mano

            for id, lm in enumerate(handLms.landmark): # per ogni punto di flessioni in quante mani trovi
                
                h, w, x  = img.shape                   # trova larghezza e altezza dello schermo

                cx, cy = int(lm.x*w), int(lm.y*h)      # coordinata x è uguale al valore assoluto tra 0 e 1 moltiplicato per la risoluzione
                x_center, y_center = int(w/2), int(h/2)

                
# trova la punta dell'indice 
                if id == 8:                            
                    cv2.circle(img, (cx, cy), 10, (255, 0, 255), cv2.FILLED) # disegna un cerchio nel punto alle coordinate cx e cy
                    cv2.circle(img, (x_center, y_center), 10, (222,222,222), cv2.FILLED)

#               #crea una record delle ultime 100 coordinate 
                last_ten.append((cx,cy))
                if len(last_ten) > 10:
                    last_ten.pop(0)

                for items in last_ten:
                    xs.append(items[0])
                    if len(xs) > 10:
                        xs.pop(0)
                    ys.append(items[1])
                    if len(ys) > 10:
                        ys.pop(0)

                    for x in xs:
                        x_counter = x_counter + x

                    for y in ys:
                        y_counter = y_counter + y

                    #mouse_x = (int(x_counter/len(last_ten)))
                    #mouse_y = (int(y_counter/len(last_ten)))
                    mouse_x = cx
                    mouse_y = cy
                    x_counter = 0
                    y_counter = 0


                print()

                print(mouse_y)
                

                counter += 1
                if counter >10:
                    pyautogui.moveTo(mouse_x, mouse_y)                                  #punta il mouse alle cordinate della punta dell'indice  
                    counter = 0

    
    #show time on the screen

    cv2.imshow('Image', img) #show image on the screen

    cv2.waitKey(1)