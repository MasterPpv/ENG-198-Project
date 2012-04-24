mjpg_streamer -i "input_uvc.so d /dev/video0 -y" -o "output_http.so -p 8090" & 
python2 dalek.py
