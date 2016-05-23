#!/usr/bin/env python

from twisted.internet import reactor, protocol
import os
import fnmatch
import commands
import sys



class ServerChoiceProtocol(protocol.Protocol):

	'''
	Server program that will perform actions depending on the clients choice
	'''

	def __init__(self, factory):
		'''
		Constructor Method
		'''

		self.factory = factory
		
	def dataReceived(self,data):
		print(data)
		'''
		Data will be received representing a choice of action to be performed
		Each choice will set in motion a different action
		'''
		if data == 'validate':
			self.validate()
		elif data == 'start server':
			self.start_server()
			
		else:
			self.get_data(data)
			
			
			
	def validate(self):
		'''
		Function that creates an empty list, then populates it when any mp3 file in my music folder
		Mp3val program then scans each file in the list individually for validation
		program then returns the output of scan to the user
		'''
			
		mp3_list = []

		def scan(musicfile):
			  scan=commands.getoutput('mp3val '+ '"' + (musicfile) + '"' + ' -lout.log')
			  print(scan)
			  


		for root, dirnames, filenames in os.walk('/home/roger/Music'):
			for filename in fnmatch.filter(filenames, '*.mp3'):
				mp3_list.append(os.path.join(root,filename ))
				
		
		for musicfile in mp3_list:
			scan=commands.getoutput('mp3val '+ '"' + (musicfile) + '"' + ' -lout.log')
			self.transport.write(scan)
			
	def start_server(self):
		'''
		Function that changes directory into musicbrainz folder
		then starts up the musicbrainz server
		'''
		os.chdir('/home/roger/musicbrainz-server') 
		os.system('plackup -Ilib -r &') 
		
		self.transport.loseConnection()
		
	
	def get_data(self,song):
		'''
		Function that passes the clients song choice into an existing python code as a command line argument
		This code then retrieves metadata of that song from the musicbrainz server
		and returns the output to the client
		'''
		
		metadata = commands.getoutput('python high_level_metadata_Done.py' + ' ' + song ) 
		print(metadata)
		self.transport.write(metadata)

class ServerChoiceFactory(protocol.ServerFactory):

	'''
	Factory class
	'''

	
	def buildProtocol(self, addr):
		'''
		Builds protocol instance
		'''
		# Build the Protocol for client connection
		return ServerChoiceProtocol(self)

print ('server running')
# Create the Factory, listen for connections & start the Reactor
Val = ServerChoiceFactory()
reactor.listenTCP(1500, Val)
reactor.run()
