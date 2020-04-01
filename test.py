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

class Commands:
    
    is_animation_on = True
    animation_time = 0.2

    mouse = Mouse.Controller()
    keyboard = Keyboard.Controller()
    config = tools.JSON.get("config.json") 

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
    
    def click_l(self, count = 1):
        self.mouse.click(Mouse.Button.left, count)
        # Check URL
        if OCR.check_current_url():
            self.go_to_top()
    
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
    
    def find(self, path, center=False):
        pos = None
        if not os.path.isdir(path):
            self.mouse.position = self.config["location"]['base']
            if not center:
                pos = pyautogui.locateOnScreen(path)
            else:
                pos = pyautogui.locateCenterOnScreen(path)
            
            if pos:
                print(">> found:", path)
            else:
                print(">> not found:", path)
            
            return pos

        else:
            print("> checking dir:", path)
            for index, file in enumerate(glob.glob(f"{path}/*.png")):
                pos = self.find(file, center=center)
                if pos:
                    self.mouse.position = pos
                    return pos
            return None
            
    def find_and_click(self, path):
        '''
            dir destekleyecek.
        '''
        pos = self.find(path, center=True) 
        self.mouse.position = pos
        self.click_l()

        
    def wait_for(self, title, path, scrolldown_enabled=False, scrollup_enabled=False, try_limit=3):
        trying = 0
        while True:
            print(f"> waiting for : {title}")
            if self.find(path):
                print("> waiting is completed!")
                break
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
                        break
            elif scrollup_enabled:
                is_bof = self.scrollup()
                if is_bof:
                    print(">> BOF")
                    break
            #Kaldırılacak!
            time.sleep(1)
    
    def go_to_top(self):
        while True:
            is_bof = self.scrollup()
            if is_bof:
                print(">> BOF")
                break
            time.sleep(1)

    def go_to_bottom(self):
        while True:
            is_eof = self.scrolldown()
            if is_eof:
                print(">> EOF")
                break
            time.sleep(1)
    def solve_recaptha(self, s_time=2):
        self.wait_for("I'am not a robot bulunacak.", r'assets/iamnotarobot', scrolldown_enabled=True)
        self.find_and_click(r'assets/box')
        time.sleep(s_time)
        # Kutuya Tıklandı
        pos = self.find(r'assets/solver/person.png', center=True)
        if pos:
            # Enable Solver
            while not self.find(r'assets/iamnotarobot-done'):
                self.mouse.position = pos
                self.click_l()
                time.sleep(2)
                refresh_pos = self.find(r'assets/solver/refresh.png', center=True)
                if refresh_pos:
                    self.mouse.position = refresh_pos
                    self.click_l()
    
    def payment_solver(self, selected_link):
        self.wait_for("Basarılı mı?", f'assets/{selected_link}/success', scrolldown_enabled=True)
        offset = self.config["payment_solver"][selected_link]["region_offset"]
        pos = self.find(f'assets/{selected_link}/resolve_payment')
        if pos:
            pos = list(pos)
            pos[0] += offset[0]
            pos[1] += offset[1]
            pos[2] = offset[2]
            pos[3] = offset[3]
            payment_solver_text = OCR.resolve_region(pos, show=True, save=f"payments/{str(datetime.datetime.now()).split('.')[0].replace(':','-')}.png")
            print("Payment Image Pos:", pos)
            payment_amount = re.match("\d+", payment_solver_text)
            if payment_amount:
                with open(f"payments/{selected_link}.txt", 'a+') as f:
                    str_log = f"#Time: {str(datetime.datetime.now()).split('.')[0]}, #Payment: {payment_amount[0]}" 
                    print(str_log)
                    f.write(str_log + "\n")
        else:
            print("Could not detect payment solver image")
                
                


def bitcoinker():    
    _iamnotarobot_ = "assets/iamnotarobot"
    _iamnotarobot_done_ = "assets/iamnotarobot-done"

    config = tools.JSON.get("config.json")
    links = config["links"]
    
    cmd = Commands()
    cmd.is_animation_on = False
    selected_link = "bitcoinker"

    cmd.link(links[selected_link])
    cmd.wait_for("HTML is done?", f'assets/{selected_link}/htmlisdone.png', scrolldown_enabled=False)
    # TODO
    # Solver eklenecek.
    cmd.solve_recaptha()
    # .... SOLVER .... 
    cmd.wait_for("Waiting process done", _iamnotarobot_done_, scrolldown_enabled=False)
    cmd.wait_for("Claim edilcek.", r'assets\bitcoinker\claim_bitcoin', scrolldown_enabled=True)
    cmd.find_and_click(r'assets\bitcoinker\claim_bitcoin')
    time.sleep(2)
    
    cmd.payment_solver(selected_link)
    
    
    cmd.link("www.google.com")

def bonusbitcoin():
    
    _iamnotarobot_ = "assets/iamnotarobot"
    _iamnotarobot_done_ = "assets/iamnotarobot-done"
    config = tools.JSON.get("config.json")
    links = config["links"]
    cmd = Commands()
    cmd.is_animation_on = False
    selected_link = "bonusbitcoin"
    
    cmd.link(links[selected_link])
    cmd.wait_for("HTML is done?", f'assets/{selected_link}/htmlisdone.png', scrolldown_enabled=False)
    # TODO
    # Solver eklenecek.
    cmd.solve_recaptha()
    # .... SOLVER .... 
    cmd.wait_for("Waiting process done", _iamnotarobot_done_, scrolldown_enabled=False)
    cmd.wait_for("Claim edilcek.", f'assets\{selected_link}\claim_now.png', scrolldown_enabled=True)
    cmd.find_and_click(f'assets\{selected_link}\claim_now.png')
    time.sleep(2)
    
    cmd.payment_solver(selected_link)
    
    
    #cmd.link("www.google.com")

if __name__ == '__main__':
    while True:
        print("Sleeping 5 mins")
        time.sleep(5 * 60)
        bitcoinker()
        #bonusbitcoin()
        

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