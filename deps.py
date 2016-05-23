import imp
import os
import apt


class Dependencies():
	''' class to install neccessary dependencies'''
	def __init__(self,deps):
		self.deps = deps
		self.get_deps()
		#self.get_mp3val()
		
	
	def get_deps(self):
		
		try:
			imp.find_module(self.deps)
			found = True
			print(self.deps + 'already installed')
		except ImportError:
			found = False
			if self.deps == 'xmltodict':
				os.system('sudo pip install xmltodict')
			else:	
				os.system('sudo apt-get install python-' + self.deps)
		
	
	@staticmethod		
	def get_mp3val():
		
		cache = apt.Cache()
		cache.open()
		result = cache["mp3val"].is_installed
		
		if result == False:
			os.system('sudo apt-get install mp3val')
		else:
			print('mp3val already installed')
			
def main():
	#os.system('sudo apt-get update')
	dependencies = ['acoustid','urllib2','xmltodict']
	for dep in dependencies:
		Dependencies(dep)
		
	Dependencies.get_mp3val()
	

if __name__ == '__main__':
	main()
