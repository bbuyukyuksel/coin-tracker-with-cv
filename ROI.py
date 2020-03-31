
#from pynput.mouse import Listener, Controller
from pynput import mouse as Mouse
from pynput import keyboard as Keyboard
import time
import pyautogui
import tools


def on_click(x, y, button, pressed):
    if(use_mouse_position):
        print("use_mouse_position : True")
        x,y = mouse.position

    if pressed:
        content = 'Event:[mouse_press]->{2}->({0}, {1})'.format(x, y, button)
        print(content)
    else:
        content = 'Event:[mouse_release]->{2}->({0}, {1})'.format(x, y, button)
        print(content)
        if handler_type == "ROI":
            handler(x,y, button, pressed)

def ROI(*args):
    global listener_is_done, process

    if '__trigger__' not in ROI.__dict__:
        ROI.__trigger__ = 0
    if '__parameter_history__' not in ROI.__dict__:
        ROI.__parameter_history__ = []
    if '__max_trigger__' not in ROI.__dict__:
        ROI.__max_trigger__ = int(process[0].split('-')[1])
    


    ROI.__parameter_history__.append(args)
    ROI.__trigger__ += 1

    if ROI.__trigger__ == ROI.__max_trigger__:
        config = tools.JSON.get("config.json")

        if   ROI.__trigger__ == 1: # Click-1
            x1, y1 = ROI.__parameter_history__[0][0], ROI.__parameter_history__[0][1]
            x2, y2 = 25,25
            region = (abs(x1 - x2), abs(y1 - y2), 2*x2, 2*y2)
            config[process[1]] = (x1,y1)
            tools.JSON.set("config.json", config)

        elif ROI.__trigger__ == 2: # Click-2
            for i in ROI.__parameter_history__:
                print(i)
    
            x1, y1 = ROI.__parameter_history__[0][0], ROI.__parameter_history__[0][1]
            x2, y2 = ROI.__parameter_history__[1][0], ROI.__parameter_history__[1][1]
            region = (x1, y1, abs(x2-x1), abs(y2-y1))
            config[process[1]] = region
            tools.JSON.set("config.json", config)
            

            #with open("test.png", "wb") as f:
            #    im.save(f)
            ##  Start Template Matching
            #location = pyautogui.locateOnScreen('test.png')
            #im = pyautogui.screenshot(region=location)
            #print("Location :>", location)
            #im.show()
            ## TEST
        else:
            print("Undefined")
       
       
        im = pyautogui.screenshot(region=region)
        im.show()

        del ROI.__trigger__
        del ROI.__parameter_history__
        del ROI.__max_trigger__
        listener_is_done = True

def start_mouse_listener():
    global listener_is_done

    mouse = Mouse.Controller()
    with Mouse.Listener(on_click=on_click) as listener:
        while not listener_is_done:
            time.sleep(1)

if __name__ == '__main__':
    global mouse, use_mouse_position, handler_type, listener_is_done, process
    use_mouse_position = False 

    # Handler
    #HANDLER = [
    #    "ROI",
    #}
    handler_type = "ROI"
    handler = ROI

    #listener_is_done = False
    #process = ("click-1", "scrollbar_top_location")
    #print("Click scrollbar_top_location")
    #start_mouse_listener()

    listener_is_done = False
    process = ("click-2", "burak")
    print("Click for burak")
    start_mouse_listener()

    #listener_is_done = False
    #process = ("click-1", "url_text_location")
    #print("Click url_text_location")
    #start_mouse_listener()

    #listener_is_done = False
    #process = ("click-2", "url_location")
    #print("Click Url Location")
    #start_mouse_listener()

