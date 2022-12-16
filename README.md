# Repository for 1. semester project for Master education in Mechanical Engineering with specialisation in Manufactoring Technology

## Overview:
[![License](https://img.shields.io/github/license/sgaasd/VT1Welding)](https://github.com/sgaasd/VT1Welding)
[![Github code size](https://img.shields.io/github/languages/code-size/sgaasd/VT1Welding)](https://github.com/sgaasd/VT1Welding)
[![Github issue tracker](https://img.shields.io/github/issues/sgaasd/VT1Welding)](https://github.com/sgaasd/VT1Welding)
[![Commit activity](https://img.shields.io/github/commit-activity/w/sgaasd/VT1Welding)](https://github.com/sgaasd/VT1Welding)


## Table of content
[Installation guide](#Installation)<br/>
[Launch Dashboard](#Dashboard)<br/>
[Launch data acquisition pipeline](#DataAcquisition)<br/>



## Intallation
In root directory run:
```
pip install -r requirements.txt
```


## Dashboard
In root directory run
```
Dashboard.py
```
To view the page open the following link: [http://127.0.0.1:8050](http://127.0.0.1:8050)

The Dashbboard will automatically open the live page showing the most recent results.

When changing the page use the three options in the righthand corner.

On the previous page use the dropdown menu to choose which results to visualise.

On the KPI page use the calendar to choose which day you would like to see the KPIs for.


## Data acquisition pipeline

Before conducting your experiment make sure that the [simi-constant-params](https://github.com/sgaasd/VT1Welding/blob/main/Data/meta/00_semi_constant_param.csv) are correct for your testing

Connect ethernet from the PLC to the PC

Make sure that both the webcam an microphone is connected to the pc

Run the robot program first then in root directory run
```
main.py
```

Then through the terminal you will be guided through


### Physical dependencies

- [ReSpeaker USB 4 Mic array](https://wiki.seeedstudio.com/ReSpeaker-USB-Mic-Array/)

- 1080p 30fps webcam, does not need to be a specific webcam but the one used was: [C920 HD Pro Webcam](https://www.logitech.com/da-dk/products/webcams/c920-pro-hd-webcam.960-001055.html)

- [Migatronic Cowelder](https://www.migatronic.com/da/)
