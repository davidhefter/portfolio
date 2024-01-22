import cv2
import numpy as np
from tracker import Tracker
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--input',default='input.mov')
parser.add_argument('--reference',default='stones.png')
parser.add_argument('--overlay',default='overlay.png')
args = parser.parse_args()

ref = cv2.imread(args.reference)
overlay = cv2.imread(args.overlay)

tracker = Tracker(ref,overlay)

cap = cv2.VideoCapture(args.input)
img_array = []
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    H = tracker.compute_homography(frame)
    if H is not None:
        frame_out = tracker.augment_frame(frame,H)
    else:
        frame_out = frame
    
    img_array.append(frame_out)

    cv2.imshow('window',frame_out)
    if cv2.waitKey(1) == 27: # hit escape to exit
        break

"""height,width=np.shape(frame_out[:,:,0])
out = cv2.VideoWriter('output.mov',cv2.VideoWriter_fourcc(*'DIVX'), 25, (width,height))
 
for i in range(len(img_array)):
    out.write(img_array[i])
out.release()"""

