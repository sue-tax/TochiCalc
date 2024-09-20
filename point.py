'''
Created on 2024/06/29

@author: sue-t
'''

if __name__ == '__main__':
    pass

import cv2

def onMouse(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(x, ',', y)

img = cv2.imread('taka.jpg')
# cv2.namedWindow('sample', cv2.WINDOW_NORMAL)
cv2.imshow('sample', img)
cv2.setMouseCallback('sample', onMouse)
cv2.waitKey(0)