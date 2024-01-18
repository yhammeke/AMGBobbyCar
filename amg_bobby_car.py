#!/usr/bin/python
import os
print(os.path.dirname(__file__))
# Package for sounds and music
import pygame
# Package for Buttons and Leds
from gpiozero import Button, PWMLED
from time import sleep, time
from datetime import datetime

# Package for random song selection
import random

# Package for file list creation
import glob

# Package for Logging
import logging

from enum import Enum

from pynput.keyboard import Key, Listener
import threading

import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Set up your Spotify credentials
client_id = '0074e2e862b943f19fd2ebdce5e147d9'
client_secret = '742c57785fae420ebeff136bfffe6553'
redirect_uri = 'http://localhost:8888/callback'

# Authenticate with Spotify
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri=redirect_uri,
                                               scope="user-modify-playback-state"))
 
 
# Play a track
track_uri = 'spotify:track:4lY38A2Od1FpAA5ApsWJ9H'  # Replace TRACK_ID with the ID of the track you want to play
sp.start_playback(uris=[track_uri])
 

#https://open.spotify.com/intl-de/track/4lY38A2Od1FpAA5ApsWJ9H?si=165640954d424001

 
# Create and configure logger
# TODO: think about creating one loggin file per day.
current_datetime = datetime.now()
log_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
logging.basicConfig(filename="/home/pi/AMGBobbyCar/logs/log_file.log" + str(log_datetime),
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
    global AMGBobbyCarIgnitionState
    print("Engine Start Process over the Ignition Switch")
    setICLightsToOff()
    playEngineStartSound()
    fadeInTheLights()
    AMGBobbyCarIgnitionState = 1

# By Transition to Engine Off:
# Stop all sounds
# Stop the Music Player
# Let the lights according to the Light Switch State (to be implemented later)
def stopEngine():
    global AMGBobbyCarIgnitionState
    print("Engine Stop Process over the Ignition Switch")
    stopMusicPlayer()
    setIgnitionToOff()
    AMGBobbyCarIgnitionState = 0

#####################################
# END OF ENGINE RELATED FUNCTIONS   #
#####################################


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
    global MusicPlayerState
    if MusicPlayerState == 1:
        led_blue.on()
    else:
        led_blue.off()
    led_red.off()
    led_ic.off()

def setICLightsToIDLE():
    #led_blue.value = 0.2
    #led_red.value = 0.2
    led_ic.blink(1,0,1,1) # Let the IC LED pulse with 2 seconds period

def activateLightsForMusic():
    print("Music Mode for Lights started.")
    # TODO: Move out to the THREAD, so that the Sleep Time will not affect the button behavior.
    # Control LEDs
    # Start with Music Player Status LED (BLUE)
    led_blue.blink(0,0,1,0)
    sleep(1)
    led_blue.on()
    
    #Continue with the rest LEDs
    led_front_left.blink(0,0,1,1)
    sleep(1)
    led_front_right.blink(0,0,1,1)
    sleep(0.5)
    led_rear.blink(0,0,1,1)
    sleep(0.5)
    
def setIgnitionToOff():
    stopTheMusic()
    setICLightsToOff()
    if led_rear.is_lit:
        fadeOutTheLights()
    else:
        setVehicleLightsToOff()
    print("Ignition State at setIgnitionOff", AMGBobbyCarIgnitionState)
    #setICLightsToIDLE()

def startMusicPlayer():
    global MusicPlayerState
    global randomSong
    global previousSong
    global songs
    # Select random song and play it:
    startNextSong()

    # Turn on the LEDs for the music mode
    activateLightsForMusic()
    
    MusicPlayerState = 1
    print("Music Player is ON")

def startNextSong():
    global previousSong
    global recentlyPlayedSongs
    global randomSong
    
    availableSongs = [song for song in songs if song not in recentlyPlayedSongs]
    
    nextSong = random.choice(availableSongs)
    print("Next Song:", nextSong)
    print("Recently Played", recentlyPlayedSongs)
    recentlyPlayedSongs.append(nextSong)
    if len(recentlyPlayedSongs) > 5:
        recentlyPlayedSongs.pop(0) # remove the oldest song
    
    # Save the previous song before the next song selection
    #previousSong = randomSong
    # Select random song from the list
    #randomSong = random.randrange(0,len(songs))
    startTheSong(nextSong)
    #print('Previous Song:', previousSong)
    sleep(0.5)

def startTheSong(song):
    #print('Selected Song:', song)
    #print('Selected Song name:', songs[song])
    # Load random song to the pygame mixer
    try:
        pygame.mixer.music.load(os.path.join(filepath, str(song)))
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
    
def stopMusicPlayer():
    global MusicPlayerState
    stopTheMusic()
    #setICLightsToOff()
    
    if led_rear.is_lit:
        fadeOutTheLights()
    else:
        setVehicleLightsToOff()
    
    # Fade out the Music Player Status LED
    led_blue.blink(0,0,0,1)
    sleep(1)
    led_blue.off()
    
    
    MusicPlayerState = 0
    
    print("Music Player is OFF")

def stopTheMusic():
    print('Stop Music or Sounds')
    pygame.mixer.music.stop()

# How to use the LED BLINK function:
# led_x.blink(on_time=1, off_time=1, n=None, background=True)

########################
# INIT BEHAVIOR
########################

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


#################################################
# IMPORTANT STATE MACHINE VARIABLES
#################################################

# Set the value of the global variable AMGBobbyCarIgnitionState according to the position of the Ignition Switch.
if IgnSwitch.is_pressed:
    AMGBobbyCarIgnitionState = 1
else:
    AMGBobbyCarIgnitionState = 0

# Music Player is OFF at startup
MusicPlayerState = 0

SireneState = 0

previousSong = 0
recentlyPlayedSongs = []


########################
# STARTUP BEHAVIOR
########################

# Turn all LEDs off at startup.
setVehicleLightsToOff()
setICLightsToOff()

# Let the IC LEDs blink.
# setICLightsToIDLE()


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
sirenTimeLimit = 45 # in seconds
martinshorn_start_time = time()

# Blue Button shall only start or stop the music player
def evaluateBlueButton():
    print("evaluateBlueButton")
    global MusicPlayerState
    if MusicPlayerState == 0: # Player shall be started
        startMusicPlayer()
    else:
        stopMusicPlayer()
    sleep(0.2)

def startMartinshorn():
    global SireneState
    global martinshorn_start_time
    # Sound Control
    try:
        pygame.mixer.music.load(os.path.join(soundsPath, "martinshorn.mp3"))
        pygame.mixer.music.set_volume(0.7)
        pygame.mixer.music.play()
        # reset the start point for the Shutdown timer
        martinshorn_start_time = time() 
        print("Martinshorn")
    except Exception as Argument:
        logging.exception("Error occurred while loading mp3 file")
    
    # Light Control
    setVehicleLightsToPolizeiMode()
    setICLightsToPolizeiMode()
    
    # State Control
    SireneState = 1
    print("SireneState: ", SireneState)

def stopMartinshorn():
    global SireneState
    # Sound Control
    stopTheMusic()
    # Light Control
    setICLightsToOff()
    if led_rear.is_lit:
        fadeOutTheLights()
    else:
        setVehicleLightsToOff()
    #State Control
    SireneState = 0
    print("SireneState: ", SireneState)

def startPoliceSiren():
    global SireneState
    global martinshorn_start_time
    
    # Sound Control
    try:
        pygame.mixer.music.load(os.path.join(soundsPath, "sirene_part1.mp3"))
        pygame.mixer.music.set_volume(0.7)
        pygame.mixer.music.play()
        # reset the start point for the Shutdown timer
        martinshorn_start_time = time() 
        print("Martinshorn")
    except Exception as Argument:
        logging.exception("Error occurred while loading mp3 file")
    
    # Light Control
    setVehicleLightsToPoliceMode()
    setICLightsToPoliceMode()
    
    # State Control
    SireneState = 1
    print("SireneState: ", SireneState)

# Steering Wheel Right Button shall Start/Stop Martinshorn if the Engine is On/Off OR
# it shall select the next song of the music player.
# If the Engine is ON AND Music Player is running, then Music Player function has higher priority.
def evaluateSteeringWheelRightButton():
    print('Right Button is pressed')
    global MusicPlayerState
    global AMGBobbyCarIgnitionState
    global SireneState
    global martinshorn_start_time
    
    if MusicPlayerState == 1:
        startNextSong()
    elif MusicPlayerState == 0 and AMGBobbyCarIgnitionState == 1:
        # Play the sirene sound.
        if SireneState == 0:
            startMartinshorn()            
        else:
            stopMartinshorn()
    else:
        print("Not wished situation")
    
    sleep(0.5)

# Steering Wheel Left Button shall Start/Stop American Police Siren if the Engine is On/Off OR
# it shall select the previous song of the music player.
# If the Engine is ON AND Music Player is running, then Music Player function has higher priority.
def evaluateSteeringWheelLeftButton():
    print('Left Button is pressed')
    global MusicPlayerState
    global AMGBobbyCarIgnitionState
    global SireneState
    global previousSong
    global martinshorn_start_time
    
    if MusicPlayerState == 1:
        startTheSong(previousSong)
    elif MusicPlayerState == 0 and AMGBobbyCarIgnitionState == 1:
        # Play the sirene sound.
        if SireneState == 0:
            startPoliceSiren()            
        else:
            stopMartinshorn()
    else:
        print("Not wished situation")
    
    sleep(0.5)
    
def on_key_press(key):
    print(f"Key: {key}")
    if key == Key.shift: # Start/Stop the Music player
        evaluateBlueButton()
    elif key == Key.page_up: # 
        evaluateSteeringWheelRightButton()
    elif key == Key.page_down:
        evaluateSteeringWheelLeftButton()

    
def on_key_release(key):
    if key == Key.enter: # Temporary solution, no need for now.
        print("Keyboard Key has been released")
    
try:
    listener_thread = threading.Thread(target=lambda: Listener(on_press=on_key_press, on_release=on_key_release).start())
    listener_thread.start()
except Exception as Argument:
        logging.exception("Error occurred while creating the thread")

##########################
# MAIN LOOP
##########################

while True:          
    
    # BLUE BUTTON LOGIC
    if blueButton.is_pressed:
        evaluateBlueButton()        
        
    # LEFT STEERING WHEEL BUTTON LOGIC #
    if leftSteeringWheelButton.is_pressed:
        evaluateSteeringWheelLeftButton()
    
    # RIGHT STEERING WHEEL BUTTON LOGIC #
    if rightSteeringWheelButton.is_pressed:
        evaluateSteeringWheelRightButton()
    
    
    if SireneState == 1:
        elapsed_time = time() - martinshorn_start_time
        if elapsed_time >= sirenTimeLimit:
            print("Martinshorn will be automatically deactivated")
            stopMartinshorn()  
    
    # Wait for the END of the song AND start the next random song.
    for event in pygame.event.get():
        if event.type == END_OF_SONG:
            print('End of song')
            # Play the next random song only if music player is on.
            if MusicPlayerState == 1:
                startNextSong()

###########################################################
                #BACKUP


    ###################
    # RED BUTTON LOGIC
    ###################    
#     if redButton.is_pressed:
#         # Turn off the ignition (it doesn´t matter if it is On or Off)
#         print("Test Trigger for RED Button")
#         setIgnitionToOff()
#         
#         # Imcrement the Vehicle Mode (Switch the mode of the AMG Bobby Car)
#         if AMGBobbyCarMode == 2:
#             AMGBobbyCarMode = 1
#         else:
#             AMGBobbyCarMode = AMGBobbyCarMode + 1
#         print("Red Button is pressed")
#         
#         if  AMGBobbyCarMode == 0:
#             if led_rear.is_lit:
#                 fadeOutTheLights()
#             announceOFFMode()
#         elif AMGBobbyCarMode == 1:
#             if led_rear.is_lit:
#                 fadeOutTheLights()
#             announceMusicMode()
#         elif AMGBobbyCarMode == 2:
#             if led_rear.is_lit:
#                 fadeOutTheLights()
#             announceCarMode()
#         else:
#             print("Incorrect AMGBobbyCarMode")
#         # Prevent too frequent mode switching
#         sleep(1)

# def announceOFFMode():
#     print('Announce OFF Mode')
#     try:
#         pygame.mixer.music.load(os.path.join(soundsPath, "offmode_announce_1.mp3"))
#     except Exception as Argument:
#         logging.exception("Error occurred while loading mp3 file")
#     pygame.mixer.music.set_volume(0.9)
#     pygame.mixer.music.play()
# 
# def announceMusicMode():
#     print('Announce Music Mode')
#     try:
#         pygame.mixer.music.load(os.path.join(soundsPath, "musicbox_announce_1.mp3"))
#     except Exception as Argument:
#         logging.exception("Error occurred while loading mp3 file")
#     pygame.mixer.music.set_volume(0.9)
#     pygame.mixer.music.play()
# 
# def announceCarMode():
#     print('Announce Car Mode')
#     try:
#         pygame.mixer.music.load(os.path.join(soundsPath, "carmode_announce_1.mp3"))
#     except Exception as Argument:
#         logging.exception("Error occurred while loading mp3 file")
#     pygame.mixer.music.set_volume(0.9)
#     pygame.mixer.music.play()

# def startRandomSong():
#     global randomSong
#     global previousSong
#     # TODO: no song repetitions for at least 5 songs.
#     # Select random song from the list
#     randomSong = random.randrange(0,len(songs))
#     previousSong = randomSong
#     print('Random song number:', randomSong)
#     print('Random song name:', songs[randomSong])
#     # Load random song to the pygame mixer
#     try:
#         pygame.mixer.music.load(os.path.join(filepath, songs[randomSong]))
#     except Exception as Argument:
#         logging.exception("Error occurred while loading mp3 file")
#     
#     # Define the volume
#     pygame.mixer.music.set_volume(0.9)
#     
#     # Play the song
#     try:
#         pygame.mixer.music.play()
#     except Exception as Argument:
#         logging.exception("Error occurred while starting the song")
#     print("Music is now playing...")
#     pygame.mixer.music.set_endevent(END_OF_SONG)
