#!/bin/bash

 cd /home/rvibek/git/covid19_jhu;
 git pull;
 git add .;
 git commit -m "$(date +'%Y-%m-%d %H:%M:%S')";
 git push
