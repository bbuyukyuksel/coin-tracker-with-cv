import argparse
import pyautogui
import OCR
import matching

from pynput import mouse as Mouse


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path", required=True,help="image yolu")
    parser.add_argument("-o", "--offset",type=int, nargs='+', required=False,help="image yolu")
    args = parser.parse_args()
    print("args", args)

    pos = matching.matching(args.path, source="screenshot", debug=True,score_threshold=0.005)
    #pos = pyautogui.locateOnScreen(args.path)
    
    if pos:
        print("Position", list(pos))
        if args.offset:
            offset = args.offset
            pos = list(pos)
            pos[0] += offset[0]
            pos[1] += offset[1]
            pos[2] = offset[2]
            pos[3] = offset[3]
            payment_solver_text = OCR.resolve_region(pos, show=True, save='test.png')
            print(payment_solver_text)

        else:
            result = OCR.resolve_region(pos, show=True)
            mouse = Mouse.Controller()
            mouse.position = pos
            print("Result:", result)
    else:
        print("Could not detect!")

