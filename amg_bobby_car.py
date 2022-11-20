#!/usr/bin/python
#from omxplayer import OMXPlayer
import os
import os.path
print(os.path.dirname(__file__))
# Package for sounds and music
import pygame
# Package for Buttons and Leds
from gpiozero import Button, PWMLED
from time import sleep

# Package for random song selection
import random

# import lib for file list creation
import glob

# importing module
import logging
 
# Create and configure logger
# TODO: think about creating one loggin file per day.
logging.basicConfig(filename="/home/pi/AMGBobbyCar/log_file.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')
 
# Creating an object
logger = logging.getLogger()
 
# Setting the threshold of logger to DEBUG
logger.setLevel(logging.DEBUG)
    

blueButton = Button(10)
redButton = Button(15)

led_white = PWMLED(2)
led_blue = PWMLED(25)
led_red = PWMLED(21)

led_front_right = PWMLED(17)
led_front_left = PWMLED(18)
led_rear = PWMLED(27)

def startEngineAndRace():
    print('Engine run and race')
    pygame.mixer.music.load("AMG-65_race.wav")
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play()
    
def startBlueTractor():
    print('StartBlueTractor')
    filepath = os.path.dirname(__file__)
    print(filepath)
    musicpath = os.path.join(filepath, "music")
    print(musicpath)
    searchpath = os.path.join(musicpath, "*.mp3")
    print(searchpath)
    songs = glob.glob(searchpath)
    # How many songs are available in the music folder
    print(len(songs))
    #print(songs)
    #os.system('omxplayer -o alsa $(youtube-dl -g -f 140 https://www.youtube.com/watch?v=LbOve_UZZ54)')
    try:
        #sonName = pygame.mixer.music.load(os.path.join(musicpath, "Traktor.mp3"))
        #random.randrange(0,len(songs))
        sonName = pygame.mixer.music.load(os.path.join(filepath, songs[random.randrange(0,len(songs))]))
    except Exception as Argument:
        logging.exception("Error occurred while loading mp3 file")
    
    pygame.mixer.music.set_volume(0.3)
    
    try:
        pygame.mixer.music.play()
    except Exception as Argument:
        logging.exception("Error occurred while starting the song")
        
def startEngineOnly():
    print('Engine start and run')
    pygame.mixer.music.load("S65_Engine_Start_and_Run.wav")
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play()

def stopEngine():
    print('Engine stop')
    pygame.mixer.music.stop()
    #os.system('killall "omxplayer.bin"')



led_white.off()
led_blue.off()
led_red.off()
led_front_left.off()
led_front_right.off()
led_rear.off()

#led_white.blink(0.1,0.1,1,1)
#led_red.blink(0.05,0.05,0,0,None,False)
#led_blue.blink(0.05,0.05,0,0)
#led_blue.blink(0.1,0.1,1,1)
#led_blue.blink(0.05,0.05,0,0)
#led_red.blink(0.05,0.05,0,0)

#led_blue.blink(0,0,1,1)
#sleep(1)

# Let the RED LED blink all the time.
led_red.blink(0,0,1,1)
#sleep(1)
#led_front_left.blink(0,0,1,1)
#led_front_left.on()
#led_front_right.on()
#led_rear.on()
#led_front_right.blink(0,0,1,1)
#led_front_right.blink(0.1,0.1,1,1)

# Initialize pygame
pygame.init()

    #led_blue.blink(0.05,0.1,0,0,4,False)
    #led_red.blink(0.05,0.1,0,0,4,False)
    #led_blue.blink(0.1,0.1,0,0,4,False)
    #led_red.blink(0.1,0.1,0,0,4,False)
    #sleep(1)

while True:    
    if blueButton.is_pressed:
        if led_front_left.is_lit:
            stopEngine()
            led_front_left.blink(0,1,0,1,1)
            led_front_right.blink(0,1,0,1,1)
            led_rear.blink(0,1,0,1,1)
            sleep(0.5)
            led_blue.off()
        else:
            startBlueTractor()
            sleep(0.5)
            led_blue.on()
            led_front_left.blink(1,0,1,0,1)
            led_front_right.blink(1,0,1,0,1)
            led_rear.blink(1,0,1,0,1)
            sleep(1)
            led_front_left.on()
            led_front_right.on()
            led_rear.on()
        sleep(0.2)
    if redButton.is_pressed:
        startEngineOnly()
        sleep(5)


        


# Define the sound file
#engine_sound_effect = pygame.mixer.Sound('AMG-63.wav')
#engine_sound_effect = pygame.mixer.Sound('AMG-65.wav')
#engine_sound_effect = pygame.mixer.Sound('AMG-65_race.wav')


#engine_sound_effect = pygame.mixer.Sound('S65_Engine_Start_and_Run.wav')
#engine_sound_effect.set_volume(0.2)
#engine_sound_effect.play()


# Play the mp3 song
# on the bluetooth speaker
# Terminal command: omxplayer -o alsa Music/kapli.mp3
#os.system('omxplayer -o alsa Music/kapli.mp3')
