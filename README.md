# AMGBobbyCar
Python Project for the AMG Bobby Car

## To Dos:

- [ ] Implementiere die erste Version der Spracherkennung (Polizei, Kindermusik, Auto, Weihnachtsbaum)


## How to stop the Python Script which is running since Boot
In the Terminal:  ps aux|grep pytho  
Then  
sudo kill -9 <Process ID>

## Hardware Configuration

### Green Button  
Function: SYSTEM ON/OFF  
**LED**: GPIO2  
**BUTTON**: GPIO3

### Steering Wheel Left Button
Function: e.g. previous song, police siren    
**BUTTON**: GPIO20

### Steering Wheel Right Button
Function: e.g. next song, fire-engine siren    
**BUTTON**: GPIO26

### Blue Button
Function: Ignition ON/OFF    
**LED**: GPIO25  
**BUTTON**: GPIO10

### Red Button
Function: Mode Switch    
**LED**: GPIO21  
**BUTTON**: GPIO15

### Ignition Switch
Function: Ignition Switch    
**BUTTON**: GPIO9  

### ON/OFF Switch
Function: Switch    
**BUTTON**: GPIO11  

### Front left light
Function: Light    
**LED**: GPIO18  

### Front right light
Function: Light    
**LED**: GPIO17

### Rear lights
Function: Light    
**LED**: GPIO27

### Blue Instrument Cluster lights
Function: Light    
**LED**: GPIO22

