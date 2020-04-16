import argparse
import cv2  

# construct the argument parser and parse command line arguments
ap = argparse.ArgumentParser()
ap.add_argument("-u","--url", type=str,required=True,
	help="Task ID")
args = vars(ap.parse_args())
if args['url'] == "0":
    src = 0
else:
    src = args['url']
cap = cv2.VideoCapture(src)

while True:
    key = cv2.waitKey(1)
    _,frame = cap.read()
    cv2.imshow(str(src), frame)
    if key == ord('q'):
        break