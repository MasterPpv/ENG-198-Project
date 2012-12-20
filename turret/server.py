#!/usr/bin/env python
# vim: tabstop=4 shiftwidth=4 noexpandtab

#from encodings import aliases
#from encodings import hex_codec
import os
import sys
import optparse
import json
import unittest
import time
import signal
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from urlparse import urlparse
from urlparse import parse_qs



class pyshoter(BaseHTTPRequestHandler):


	"""
	Server request handler.
	"""

	# URI Handling Functions

	def log_message(self,  *args, **kwargs):
		pass



	def move_up(self, params):
		"""
		move up.
		"""
		succsess=self.turret.up()

		output = {"success":"up"}

		self.respond()
		output = json.dumps(output)
		self.wfile.write(output)

	def move_down(self, params):
		"""
		move down.
		"""
		succsess=self.turret.down()

		output = {"success":"down"}

		self.respond()
		output = json.dumps(output)
		self.wfile.write(output)




	def move_left(self, params):
		"""
		move left.
		"""
		succsess=self.turret.left()

		output = {"success":"left"}

		self.respond()
		output = json.dumps(output)
		self.wfile.write(output)



	def move_right(self, params):
		"""
		move right.
		"""
		succsess=self.turret.right()

		output = {"success":"right"}

		self.respond()
		output = json.dumps(output)
		self.wfile.write(output)

	def move_stop(self, params):
		"""
		move stop.
		"""
		succsess=self.turret.stop()

		output = {"success":"stop"}

		self.respond()
		output = json.dumps(output)
		self.wfile.write(output)

	def move_fire(self, params):
		"""
		move fire.
		"""
		succsess=self.turret.fire()
		time.sleep(1)

		output = {"success":"fire"}

		self.respond()
		output = json.dumps(output)
		self.wfile.write(output)

	def scriptPage(self, params):
		"""
		Display the webpage
		"""
		parsedURL = urlparse(self.path)

		xpath = parsedURL.path.replace("/","")
		f = open(xpath)
		if f:
			self.send_response(200)
			self.end_headers()
			self.wfile.write(f.read())
		else:
			self.send_error(404, "wrong web file app file path")
	def jarloader(self, params):
		"""
		Display the applit
		"""
		parsedURL = urlparse(self.path)

		xpath = parsedURL.path.replace("/","")
		f = open(xpath)
		if f:
			self.send_response(200)
			self.end_headers()
			self.wfile.write(f.read())
		else:
			self.send_error(404, "wrong webe file app file path")

	def mobileloader(self, params):
		"""
		Display the mobile webpage
		"""
		parsedURL = urlparse(self.path)

		xpath = parsedURL.path.replace("/","")
		f = open(xpath)
		if f:
			self.send_response(200)
			self.end_headers()
			self.wfile.write(f.read())
		else:
			self.send_error(404, "wrong webe file app file path")

# These map URIs to handlers depending on request method
	GET_PATHS = {
		'index.html':scriptPage,
		'USB_Web_Launcher_Client.jar':jarloader,
		'mobile.html':mobileloader,
		'gun': {
			'up': move_up,
			'down': move_down,
			'left': move_left,
			'right': move_right,
			'stop': move_stop,
			'fire': move_fire,
			'temp2': move_down,

		},
	}

	POST_PATHS = {

	}



	def explode_path(self, parsedURL):
		"""
		Seperate a URL path into subcomponents for each directory.

		@type  parsedURL: parsed URL path
		@param parsedURL: The path to be seperated.

		@rtype: list
		@return: A list of all the directories in the path.
		"""

		exploded_path = parsedURL.path[1:].split('/')
		search_paths = []

		if exploded_path[0] == '':
			self.send_error(403, "Requests to the root are invalid.\
					Did you mean /index.html?")
			return

		for path in exploded_path:
			if path is not '':
				search_paths.append(path)

		search_paths.append('')
		return search_paths


	def walk_path(self, search_dict, search_path):
		"""
		Walk the PATHS object to find the correct handler based on the
		URL query sent.

		@type  search_dict: dictionary
		@param search_dict: Dictionary of different request handlers.

		@type  search_path: list
		@param search_path: Exploded URL list of path components.

		@rtype: function
		@return: The server class function that should be used as the
				handler for the given URL request.
		"""

		first_item = search_path.pop(0)
		if first_item in search_dict:
			if isinstance(search_dict[first_item], dict):
				return self.walk_path(search_dict[first_item], \
						search_path)
			else:
				return search_dict[first_item]
		else:
			return None

	def send_error(self, code, text):
		"""
		Send out an error to the requestor using JSON.

		@type  code: int
		@param code: HTTP/1.1 status code to send out.

		@type  text: string
		@param text: Error message to send out.
		"""

		# send_error doesn't do JSON responses; we
		# want json, so here's our own error thing
		self.send_response(code)
		self.send_header('Content-type', 'application/json')
		self.end_headers()
		self.wfile.write(json.dumps({'error': text}))

	def respond(self):
		"""
		Send out an HTTP 200 (OK status) and JSON content-type header.
		"""
		self.send_response(200)
		self.send_header('Content-type', 'application/json')
		self.end_headers()

	# HTTP Request Handlers

	def do_GET(self):
		"""
		Process a client's GET request, parsing the URL and passing data
		to the appropriate handler method, and writing JSON data out.
		"""
		parsedURL = urlparse(self.path)
		params = parse_qs(parsedURL.query)

		search_paths = self.explode_path(parsedURL)
		handler = self.walk_path(self.GET_PATHS, search_paths)
		if handler is not None:
			handler(self, params)
		else:
			self.send_error(404, "Unknown resource identifier: %s" % self.path)


	def do_POST(self):pass

