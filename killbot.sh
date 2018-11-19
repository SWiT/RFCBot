#!/bin/bash
echo "End wiimote process"
sudo pkill -ef -9 "^wminput"
echo "End drive.py"
sudo pkill -ef -9 "python.*drive\.py"
