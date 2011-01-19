#!/bin/bash
#
# shaozx@gmail.com  2010-10-19
#
# Usage:
#    ./netspeed.sh             runs 60 seconds by step 1s, default to eth0
#    ./netspeed.sh eth1 10     runs 10 seconds by step 1s, default to eth1
#    ./netspeed.sh eth1 90 5   runs 90 seconds by step 5s, default to eth1


IF="eth0"     # net card device
TIME=60       # run $TIME seconds before quit
STEP=1        # wait $STEP seconds
IFCONF="/sbin/ifconfig"
[ ! -x "/sbin/ifconfig" ] &&
	IFCONF=`type ifconfig | awk '{print $NF}' | sed 's/(\|)//g'`

[ "$1" != "" ] && IF=$1
[ "$2" != "" ] && TIME=$2
[ "$3" != "" ] && STEP=$3


## ========================================= ##
##           DO NOT NEED CHANGE              ##
## ========================================= ##

export LC_ALL=C

function show_sum()
{
	#printf "\n%s\n" "[`date +'%Y-%m-%d %H:%M:%S'`](END)"
	echo 
	echo
	#printf "%d seconds,\n" $RUN
	#printf "rx from %d to %d\n" $RX_I $RX
	#printf "tx from %d to %d\n" $TX_I $TX
	echo   '-----------------------------------'
	printf "|    |    TOTAL(K)   |   AVG(K/S) |\n"
	echo   '|---------------------------------|'
	printf "|RX  |%12d   |%10d  |    runs %d seconds\n"  \
		$(( (RX-RX_I)/1024 )) $(( (RX-RX_I)/1024/$RUN )) \
		$RUN
	printf '|---------------------------------|    rx from %d to %d\n' \
		$RX_I $RX
	printf "|TX  |%12d   |%10d  |    tx from %d to %d\n" \
		$(( (TX-TX_I)/1024 )) $(( (TX-TX_I)/1024/$RUN )) \
		$TX_I  $TX
	echo   '-----------------------------------'
	exit 0
}

trap show_sum INT
stty intr ^C

TX_OLD=0
RX_OLD=0

echo 
echo "   IF: $IF     TIME: ${TIME}s (step=${STEP}s) (down/up)"
echo '----------------------------------------------------------'

while [ 1 ]
do
	LINE=`$IFCONF $IF | grep "TX bytes"`

	RX=`echo $LINE | cut -d: -f2 | awk '{print $1}'`
	TX=`echo $LINE | cut -d: -f3 | awk '{print $1}'`

	if [ $TX_OLD -eq 0 -a $RX_OLD -eq 0 ]
	then
		RX_I=$RX; TX_I=$TX; RX_OLD=$RX; TX_OLD=$TX; RUN=0
		sleep $STEP
		continue
	fi

	RUN=$((RUN+STEP))
	if [ $RUN -ge $TIME ]
	then
		show_sum
		break
	fi

	RX_SUB=`expr $RX - $RX_OLD`
	TX_SUB=`expr $TX - $TX_OLD`
	RX_SUB=`expr $RX_SUB / $STEP / 1024`
	TX_SUB=`expr $TX_SUB / $STEP / 1024`

	RX_OLD=$RX
	TX_OLD=$TX

	printf "%s%-10s" "[`date +'%Y-%m-%d %H:%M:%S'`]" "($((TIME-RUN)))"
	printf "%10d%10d (K/S)\n" $RX_SUB $TX_SUB

	sleep $STEP

done
