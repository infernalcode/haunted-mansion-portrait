import digitalio
import audioio
import audiomp3
import board
import neopixel
from random import randrange
import time
from adafruit_led_animation.animation.solid import Solid
from adafruit_led_animation.animation.pulse import Pulse
from adafruit_led_animation.animation.comet import Comet
from adafruit_led_animation.animation.sparklepulse import SparklePulse

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
solid = Solid(strip, color=COLOR)
comet = Comet(strip, speed=0.01, color=COLOR, tail_length=2)
sparkle_pulse = SparklePulse(strip, speed=0.001, period=10, color=COLOR)

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

def lightning():
  # number of flashes per cycle
  flashCount = randrange(15, 25)

  # flash duration range - ms
  flashDurationMin = 25
  flashDurationMax = 150

  # time to next flash range - ms
  nextFlashDelayMin = 25
  nextFlashDelayMax = 75

  # randomize pause between strikes
  pauseBottom = 5000
  pauseTop = 10000
  strikeDelay = randrange(pauseBottom, pauseTop)

  # flash led while playing

  for flash in range(flashCount):
    pulse.animate()
    duration = randrange(flashDurationMin, flashDurationMax) / 1000
    time.sleep(duration)


def delay():
  strip.fill(0)
  strip.show()

  delay = randrange(5, 11)
  print("delay: " + str(delay))
  time.sleep(delay)

while True:
  sound = randrange(0, 2)
  playSound(sound, callback=lightning)
  delay()