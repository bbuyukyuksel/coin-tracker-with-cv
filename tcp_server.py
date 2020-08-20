from socket import *
import urllib

import re
import time
import threading
from commands import Commands

class TCPServer(threading.Thread):
    def __init__(self, host='', port=8081):
        super().__init__()
        self.host = host
        self.port = port

    def run(self):
        serverSocket = socket(AF_INET, SOCK_STREAM)
        #Prepare a sever socket
        serverSocket.bind(('', 8081))
        serverSocket.listen(1)
        print("Ready to server")
        #Establish the connection
        connectionSocket, addr = serverSocket.accept()
        try:
            self.data = connectionSocket.recv(1024)
            #Send one HTTP header line into socket
            connectionSocket.send('HTTP/1.0 200 OK\r\n\r\n'.encode())
            #outputdata = "Welcome to coin tracker"
            #for i in range(0, len(outputdata)):
            #    connectionSocket.send(outputdata[i].encode())
            #connectionSocket.close()
        except IOError:
            pass
            #Send response message for file not found
            #connectionSocket.send('404 Not Found')
            #Close client socket
            #connectionSocket.close()
        serverSocket.close()
        return self

    def get_request(self) -> dict:
        data = self.request()
        get_request = re.match('GET(.*)HTTP/1.1', data).group(1).strip()
        if get_request.startswith('/?'):
            get_request_pairs = get_request[2:].split('&')
            get_request_params = {i.split('=')[0]:i.split('=')[1] for i in get_request_pairs}
        return get_request_params

    def get_request_extract_link(self):
        data = self.request()
        get_request = re.match('GET(.*)HTTP/1.1', data).group(1).strip()
        return get_request.split('link=')[1]
    
    def request(self):
        return self.data.decode('utf-8')
        


def captcha_solver():
    cmd = Commands()
    cmd.is_animation_on = False
    STATE = 'INIT'

    while True:
        if STATE == 'INIT':
            print(f"State: {STATE}")
            print("Solve Recaptha")
            STATE = 'FIND_BOX'

        elif STATE == 'FIND_BOX':
            print(f"State: {STATE}")
            pos = cmd.find('assets/box', center=True)
            if pos:
                cmd.setMousePosition(pos).click_l(close_after_click=False)
                STATE = 'CHECK_VIEW'; continue;
            STATE = 'INIT'
            
        elif STATE == 'CHECK_VIEW':
            print(f"State: {STATE}")
            cmd.resetMousePosition()
            pos_image_view = cmd.find('assets/solver/solver_image', center=True)
            if pos_image_view: STATE = 'SWITCH_TO_AUDIO'; continue;

            cmd.resetMousePosition()
            pos_audio_view = cmd.find('assets/solver/solver_audio', center=True)
            if pos_audio_view: STATE = 'SOLVE_AUDIO'; continue;

            if not (pos_image_view or pos_audio_view):
                # Her ikiside bulunamadıysa.
                STATE = 'INIT'; continue
            
        elif STATE == 'SWITCH_TO_AUDIO':
            cmd.resetMousePosition()
            pos = cmd.find('assets/solver/solver_image', center=True)
            if pos:
                cmd.setMousePosition(pos).click_l(close_after_click=False)
                STATE = 'SOLVE_AUDIO'; continue;
            else:
                STATE = 'CHECK_VIEW'; continue;

        elif STATE == 'SOLVE_AUDIO':
            print(f"State: {STATE}")
            cmd.resetMousePosition()
            pos = cmd.find('assets/play.png', center=True) 
            if pos: 
                cmd.setMousePosition(pos).click_r()
                time.sleep(0.5)
            
                cmd.resetMousePosition()           
                pos = cmd.find('assets/inspect.png', center=True)
                time.sleep(2)

                if pos: 
                    cmd.setMousePosition(pos).click_l(close_after_click=False)
                    pos = cmd.find('assets/console.png', center=True)
                    if pos:
                        cmd.setMousePosition(pos).click_l(close_after_click=False)
                        # Consol ekranında.
                        get_data_from_website = [
                            "clear();",
                            "var src = document.getElementById('audio-source').src;",
                            "src;",
                        ]
                        cmd.find_and_click('assets/script_area.png', close_after_click=False)    
                        for i, script in enumerate(get_data_from_website):
                            print(i, script)
                            time.sleep(0.5)
                            cmd.type(script).enter()
                            time.sleep(0.2)

                        server = TCPServer()
                        server.start()

                        get_request_to_python = [
                            "var xhttp = new XMLHttpRequest();",
                            f"xhttp.open('GET', 'http://127.0.0.1:8081?link='+src, true);",
                            "xhttp.send();"
                        ]
                        for i, script in enumerate(get_request_to_python):
                            print(i, script)
                            time.sleep(0.5)
                            cmd.type(script).enter()
                        
                        server.join()
                        __link__ = server.get_request_extract_link()
                        print("Link:", __link__)
                        urllib.urlretrieve (__link__, "audio.mp3")
                        #print(server.get_request().get('src'))
                        STATE = "FINISH"


            else:
                STATE = 'INIT'; continue;
            

        elif STATE == 'ERROR:SO_MUCH_QUERY':
            print(f"State: {STATE}")

        elif STATE == 'FINISH':
            pass
        time.sleep(2)


if __name__ == '__main__':

    captcha_solver()
    
    '''
    server = TCPServer()
    server.start()
    server.join()
    server.request()
    '''
   
    
    
    


