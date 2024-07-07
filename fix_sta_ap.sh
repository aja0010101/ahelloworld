#!/bin/sh
#
# Fix loss of AP when STA (Client) mode fails by reverting to default
# AP only configuration. Default AP configuration is assumed to be in
# /etc/config/wireless.ap-only
#
 
sta_err=0
i=15
until [ "$sta_err" -ge 8 ] || [ "$i" -le 0 ]
do
    if [ $(iwinfo | grep -c "ESSID: unknown") -ge 1 ]; then
        sta_err=$((sta_err+1))
    fi
    
    if [ "$sta_err" -ge 8 ]; then
        cp /etc/config/wireless.ap-only /etc/config/wireless
        sleep 1
        wifi up
        sleep 2
    fi
    
    i=$((i-1))
    sleep 1
done
