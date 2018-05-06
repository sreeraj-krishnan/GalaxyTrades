import sys
import json
import os
from pprint import pprint

class JSONReader(object):
	
	def __init__(self, filename):
		self.filename = filename
	
	
	def get_json(self):
	    fullpath = self.filename
            cwd = os.getcwd()
            if not os.path.isfile(fullpath):
                fullpath = os.path.join(cwd , self.filename)
                if not os.path.isfile(fullpath):
                    print "File ", self.filename  ," does not exist "
                    sys.exit()
            else:
                fullpath = self.filename
			
            with open(fullpath) as data_file: 
		data = json.load(data_file)
		
            return data


if __name__ == '__main__':
    pass
    #j = JSONReader(sys.argv[1])

    #print j.get_json()['symbols'][0]['name']
    #print j.get_json()['symbols'][0]['repeat']
    #print str(j.get_json()['symbols'][0]['next_allowed_for_subtraction'][0])

