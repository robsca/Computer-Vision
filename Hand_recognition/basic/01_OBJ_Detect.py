
import pyautogui   # control mouse
import time      
import cv2         #camera vision
import mediapipe as mp # modulo di riconoscimento -> check


image_captured = cv2.VideoCapture(0)  # apri camera al canale 0, il canale dipende a seconda del dispositivo
mphands = mp.solutions.hands          # utilizza il modulo Mediapipe per trovare le mani
hands = mphands.Hands()

mpDraw = mp.solutions.drawing_utils   # trova i punti di flessione della mano e li mostra sullo schermo

def main():
    mouse_x = 500
    mouse_y = 500
    coords_in_time = []
    while True:                                             # LOOP

        clock = time.perf_counter() * 40  #  measer time in 1/60 seconds
        sleep = int(clock) + 1 - clock   #  time till the next 1/60 
        time.sleep(sleep/40)      


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

                    if id == 8:                            # id 8 = trova la punta dell'indice -> conta le falangi
                        #trova le coordinate della falange
                        cv2.circle(img, (cx, cy), 25, (255, 0, 255), cv2.FILLED) # disegna un cerchio nel punto alle coordinate cx e cy
                        #mettile le ultime 100 in una lista
                        coords_in_time.append([cx,cy])
                        if len(coords_in_time) >= 100:
                            del coords_in_time[0]
                        #lunghezza lista
                        print(len(coords_in_time))
                        #coordinate
                        c = coords_in_time[::-1]
                        #print(c)
                        #le ultime dieci coordinate
                        last_ten = c[:10]
                        #le ultime due
                        last_two = last_ten[:2]
                        print(last_two[0])
                        if len(last_two) == 2:
                            print(f'Lastest 2 coordinates: {last_two}')
                            print(f'current position: {last_two[0]}')
                            print(f'precedent position: {last_two[1]}')

                            x1 = last_two[0][0]
                            x2 = last_two[1][0]
                            y1 = last_two[0][1]
                            y2 = last_two[1][1]

                            difference_x = x1 - x2
                            difference_y = y1 - y2
                            print(difference_x)
                            print(difference_y)

                            
                        
                            
                            
                            pyautogui.moveTo(mouse_x, mouse_y)


                            

                                


                            






        cv2.imshow('Image', img) #show image on the screen

        cv2.waitKey(1)
if __name__ == '__main__':
    main() 