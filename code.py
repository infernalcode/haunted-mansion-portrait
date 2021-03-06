import digitalio
import audioio
import audiomp3
import board
import neopixel
from random import randrange
import time
from adafruit_led_animation.animation.pulse import Pulse

# Neopixel setup
NUM_PIXELS = 100  # Number of pixels used in project
NEOPIXEL_PIN = board.D5
POWER_PIN = board.D10

strip = neopixel.NeoPixel(NEOPIXEL_PIN, NUM_PIXELS, brightness=1, auto_write=False)
strip.fill(0)  # NeoPixels off ASAP on startup
strip.show()

#  default NeoPixel color is white
COLOR = (255, 255, 255)

#  NeoPixel animations
pulse = Pulse(strip, speed=0.01, color=COLOR, period=0.015)

# Audio Setup
AUDIO_LIBRARY = [
  open("audio/0001.mp3", "rb"),
  open("audio/0002.mp3", "rb")
]
MP3_DECODER = audiomp3.MP3Decoder(AUDIO_LIBRARY[0])
audio_enable = digitalio.DigitalInOut(board.D10)
audio_enable.direction = digitalio.Direction.OUTPUT
audio_enable.value = True

def playSound(filename, callback=lambda: {}):
  file = AUDIO_LIBRARY[filename]
  print("Playing sound file " + str(filename))
  with audioio.AudioOut(board.A0) as audio:
    MP3_DECODER.file = file
    audio.play(MP3_DECODER)

    while audio.playing:
        callback()
        pass

def thunder():
  flash_count = randrange(15, 25)
  flash_duration_min = 25
  flash_duration_max = 150

  # flash led while playing
  for flash in range(flash_count):
    pulse.animate()
    duration = randrange(flash_duration_min, flash_duration_max)
    time.sleep(duration)

def delay():
  strip.fill(0)
  strip.show()

  delay = randrange(5, 11)
  print("delay: " + str(delay))
  time.sleep(delay)

while True:
  sound = randrange(0, 2)
  playSound(sound, callback=thunder)
  delay()