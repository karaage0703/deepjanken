#!/usr/bin/env python3
"""Demonstrates simultaneous control of two servos on the hat.

One servo uses the simple default configuration, the other servo is tuned to
ensure the full range is reachable.
"""

from time import sleep
from gpiozero import Servo
from aiy.pins import PIN_A
from aiy.pins import PIN_B
from aiy.pins import PIN_C

# Create a default servo that will not be able to use quite the full range.
# simple_servo = Servo(PIN_A)
# Create a servo with the custom values to give the full dynamic range.
gu_servo = Servo(PIN_A, initial_value=0, min_pulse_width=.0006, max_pulse_width=.00235)
choki_servo = Servo(PIN_B, initial_value=0, min_pulse_width=.0006, max_pulse_width=.00235)
pa_servo = Servo(PIN_C, initial_value=0, min_pulse_width=.0006, max_pulse_width=.00235)

print("init")
gu_servo.max()
gu_servo.min()
choki_servo.max()
choki_servo.min()
pa_servo.max()
pa_servo.min()

sleep(5)
print("gu")
gu_servo.max()
sleep(5)
gu_servo.min()
sleep(5)

print("choki")
choki_servo.max()
sleep(5)
choki_servo.min()
sleep(5)

print("pa")
pa_servo.max()
sleep(5)
pa_servo.min()
sleep(5)


# gu_servo.value=1.0
# gu_servo.value=0.0
# gu_servo.value=-1.0
# gu_servo.mid()
