#!/usr/bin/python
import os
import os.path
print(os.path.dirname(__file__))
# Package for sounds and music
import pygame
# Package for Buttons and Leds
from gpiozero import Button, PWMLED
from time import sleep, time
import datetime

# Package for random song selection
import random

# Package for file list creation
import glob

# Package for Logging
import logging

from enum import Enum

from pynput.keyboard import Key, Listener
import threading
 
# Create and configure logger
# TODO: think about creating one loggin file per day.
logging.basicConfig(filename="/home/pi/AMGBobbyCar/log_file.log" + str(datetime.datetime.now()),
                    format='%(asctime)s %(message)s',
                    filemode='w')
 
# Creating an object
logger = logging.getLogger()
# Setting the threshold of logger to DEBUG
logger.setLevel(logging.DEBUG)

##########################
# HARDWARE CONFIGURATION #
##########################

# Buttons
blueButton = Button(10)  # Instrument Cluster Blue Button
redButton = Button(15)   # Instrument Cluster Red Button
leftSteeringWheelButton = Button(20)  # Left Button of the Steering Wheel 
rightSteeringWheelButton = Button(26) # Right Button of the Steering Wheel

# Switches
IgnSwitch = Button(9)    # Ignition Switch
OnOffSwitch = Button(11) # On Off Button

# Lights
led_white = PWMLED(2) # Power ON LED
led_blue = PWMLED(25) # Instrument Cluster Right LED
led_red = PWMLED(21)  # Instrument Cluster Left LED

led_front_right = PWMLED(17)  # Front right headlight
led_front_left = PWMLED(18)   # Front left headlight
led_rear = PWMLED(27)         # Taillights
led_ic = PWMLED(22)           # Instrument Cluster Backlight

#####################################
# END OF THE HARDWARE CONFIGURATION #
#####################################

#####################################
# ENGINE RELATED FUNCTIONS          #
#####################################

def playEngineStartSound():
    try:
        pygame.mixer.music.load(os.path.join(soundsPath, "AMG-65_race.wav"))
        pygame.mixer.music.set_volume(0.7)
        pygame.mixer.music.play()
        print("Engine started")
    except Exception as Argument:
        logging.exception("Error occurred while loading mp3 file")

def startEngine():
    print("Engine Start Process over the Ignition Switch")
    setICLightsToOff()
    playEngineStartSound()
    fadeInTheLights()

def stopEngine():
    print("Engine Stop Process over the Ignition Switch")
    setIgnitionToOff()

#####################################
# END OF ENGINE RELATED FUNCTIONS   #
#####################################

def startMusicMode():
    print("Music Mode started")
    # Control LEDs
    led_front_left.blink(0,0,1,1)
    sleep(1)
    led_front_right.blink(0,0,1,1)
    sleep(0.5)
    led_rear.blink(0,0,1,1)
    

def startRandomSong():
    # TODO: no song repetitions for at least 5 songs.
    # Select random song from the list
    randomSong = random.randrange(0,len(songs))
    previousSong = randomSong
    print('Random song number:', randomSong)
    print('Random song name:', songs[randomSong])
    # Load random song to the pygame mixer
    try:
        pygame.mixer.music.load(os.path.join(filepath, songs[randomSong]))
    except Exception as Argument:
        logging.exception("Error occurred while loading mp3 file")
    
    # Define the volume
    pygame.mixer.music.set_volume(0.9)
    
    # Play the song
    try:
        pygame.mixer.music.play()
    except Exception as Argument:
        logging.exception("Error occurred while starting the song")
    print("Music is now playing...")
    pygame.mixer.music.set_endevent(END_OF_SONG)

def startTheSong(song):
    print('Selected Song number:', song)
    print('Selected Song name:', songs[song])
    # Load random song to the pygame mixer
    try:
        pygame.mixer.music.load(os.path.join(filepath, songs[song]))
    except Exception as Argument:
        logging.exception("Error occurred while loading mp3 file")
    
    # Define the volume
    pygame.mixer.music.set_volume(0.9)
    
    # Start playing the song
    try:
        pygame.mixer.music.play()
    except Exception as Argument:
        logging.exception("Error occurred while starting the song")
    print("Music is now playing...")
    pygame.mixer.music.set_endevent(END_OF_SONG)
    
def announceOFFMode():
    print('Announce OFF Mode')
    try:
        pygame.mixer.music.load(os.path.join(soundsPath, "offmode_announce_1.mp3"))
    except Exception as Argument:
        logging.exception("Error occurred while loading mp3 file")
    pygame.mixer.music.set_volume(0.9)
    pygame.mixer.music.play()

def announceMusicMode():
    print('Announce Music Mode')
    try:
        pygame.mixer.music.load(os.path.join(soundsPath, "musicbox_announce_1.mp3"))
    except Exception as Argument:
        logging.exception("Error occurred while loading mp3 file")
    pygame.mixer.music.set_volume(0.9)
    pygame.mixer.music.play()

def announceCarMode():
    print('Announce Car Mode')
    try:
        pygame.mixer.music.load(os.path.join(soundsPath, "carmode_announce_1.mp3"))
    except Exception as Argument:
        logging.exception("Error occurred while loading mp3 file")
    pygame.mixer.music.set_volume(0.9)
    pygame.mixer.music.play()

def stopTheMusic():
    print('Stop Music or Sounds')
    pygame.mixer.music.stop()

def fadeOutTheLights():
    led_front_left.blink(0,1,0,1,1)
    led_front_right.blink(0,1,0,1,1)
    led_rear.blink(0,1,0,1,1)
    sleep(0.5)

def fadeInTheLights():
    led_front_left.blink(1,0,1,0,1)
    led_front_right.blink(1,0,1,0,1)
    led_rear.blink(1,0,1,0,1)
    led_ic.blink(1,0,1,0,1)
    sleep(1)
    led_front_left.on()
    led_front_right.on()
    led_rear.on()
    led_ic.on()

def setVehicleLightsToOff():
    led_front_left.off()
    led_front_right.off()
    led_rear.off()
    sleep(0.5)

def setVehicleLightsToPoliceMode():
    led_front_left.blink(0.1,0.1,0,0)
    sleep(0.05)
    led_front_right.blink(0.1,0.1,0,0)
    led_rear.blink(0.1,0.1,0,0)

def setVehicleLightsToPolizeiMode():
    led_front_left.blink(1,1,0,0)
    sleep(0.5)
    led_front_right.blink(1,1,0,0)
    led_rear.blink(0.5,0.5,0,0)

def setICLightsToPoliceMode():
    led_blue.blink(0.1,0.1,0,0)
    led_red.blink(0.1,0.1,0,0)

def setICLightsToPolizeiMode():
    led_blue.blink(0.5,0.5,0,0)
    sleep(0.25)
    led_red.blink(0.5,0.5,0,0)

def setICLightsToOff():
    led_blue.off()
    led_red.off()
    led_ic.off()

def setICLightsToIDLE():
    #led_blue.value = 0.2
    #led_red.value = 0.2
    led_ic.blink(1,0,1,1) # Let the IC LED pulse with 2 seconds period

def setIgnitionToOff():
    stopTheMusic()
    setICLightsToOff()
    if led_rear.is_lit:
        fadeOutTheLights()
    else:
        setVehicleLightsToOff()
    print("Ignition State at setIgnitionOff", AMGBobbyCarIgnitionState)
    setICLightsToIDLE()
    

#blink(on_time=1, off_time=1, n=None, background=True)

# Turn all LEDs off at startup.
setVehicleLightsToOff()
setICLightsToOff()

# Let the IC LEDs blink.
setICLightsToIDLE()

# Initialize pygame library
pygame.init()

# Define the event for the end of the song
END_OF_SONG = pygame.USEREVENT+1

# Define the path to the music folder
filepath = os.path.dirname(__file__)
musicpath = os.path.join(filepath, "music")
print(musicpath)
soundsPath = os.path.join(filepath, "sounds")
print(soundsPath)
searchpath = os.path.join(musicpath, "*.mp3")
print(searchpath)
songs = glob.glob(searchpath)
# How many songs are available in the music folder
print(len(songs), 'songs have been found.')

previousSong = 0

# Define the Vehicle Mode
class VehicleMode(Enum):
    OFF = 0
    MUSIC = 1
    CAR = 2
AMGBobbyCarMode = 2

# Define the ignition state
# 0 --> OFF
# 1 --> ON
AMGBobbyCarIgnitionState = 0

SireneState = 0

def turnICLEDOn():
    print("ON/OFF Switch is now ON")
    led_ic.on()

def turnICLEDOff():
    print("ON/OFF Switch is now OFF")
    led_ic.off()
    
OnOffSwitch.when_pressed = turnICLEDOn
OnOffSwitch.when_released = turnICLEDOff

IgnSwitch.when_pressed = startEngine
IgnSwitch.when_released = stopEngine

# Organize the time limit for Martinshorn
sirenTimeLimit = 30 # in seconds
martinshorn_start_time = time()


def evaluateBlueButton():
    print("evaluateBlueButton")
    global AMGBobbyCarIgnitionState
    global AMGBobbyCarMode
    print("Ignition State", AMGBobbyCarIgnitionState)
    print("Car Mode", AMGBobbyCarMode)
    if AMGBobbyCarIgnitionState == 0:
        if AMGBobbyCarMode == 1:                
            # Start music mode
            startMusicMode()
            # Select random song from the list
            randomSong = random.randrange(0,len(songs))
            # Save the previous song before the next song selection
            previousSong = randomSong
            startTheSong(randomSong)
            print('Previous Song:', previousSong)
            sleep(0.5)
            led_red.blink(0,0,1,1)
            sleep(1)
            led_blue.blink(0,0,1,1)
        elif AMGBobbyCarMode == 2:
            startEngine()               
            
        AMGBobbyCarIgnitionState = 1
    else:
        print("Blue Button is pushed.Ignition is not equal to 0 and shall be set to 0.")
        setIgnitionToOff()
        AMGBobbyCarIgnitionState = 0
    sleep(0.2)

def evaluateSteeringWheelRightButton():
    print('Right Button is pressed')
    global AMGBobbyCarIgnitionState
    global AMGBobbyCarMode
    global previousSong
    global SireneState
    global martinshorn_start_time
    if AMGBobbyCarMode == 1 and AMGBobbyCarIgnitionState == 1:
        # Save the previous song before the next song selection
        previousSong = randomSong
        # Select random song from the list
        randomSong = random.randrange(0,len(songs))
        startTheSong(randomSong)
        print('Previous Song:', previousSong)
        sleep(0.5)
    elif AMGBobbyCarMode == 2:
        # Play the sirene sound.
        if SireneState == 0:
            try:
                pygame.mixer.music.load(os.path.join(soundsPath, "martinshorn.mp3"))
                pygame.mixer.music.set_volume(0.7)
                pygame.mixer.music.play()
                martinshorn_start_time = time() # reset the start point for the timer
                print("Martinshorn")
            except Exception as Argument:
                logging.exception("Error occurred while loading mp3 file")
            setVehicleLightsToPolizeiMode()
            setICLightsToPolizeiMode()
            SireneState = 1
        else:
            setIgnitionToOff()
            SireneState = 0
        sleep(0.5)

def on_key_press(key):
    print(f"Key: {key}")
    if key == Key.up:
        evaluateBlueButton()
    elif key == Key.right:
        evaluateSteeringWheelRightButton()

    
def on_key_release(key):
    print("Keyboard Key has been released")
    
try:
    listener_thread = threading.Thread(target=lambda: Listener(on_press=on_key_press, on_release=on_key_release).start())
    listener_thread.start()
except Exception as Argument:
        logging.exception("Error occurred while creating the thread")

while True:          
    
    ###################
    # BLUE BUTTON LOGIC
    ###################
    if blueButton.is_pressed:
        evaluateBlueButton()        
    
    ###################
    # RED BUTTON LOGIC
    ###################    
    if redButton.is_pressed:
        # Turn off the ignition (it doesn´t matter if it is On or Off)
        print("Test Trigger for RED Button")
        setIgnitionToOff()
        
        # Imcrement the Vehicle Mode (Switch the mode of the AMG Bobby Car)
        if AMGBobbyCarMode == 2:
            AMGBobbyCarMode = 1
        else:
            AMGBobbyCarMode = AMGBobbyCarMode + 1
        print("Red Button is pressed")
        
        if  AMGBobbyCarMode == 0:
            if led_rear.is_lit:
                fadeOutTheLights()
            announceOFFMode()
        elif AMGBobbyCarMode == 1:
            if led_rear.is_lit:
                fadeOutTheLights()
            announceMusicMode()
        elif AMGBobbyCarMode == 2:
            if led_rear.is_lit:
                fadeOutTheLights()
            announceCarMode()
        else:
            print("Incorrect AMGBobbyCarMode")
        # Prevent too frequent mode switching
        sleep(1)
    
    ####################################
    # LEFT STEERING WHEEL BUTTON LOGIC #
    ####################################
    if leftSteeringWheelButton.is_pressed:
        print('Left Button is pressed')
        if AMGBobbyCarMode == 1 and AMGBobbyCarIgnitionState == 1:
            # Select random song from the list
            # randomSong = random.randrange(0,len(songs))
            startTheSong(previousSong)
            print('Previous Song:', previousSong)
        elif AMGBobbyCarMode == 2:
            # Play the sirene sound.
            if SireneState == 0:
                try:
                    pygame.mixer.music.load(os.path.join(soundsPath, "sirene_part1.mp3"))
                    pygame.mixer.music.set_volume(0.2)
                    pygame.mixer.music.play()
                    print("Sirene")
                except Exception as Argument:
                    logging.exception("Error occurred while loading mp3 file")
                setVehicleLightsToPoliceMode()
                setICLightsToPoliceMode()
                SireneState = 1
            else:
                setIgnitionToOff()
                SireneState = 0
        else:
            print("Szenario noch nicht implementiert")
        sleep(0.5)
    
    #####################################
    # RIGHT STEERING WHEEL BUTTON LOGIC #
    #####################################
    if rightSteeringWheelButton.is_pressed:
        evaluateSteeringWheelRightButton()
    
    if SireneState == 1:
        elapsed_time = time() - martinshorn_start_time
        if elapsed_time >= sirenTimeLimit:
            print("Martinshorn will be automatically deactivated")
            setIgnitionToOff()
            SireneState = 0
            
    #rightSteeringWheelButton.when_released = stopTheMusic()    
    
    # Wait for the END of the song.
    for event in pygame.event.get():
        if event.type == END_OF_SONG:
            print('End of song')
            # Play the next random song only in music mode.
            if AMGBobbyCarMode == 1 and AMGBobbyCarIgnitionState == 1:
                startRandomSong()


