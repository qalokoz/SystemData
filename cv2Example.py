import cv2
import numpy as np
cap = cv2.VideoCapture('./file')
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
new_width = 640
new_height = 480

# Create a VideoWriter object to save the resized video
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('resized_video.mp4', fourcc, 20.0, (new_width, new_height))
while(cap.isOpened()):
    ret, frame = cap.read()
    if ret==True:
        resized_frame = cv2.resize(frame, (new_width, new_height), interpolation = cv2.INTER_LINEAR)
        cv2.imshow('Resized Frame',resized_frame)
        out.write(resized_frame)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
    else:
        break
cap.release()
out.release()
cv2.destroyAllWindows()
