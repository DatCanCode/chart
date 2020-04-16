#!/bin/bash
pid=`ps -ef | grep '[s]h -c cd /home/webuser/NhanDienCrystalFacenet/ && python3 routes.py' | awk '{ print $2 }'`
if [ -z "$pid" ]; then
cd /home/webuser/NhanDienCrystalFacenet/ && python3 routes.py
#else
#echo $pid
fi
