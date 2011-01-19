#!/usr/bin/env bash
# shaozx@gmail.com  2009-10-12
#     sudo apt-get install bluez-utils
#     sh bluelock.sh &

# Set your bluetooth address here. Get it with "hcitool scan".
BT_ADDR="00:22:A5:83:A8:F8"

# CONTROL MODE
# 0 auto unlock only
# 1 auto lock only
# 2 both lock and unlock
MODE=2

# How often to check for the device? Note that scanning too often may have a
# negative impact on your battery life.
FREQ_LOCK=120        # lock screen, 180 seconds later
FREQ_UNLOCK=7        # unlock screen


# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !!!!  STOP HERE !!!! NOTHING MORE TO CONFIGURE !!!!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

export LC_ALL=C

HCITOOL="hcitool"
SCREEN_CMD="gnome-screensaver-command"

BT_CMD="$HCITOOL name $BT_ADDR"
SCREEN_LOCK="$SCREEN_CMD -l"
SCREEN_UNLOCK="$SCREEN_CMD -d"
SCREEN_QUERY="$SCREEN_CMD -q"

# Do we have hcitool?
which $HCITOOL > /dev/null
if [ $? -ne 0 ]
then
    echo "$HCITOOL not found, install bluez-utils first."
    echo "Command: sudo apt-get install bluez-utils"
    exit 1
fi

# Do we have gnome-screensaver-command?
which $SCREEN_CMD > /dev/null
if [ $? -ne 0 ]
then
    echo "$SCREEN_CMD not found"
    exit 1
fi

# start screen-saver
#gnome-screensaver 1>/dev/null 2>/dev/null

# Enter main loop
while true
do
    printf "\n$(date +'%Y%m%d %H:%M:%S') MODE=$MODE "

    SSTAT=`$SCREEN_QUERY | awk 'NR==1{print $4}'`
    if [ "$SSTAT" = "active" ]
    then
        SSTAT=1
    elif [ "$SSTAT" = "inactive" ]
    then
        SSTAT=0
    else
        printf "\nerror screensaver, will retry later.\n"
        sleep 60 && continue
    fi

    printf "SSTAT[$SSTAT] "

    [ $MODE -eq 0 -a $SSTAT -eq 0 ] && sleep $FREQ_LOCK && continue
    [ $MODE -eq 1 -a $SSTAT -eq 1 ] && sleep $FREQ_UNLOCK && continue

    BSTAT=`$BT_CMD`
    [ $? -ne 0 ] && echo "error bluetooth" && sleep 60 && continue

    BSTAT=${#BSTAT}
    [ $BSTAT -gt 0 ] && BSTAT=1

    printf "BSTAT=$BSTAT "

    RETVAL="${MODE}${SSTAT}${BSTAT}"
    printf "RETVAL=$RETVAL "

    if [ $RETVAL = "100" -o $RETVAL = "200" ]
    then
        # confirm again ( prevent lock by mistake )
        #
        # sleep 3
        # BSTAT=`$BT_CMD`
        # [ $? -ne 0 ] && echo "error bluetooth" && sleep 60 && continue
        # BSTAT=${#BSTAT}
        # [ $BSTAT -gt 0 ] && continue
        #
        printf " LOCK "
        `$SCREEN_LOCK`
        sleep $FREQ_UNLOCK
        continue
    fi

    if [ $RETVAL = "211" -o $RETVAL = "011" ]
    then
        printf " UNLOCK "
        `$SCREEN_UNLOCK`
        sleep $FREQ_LOCK
        continue
    fi

    #else
    [ $SSTAT -eq 1 ] && sleep $FREQ_UNLOCK && continue
    [ $SSTAT -eq 0 ] && sleep $FREQ_LOCK && continue

done

##   =========================================================
##   only deal with there condition:
##   MODE     SSTAT    BSTAT    OPERATION
##   0        0        ?        NOTHING
##   1        1        ?        NOTHING
##   1        0        0        LOCK
##   2        0        0        LOCK
##   2        1        1        UNLOCK
##   0        1        1        UNLOCK
##   0        1        0        NOTHING
##   1        0        1        NOTHING
##   2        0        1        NOTHING
##   2        1        0        NOTHING
##
##   =========================================================
##   unlock only
##   MODE     SSTAT    BSTAT    OPERATION
##   0        0        ?        NOTHING
##   0        1        0        NOTHING
##   0        1        1        UNLOCK
##
##   lock only
##   MODE     SSTAT    BSTAT    OPERATION
##   1        0        0        LOCK
##   1        0        1        NOTHING
##   1        1        ?        NOTHING
##
##   both lock and unlock
##   MODE     SSTAT    BSTAT    OPERATION
##   2        0        0        LOCK
##   2        1        0        NOTHING
##   2        0        1        NOTHING
##   2        1        1        UNLOCK

