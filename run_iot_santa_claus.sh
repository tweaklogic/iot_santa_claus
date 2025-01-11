#!/bin/bash
# Sometime due to Kasa connectivity error the
# program exits, in case that happens, it is
# restarted. If the program is quit then we
# exit gracefully. 

export DISPLAY=:0

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
pushd "$SCRIPT_DIR" || exit

while true
do
	source python3-venv/bin/activate
	if [ "x$1" == "xadd" ]
	then
		python3 iot_santa_claus.py capture
		python3 iot_santa_claus.py train
		break
	else
		python3 iot_santa_claus.py recog
		if  [ "x$?" == "x0" ]
		then
			break
		fi
	fi
	sleep 5
done
popd
