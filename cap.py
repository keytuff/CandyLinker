from PIL import Image
import cv2 as cv
import numpy as np

class Cap:
    def screencap(self, adb):
        img = adb.screencap()
        #img.save('cap.png')
        '''
        # Our operations on the frame come here
        gray = cv.cvtColor(np.asarray(img), cv.COLOR_RGB2GRAY)
        cvImg = cv.GaussianBlur(gray, (5, 5), 0)
        cvImg = cv.Canny(cvImg, 1, 10)
        img = Image.fromarray(cvImg)
        img.show()
        img.save('cap.png')
        '''
        return img
 