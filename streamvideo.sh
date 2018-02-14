#!/bin/bash
echo "Using raspivid piped to cvlc to stream over http on port 8160."
raspivid -o - -t 0 -w 640 -h 480 -fps 30 |cvlc -vvv stream:///dev/stdin --sout '#standard{access=http,mux=ts,dst=:8160}' :demux=h264


