import cv2
import numpy as np

def PerspectiveTransform(path,cropped_xy,xx1,yy1,xx2,yy2,xx3,yy3,xx4,yy4):
    try:
        image = cv2.imread(path)
        cropped_image = image[cropped_xy[0]:cropped_xy[1],cropped_xy[2]:cropped_xy[3]]
        resize = cv2.resize(cropped_image, (400, 400))
    # Define the points for the perspective transform (source points)
    # These points should correspond to a quadrilateral in the original image
        pts1 = np.float32([[xx1, yy1], [xx2, yy2], [xx3, yy3], [xx4, yy4]])

    # Define the destination points (where you want to map the source points)
        pts2 = np.float32([[0, 0], [400, 0], [0, 400], [400, 400]])

    # Calculate the perspective transform matrix
        matrix = cv2.getPerspectiveTransform(pts1, pts2)

    # Apply the perspective warp
        result = cv2.warpPerspective(resize, matrix, (400, 400))
    
    except Exception as e:
        print(e)
    return result