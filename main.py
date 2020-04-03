from threading import Thread, Event
from time import sleep
from commands import Commands
import tools
import time
from pynput import keyboard as Keyboard
import OCR
import datetime
import globals
from faucets import *

def automate(recipe_handler, sleeptime, stop_event):
    recipe_counter = 1
    while not stop_event.wait(1):
        print(recipe_handler, "çalışıyor..")
        while globals.WAIT:
            print("Uyuyor")
            sleep(5)
        globals.WAIT = True
        recipe_handler()
        
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
        'bitcoinker'   : 5  * 60, # 5 DK
        'bonusbitcoin' : 15 * 60, # 15 DK
        'freebitco'    : 60 * 60, # 60 DK 
    }

    listener = Keyboard.Listener(on_release=on_release)
    listener.start()


    threads = []
    for recipe_name in recipe_times.keys():
        x = Thread(target=automate, args=(eval(recipe_name),recipe_times[recipe_name], thread_kill_signal))
        x.start()
        threads.append([recipe_name, x])
    
    
    while not thread_kill_signal.wait(1.5):
        with open("logs/thread_status.txt", 'a+') as f:
            for i in threads:
                str_log = f"{str(datetime.datetime.now()).split('.')[0]} Recipe: {i[0]}, is_alive: {i[1].is_alive()}, wait_status:{globals.WAIT}\n"
                f.write(str_log)
                
                if not i[1].is_alive():
                    str_log = f">>> {str(datetime.datetime.now()).split('.')[0]} Tekrar uyandırılıyor Recipe: {i[0]}"
                    f.write(str_log)
                    print(str_log)
                    i[1] = Thread(target=automate, args=(eval(i[0]),recipe_times[i[0]], thread_kill_signal))
                    i[1].start()
                    globals.WAIT = False

    

