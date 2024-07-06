# ESW - Lung Sound Recorder

```
- wheeze
- none
- nonwheeze
- crackle
```
These are the classes we are classifying the audio to.

## How to initialize

- Install the required python libraries
- Connect the device you are running the server on, and the esps to the same Wifi.
- In the  ```server.py``` code, have to update the ```esp_ip``` variable with the Ip address of the ESP
- This is done to obtain the audio file in the File system of the ESP.
- And also update the ```ip``` to ip address of the PC.
- In the ESP code, update the  ```address ``` varaible with the above ip address of the PC. 
- This is to send "start" and "stop" requests to the server.

## Running the server

```
python3 server.py
```

Open the URL in the terminal. You can login and record the sounds. To start the recording, simply unplug & plug the ESP. 

Default credentials we are using to use this model. (use this in login page)

```
Username: bunny
Password: 123456
```

## Other files

- You can find other noise reduction files, classificaiton files in ```misc``` folder.
- the static and templates folders are for the UI
