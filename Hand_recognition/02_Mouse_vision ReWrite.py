import pyautogui   # control mouse
import time        # 
import cv2         # camera vision
import mediapipe as mp # modulo di riconoscimento -> check
import pygame
import math

from pygame.constants import BUTTON_LEFT

pygame.init()
pygame.font.init()

window = pygame.display.set_mode((300,120))
myfont = pygame.font.SysFont('couriernew', 40)

pygame.display.set_caption('Control: Mouse')


def draw():
    if len(coords) >= 5:
        x = coords[-1]
        z = coords[-2]
        pygame.draw.line(window, (255,255,255),x, z,5)

camera = cv2.VideoCapture(0)  # apri camera al canale 0, il canale dipende a seconda del dispositivo

trova_mani = mp.solutions.hands          # utilizza il modulo Mediapipe per trovare le mani
crea_mani  = trova_mani.Hands(max_num_hands = 1 ,min_detection_confidence=0.6, min_tracking_confidence=0.6)

disegna_mani = mp.solutions.drawing_utils   # trova i punti di flessione della mano e li mostra sullo schermo

run = True
fps = 60
clock = pygame.time.Clock()

coords = []

while run:           # LOOP
    clock.tick(fps)

    pygame.time.delay(0)
    window.fill((0,0,0))
    pygame.display.update()
    window = pygame.display.set_mode((160,100))
    pygame.display.set_caption('ciao')
    window.fill((0,0,0))



    def draw(lista):
        if len(lista) >= 5:
            x = lista[-1]
            z = lista[-2]
            pygame.draw.line(window, (255,255,255),x, z,5)
            pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    success, immagine_mirror = camera.read()                       # trova l'immagine a specchio
    immagine = cv2.flip(immagine_mirror,1)     
    immagine.flags.writeable = False                # ruota l'immagine orizzontalmente
    imgTO_process = cv2.cvtColor(immagine, cv2.COLOR_BGR2RGB)             # cambia i valori del colore -> perchè?
    results = crea_mani.process(imgTO_process)                            # trova la mano con il modulo di computer vision
    #print(results.multi_hand_landmarks)
    
    if results.multi_hand_landmarks:                   # se la mano viene individuata
        circle_green = pygame.draw.circle(window,(0,255,0),(20,40), 5, 10)
        pygame.display.update()
        # render text

        for handLms in results.multi_hand_landmarks:   # per ogni mano che viene individuata
            
            disegna_mani.draw_landmarks(immagine, handLms, trova_mani.HAND_CONNECTIONS) # unisci i punti di flessione all'interno della mano

            for id, lm in enumerate(handLms.landmark): # per ogni punto di flessioni in quante mani trovi 
                h, w, x  = immagine.shape                   # trova larghezza e altezza dello schermo
                cx, cy = int(lm.x*w), int(lm.y*h)      # coordinata x è uguale al valore assoluto tra 0 e 1 moltiplicato per la risoluzione

                
                if id == 8:                            # id 8 = trova la punta dell'indice -> conta le falangi
                    indice_x, indice_y = int(lm.x*w), int(lm.y*h)      # coordinata x è uguale al valore assoluto tra 0 e 1 moltiplicato per la risoluzione
                    indice = cv2.circle(immagine, (indice_x, indice_y), 10, (255, 0, 255), cv2.FILLED) # disegna un cerchio nel punto alle coordinate cx e cy

                elif id == 12:
                    medio_x, medio_y = int(lm.x*w), int(lm.y*h)      # coordinata x è uguale al valore assoluto tra 0 e 1 moltiplicato per la risoluzione
                    medio = cv2.circle(immagine, (medio_x, medio_y), 10, (255, 255,0), cv2.FILLED) # disegna un cerchio nel punto alle coordinate cx e cy

                #una volta che ha tutti i punti che ti servono -> calcola tutte le distanze che ti servono
                elif id == 16:
                    anulare_x, anulare_y = int(lm.x*w), int(lm.y*h)      
                    anulare = cv2.circle(immagine, (anulare_x, anulare_y), 10, (0, 255,0), cv2.FILLED) 
                    
                    distanza_Anul_Index = math.sqrt((anulare_x - indice_x)**2 + (anulare_y - indice_y)**2)
                    print('Distanza Indice Anulare:')
                    print(distanza_Anul_Index)
                  

                    print('Distanza Indice Medio:')
                    distanza_due_dita = math.sqrt((medio_x - indice_x)**2 + (medio_y- indice_y)**2)
                    print(distanza_due_dita)

                    #activation distance
                    lista = []  # la lista si aggiorna a ogni attivazione
                    distanze =[]
                    indice_vel = 0

                    if distanza_Anul_Index <= 90: #:or distanza_due_dita <= 50:
                        action = True

                        for e in range(len(lista)):
                            if e%len(lista)!=1:
                                x , y = lista[e][0], lista[e][1]
                                x1, y1 = lista[e+1][0], lista[e+1][1]
                                #calculate distances
                                distance = math.sqrt((x-x1)**2+(y-y1)**2)
                                distanze.append(distance)
                                num_distances = len(distanze)
                                indice_vel = math.sqrt((sum(distanze)/num_distances)/100)

                        # posizione del mouse -> in mezzo tra le dita
                   
                        print(indice_vel)
                        x_m = (indice_x + abs(medio_x)/2) +indice_vel
                        y_m = (indice_y + abs(medio_y)/2) +indice_vel
                        # inserire lista 
                        lista.append([x_m,y_m])
                        #muovi il muose
                        pyautogui.moveTo(x_m,y_m)
                        

                        # action distance
                        if action:
                            if distanza_Anul_Index <= 55:
                                double = True
                            else:
                                double = False
                                

                            
                            if distanza_due_dita <25:
                                click = True
                            else:
                                click = False

                            counter = 0
                            if counter == 0:
                                pyautogui.mouseUp(x_m, y_m, button = 'left')
                            if double and click:
                                print('Double Click')

                                counter =+1
                                start_pos = pyautogui.position()

                                pyautogui.doubleClick()
                                pyautogui.mouseDown(start_pos[0],start_pos[1],button = 'left')
                                
                                if counter >=10:
                                    print('DRAG')

                                    actual = pyautogui.position()

                                label = myfont.render('DoubleClicked', 1, (255,255,255))
                                window.blit(label, (0, 0))

                            if click and not double:
                                print('click')
                                pyautogui.click()
                                label = myfont.render('Clicked', 1, (255,255,255))
                                window.blit(label, (0, 0))

                            if not click and not double:
                                circle_green = pygame.draw.circle(window,(0,255,0),(20,40), 5, 10)
                                pygame.display.update()


                            draw(lista)
                            pygame.display.update()
                    else:
                        pass
                        

                        
                    
    #show time on the screen
    cv2.imshow('Image', immagine) #show image on the screen
    cv2.waitKey(1)           #image every millisecond

#calcola la media della distanza tra le ultime posizione

#creare una lista delle ultime 100 coordinate 
#usare la lista per calcolare la velocita
#predere la distanza tra i punti sommarla e dividerla per il numero della lunghezza della lista
#usare questo valore per sommarlo all'indice di velocità -> moltiplica

