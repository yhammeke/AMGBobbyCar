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
leftSteeringWheelButton = Button(26)
rightSteeringWheelButton = Button(20)

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
    
def startMusicMode():
    print('startMusicMode')
    
    startRandomSong()
    
    # Control LEDs
    led_front_left.blink(0,0,1,1)
    sleep(1)
    led_front_right.blink(0,0,1,1)
    sleep(0.5)
    led_rear.blink(0,0,1,1)
    

def startRandomSong():
    
    # Select random song from the list
    randomSong = random.randrange(0,len(songs))
    print('Random song number:', randomSong)
    print('Random song name:', songs[randomSong])
    # Load random song to the pygame mixer
    try:
        pygame.mixer.music.load(os.path.join(filepath, songs[randomSong]))
    except Exception as Argument:
        logging.exception("Error occurred while loading mp3 file")
    
    # Define the volume
    pygame.mixer.music.set_volume(0.3)
    
    # Start playing the song
    try:
        pygame.mixer.music.play()
    except Exception as Argument:
        logging.exception("Error occurred while starting the song")
    print("Music is now playing...")
    pygame.mixer.music.set_endevent(END_OF_SONG)
    
def startEngineOnly():
    print('Engine start and run')
    pygame.mixer.music.load("S65_Engine_Start_and_Run.wav")
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play()

def stopEngine():
    print('Engine stop')
    pygame.mixer.music.stop()
    #os.system('killall "omxplayer.bin"')


# Turn all LEDs off at startup.

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


# Let the RED LED blink all the time.
led_red.blink(0,0,1,1)

# Initialize pygame
pygame.init()

# Define the event for the end of the song
END_OF_SONG = pygame.USEREVENT+1

# Define the path to the music folder
filepath = os.path.dirname(__file__)
musicpath = os.path.join(filepath, "music")
print(musicpath)
searchpath = os.path.join(musicpath, "*.mp3")
print(searchpath)
songs = glob.glob(searchpath)
# How many songs are available in the music folder
print(len(songs), 'songs have been found.')

# Define the vehicle status
vehicleMode = "OFF"

while True:    
    if blueButton.is_pressed:
        if vehicleMode == "OFF":
            # Start music mode
            startMusicMode()
            sleep(0.5)
            led_red.blink(0,0,1,1)
            sleep(1)
            led_blue.blink(0,0,1,1)
            #led_blue.on()
            #led_front_left.blink(1,0,1,0,1)
            #led_front_right.blink(1,0,1,0,1)
            #led_rear.blink(1,0,1,0,1)
            #sleep(1)
            #led_front_left.on()
            #led_front_right.on()
            #led_rear.on()
            vehicleMode = "MUSIC"
        elif vehicleMode == "MUSIC":
            stopEngine()
            led_front_left.blink(0,1,0,1,1)
            led_front_right.blink(0,1,0,1,1)
            led_rear.blink(0,1,0,1,1)
            sleep(0.5)
            led_blue.off()
            vehicleMode = "OFF"
        sleep(0.2)
    if redButton.is_pressed:
        startEngineOnly()
        sleep(5)
    
    if leftSteeringWheelButton.is_pressed:
        print('Left Button is pressed')
    
    
    if rightSteeringWheelButton.is_pressed:
        print('Right Button is pressed')
    
    for event in pygame.event.get():
        if event.type == END_OF_SONG:
            print('End of song')
            startRandomSong()


        


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
