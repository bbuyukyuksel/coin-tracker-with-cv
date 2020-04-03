import tools
import datetime
from commands import Commands
import time

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
    selected_link = "bitcoinker"
    cmd.link(links[selected_link])
    cmd.wait_for("HTML is done?", f'assets/{selected_link}/htmlisdone.png', scrolldown_enabled=False)
    # Solve Recaptha
    if cmd.solve_recaptcha():
        print("solve_recaptcha fail")
        tools.Logging.fail(f"logs/time/{selected_link}.txt")
        cmd.link("www.google.com")
        return
    # _____________________________
    cmd.wait_for("Waiting process done", _iamnotarobot_done_, scrolldown_enabled=False)
    cmd.wait_for("Claim edilcek.", r'assets\bitcoinker\claim_bitcoin', scrolldown_enabled=True, sensitive=True)
    cmd.find_and_click(r'assets\bitcoinker\claim_bitcoin', sensitive=True)
    time.sleep(2)
    # Payment Solver
    cmd.payment_solver(selected_link, sensitive=True)
    # _____________________________
    tools.Logging.success(f"logs/time/{selected_link}.txt")
    cmd.link("www.google.com")

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
    selected_link = "bonusbitcoin"
    
    cmd.link(links[selected_link])
    cmd.wait_for("HTML is done?", f'assets/{selected_link}/htmlisdone.png', scrolldown_enabled=False)
    
    if cmd.solve_recaptcha():
        print("solve_recaptcha fail")
        tools.Logging.fail(f"logs/time/{selected_link}.txt")
        cmd.link("www.google.com")
        return
    
    cmd.wait_for("Waiting process done", _iamnotarobot_done_, scrolldown_enabled=False)
    cmd.wait_for("Claim edilcek.", f'assets\{selected_link}\claim_now.png', scrolldown_enabled=True, sensitive=True)
    cmd.find_and_click(f'assets\{selected_link}\claim_now.png', sensitive=True)
    time.sleep(2)
    
    cmd.payment_solver(selected_link, sensitive=True)
    tools.Logging.success(f"logs/time/{selected_link}.txt")
    cmd.link("www.google.com")

def freebitco():
    '''
        Recipe name: bonusbitcoin
    '''
    _iamnotarobot_ = "assets/iamnotarobot"
    _iamnotarobot_done_ = "assets/iamnotarobot-done"

    config = tools.JSON.get("config.json")
    links = config["links"]
    cmd = Commands()
    cmd.is_animation_on = True
    selected_link = "freebitco"
    
    cmd.link(links[selected_link])
    cmd.wait_for("HTML is done?", f'assets/{selected_link}/htmlisdone.png', scrolldown_enabled=False)
    cmd.mouse.position = config["location"]["temp"]
    cmd.click_l()

    if cmd.solve_recaptcha():
        print("solve_recaptcha fail")
        tools.Logging.fail(f"logs/time/{selected_link}.txt")
        cmd.link("www.google.com")
        return
        
    cmd.wait_for("Waiting process done", _iamnotarobot_done_, scrolldown_enabled=False)
    cmd.wait_for("Roll edilcek.", f'assets/{selected_link}/roll.png', scrolldown_enabled=True, sensitive=True)
    cmd.find_and_click(f'assets/{selected_link}/roll.png', sensitive=True)
    time.sleep(2)
    cmd.mouse.position = config["location"]["temp"]
    cmd.click_l()
    cmd.payment_solver(selected_link, sensitive=True)
    tools.Logging.success(f"logs/time/{selected_link}.txt")
    cmd.link("www.google.com")