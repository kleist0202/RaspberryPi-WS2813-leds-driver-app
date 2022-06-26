# RaspberryPi - Control RGB LED Strip from your browser

Controlling RGB WS2813 LED strip from your browser with a Raspberry Pi. 

### General info

Application is written in flask and deployed with Gunicorn and contenerized with Docker. </br>
It uses ```adafruit-circuitpython-neopixel-spi``` python library to control leds via SPI pin.
Python container with application communicates with nginx container for reverse proxy which can be configured as you like.

### Hardware requirements

In order to make this project work, you will need some of these hardware:

* [ ] Raspberry Pi - I tested it only on Raspberry Pi 4 but should work on 2, 3.
* [ ] WS2813 RGB LED Strip - but should also works with WS2812.
* [ ] Pi Power Supply - need 5V for Raspberry.
* [ ] LED Strip Power Supply - Supply voltage: 100 V to 240 V. Output voltage: 5 V DC. Output current: 8. A Capacity: (at least) 40 W.
* [ ] Wiring - You need 2 wires to connect the LEDs D0 data signal and ground.
* [ ] *(Optional)* Soldering Iron .
* [ ] Tools - a wire cutter/stripper would be most helpful to you.  

### Distro

On my Raspberry Pi 4 I installed Ubuntu 22.04 LTS server (but you can try with other distros).

### Installation 

####  Hardware

For this project, you need to connect two pins: ground and D0 data signal:

| Color |  GPIO Pin |
|-------|:---------:| 
| Green |    10     | 
| Black |    GND   |  

### Software

#### 1. Install docker and docker-compose and activate docker service.
#### 2. Clone repostitory into your system (you will need git or just download zip).
#### 3. Enter project diretory.
#### 4. Enter command:
    docker-compose up -d
#### 5. Wait till images and containers are built.
#### 6. Enter IP address of your Raspberry Pi in browser.
#### 7. Enjoy changing your led strip colors!
