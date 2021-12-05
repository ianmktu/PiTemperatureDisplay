#!/usr/bin/env python
import bme680
import unicornhathd as unicorn
import time, colorsys
import numpy as np
from datetime import datetime

canvas = None

zero = [[0,1,1,1,0],
        [1,0,0,0,1],
        [1,0,0,1,1],
        [1,0,1,0,1],
        [1,1,0,0,1],
        [1,0,0,0,1],
        [0,1,1,1,0]]

one = [[0,0,1,0,0],
       [0,1,1,0,0],
       [0,0,1,0,0],
       [0,0,1,0,0],
       [0,0,1,0,0],
       [0,0,1,0,0],
       [0,1,1,1,0]]

two = [[0,1,1,1,0],
       [1,0,0,0,1],
       [0,0,0,0,1],
       [0,0,1,1,0],
       [0,1,0,0,0],
       [1,0,0,0,0],
       [1,1,1,1,1]]

three = [[0,1,1,1,0],
         [1,0,0,0,1],
         [0,0,0,0,1],
         [0,0,1,1,0],
         [0,0,0,0,1],
         [1,0,0,0,1],
         [0,1,1,1,0]]

four = [[0,0,0,1,0],
        [0,0,1,1,0],
        [0,1,0,1,0],
        [1,0,0,1,0],
        [1,1,1,1,1],
        [0,0,0,1,0],
        [0,0,0,1,0]]

five = [[1,1,1,1,1],
        [1,0,0,0,0],
        [1,1,1,1,0],
        [0,0,0,0,1],
        [0,0,0,0,1],
        [1,0,0,0,1],
        [0,1,1,1,0]]

six = [[0,1,1,1,0],
       [1,0,0,0,1],
       [1,0,0,0,0],
       [1,1,1,1,0],
       [1,0,0,0,1],
       [1,0,0,0,1],
       [0,1,1,1,0]]

seven = [[1,1,1,1,1],
         [0,0,0,0,1],
         [0,0,0,1,0],
         [0,0,1,0,0],
         [0,0,1,0,0],
         [0,0,1,0,0],
         [0,0,1,0,0]]

eight = [[0,1,1,1,0],
         [1,0,0,0,1],
         [1,0,0,0,1],
         [0,1,1,1,0],
         [1,0,0,0,1],
         [1,0,0,0,1],
         [0,1,1,1,0]]

nine = [[0,1,1,1,0],
        [1,0,0,0,1],
        [1,0,0,0,1],
        [0,1,1,1,1],
        [0,0,0,0,1],
        [1,0,0,0,1],
        [0,1,1,1,0]]

zero_small = [[1,1,1],
              [1,0,1],
              [1,0,1],
              [1,0,1],
              [1,1,1]]

one_small = [[0,0,1],
             [0,0,1],
             [0,0,1],
             [0,0,1],
             [0,0,1]]

two_small = [[1,1,1],
             [0,0,1],
             [1,1,1],
             [1,0,0],
             [1,1,1]]

three_small = [[1,1,1],
               [0,0,1],
               [1,1,1],
               [0,0,1],
               [1,1,1]]

four_small = [[1,0,1],
              [1,0,1],
              [1,1,1],
              [0,0,1],
              [0,0,1]]

five_small = [[1,1,1],
              [1,0,0],
              [1,1,1],
              [0,0,1],
              [1,1,1]]

six_small = [[1,1,1],
             [1,0,0],
             [1,1,1],
             [1,0,1],
             [1,1,1]]

seven_small = [[1,1,1],
               [0,0,1],
               [0,1,0],
               [0,1,0],
               [0,1,0]]

eight_small = [[1,1,1],
               [1,0,1],
               [1,1,1],
               [1,0,1],
               [1,1,1]]

nine_small = [[1,1,1],
              [1,0,1],
              [1,1,1],
              [0,0,1],
              [1,1,1]]

def get_number_array(number):
  if number == 1:
    return one
  elif number == 2:
    return two
  elif number == 3:
    return three
  elif number == 4:
    return four
  elif number == 5:
    return five
  elif number == 6:
    return six
  elif number == 7:
    return seven
  elif number == 8:
    return eight
  elif number == 9:
    return nine
  else:
    return zero

def get_small_number_array(number):
  if number == 1:
    return one_small
  elif number == 2:
    return two_small
  elif number == 3:
    return three_small
  elif number == 4:
    return four_small
  elif number == 5:
    return five_small
  elif number == 6:
    return six_small
  elif number == 7:
    return seven_small
  elif number == 8:
    return eight_small
  elif number == 9:
    return nine_small
  else:
    return zero_small

def place_number(number, start_x, start_y, multiply=1):
  for y in range(7):
    for x in range(5):
      if number[y][x] != 0:
        canvas[start_x+x, start_y+y] = int(number[y][x] * multiply)

def place_small_number(number, start_x, start_y, multiply=1):
  for y in range(5):
    for x in range(3):
      if number[y][x] != 0:
        canvas[start_x+x, start_y+y] = int(number[y][x] * multiply)

if __name__ == "__main__":
  sensor = bme680.BME680()
  sensor.set_humidity_oversample(bme680.OS_2X)
  sensor.set_pressure_oversample(bme680.OS_4X)
  sensor.set_temperature_oversample(bme680.OS_8X)
  sensor.set_filter(bme680.FILTER_SIZE_3)

  unicorn.brightness(0.1)
  unicorn.rotation(270)

  current_temperature= "00.0"
  current_humidity= "00.0"

  while True:
    canvas = np.zeros([16,16], dtype=int)

    output = "{0:.1f} C, {1:.1f} %RH".format(sensor.data.temperature, sensor.data.humidity)
    print(str(datetime.now()))
    print(output)

    if sensor.get_sensor_data():
      current_temperature = str(np.around(sensor.data.temperature, decimals=1))
      current_humidity = str(np.around(sensor.data.humidity, decimals=1))

    temperature_tens = get_number_array(int(current_temperature[0]))
    temperature_units = get_number_array(int(current_temperature[1]))
    temperature_tenths = get_small_number_array(int(current_temperature[3]))

    humidity_tens = get_number_array(int(current_humidity[0]))
    humidity_units = get_number_array(int(current_humidity[1]))
    humidity_tenths = get_small_number_array(int(current_humidity[3]))

    place_number(temperature_tens, 1, 1)
    place_number(temperature_units, 7, 1)
    place_small_number(temperature_tenths, 13, 1)

    place_number(humidity_tens, 1, 9, 2)
    place_number(humidity_units, 7, 9, 2)
    place_small_number(humidity_tenths, 13, 9, 2)

    canvas = np.fliplr(canvas)

    for y in range(16):
      for x in range(16):
        if canvas[x,y] == 1:
          unicorn.set_pixel(x, y, 255, 25, 0)
        elif canvas[x,y] == 2:
          unicorn.set_pixel(x, y, 255, 45, 0)
        else:
          unicorn.set_pixel(x, y, 0, 0, 0)

    unicorn.show()

    time.sleep(15)
