import GUI
import HAL
import cv2

# Enter sequential code!
i = 0
prev_err = 0
sum_errs = 0

while True:
    # Enter iterative code!
    img = HAL.getImage()
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    red_mask = cv2.inRange(hsv, (0, 125, 125), (30, 255, 255))
    contours, hierarchy = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    M = cv2.moments(contours[0])
    
    if M["m00"] != 0:
      cX = M["m10"] / M["m00"]
      cY = M["m01"] / M["m00"]
    else:
      cX, cY = 0, 0
      
    if cX > 0:
      err = 320 - cX
      HAL.setV(4)
      sum_errs += err
      HAL.setW(0.005 * err + 0.005 * (err - prev_err) + 0.005 * sum_errs)
      prev_err = err
    
    GUI.showImage(red_mask)
    print('%d cX: %.2f cY: %.2f' % (i, cX, cY))
    i += 1
