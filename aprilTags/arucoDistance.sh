#!/bin/bash

export DISPLAY=:0.0

sleep 15
if [ -c /dev/video0 ]
then
  cd /home/issacpv/project
  source /home/issacpv/project/env/bin/activate
  python3  arucoDistance.py
fi
