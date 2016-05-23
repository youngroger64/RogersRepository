import fnmatch
import commands
from twisted.internet import reactor, protocol
import time


class ChoiceClientProtocol(protocol.Protocol):

	'''
	Client Class that presents user with a choice of actions to take
	Choice 1) Validate a music file
	Choice 2) Start the Musicbrainz Server
	Choice 3) Retrieve metadat for a music file
	'''

	

	def connectionMade(self):
		'''
		When connection is made, present user with options
		Send users choice to the server
		'''
		
		print(' -------------------------------------')
		print(' What action would you like to perform\n -------------------------------------')
		choice = int(input(' 1: Validate musicfiles \n 2: Start Musicbrainz Server \n 3: Enter a song to retrieve metadata: \n ------------------------------------- \n    Enter Choice here:  '))
		
		
		if choice == 1:
			self.transport.write('validate')
		elif choice ==2:
			self.transport.write('start server')
			
			self.transport.loseConnection()
			
		else:
			self.song_title()
		
				
	def song_title(self):
			print(' -------------------------------------')
			print(' -------------------------------------')
			song = raw_input('    Enter Song Title: ')
			
			self.transport.write("'" + (song) + "'")
			
			

				
	def dataReceived(self,data):
		''' Print the data received from the server '''
		print (data)
		reactor.stop()
			
		
		
			
				   


class ChoiceClientFactory(protocol.ClientFactory):

    '''
    Factory Class to create the protocol
    '''

    def buildProtocol(self, addr):
        '''
        Buid Protocol that will return the client protocol
        '''

        
        return ChoiceClientProtocol(self)


# Create the Factory, connect to the server & run the reactor
Val = ChoiceClientFactory()
reactor.connectTCP('localhost', 1500, Val)
reactor.run()
