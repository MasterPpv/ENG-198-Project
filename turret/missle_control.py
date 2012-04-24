

class missle_control(object):
	letterinput = "o"
	def server_status(self):
		return {
			'server_active': "yes",
			'time':"not impimented",
			
		}
	def up(self): 
		#print self.letterinput
		self.letterinput = "w"
		print self.letterinput
		#return "up";
	def down(self): 
		
		self.letterinput = "s" 
		print self.letterinput
		#return "down";
	def left(self): 
		
		self.letterinput = "a"
		print self.letterinput
		#return "left";
	def right(self): 
		 
		self.letterinput = "d"
		print self.letterinput
		#return "right";
	def stop(self): 
		 
		self.letterinput = " "
		print "\"stop\""
		#return "stop";
	def fire(self):
		#global letterinput
		self.letterinput = "f"
		print self.letterinput
		#return "fire";
	
	


