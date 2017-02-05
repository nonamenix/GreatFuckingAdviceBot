#!/usr/bin/env bash

PID=$(cat ".pid")

if ps -p $PID > /dev/null
then exit 0
else exit -1
fi
