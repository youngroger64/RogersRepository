import acoustid
import json
import urllib2
import xmltodict
import sys

sys.argv

# Main Class
class MetaData:
	'''
	Implements an object
	'''

	def __init__(self, line_word, before_word, after_word, path, api_key):
		
		
		self.line_word = line_word
		self.before_word = before_word
		self.after_word = after_word
		self.path = path
		self.api_key = api_key
		
	def __str__(self):
		
		line_before_after = self.line_word, self.before_word, self.after_word
		
	
	def fingerprint_func(self):
		
		fingerprint = acoustid.fingerprint_file(self.path)
		self.line = fingerprint
		
		self.line = str(self.line)
		self.line_word = ""
		self.after_word = "')"
		self.before_word = ", '"
		self.num = 1
		self.lines_func()
		self.duration_func()
	
	
	def duration_func(self):
		self.line_word = ""
		self.after_word = "."
		self.before_word = "("
		self.num = 2
		self.artist = ""
		self.file_name = ""
		self.label = ""
		self.genre = ""
		self.length = "" 
		self.song = ""
		self.tracknum = ""
		self.date = ""
		self.lines_func()
		
		
	
	def id_func(self):
		key = self.api_key
		duration = self.duration
		fingerprint = self.fingerprint
		
		website = "http://api.acoustid.org/v2/lookup?client="+key+"&duration="+duration+"&fingerprint="+fingerprint+"&meta=recordingids"
		response = urllib2.urlopen(website)
		
		data = json.load(response)
		self.line = str(data)
		
		self.line_word = "[{u'recordings': [{u'id': u'"
		self.after_word = "'}"
		self.before_word = "[{u'recordings': [{u'id': u'"
		self.num = 3
		self.lines_func()
		
		
	################ MetaData ###############################
	
	
	def error_check_func(self):
		ID = self.ID
		website = "http://acousticbrainz.org/"+ID+"/high-level"
		
		try:
			response = urllib2.urlopen(website)
		except urllib2.HTTPError, e:
			if e.code:
				print "ERROR"
				apikey = self.api_key
				fingerprint = self.fingerprint
				duration = self.duration
				
				
				data = acoustid.lookup(apikey, fingerprint, duration)
				
				result = acoustid.parse_lookup_result(data)
				
				for line in result:
					self.song = line[2]
					self.artist = line[3]
				self.dict_func()
				
				return None
				
		except urllib2.URLError, e:
			print e.args,"tr"
		self.artist_func()
	
	
	def artist_func(self):
		ID = self.ID
		website = "http://acousticbrainz.org/"+ID+"/high-level"
		print (ID)
	
		response = urllib2.urlopen(website)
		URL = "http://127.0.0.1:5000/ws/2/recording/15ad175a-8520-4d58-b39c-33d06e1ec3db?inc=aliases%2Bartist-credits%2Breleases"
		response = urllib2.urlopen(URL)
				

		
		response = urllib2.urlopen(website)
		self.data = json.load(response)   
		#print self.data
		
		#print data
		self.artist = (self.data['metadata']['tags']['artist'][0])
		metadata = (self.data['metadata'])
		tags = (self.data['metadata']['tags'])
		self.file_name_func()
		#print metadata
		#print self.artist
		
	def file_name_func(self):
		try:
			self.file_name = (self.data['metadata']['tags']['file_name'])
			self.label_func()
		except :
			self.label_func()
		#print self.file_name
		
		
	def label_func(self):
		try:
			self.label = (self.data['metadata']['tags']['label'][0])
			genre_func()
		except:
		#print self.label
			self.genre_func()
	def genre_func(self):
		try:
			self.genre = (self.data['metadata']['tags']['length'][0])
			self.title_func()
		except:
		#print self.genre
			self.title_func()
		
			
	def title_func(self):
		try:
			self.song = (self.data['metadata']['tags']['title'][0])
			self.tracknum_func()
		except:
		#print self.song
			self.tracknum_func()
		
		
	def tracknum_func(self):
		try:
			self.tracknum = (self.data['metadata']['tags']['tracknumber'][0])
			self.date_func()
		except:
		#print self.tracknum
			self.date_func()
		
	def date_func(self):
		try:
			self.date = (self.data['metadata']['tags']['date'][0])
			self.dict_func()
		except:
			self.dict_func()
		
		#print self.date
	def dict_func(self):
		#self.label = "0"
		self.dict_list = {'Artist': self.artist, 'File Name': self.file_name, 'Label': self.label, 'Genre': self.genre, 'Length': self.duration, 'Song': self.song, 'Tracknum' : self.tracknum, 'Date' : self.date}
		
		print "Artist:",self.dict_list['Artist']
		print "File Name:",self.dict_list['File Name']
		print "Label:",self.dict_list['Label']
		print "Genre:",self.dict_list['Genre']
		print "Length:",self.dict_list['Length']
		print "Song:",self.dict_list['Song']
		print "Track Number:",self.dict_list['Tracknum']
		print "Date of realease:",self.dict_list['Date']

	################ LineFunc #####################
	
	def lines_func(self):
		
		line = str(self.line)

		if self.line_word in line:
			#deletes everything before and including selected string
			line=line.split(self.before_word ,-1)[-1] 
			#deletes everything after and including selected string
			line=line.split(self.after_word,1)[0]
			
			#gets rid of whitespaces
			line=line.strip()
			
			
		if self.num == 1:
			self.fingerprint = line
			#print line
		elif self.num == 2:
			self.duration = line
			self.id_func()
			#print line
		elif self.num == 3:
			self.ID = line
			#print self.ID
			self.error_check_func()



def main():
	'''
	Main function to test code
	'''
	x = ("")
	y = ('')
	z = ('') ################  ENTER FILE NAME ##################################
	p = "/home/roger/" + sys.argv[1]
	a = "9xdt1PNn"
	
	
	test = MetaData(x, y, z, p, a)

	test.fingerprint_func()

if __name__ == '__main__':
	main()












 

