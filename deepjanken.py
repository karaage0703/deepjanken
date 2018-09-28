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

from picamera import Color
from picamera import PiCamera

from aiy.vision import inference
from aiy.vision.models import utils

from PIL import Image
from time import sleep
import pygame
from pygame.locals import *
import os
import random

photo_filename = 'janken.jpg'
font_size = 150

def read_labels(label_path):
    with open(label_path) as label_file:
        return [label.strip() for label in label_file.readlines()]

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

def janken_screen():
    screen.fill((0,0,0))
    text = big_font.render("Jan", True, (255,255,255))
    screen.blit(text, [size[0]/2-font_size/2, size[1]/2-font_size/2])
    pygame.display.update()
    sleep(2.0)
    screen.fill((0,0,0))
    text = big_font.render("Ken", True, (255,255,255))
    screen.blit(text, [size[0]/2-font_size/2, size[1]/2-font_size/2])
    pygame.display.update()
    sleep(2.0)
    screen.fill((0,0,0))
    text = big_font.render("Pon", True, (255,255,255))
    screen.blit(text, [size[0]/2-font_size/2, size[1]/2-font_size/2])
    pygame.display.update()
    sleep(2.0)

    screen.fill((0,0,0))
    pygame.display.update()

def result_screen(result):
    if result == 'win':
        text = big_font.render("You Win!", True, (255,255,255))
        screen.blit(text, [size[0]/4-font_size*1.5/2 , size[1]/4*3-font_size/2])

    if result == 'draw':
        text = big_font.render("Draw", True, (255,255,255))
        screen.blit(text, [size[0]/4-font_size*1.5/2 , size[1]/4*3-font_size/2])

    if result == 'lose':
        text = big_font.render("You Lose...", True, (255,255,255))
        screen.blit(text, [size[0]/4-font_size*1.5/2 , size[1]/4*3-font_size/2])

def janken(your_hand):
    ai_hand = random.choice(['gu', 'choki', 'pa'])

    screen.fill((0,0,0))

    text = font.render("AI", True, (255,255,255))
    screen.blit(text, [size[0]/4-font_size/2 , size[1]/4-font_size/2])
    text = font.render("You", True, (255,255,255))
    screen.blit(text, [size[0]/4*3-font_size/2 , size[1]/4-font_size/2])

    if ai_hand == 'gu':
        text = font.render("Gu", True, (255,255,255))
        screen.blit(text, [size[0]/4-font_size/2 , size[1]/2-font_size/2])

    if ai_hand == 'choki':
        text = font.render("Choki", True, (255,255,255))
        screen.blit(text, [size[0]/4-font_size/2, size[1]/2-font_size/2])

    if ai_hand == 'pa':
        text = font.render("Pa", True, (255,255,255))
        screen.blit(text, [size[0]/4-font_size/2, size[1]/2-font_size/2])

    if your_hand == 'gu':
        text = font.render("Gu", True, (255,255,255))
        screen.blit(text, [size[0]/4*3-font_size/2 , size[1]/2-font_size/2])

    if your_hand == 'choki':
        text = font.render("Choki", True, (255,255,255))
        screen.blit(text, [size[0]/4*3-font_size/2 , size[1]/2-font_size/2])

    if your_hand == 'pa':
        text = font.render("Pa", True, (255,255,255))
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
    sleep(5.0)

def main():
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

    model = inference.ModelDescriptor(
        name='mobilenet_based_classifier',
        input_shape=(1, args.input_height, args.input_width, args.input_depth),
        input_normalizer=(args.input_mean, args.input_std),
        compute_graph=utils.load_compute_graph(args.model_path))
    labels = read_labels(args.label_path)

    print("Taking photo")
    with PiCamera() as camera:
        camera.resolution = (640, 480)
        camera.start_preview()
        sleep(3.000)
        camera.capture(photo_filename) 

    with inference.ImageInference(model) as image_inference:
        image = Image.open(photo_filename)
        result = image_inference.run(image)
        processed_result = process(result, labels, args.output_layer,
                                    args.threshold, args.top_k)
        message = get_message(processed_result, args.threshold, args.top_k)

    return message

if __name__ == '__main__':
    pygame.init()
    font = pygame.font.Font(None, font_size)
    big_font = pygame.font.Font(None, (int)(font_size*1.5))
    size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
    print("Framebuffer size: %d x %d" % (size[0], size[1]))
    screen = pygame.display.set_mode(size, pygame.FULLSCREEN)

    janken_screen()
    your_hand = main()
    janken(your_hand)