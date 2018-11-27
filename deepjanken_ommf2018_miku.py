#!/usr/bin/env python3
#
# This program is modified by karaage0703
# Base software is mobilenet_based_classifier.py
# Add deepjanken function
#
# Copyright 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Script to run generic MobileNet based classification model."""
import argparse

from aiy.toneplayer import TonePlayer
from aiy.leds import Leds

from gpiozero import Button

from picamera import Color
from picamera import PiCamera

from aiy.vision import inference
from aiy.vision.models import utils

from PIL import Image
from time import sleep
import time
import pygame
from pygame.locals import *
import os
import random
import sys
import subprocess

import pygame.midi
from time import sleep

from gpiozero import Servo
from aiy.pins import PIN_A
from aiy.pins import PIN_B
from aiy.pins import PIN_C

instrument = 0

BUZZER_GPIO = 22
BUTTON_GPIO = 23

toneplayer = TonePlayer(BUZZER_GPIO)
leds = Leds()
button = Button(BUTTON_GPIO)

BEEP_SOUND = ('E6q', 'C6q')
RED = (0xFF, 0x00, 0x00)
GREEN = (0x00, 0xFF, 0x00)
BLUE = (0x00, 0x00, 0xFF)
WHITE = (0xFF, 0xFF, 0xFF)

gu_servo = Servo(PIN_A, initial_value=0, min_pulse_width=.0006, max_pulse_width=.00235)
choki_servo = Servo(PIN_B, initial_value=0, min_pulse_width=.0006, max_pulse_width=.00235)
pa_servo = Servo(PIN_C, initial_value=0, min_pulse_width=.0006, max_pulse_width=.00235)

shutter_numb = 0
photo_filename = 'janken.jpg'
photo_dir = os.path.expanduser('/home/pi/janken_data')

font_size = 150

parser = argparse.ArgumentParser()
parser.add_argument('--model_path', required=True,
    help='Path to converted model file that can run on VisionKit.')
parser.add_argument('--label_path', required=True,
    help='Path to label file that corresponds to the model.')
parser.add_argument('--input_height', type=int, required=True, help='Input height.')
parser.add_argument('--input_width', type=int, required=True, help='Input width.')
parser.add_argument('--input_layer', required=True, help='Name of input layer.')
parser.add_argument('--output_layer', required=True, help='Name of output layer.')
parser.add_argument('--input_mean', type=float, default=128.0, help='Input mean.')
parser.add_argument('--input_std', type=float, default=128.0, help='Input std.')
parser.add_argument('--input_depth', type=int, default=3, help='Input depth.')
parser.add_argument('--threshold', type=float, default=0.1,
    help='Threshold for classification score (from output tensor).')
parser.add_argument('--top_k', type=int, default=1, help='Keep at most top_k labels.')
args = parser.parse_args()


def miku_first_gu():
    midiOutput.write_sys_ex(0, b'\xF0\x43\x79\x09\x11\x0A\x00\x15\x01\x23\x47\x0C\xF7')
    midiOutput.write_short(0xB0, 0x5B, 0x1F) # reverb

    midiOutput.note_on(64,80)
    sleep(.300)
    midiOutput.note_off(64,80)

    midiOutput.note_on(62,80)
    sleep(.300)
    midiOutput.note_off(62,80)

    midiOutput.note_on(64,80)
    sleep(.300)
    midiOutput.note_off(64,80)

    midiOutput.note_on(66,80)
    sleep(.300)
    midiOutput.note_off(66,80)

    midiOutput.note_on(68,80)
    sleep(.900)
    midiOutput.note_off(68,80)

def miku_win():
    midiOutput.write_sys_ex(0, b'\xF0\x43\x79\x09\x11\x0A\x00\x00\x3F\x29\x43\x64\x08\xF7')
    midiOutput.write_short(0xB0, 0x5B, 0x3F) # reverb

    midiOutput.note_on(64,80)
    sleep(.300)
    midiOutput.note_off(64,80)

    midiOutput.note_on(66,80)
    sleep(.300)
    midiOutput.note_off(66,80)

    midiOutput.note_on(64,80)
    sleep(.300)
    midiOutput.note_off(64,80)

    midiOutput.note_on(64,80)
    sleep(.300)
    midiOutput.note_off(64,80)

    midiOutput.note_on(60,80)
    sleep(.500)
    midiOutput.note_off(60,80)

    midiOutput.note_on(60,80)
    sleep(.700)
    midiOutput.note_off(60,80)

def miku_lose():
    midiOutput.write_sys_ex(0, b'\xF0\x43\x79\x09\x11\x0A\x00\x00\x3F\x29\x43\x05\x00\x36\xF7')
    midiOutput.write_short(0xB0, 0x5B, 0x3F) # reverb

    midiOutput.note_on(64,80)
    sleep(.300)
    midiOutput.note_off(64,80)

    midiOutput.note_on(66,80)
    sleep(.300)
    midiOutput.note_off(66,80)

    midiOutput.note_on(64,80)
    sleep(.300)
    midiOutput.note_off(64,80)

    midiOutput.note_on(64,80)
    sleep(.300)
    midiOutput.note_off(64,80)

    midiOutput.note_on(66,80)
    sleep(.700)
    midiOutput.note_off(66,80)

    midiOutput.note_on(64,80)
    sleep(.300)
    midiOutput.note_off(64,80)

    midiOutput.note_on(66,80)
    sleep(.300)
    midiOutput.note_off(66,80)

def miku_draw():
    midiOutput.write_sys_ex(0, b'\xF0\x43\x79\x09\x11\x0A\x00\x00\x01\x09\xF7')
    midiOutput.write_short(0xB0, 0x5B, 0x3F) # reverb

    midiOutput.note_on(64,80)
    sleep(.800)
    midiOutput.note_off(64,80)

    midiOutput.note_on(62,80)
    sleep(.200)
    midiOutput.note_off(62,80)

    midiOutput.note_on(64,80)
    sleep(.300)
    midiOutput.note_off(64,80)

def miku_hatena():
    midiOutput.write_sys_ex(0, b'\xF0\x43\x79\x09\x11\x0A\x00\x19\x72\x3F\x00\x40\xF7')
    midiOutput.write_short(0xB0, 0x5B, 0x3F) # reverb

    midiOutput.note_on(64,80)
    sleep(.300)
    midiOutput.note_off(64,80)

    midiOutput.note_on(64,80)
    sleep(.300)
    midiOutput.note_off(64,80)

    midiOutput.note_on(66,80)
    sleep(.500)
    midiOutput.note_off(66,80)

    midiOutput.note_on(64,80)
    sleep(.200)
    midiOutput.note_off(64,80)

    midiOutput.note_on(66,80)
    sleep(.300)
    midiOutput.note_off(66,80)

def loadFile():
    global shutter_numb

    if os.path.isdir(photo_dir):
        pass
    else:
        print("make photo directory")
        os.mkdir(photo_dir)
        filename = os.path.join(photo_dir, 'camera.set')
        with open(filename, mode='w') as fp:
            fp.write('0')

    filename = os.path.join(photo_dir, 'camera.set')

    with open(filename) as fp:
        fp = open(filename)
        tmp_shutter_numb = fp.readlines()
        tmp_shutter_numb = tmp_shutter_numb[0].rstrip()
        shutter_numb = int(tmp_shutter_numb)

def read_labels(label_path):
    with open(label_path) as label_file:
        return [label.strip() for label in label_file.readlines()]


model = inference.ModelDescriptor(
    name='mobilenet_based_classifier',
    input_shape=(1, args.input_height, args.input_width, args.input_depth),
    input_normalizer=(args.input_mean, args.input_std),
    compute_graph=utils.load_compute_graph(args.model_path))
labels = read_labels(args.label_path)


def get_message(result, threshold, top_k):
    if result:
        return '%s' % '\n'.join(result)
    else:
        return 'Nothing detected when threshold=%.2f, top_k=%d' % (threshold, top_k)

def process(result, labels, tensor_name, threshold, top_k):
    """Processes inference result and returns labels sorted by confidence."""
    # MobileNet based classification model returns one result vector.
    assert len(result.tensors) == 1
    tensor = result.tensors[tensor_name]
    probs, shape = tensor.data, tensor.shape
    assert shape.depth == len(labels)
    pairs = [pair for pair in enumerate(probs) if pair[1] > threshold]
    pairs = sorted(pairs, key=lambda pair: pair[1], reverse=True)
    pairs = pairs[0:top_k]
    # return [' %s (%.2f)' % (labels[index], prob) for index, prob in pairs]
    return ['%s' % (labels[index]) for index, prob in pairs]

def test_mode(test_time = 30):
    with PiCamera(sensor_mode=4, resolution=(1640, 1232), framerate=30) as camera:
        camera.start_preview()

        with inference.CameraInference(model) as camera_inference:
            for result in camera_inference.run(test_time):
                processed_result = process(result, labels, args.output_layer,
                                           args.threshold, 1)
                message = get_message(processed_result, args.threshold, 1)
                # print(message)

                camera.annotate_text_size = 120
                # camera.annotate_foreground = Color('black')
                # camera.annotate_background = Color('white')
                # PiCamera text annotation only supports ascii.
                camera.annotate_text = '\n %s' % message.encode(
                    'ascii', 'backslashreplace').decode('ascii')

def manual_screen():
    screen.fill((255,255,255))
    text = japanese_font.render(u"ボタンを押したら始まるよ！", True, (0,0,0))
    screen.blit(text, [size[0]/2-font_size/2-300, size[1]/2-font_size/2-200])
    text = japanese_font.render(u"ボタン長押しで認識モードだよ！", True, (0,0,0))
    screen.blit(text, [size[0]/2-font_size/2-350, size[1]/2-font_size/2+200])
    pygame.display.update()

def first_gu():
    screen.fill((255,255,255))
    text = japanese_font.render(u"最初はグー", True, (0,0,0))
    screen.blit(text, [size[0]/2-font_size/2-50, size[1]/2-font_size/2])
    pygame.display.update()
    miku_first_gu()
    sleep(3.0)
    screen.fill((255,255,255))
    pygame.display.update()

    test_mode(test_time = 30)
    gu_servo.min()

def janken_screen():
    midiOutput.write_sys_ex(0, b'\xF0\x43\x79\x09\x11\x0A\x00\x24\x7B\x08\x7B\x55\x7B\xF7')
    midiOutput.write_short(0xB0, 0x5B, 0x1F) # reverb

    screen.fill((255,255,255))
    text = japanese_font.render(u"ジャン", True, (0,0,0))
    screen.blit(text, [size[0]/2-font_size/2, size[1]/2-font_size/2])
    pygame.display.update()
    midiOutput.note_on(70,80)
    sleep(.200)
    midiOutput.note_off(70,80)

    midiOutput.note_on(70,80)
    sleep(.200)
    midiOutput.note_off(70,80)

    sleep(1.0)

    screen.fill((255,255,255))
    text = japanese_font.render(u"ケン", True, (0,0,0))
    screen.blit(text, [size[0]/2-font_size/2, size[1]/2-font_size/2])
    pygame.display.update()
    midiOutput.note_on(68,80)
    sleep(.200)
    midiOutput.note_off(68,80)

    midiOutput.note_on(68,80)
    sleep(.200)
    midiOutput.note_off(68,80)

    sleep(1.0)

    screen.fill((255,255,255))
    text = japanese_font.render(u"ポン", True, (0,0,0))
    screen.blit(text, [size[0]/2-font_size/2, size[1]/2-font_size/2])
    pygame.display.update()
    midiOutput.note_on(70,80)
    sleep(.200)
    midiOutput.note_off(70,80)

    midiOutput.note_on(70,80)
    sleep(.200)
    midiOutput.note_off(70,80)

    sleep(1.0)

    screen.fill((255,255,255))
    pygame.display.update()

def result_screen(result):
    if result == 'win':
        text = japanese_font.render(u"あなたの勝ち！", True, (0,0,0))
        screen.blit(text, [size[0]/4-font_size*1.5/2 , size[1]/4*3-font_size/2])
        pygame.display.update()
        miku_lose()

    if result == 'draw':
        text = japanese_font.render(u"ひきわけ！", True, (0,0,0))
        screen.blit(text, [size[0]/4-font_size*1.5/2 , size[1]/4*3-font_size/2])
        pygame.display.update()
        miku_draw()

    if result == 'lose':
        text = japanese_font.render(u"あなたの負け！", True, (0,0,0))
        screen.blit(text, [size[0]/4-font_size*1.5/2 , size[1]/4*3-font_size/2])
        pygame.display.update()
        miku_win()

    if result == 'etc':
        text = japanese_font.render(u"それ何の手？", True, (0,0,0))
        screen.blit(text, [size[0]/4-font_size*1.5/2 , size[1]/4*3-font_size/2])
        pygame.display.update()
        miku_hatena()


def janken(your_hand):
    janken_result = 'etc'
    ai_hand = random.choice(['gu', 'choki', 'pa'])

    screen.fill((255,255,255))

    text = japanese_font.render("Deep Janken", True, (0,0,0))
    screen.blit(text, [size[0]/4-font_size/2-100 , size[1]/4-font_size/2])
    text = japanese_font.render("You", True, (0,0,0))
    screen.blit(text, [size[0]/4*3-font_size/2 , size[1]/4-font_size/2])

    if ai_hand == 'gu':
        text = japanese_font.render(u"グー", True, (0,0,0))
        screen.blit(text, [size[0]/4-font_size/2 , size[1]/2-font_size/2])
        gu_servo.max()

    if ai_hand == 'choki':
        text = japanese_font.render(u"チョキ", True, (0,0,0))
        screen.blit(text, [size[0]/4-font_size/2, size[1]/2-font_size/2])
        choki_servo.max()

    if ai_hand == 'pa':
        text = japanese_font.render(u"パー", True, (0,0,0))
        screen.blit(text, [size[0]/4-font_size/2, size[1]/2-font_size/2])
        pa_servo.max()

    if your_hand == 'gu':
        text = japanese_font.render(u"グー", True, (0,0,0))
        screen.blit(text, [size[0]/4*3-font_size/2 , size[1]/2-font_size/2])

    if your_hand == 'choki':
        text = japanese_font.render(u"チョキ", True, (0,0,0))
        screen.blit(text, [size[0]/4*3-font_size/2 , size[1]/2-font_size/2])

    if your_hand == 'pa':
        text = japanese_font.render(u"パー", True, (0,0,0))
        screen.blit(text, [size[0]/4*3-font_size/2 , size[1]/2-font_size/2])

    if your_hand == 'etc':
        text = japanese_font.render(u"はてな？", True, (0,0,0))
        screen.blit(text, [size[0]/4*3-font_size/2 , size[1]/2-font_size/2])

    if ai_hand == 'gu':
        if your_hand == 'gu':
            janken_result = 'draw'
        if your_hand == 'choki':
            janken_result = 'lose'
        if your_hand == 'pa':
            janken_result = 'win'

    if ai_hand == 'choki':
        if your_hand == 'gu':
            janken_result = 'win'
        if your_hand == 'choki':
            janken_result = 'draw'
        if your_hand == 'pa':
            janken_result = 'lose'

    if ai_hand == 'pa':
        if your_hand == 'gu':
            janken_result = 'lose'
        if your_hand == 'choki':
            janken_result = 'win'
        if your_hand == 'pa':
            janken_result = 'draw'

    result_screen(janken_result)

    pygame.display.update()
    sleep(10.0)

def hand_recog():
    global shutter_numb

    # load shutter number from setting file
    loadFile()
    filename = os.path.join(photo_dir, 'camera.set')

    shutter_numb +=1
    # write shutter number to setting file
    with open(filename, mode='w') as fp:
        fp.write(str(shutter_numb))

    print("Taking photo")
    with PiCamera(sensor_mode=4, resolution=(1640, 1232), framerate=30) as camera:
        # camera.awb_mode = 'sunlight'
        camera.start_preview()
        sleep(3.000)
        camera.capture(photo_filename)

        filename = os.path.join(photo_dir, str("{0:06d}".format(shutter_numb)) + '.jpg')
        camera.capture(filename)

    with inference.ImageInference(model) as image_inference:
        image = Image.open(photo_filename)
        result = image_inference.run(image)
        processed_result = process(result, labels, args.output_layer,
                                    args.threshold, args.top_k)
        message = get_message(processed_result, args.threshold, args.top_k)

    return message

def KeepWatchForSeconds(seconds):
    GoFlag = True
    while seconds > 0:
        time.sleep(0.1)
        seconds -= 0.1
        if not button.is_pressed:
            GoFlag = False
            break
    return GoFlag

def run():
    if KeepWatchForSeconds(3):
        print("Go test mode")
        leds.update(Leds.rgb_on(BLUE))
        test_mode(test_time = 100)
        manual_screen()
        leds.update(Leds.rgb_on(WHITE))

    else:
        print("Beep sound")
        toneplayer.play(*BEEP_SOUND)

        leds.update(Leds.rgb_on(RED))
        print("process")
        gu_servo.max()
        first_gu()
        janken_screen()
        your_hand = hand_recog()
        janken(your_hand)

        print("Done")
        gu_servo.min()
        choki_servo.min()
        pa_servo.min()
        leds.update(Leds.rgb_on(WHITE))
        manual_screen()

def main():
    button.when_pressed = run
    leds.update(Leds.rgb_on(WHITE))
    manual_screen()

    while True:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    leds.update(Leds.rgb_off())
                    midiOutput.close()
                    pygame.midi.quit()
                    sys.exit()

if __name__ == '__main__':
    pygame.init()
    pygame.midi.init()

    gu_servo.max()
    gu_servo.min()
    choki_servo.max()
    choki_servo.min()
    pa_servo.max()
    pa_servo.min()

    for i in range(pygame.midi.get_count()):
        interf, name, input_dev, output_dev, opened = pygame.midi.get_device_info(i)
        if output_dev and b'NSX-39 ' in name:
            print(i)
            midiOutput = pygame.midi.Output(i)

    midiOutput.set_instrument(instrument)

    font = pygame.font.Font(None, font_size)
    japanese_font = pygame.font.Font(os.path.join('/usr/share/fonts/truetype/fonts-japanese-gothic.ttf'), 60)
    big_font = pygame.font.Font(None, (int)(font_size*1.5))
    size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
    print("Framebuffer size: %d x %d" % (size[0], size[1]))
    screen = pygame.display.set_mode(size, pygame.FULLSCREEN)

    main()
