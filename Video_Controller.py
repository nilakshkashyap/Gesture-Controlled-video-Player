from cvzone.HandTrackingModule import HandDetector
import cv2

cap=cv2.VideoCapture(0)
detector = HandDetector(maxHands=1, detectionCon=0.95)

"""
    fist: play,
    palm: pause,
    index finger: rewind,
    thumb: forward
"""
player = cv2.VideoCapture("video.mp4")

cv2.namedWindow("Video")
cv2.moveWindow("Video", 50, 100)

cv2.namedWindow("Camera")
cv2.moveWindow("Camera", 700, 100)
while True:
    ret1,frame1 = cap.read()
    frame1 = cv2.flip(frame1, 1)
    hands, frame1 = detector.findHands(frame1)
    ret2, frame2 = player.read()
    gesture=None
    if player.get(cv2.CAP_PROP_POS_FRAMES) >= player.get(cv2.CAP_PROP_FRAME_COUNT) - 1:
        player.set(cv2.CAP_PROP_POS_FRAMES, player.get(cv2.CAP_PROP_POS_FRAMES) - 1)
    else:
        player.set(cv2.CAP_PROP_POS_FRAMES, player.get(cv2.CAP_PROP_POS_FRAMES))
    if hands:
        hand1=hands[0]
        fingers = detector.fingersUp(hand1)
        if fingers==[0,0,0,0,0]:
            gesture="fist"
        elif fingers==[1,1,1,1,1]:
            gesture="palm"
        elif fingers==[0,1,0,0,0]:
            gesture="index finger"
        elif fingers==[1,0,0,0,0]:
            gesture="thumb"
        else:
            gesture=None
            if player.get(cv2.CAP_PROP_POS_FRAMES) >= player.get(cv2.CAP_PROP_FRAME_COUNT) - 1:
                player.set(cv2.CAP_PROP_POS_FRAMES, player.get(cv2.CAP_PROP_POS_FRAMES) - 1)
            else:
                player.set(cv2.CAP_PROP_POS_FRAMES, player.get(cv2.CAP_PROP_POS_FRAMES))

        if gesture:
            if gesture == "fist": #play
                if player.get(cv2.CAP_PROP_POS_FRAMES)>=player.get(cv2.CAP_PROP_FRAME_COUNT)-1:
                    player.set(cv2.CAP_PROP_POS_FRAMES, player.get(cv2.CAP_PROP_POS_FRAMES)-1)
                else:
                    player.set(cv2.CAP_PROP_POS_FRAMES, player.get(cv2.CAP_PROP_POS_FRAMES))
            elif gesture == "palm": #pause
                player.set(cv2.CAP_PROP_POS_FRAMES, player.get(cv2.CAP_PROP_POS_FRAMES)-1)
            elif gesture == "index finger": #rewind
                player.set(cv2.CAP_PROP_POS_FRAMES, max(0, player.get(cv2.CAP_PROP_POS_FRAMES) - 10))
            elif gesture == "thumb": #forward
                player.set(cv2.CAP_PROP_POS_FRAMES,
                           min(player.get(cv2.CAP_PROP_FRAME_COUNT)-1, player.get(cv2.CAP_PROP_POS_FRAMES) + 10))

    cv2.imshow('Video', frame2)
    cv2.imshow("Camera",frame1)
    key=cv2.waitKey(1)
    if key == ord('q'):
        break