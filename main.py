from threading import Thread, Event
from time import sleep
from pynput import keyboard as Keyboard

import random
import time
import datetime

import globals
import tools
import OCR
from commands import Commands
from faucets import *

def automate(recipe_name, sleeptime, stop_event):
    recipe_param = None
    if "moon" in recipe_name:
        recipe_handler, recipe_param = recipe_name.split("_")
        recipe_handler = eval(recipe_handler)
    else:
        recipe_handler = eval(recipe_name)

    recipe_counter = 1
    while not stop_event.wait(1):
        print(recipe_handler, "çalışıyor..")
        #sleep(sleeptime)
        while globals.WAIT:
            print(recipe_handler, "uyuyor..")
            sleep(5)
        globals.WAIT = True
        
        # Run Handler
        recipe_handler(recipe_param) if recipe_param else recipe_handler()
        cmd = Commands()
        cmd.close_other_tabs()
        '''
        # Close Tabs
        while stop_event.wait(1):
            link = OCR.resolve_url()
            print("Link", link)
            if "linkedin" not in link and "coinpot" not in link and "google" not in link:
                OCR.close_tab()
                sleep(1)
            else:
                break
        print("Tablar Kapatıldı..")
        '''
        globals.WAIT = False
        recipe_counter += 1
        print(f"Recipe name: {recipe_handler.__doc__} -> {recipe_counter}. kez gerçekleşti.")
        sleep(sleeptime)

        

globals.WAIT = False

def on_release(key):
    global thread_kill_signal
    if key == Keyboard.Key.f12:
        print('{0} released'.format(key))
        thread_kill_signal.set()
        # Stop listener
        return False

if __name__ == '__main__':
    global thread_kill_signal
    thread_kill_signal = Event()
    
    recipe_times = {
        #'bitcoinker'         : random.randint(8,20) * 60, # 5 DK
        #'freebitco'           : 60*60,#random.randint(60,70) * 60, # 60 DK 
        'moon_moonlite'       : 5* 60,
        'moon_moonbitcoincash': 5* 60,
        'bonusbitcoin'        : 15*60,#random.randint(15,20) * 60, # 15 DK
        'moon_moondoge'       : 5* 60,
        'moon_moondash'       : 5* 60,
        'moon_moonbit'        : 5* 60,
        'bitfun'              : 4 *60,#random.randint(5,7) * 60, # 60 DK 
    }
    
    listener = Keyboard.Listener(on_release=on_release)
    listener.start()

    threads = []
    for recipe_name in recipe_times.keys():
        x = Thread(target=automate, args=(recipe_name,recipe_times[recipe_name], thread_kill_signal))
        x.start()
        threads.append([recipe_name, x])
    
    while not thread_kill_signal.wait(1.5):
        with open("logs/thread_status.txt", 'a+') as f:
            for i in threads:
                if not i[1].is_alive():
                    str_log = f">>> {str(datetime.datetime.now()).split('.')[0]} Tekrar uyandırılıyor Recipe: {i[0]}"
                    f.write(str_log)
                    print(str_log)
                    i[1] = Thread(target=automate, args=(i[0],recipe_times[i[0]], thread_kill_signal))
                    i[1].start()
                    globals.WAIT = False

    

