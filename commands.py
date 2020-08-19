from pynput import mouse as Mouse
from pynput import keyboard as Keyboard
import pyautogui
import tools
import time
import os
import glob
import OCR
import re
import datetime
import matching
import globals

class Commands:
    
    is_animation_on = True
    animation_time = 0.2

    mouse = Mouse.Controller()
    keyboard = Keyboard.Controller()
    config = tools.JSON.get("config.json")
    selected_link = None 

    def ctrl_(self, key):
        with self.keyboard.pressed(Keyboard.Key.ctrl_l):
            self.keyboard.press(key)
            self.keyboard.release(key)
    def type(self, text):
        if self.is_animation_on:
            for ch in text:
                self.keyboard.type(ch)
                time.sleep(self.animation_time)
        else:
            self.keyboard.type(text)
    def enter(self):
        self.keyboard.press(Keyboard.Key.enter)
        self.keyboard.release(Keyboard.Key.enter)
    def remove(self):
        self.keyboard.press(Keyboard.Key.backspace)
        self.keyboard.release(Keyboard.Key.backspace)

    def link(self, url):
        self.mouse.position = self.config["location"]["url_text"]
        self.mouse.click(Mouse.Button.left)
        self.ctrl_('a')
        self.type(url)
        self.enter()
    
    def click_r(self, count=1):
        self.mouse.click(Mouse.Button.right, count)

    def click_l(self, count = 1, close_after_click=True):
        '''
         if new tab is opened return [True] or return [False]
        '''
        self.mouse.click(Mouse.Button.left, count)
        time.sleep(2)

        if not close_after_click:
            return False
        
        # Check URL
        if OCR.check_current_url():
            time.sleep(1)
            self.go_to_top()
            return True
        return False
    
    def scrolldown(self, s_time=None):
        if self.find("assets/process/eof"):
            return "eof"
        self.mouse.position = self.config["location"]["scrollbar_bottom"]
        if s_time is None:
            self.click_l()
        else:
            self.mouse.press(Mouse.Button.left)
            time.sleep(s_time)
            self.mouse.release(Mouse.Button.left)
    
    def scrollup(self, s_time=None):
        if self.find("assets/process/bof"):
            return "eof"
        
        self.mouse.position = self.config["location"]["scrollbar_top"]
        if s_time is None:
            self.click_l()
        else:
            self.mouse.press(Mouse.Button.left)
            time.sleep(s_time)
            self.mouse.release(Mouse.Button.left)
    
    def find(self, path, center=False, sensitive=False):
        '''
            Return [Center of Image's Position] or [None]
        '''
        pos = None
        if not os.path.isdir(path):
            #base_pos = list(self.config["location"]['widthxheight'])
            #self.mouse.position = ((base_pos[0]//2)+50,base_pos[1]//2)
            self.mouse.position = self.config["location"]['base']

            if sensitive:
                print(">> Sensitive Mode: Enabled")
                pos = matching.matching(template_img_path=path, source="screenshot", debug=False, score_threshold=self.config["ocr_settings"]['matching_threshold'], center=center)
            else:
                if not center:
                    pos = pyautogui.locateOnScreen(path)
                else:
                    pos = pyautogui.locateCenterOnScreen(path)
                
            if pos:
                print(">> found:", path)
            else:
                #print(">> not found:", path)
                pass
            
            return pos

        else:
            print("> checking dir:", path)
            for index, file in enumerate(glob.glob(f"{path}/*.png")):
                pos = self.find(file, center=center, sensitive=sensitive)
                if pos:
                    self.mouse.position = pos
                    return pos
            return None
            
    def find_and_click(self, path, sensitive=False, close_after_click=True):
        '''
            if find function is successed : 
                return [True]  : new tab opened
                return [False] : new tab is not opened
            else
                return None
        '''
        pos = self.find(path, center=True, sensitive=True) 
        if pos:
            self.mouse.position = pos
            return self.click_l(close_after_click=close_after_click) #if new tab is opened return True
        return None
        

        
    def wait_for(self, title, path, scrolldown_enabled=False, try_limit=1, sensitive=False, timeout = None):
        trying = 0
        __alert__ = 0
        __timeout_flag__ = False
        __exit_flag__ = False
        begin_time = datetime.datetime.now()

        if not timeout:
            timeout = globals.TIMEOUT
        
        while True:
            # Timeout Control
            if (datetime.datetime.now() - begin_time).seconds > timeout:
                __timeout_flag__ = True
                break
            # Alert Control
            if (__alert__ > 10):
                __exit_flag__ = True        
                break

            print(f"> waiting for : {title}")
            if self.find(path, sensitive=sensitive):
                print("> waiting is completed!")
                break
            else:
                __alert__ += 1

            if scrolldown_enabled:
                is_eof = self.scrolldown()
                if is_eof:
                    print(">> EOF")
                    if trying < try_limit:
                        print("Trying to find again")
                        trying +=1
                        self.go_to_top()
                    else:
                        print("Could not found, Tring Limit:", trying)
                        __exit_flag__ = True
                        break
            #Kaldırılacak!
            time.sleep(1)

        # if an error occured return True Flag
        return __timeout_flag__ or __exit_flag__
    
    def go_to_top(self):
        '''
            if there is an alert return [True], else [False]
        '''
        __alert__ = 0
        while True:
            if __alert__ > 20:
                return True
            is_bof = self.scrollup()
            if is_bof:
                print(">> BOF")
                break
            else:
                __alert__ += 1
            time.sleep(1)
        return False

    def go_to_bottom(self):
        __alert__ = 0
        while True:
            if __alert__ > 20:
                return True
            is_eof = self.scrolldown()
            if is_eof:
                print(">> EOF")
                break
            else:
                __alert__ += 1
            time.sleep(1)
        return False
        
    def solve_recaptcha(self, s_time=2, firstly_go_to_top=True, scrolldown_enabled=True):
        __critical_alert_flag__ = 0
        __critical_alert_count__ = 15

        while True:
            if __critical_alert_flag__ > __critical_alert_count__:
                break

            __critical_alert_flag__ += 1
            if firstly_go_to_top:
                self.go_to_top()
            self.wait_for("I'am not a robot bulunacak.", r'assets/iamnotarobot', scrolldown_enabled=scrolldown_enabled, sensitive=False)
            if not self.find_and_click(r'assets/box',sensitive=False):
                break
            time.sleep(s_time)

        __critical_alert_flag__ = 0
        # Kutuya Tıklandı
        pos = self.find(r'assets/solver/person', center=True)
        time.sleep(3)
        if pos:
            # Enable Solver
            while not self.find(r'assets/iamnotarobot-done'):
                if __critical_alert_flag__ > __critical_alert_count__:
                    break

                __critical_alert_flag__ += 1
                pos = self.find(r'assets/solver/person', center=True)
                time.sleep(4)
                if not pos:
                    continue
                self.mouse.position = pos
                self.click_l()
                refresh_flag = self.wait_for("Process'in kabulü bekleniyor...", f"assets/iamnotarobot-done", timeout=30, scrolldown_enabled=scrolldown_enabled)
                if refresh_flag:
                    refresh_pos = self.find(r'assets/solver/refresh', center=True)
                    if refresh_pos:
                        self.mouse.position = refresh_pos
                        self.click_l()
        # If an error occured return error flag : True
        return __critical_alert_flag__ > __critical_alert_count__

    def payment_solver(self, selected_link, sensitive=False):
        self.wait_for("Basarılı mı?", f'assets/{selected_link}/success', scrolldown_enabled=True, sensitive=sensitive)
        offset = self.config["payment_solver"][selected_link]["region_offset"]
        pos = self.find(f'assets/{selected_link}/resolve_payment', sensitive=sensitive)
        if pos:
            pos = list(pos)
            pos[0] += offset[0]
            pos[1] += offset[1]
            pos[2] = offset[2]
            pos[3] = offset[3]
            save_path = f"payments/{selected_link}"
            if not os.path.isdir(save_path):
                os.makedirs(save_path, exist_ok=True)
            payment_solver_text = OCR.resolve_region(pos, show=True, save=f"{save_path}/{str(datetime.datetime.now()).split('.')[0].replace(':','-')}.png")
            print("Payment Image Pos:", pos)
            payment_amount = re.match("\d+", payment_solver_text)
            if payment_amount:
                with open(f"payments/{selected_link}.txt", 'a+') as f:
                    str_log = f"#Time: {str(datetime.datetime.now()).split('.')[0]}, #Payment: {payment_amount[0]}" 
                    print(str_log)
                    f.write(str_log + "\n")
        else:
            print("Could not detect payment solver image")
                
    def close_other_tabs(self):
        time.sleep(2)
        pos = self.find(r'assets/localhost.png', center=True)
        if pos:
            self.mouse.position = pos
            self.click_r()
            time.sleep(0.5)
            pos = self.find(r'assets/close_other_tabs.png', center=True)
            if pos:
                self.mouse.position = pos
                self.click_l(close_after_click=False)
                time.sleep(2)


if __name__ == '__main__':
    
    cmd = Commands()
    cmd.close_other_tabs()
    exit()
    while True:
        bonusbitcoin()
        bitcoinker()
        print("Sleeping 5 mins")
        time.sleep(5 * 60)
        

    '''
    config = tools.JSON.get("config.json")
    scrollbar_location = np.array(config["scrollbar_location"])
    mouse_location = np.array(cmd.params[1])

    d = scrollbar_location-mouse_location
    #d = math.sqrt((d[0]**2 + d[1]**2))
    d = abs(d[0])
    if d < 50:
        print("# Scrollbar Area (!) URL checking is skipping..")
    else:
        print("URL Kontrol ediliyor..")
        OCR.check_current_url()
        print("Devam ediyor..")

    position = pyautogui.locateOnScreen('assets/person.png')
    if position:
        print("Re-Capthca Solver is Enabled!")
        print(np.array(position[:2]))
        print(np.array(position[2:]))

        position = np.array(position[:2]) + (np.array(position[2:])/2)
        mouse.position = position
        mouse.click(Button.left)

        while True:
            if pyautogui.locateOnScreen('assets/iamnotarobot-dark.png') or pyautogui.locateOnScreen('assets/iamnotarobot-light.png'):
                break
            else:
                print("Waiting process ..")
        print("Process is completed !")
    '''