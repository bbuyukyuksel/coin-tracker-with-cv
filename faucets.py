import tools
import datetime
from commands import Commands
import time
import os
import OCR
import inspect

def bitcoinker():
    '''
        Recipe name: bitcoinker
    '''    
    _iamnotarobot_ = "assets/iamnotarobot"
    _iamnotarobot_done_ = "assets/iamnotarobot-done"
    config = tools.JSON.get("config.json")
    links = config["links"]
    cmd = Commands()
    cmd.is_animation_on = True
    cmd.animation_time = 0.01
    selected_link = "bitcoinker"
    cmd.link(links[selected_link])
    cmd.wait_for("HTML is done?", f'assets/{selected_link}/htmlisdone.png', scrolldown_enabled=False)

    if cmd.solve_recaptcha():
        print("solve_recaptcha fail")
        tools.Logging.fail(f"logs/time/{selected_link}.txt", "solve_recaptcha fail")
        cmd.link("localhost")
        exit()
    
    if cmd.wait_for("Waiting process done", _iamnotarobot_done_, scrolldown_enabled=False):
        cmd.link("localhost")
        tools.Logging.fail(f"logs/time/{selected_link}.txt", "Process done yakalanamadı.")
        exit()
    if not cmd.wait_for("Claim edilcek.", f'assets/bitcoinker/claim_bitcoin', scrolldown_enabled=True, sensitive=True):
        cmd.find_and_click(f'assets/bitcoinker/claim_bitcoin', sensitive=True)
        time.sleep(2)
        cmd.payment_solver(selected_link, sensitive=True)
        tools.Logging.success(f"logs/time/{selected_link}.txt")
    else:
        tools.Logging.fail(f"logs/time/{selected_link}.txt", "Claim edilemedi!")
        cmd.link("localhost")

def bitfun():
    '''
        Recipe name: bitcoinker
    '''    
    _iamnotarobot_ = "assets/iamnotarobot"
    _iamnotarobot_done_ = "assets/iamnotarobot-done"
    config = tools.JSON.get("config.json")
    links = config["links"]
    cmd = Commands()
    cmd.is_animation_on = True
    cmd.animation_time = 0.01
    selected_link = "bitfun"
    cmd.link(links[selected_link])
    cmd.wait_for("HTML is done?", f'assets/{selected_link}/htmlisdone', scrolldown_enabled=False)
    cmd.wait_for("Searching claim button?", f'assets/{selected_link}/claim', scrolldown_enabled=True, sensitive=True)
    cmd.find_and_click(f'assets/{selected_link}/claim', sensitive=True)
    
    if cmd.solve_recaptcha(firstly_go_to_top=False):
        print("solve_recaptcha fail")
        tools.Logging.fail(f"logs/time/{selected_link}.txt", "solve_recaptcha fail")
        cmd.link("localhost")
        exit()
    
    time.sleep(2)
    cmd.find_and_click(f'assets/{selected_link}/claim', sensitive=True)
    time.sleep(2)
    
    if not cmd.wait_for("Searching claim button?", f'assets/{selected_link}/close', scrolldown_enabled=False, sensitive=True):
        cmd.find_and_click(f'assets/{selected_link}/close', sensitive=True)
        tools.Logging.success(f"logs/time/{selected_link}.txt")
    else:
        tools.Logging.fail(f"logs/time/{selected_link}.txt", "Claim edilemedi!")
    cmd.link("localhost")


def bonusbitcoin():
    '''
        Recipe name: bonusbitcoin
    '''
    _iamnotarobot_ = "assets/iamnotarobot"
    _iamnotarobot_done_ = "assets/iamnotarobot-done"

    config = tools.JSON.get("config.json")
    links = config["links"]
    cmd = Commands()
    cmd.is_animation_on = True
    cmd.animation_time = 0.01
    selected_link = "bonusbitcoin"
    
    cmd.link(links[selected_link])
    cmd.wait_for("HTML is done?", f'assets/{selected_link}/htmlisdone.png', scrolldown_enabled=False)
    
    cmd.wait_for("I'am not a robot bulunacak.",_iamnotarobot_, scrolldown_enabled=True, sensitive=False)
    if cmd.solve_recaptcha(scrolldown_enabled=False, firstly_go_to_top=False):
        print("solve_recaptcha fail")
        tools.Logging.fail(f"logs/time/{selected_link}.txt", "solve_recaptcha fail")
        cmd.link("localhost")
        exit()
    
    cmd.wait_for("Waiting process done", _iamnotarobot_done_, scrolldown_enabled=False)
    if not cmd.wait_for("Claim edilcek.", f'assets\{selected_link}\claim_now.png', scrolldown_enabled=True, sensitive=True):
        time.sleep(2)
        cmd.find_and_click(f'assets\{selected_link}\claim_now.png', sensitive=True)
        #cmd.payment_solver(selected_link, sensitive=True)
        tools.Logging.success(f"logs/time/{selected_link}.txt")
    else:
        tools.Logging.fail(f"logs/time/{selected_link}.txt", "Claim edilemedi!")
    cmd.link("localhost")

def freebitco():
    '''
        Recipe name: freebitco
    '''
    _iamnotarobot_ = "assets/iamnotarobot"
    _iamnotarobot_done_ = "assets/iamnotarobot-done"

    config = tools.JSON.get("config.json")
    links = config["links"]
    cmd = Commands()
    cmd.is_animation_on = True
    cmd.animation_time = 0.01
    selected_link = "freebitco"
    
    cmd.link(links[selected_link])
    cmd.wait_for("HTML is done?", f'assets/{selected_link}/htmlisdone.png', scrolldown_enabled=False)
    cmd.mouse.position = config["location"]["temp"]
    cmd.click_l()

    if cmd.solve_recaptcha():
        print("solve_recaptcha fail")
        tools.Logging.fail(f"logs/time/{selected_link}.txt", "solve_recaptcha fail")
        cmd.link("localhost")
        exit()
        
    cmd.wait_for("Waiting process done", _iamnotarobot_done_, scrolldown_enabled=False)
    if not cmd.wait_for("Roll edilcek.", f'assets/{selected_link}/roll.png', scrolldown_enabled=True, sensitive=True):
        cmd.find_and_click(f'assets/{selected_link}/roll.png', sensitive=True)
        time.sleep(2)
        cmd.mouse.position = config["location"]["temp"]
        cmd.click_l()
        #cmd.payment_solver(selected_link, sensitive=True)
        tools.Logging.success(f"logs/time/{selected_link}.txt")
        
    else:
        tools.Logging.fail(f"logs/time/{selected_link}.txt", "Claim edilemedi!")
    cmd.link("localhost")


def moon(selected_link):
    f'''
        Recipe name: {selected_link}
    '''
    this_func = eval(inspect.stack()[0][3])

    def check():
        if "blank" in OCR.resolve_url():
            print("! RESET")
            return this_func(selected_link)
        else:
            if OCR.check_current_url():
                time.sleep(1)
                cmd = Commands()
                cmd.go_to_top()

    BASE_ASSET_DIR = f'assets/__faucets__/{selected_link}'

    _iamnotarobot_ = "assets/iamnotarobot"
    _iamnotarobot_done_ = "assets/iamnotarobot-done"

    config = tools.JSON.get("config.json")
    links = config["links"]
    cmd = Commands()
    cmd.is_animation_on = True
    cmd.animation_time = 0.01
    
    cmd.link(links[selected_link])
    cmd.wait_for("HTML is done?", os.path.join(BASE_ASSET_DIR, "htmlisdone"), scrolldown_enabled=False)
    cmd.mouse.position = config["location"]["temp"]
    cmd.click_l(close_after_click=False)
    time.sleep(5)
    check()
    time.sleep(2)

    # Double Close Check
    if not cmd.wait_for("Reklam Kapatılacak.", os.path.join(BASE_ASSET_DIR, 'close'), scrolldown_enabled=False, sensitive=True):
        cmd.find_and_click(os.path.join(BASE_ASSET_DIR, 'close'), sensitive=True, close_after_click=False)
        time.sleep(2)
        check()
        time.sleep(2)

    if not cmd.wait_for("Reklam Kapatılacak.", os.path.join(BASE_ASSET_DIR, 'close'), scrolldown_enabled=False, sensitive=True, timeout=10):
        cmd.find_and_click(os.path.join(BASE_ASSET_DIR, 'close'), sensitive=True, close_after_click=False)
        time.sleep(2)
        check()
        time.sleep(2)
    ###.............

    if not cmd.wait_for("Claim edilcek.", os.path.join(BASE_ASSET_DIR, 'claim'), scrolldown_enabled=True, sensitive=True):
        cmd.find_and_click(os.path.join(BASE_ASSET_DIR, 'claim'), sensitive=True, close_after_click=False)
        time.sleep(2)
        check()

    if cmd.solve_recaptcha(scrolldown_enabled=False, firstly_go_to_top=False):
        print("solve_recaptcha fail")
        tools.Logging.fail(f"logs/time/{selected_link}.txt", "solve_recaptcha fail")
        cmd.link("localhost")
        exit()
        
    cmd.wait_for("Waiting process done", _iamnotarobot_done_, scrolldown_enabled=False)

    if not cmd.wait_for("Claim edilcek.", os.path.join(BASE_ASSET_DIR, 'claim'), scrolldown_enabled=True, sensitive=True):
        cmd.find_and_click(os.path.join(BASE_ASSET_DIR, 'claim'), sensitive=True, close_after_click=False)
        time.sleep(2)
        check()
        tools.Logging.success(f"logs/time/{selected_link}.txt")
    else:
        tools.Logging.fail(f"logs/time/{selected_link}.txt", "Claim edilemedi!")
    
    time.sleep(5)
    cmd.link("localhost")
    time.sleep(5)

