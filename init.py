import commands
import numpy as np
from pynput import mouse
import time
import os
import copy
import argparse

def main(im_path):
    '''
        .............................

        Offset ayarlamak için     : o
        Son konumu göstermek için : s
        Çıkış için                : e

        .............................

    '''
    print(main.__doc__)
    print("! Lütfen Tarayıcınızı Açın")
    print("# Scrolldown ve ScrollUp klasörlerinin güncel olduğundan emin olun.")
    print("> Scrollbar-Down Lokasyonu Tespit Edilecek.")

    m = mouse.Controller()
    cmd = commands.Commands()

    pos = None
    last_pos = None

    while True:
        if not pos:
            pos = cmd.find(im_path, sensitive=True, center=True)
            last_pos = pos
            time.sleep(2)
            continue

        set = input("# Offset ayarı için [o/O], İlgili konumu kaydetmek için [s/S].\n->")
        temp_pos = list(pos)
        m.position = temp_pos
        if set.lower() == 'o':
            offset = input(">Lütfen offset'i girin (x,y)\n->")
            if '(' in offset and ')' in offset:
                offset = eval(offset)
            else:
                offset = f"({offset})"
            offset = eval(offset)
            temp_pos[0] += offset[0]
            temp_pos[1] += offset[1]
            print("# Mouse pozisyonu ayarlanıyor..")
            m.position = temp_pos
            last_pos = temp_pos
        elif set.lower() == 's':
            print(">>> Position:", last_pos)
            print("# Kaydedilecek")
        elif set.lower() == 'e':
            print("Çıkılıyor..")

            break
        else:
            print("! Bilinmeyen parametre", set)

if __name__ == '__main__':

    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--path", required=True,help="aranacak imgenin dosya yolu")
    args = vars(ap.parse_args())
    #"assets/process/scrollbar-down"
    main(im_path=args["path"])

