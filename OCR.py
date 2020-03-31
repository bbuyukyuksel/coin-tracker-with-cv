import cv2 
import pytesseract 
import numpy as np
import pyautogui
import tools
from pynput import keyboard as Keyboard
import time
import re

def fix_false_chs(string):
  CH = {
    "|" : "l",
    " " : "",
    
  }
  for i,j in CH.items():
    string = string.replace(i, j)
  return string

def doOcr(img, show=False):
  config = tools.JSON.get("config.json")
  scale = config["ocr_settings"]["resize"]
  img = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
  ret, th2 = cv2.threshold(img,200,255,cv2.THRESH_BINARY_INV)

  size = tuple(np.array(th2.shape) * scale)
  size = (int(size[1]), int(size[0])) 
  sized = cv2.resize(th2.copy(), dsize=size, interpolation=cv2.INTER_CUBIC)
  if show:
    cv2.imshow("current text", sized)
    cv2.waitKey(1000)
    cv2.destroyAllWindows()
  custom_config = r'--oem 2 --psm 4'
  return fix_false_chs(pytesseract.image_to_string(sized, config=custom_config))

def rotateImage(image, angle):
  image_center = tuple(np.array(image.shape[1::-1]) / 2)
  rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
  result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
  return result

def close_tab():
  time.sleep(2)
  print("Tab Kapatılıyor..")
  keyboard = Keyboard.Controller()
  keyboard.press(Keyboard.Key.esc)
  time.sleep(0.1)
  keyboard.release(Keyboard.Key.esc)
    
  with keyboard.pressed(Keyboard.Key.ctrl_l):
    keyboard.press('w')
    keyboard.release('w')
  print("Tab Kapatıldı.")

def resolve_url():
  if '__first_trigger__' not in resolve_url.__dict__:    
    config = tools.JSON.get("config.json")
    pytesseract.pytesseract.tesseract_cmd = config["ocr_settings"]["tesseract_path"]
  if '__region__' not in resolve_url.__dict__:
    config = tools.JSON.get("config.json")
    resolve_url.__region__ = config["location"]["url_area"]

  ss_region = pyautogui.screenshot(region=resolve_url.__region__)
  img_url_bar = np.array(ss_region) 
  # Convert RGB to BGR 
  img_url_bar = img_url_bar[:, :, ::-1].copy() 
  result = doOcr(img_url_bar)
  return result

def resolve_region(region, show=False):
  ss_region = pyautogui.screenshot(region=region)
  img_url_bar = np.array(ss_region) 
  # Convert RGB to BGR 
  img_url_bar = img_url_bar[:, :, ::-1].copy() 
  result = doOcr(img_url_bar, show)
  return result

def check_current_url():
  config = tools.JSON.get("config.json")
  found = False
  while not found:
    time.sleep(2)
    result = resolve_url()
    print("_"*50)
    print("->", result)
    
    if result != '':
      for index, title_link in enumerate(config["links"].items()):
        title, link = title_link
        link = re.findall('(?:\.\w+\.)|(?://[^w]\w+\.)', link)[0].replace('.', '').replace('//', '')
        min_sentences = result if len(result) <= len(link) else link
        max_sentences = result if len(result) >  len(link) else link
        print("{:<3} Searching ... '{}' is in '{}' ?".format(index,min_sentences, max_sentences))

        if min_sentences in max_sentences and min_sentences :
          found = True
          break
      if not found:
        print("# => Answer: False")
        close_tab()
      print("_"*50)
      print(f"True page? {found}")
      return not found

    else:
      print("Result is empty!")

if __name__ == '__main__':
  '''
    TEST Code.
    >> import OCR
    >> OCR.resolve_url()
    ...
  '''
  
  config = tools.JSON.get("config.json")
  found = False
  while not found:
    time.sleep(2)
    result = resolve_url()
    print("_"*50)
    print("->", result)
    
    if result != '':
      for index, title_link in enumerate(config["links"].items()):
        title, link = title_link
        link = re.findall('(?:\.\w+\.)|(?://[^w]\w+\.)', link)[0].replace('.', '').replace('//', '')
        min_sentences = result if len(result) <= len(link) else link
        max_sentences = result if len(result) >  len(link) else link
        print("{:<3} Searching ... '{}' is in '{}' ?".format(index,min_sentences, max_sentences))

        if min_sentences in max_sentences and min_sentences :
          found = True
          break
      if not found:
        print("# => Answer: False")
        close_tab()
      print("_"*50)
      print(f"True page? {found}")

    else:
      print("Result is empty!")