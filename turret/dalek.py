import os
import sys
import termios
import fcntl

import platform
import time
import socket
import urllib
import re
import json
import threading
import thread

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import server as a


import pygame

import usb.core
import usb.util

#from missle_control import missle_control

# Protocol command bytes
DOWN    = 0x01
UP      = 0x02
LEFT    = 0x04
RIGHT   = 0x08
FIRE    = 0x10
STOP    = 0x20

DEVICE = None

exterminate = "ext1.wav"
dalekGun  = "dalekgun.wav"


def usage():
    print ""
    print "Commands:"
    print "  W          - move up"
    print "  S          - move down"
    print "  D          - move right"
    print "  A          - move left"
    print "  Space      - stop"
    print "  F          - fire"
    print "  R          - reset to center position"
    print "  K          - kill program"    
    print ""


def setup_usb():
    # Tested only with the Cheeky Dream Thunder
    global DEVICE 
    DEVICE = usb.core.find(idVendor=0x2123, idProduct=0x1010)

    if DEVICE is None:
        raise ValueError('Missile device not found')

    # On Linux we need to detach usb HID first
    if "Linux" == platform.system():
        try:
            DEVICE.detach_kernel_driver(0)
        except Exception, e:
            pass # already unregistered    

    DEVICE.set_configuration()


def send_cmd(cmd):
    DEVICE.ctrl_transfer(0x21, 0x09, 0, 0, [0x02, cmd, 0x00,0x00,0x00,0x00,0x00,0x00])


def play_sound(wavFile):
	if os.path.isfile(wavFile):
		pygame.init()
		sound = pygame.mixer.Sound(wavFile)
		sound.play()

		    
def getch():
	fd = sys.stdin.fileno()
	
	oldterm = termios.tcgetattr(fd)
	newattr = termios.tcgetattr(fd)
	newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
	termios.tcsetattr(fd, termios.TCSANOW, newattr)

	oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
	fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)

	try:
		while 1:
			try:
				c = sys.stdin.read(1)
				break
			except IOError: pass
	finally:
		termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
		fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)
	return c

class control():

    def right(self) :
        send_cmd(RIGHT)
    def left(self) :
        send_cmd(LEFT)
    def up(self) :
        send_cmd(UP)
    def down(self) :
        send_cmd(DOWN)
    def stop(self) :
        send_cmd(STOP)
    def fire(self) :
        send_cmd(FIRE)
        play_sound(dalekGun)
        time.sleep(5)
	termios.tcflush(sys.stdin, termios.TCIOFLUSH)
    def exit(self) :
        print""
	print "SHUT DOWN SEQUENCE INITIATED"
        sys.exit(0)
        

def listen(server) :
	
	while 1:
		x=getch()
                #try: 
			
			#x = raw_input('hi')
			#x = gitch()
		
		'''
		try:
			print x
			print "hi"
		except:
			time.sleep(1)
		time.sleep(2)
		'''
		#print x		
		#x="o"
		#	print "error"
		if x == 'w':
			send_cmd(UP)
		if x == 'a':
			send_cmd(LEFT)	
		if x == 's':
			send_cmd(DOWN)
		if x == 'd':
			send_cmd(RIGHT)
		if x == ' ':
			send_cmd(STOP)
		if x == 'f':
			print "yes I think i am :)"
			send_cmd(FIRE)
			play_sound(dalekGun)
			time.sleep(5)
			termios.tcflush(sys.stdin, termios.TCIOFLUSH)
		if x == 'r':
			send_cmd(LEFT)
			time.sleep(6)
			send_cmd(DOWN)
			time.sleep(1)
			send_cmd(RIGHT)
			time.sleep(3)
			send_cmd(UP)
			time.sleep(.5)
			send_cmd(STOP)
			termios.tcflush(sys.stdin, termios.TCIOFLUSH)
		if x == 'k':
			print""
			print "SHUT DOWN SEQUENCE INITIATED"
                        server.shutdown()
                        break

class turretHandler (a.pyshoter)  :
    turret = control()

def Thread_listen(Thread,listen): pass
def main(args):
	#play_sound(exterminate)	
	usage()
        setup_usb()
	server = HTTPServer(('', 7000), turretHandler)
	#Thread_listen(threading.Thread(),listen)
	thread.start_new_thread(listen,(server,))	
	
	
	server.allow_reuse_address = True
	server.serve_forever()
	
	sys.exit(0)

if __name__ == '__main__':
    main(sys.argv)
