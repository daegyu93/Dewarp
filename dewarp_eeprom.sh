#!/bin/bash

python3 save_config.py $1 

export DISPLAY=:0

gst-launch-1.0 nvv4l2camerasrc device=/dev/video$1 ! \
"video/x-raw(memory:NVMM),format=(string)UYVY,width=(int)1920,height=(int)1080,framerate=(fraction)30/1" ! \
queue ! nvvidconv ! nvdewarper config-file=config/dewarper_config_$1.txt ! nvvidconv ! nv3dsink