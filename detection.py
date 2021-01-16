from cv2 import cv2 as cv 
import time
import os

# Displays (and reads) given worning on the screen of your laptop (only mac os) 
def notify(title, text):
    os.system("""
              osascript -e 'display notification "{}" with title "{}"'
              """.format(text, title))
    os.system('say "Intruder is coming!"')


# Defines a video capture object, creates empty variable static_bg 
# that will be later used to detect changes in the video 
vid = cv.VideoCapture(0) 
static_bg = None

# First pick of my camera was always dark so I added 5 second pause
time.sleep(5)

while(True):  
    motion = 0 
    # Capture the video frame 
    # by frame 
    ret, frame = vid.read() 
    
    # Flips frame horizontally, converts it to grayscale
    # and adds Gaussian to reduce noise and details
    flip = cv.flip(frame, 1)
    gray_frame = cv.cvtColor(flip, cv.COLOR_BGR2GRAY)
    gray_img = cv.GaussianBlur(gray_frame, (21,21), 0)
    
    # Assigns starting background to our static_bg
    if static_bg is None:
        static_bg = gray_img
        continue
    
    # Calculates the difference to distinguish new objects on the frame
    difference = cv.absdiff(static_bg,gray_img)
    
    
    # Adds thresholding, noises removal 
    threshold = cv.threshold(difference, 70, 255, cv.THRESH_BINARY)[1]
    thresh = cv.dilate(threshold, None, iterations = 2)
    
    
    cnts,_ = cv.findContours(thresh.copy(),  
                       cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE) 
  
    for contour in cnts: 
        if cv.contourArea(contour) < 10000:
            continue
        motion = 1
  
        (x, y, w, h) = cv.boundingRect(contour) 
        # making green rectangle arround the moving object 
        cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
    
    # Uncomment to display the frame
    cv.imshow('Thresh', thresh)  
    
    # If there is motion sends alert       
    if motion == 1:
        time.sleep(1)
        notify("Alert", "Detected unknown movement.")
        time.sleep(4)
    
    # Press 'q' to quit or 'ctrl c'
    if cv.waitKey(1) & 0xFF == ord('q'): 
        break
  
# After the loop release the cap object, 
# destroys all the windows
vid.release() 
cv.destroyAllWindows() 