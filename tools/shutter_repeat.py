# -*- coding: utf-8 -*-
import subprocess
import picamera
import os
from time import sleep

shutter_numb = 0
photo_dir = os.path.expanduser('/home/pi/photo_data')

camera = picamera.PiCamera()

def setting():
    camera.resolution = (1640,1232)
#    camera.awb_mode = 'sunlight'
    camera.sensor_mode = 4
    camera.framerate=30
    # camera.brightness = 50
    # camera.flash_mode = 'on'
    # camera.exposure_compensation = 0

def preview(preview_time = 3):
    camera.start_preview()
    sleep(preview_time)
    camera.stop_preview()

def loadFile():
    global shutter_numb

    if os.path.isdir(photo_dir):
        pass
    else:
        print("make photo directory")
        os.mkdir(photo_dir)

    filename = os.path.join(photo_dir, 'camera.set')

    with open(filename) as fp:
        fp = open(filename)
        tmp_shutter_numb = fp.readlines()
        tmp_shutter_numb = tmp_shutter_numb[0].rstrip()
        shutter_numb = int(tmp_shutter_numb)

def shutter():
    global shutter_numb

    # load shutter number from setting file
    loadFile()

    filename = os.path.join(photo_dir, 'camera.set')

    shutter_numb +=1

    # write shutter number to setting file
    with open(filename, mode='w') as fp:
        fp.write(str(shutter_numb))

    # take photo
    filename = os.path.join(photo_dir, str("{0:06d}".format(shutter_numb)) + '.jpg')
    print(filename)
    with open(filename, mode='wb') as fp:
        camera.capture(fp)

if __name__ == '__main__':
    setting()
    preview(preview_time=5)
    try:
        while True:
            preview(preview_time=2)
            shutter()

    except KeyboardInterrupt:
        print('interrupted!')
        camera.close()
