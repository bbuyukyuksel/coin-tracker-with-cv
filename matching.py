
import numpy as np
from matplotlib import pyplot as plt
import cv2
from pynput import mouse as Mouse
import pyautogui
import tools


def matching(template_img_path, source="screenshot", debug=False, score_threshold=0.001, center=False):
    template = cv2.imread(template_img_path, 0)
    #img = cv2.imread('ss.png',0)
    if source == "screenshot":
        source = pyautogui.screenshot()

    source = np.array(source) 
    source = source[:, :, ::-1].copy() 
    source = cv2.cvtColor(source.copy(), cv2.COLOR_BGR2GRAY)

    w, h = template.shape[::-1]
    # All the 6 methods for comparison in a list
    methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
                'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']

    meth = methods[-1]    
    img = source.copy()
    method = eval(meth)

    # Apply template Matching
    res = cv2.matchTemplate(img,template,method)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
    if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
        top_left = min_loc
    else:
        top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)


    cropped = img[top_left[1]:top_left[1]+h, top_left[0]:top_left[0]+w].copy()
    ret2,th1 = cv2.threshold(template,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    ret2,th2 = cv2.threshold(cropped,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    
    score = abs(np.sum((template/255) - (cropped/255))/template.size)   #Direct Score
    score = abs(np.sum((th1/255) - (th2/255))/template.size)            #Thresholded image score

    if debug:
        print("Top Left:", top_left, "Bottom Right", bottom_right)
        cv2.rectangle(img,top_left, bottom_right, 0, 2)

        plt.subplot(321),plt.imshow(res,cmap = 'gray')
        plt.title('Matching Result'), plt.xticks([]), plt.yticks([])

        plt.subplot(322),plt.imshow(img,cmap = 'gray')
        plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
        plt.subplot(323),plt.imshow(template,cmap = 'gray')
        plt.title('Matching Result'), plt.xticks([]), plt.yticks([])

        plt.subplot(324),plt.imshow(cropped,cmap = 'gray')
        plt.title('Matching Result'), plt.xticks([]), plt.yticks([])

        plt.subplot(325),plt.imshow(th1,cmap = 'gray')
        plt.title('template-threshold'), plt.xticks([]), plt.yticks([])
        plt.subplot(326),plt.imshow(th2,cmap = 'gray')
        plt.title('cropped-threshold'), plt.xticks([]), plt.yticks([])

        plt.suptitle(f"{meth} score:{score}")
        plt.show()

    

    if score < score_threshold:
        if debug:
            print(score, "<", score_threshold, score < score_threshold)
        print("(!) template is matched")
        if center:
            return (top_left[0] + w//2, top_left[1] + h//2)
        else:
            #Bound Box
            return (top_left[0], top_left[1], w, h)
    else:
        print("(!) template image could not found!")
        return None


if __name__ == '__main__':
    config = tools.JSON.get("config.json")

    path = r'd:\\Peresthayal\\WorkStation\\Projects\\Python_Apps\\coin-tracker\\coin-tracker-with-cv\\assets\\freebitco\\resolve_payment.png'
    pos = matching(template_img_path=path, source="screenshot", debug=True, score_threshold=config["ocr_settings"]['matching_threshold'], center=True)
    if pos:
        mouse = Mouse.Controller()
        mouse.position = pos[:2]

    print("Position", pos)