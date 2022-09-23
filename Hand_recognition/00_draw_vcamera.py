import pyautogui   # control mouse
import time        # 
import cv2         # camera vision
import mediapipe as mp # modulo di riconoscimento -> check
import pygame
pygame.init()

ciao = pygame.display.set_mode((1200,750))
pygame.display.set_caption('TITLE')
ciao.fill((0,0,0))



def draw():
    if len(coords) >= 5:
        x = coords[-1]
        z = coords[-2]
        pygame.draw.line(ciao, (255,255,255),x, z,5)
        pygame.display.update()


camera = cv2.VideoCapture(0)  # apri camera al canale 0, il canale dipende a seconda del dispositivo

trova_mani = mp.solutions.hands          # utilizza il modulo Mediapipe per trovare le mani
crea_mani  = trova_mani.Hands(max_num_hands=1,min_detection_confidence=0.1, min_tracking_confidence=0.1)

disegna_mani = mp.solutions.drawing_utils   # trova i punti di flessione della mano e li mostra sullo schermo

run = True
fps = 60
clock = pygame.time.Clock()

coords = []

while run:                                             # LOOP
    clock.tick(fps)

    pygame.time.delay(0)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    success, immagine_mirror = camera.read()          # trova l'immagine a specchio
    immagine = cv2.flip(immagine_mirror,1)                         # ruota l'immagine orizzontalmente
    imgRGB = cv2.cvtColor(immagine, cv2.COLOR_BGR2RGB)       # cambia i valori del colore -> perchè?
    results = crea_mani.process(imgRGB)                     # trova la mano con il modulo di computer vision

    #print(results.multi_hand_landmarks)
    
    if results.multi_hand_landmarks:                   # se la mano viene individuata

        for handLms in results.multi_hand_landmarks:   # per ogni mano che viene individuata
            disegna_mani.draw_landmarks(immagine, handLms, trova_mani.HAND_CONNECTIONS) # unisci i punti di flessione all'interno della mano

            for id, lm in enumerate(handLms.landmark): # per ogni punto di flessioni in quante mani trovi 
                h, w, x  = immagine.shape                   # trova larghezza e altezza dello schermo
                cx, cy = int(lm.x*w), int(lm.y*h)      # coordinata x è uguale al valore assoluto tra 0 e 1 moltiplicato per la risoluzione
                
                if id == 8:                            # id 8 = trova la punta dell'indice -> conta le falangi
                    cv2.circle(immagine, (cx, cy), 25, (255, 0, 255), cv2.FILLED) # disegna un cerchio nel punto alle coordinate cx e cy
                    #pyautogui.moveTo(cx,cy)                                  #punta il mouse alle cordinate della punta dell'indice      
                    coords.append((cx,cy)) 

                    draw()

    
    #show time on the screen
    cv2.imshow('Image', immagine) #show image on the screen
    cv2.waitKey(1)           #image every millisecond

