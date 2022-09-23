import cv2, time, mediapipe as mp

class identificatoreMani():
    def __init__(self, mode = False, maxHands = 2, detectionCon = 0.7, trackCon = 0.8):
    #Hyperparameters
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon
    # module recognizer
        self.mpHands = mp.solutions.hands
    #find hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.detectionCon, self.trackCon)
    #find structure
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw = True):
    #transform image
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    #process image
        results = self.hands.process(imgRGB) # -> data about the detections
    #analize results
        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img
    
        
def main():
#apri camera
    camera  = cv2.VideoCapture(0)
    
#crea oggetto
    detector = identificatoreMani()

#loooooooop
    while True:
        success, img = camera.read()
        detector.findHands(img)

        cv2.imshow('IMAGE', img)
        cv2.waitKey(1)

if __name__ == '__main__':
    main()