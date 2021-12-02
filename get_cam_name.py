import re
import subprocess
import cv2
import os

MODE=0
DEBUG=0

def print_info(idx, name):
    print(f'[{idx}] -> {name}')

def get_camera_info_2(cam='C270'):
    cam_info = {}
    cmd = ["/usr/bin/v4l2-ctl", "--list-devices"]

    out, err = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8').communicate()
    
    for cnt in [cnts.split("\n\t") for cnts in out.strip().split("\n\n")]:
        cam_info[cnt[1]]=cnt[0]

    return cam_info

def get_camera_info():
    
    root = "/sys/class/video4linux"
    cam_info={}
    
    for index in sorted([file for file in os.listdir(root)]):        
        # Get Camera Name From /sys/class/video4linux/<video*>/name
        real_file = os.path.realpath("/sys/class/video4linux/" + index + "/name")
        with open(real_file, "r") as name_file:
            name = name_file.read().rstrip()
        # Setup Each Camera and Index ( video* )    
        cam_info[index]=name

    return cam_info


# cam_info = get_camera_info()
cam_info = get_camera_info_2()
cam_list = []

for idx, (key, val) in enumerate(cam_info.items()):
    cam_list.append(key)
    print(f'[{idx}] -> {key}   {val}')

if not DEBUG:
    sel = int(input('\nPlease Enter Index of Camera to Open: '))
    cap = cv2.VideoCapture(cam_list[sel])
    try:
        while(True):
            ret, frame = cap.read()
            cv2.imshow("test", frame)
            if cv2.waitKey(1)==ord('q'): break
    except Exception as e:
        print(f"Can't Open Camera:{sel}, Please Select {sel-1}")   
        cap.release()
        cv2.destroyAllWindows()