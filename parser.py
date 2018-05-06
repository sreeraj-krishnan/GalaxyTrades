import sys
import os

class Parser(object):

    lines=[]

    def __init__(self, filename):
        self.filename = filename
        self.fullpath = str()

    def readlines(self):
        self.fullpath=self.filename
        cwd = os.getcwd()
        if not os.path.isfile(self.filename):
            self.fullpath = os.path.join(cwd , self.filename)
            if not os.path.isfile(fullpath):
                print "File ", self.filename  ," does not exist "
                sys.exit()
        else:
            self.fullpath = self.filename

        try:
            fileobj = open(self.fullpath, 'r')
            for line in fileobj.xreadlines():
                yield line

            fileobj.close()


        except Exception as e:
            print e
            pass
	
    def tokens(self):
	for line in self.readlines():
    	    tokens = line.split()
            yield tokens

    """ 
        Return type of the line, currently considering only 4 types of lines and the tokens of the line
        1. ALIAS line
        2. TRADE line , like an item is traded ( as in 'glob glob Silver is 34 Credits' )
        3. QUESTION - A question to be answered
        4. UNKNOWN line

        Some assumptions here, if 'is' is not found in the line then its an UNKNOWN
        A question is considered if it starts with 'how' and ends with question mark 
        An alias to roman symbol is considered if there are only 3 tokens and middle token is 'is'
    """

    def parse_single_line(self):
	for line in self.readlines():
    	    tokens = line.split()
            
            lower_case_tokens = list(map(str.lower, tokens))

            Type = ""
            token_length = len(tokens)

            if not "is" in lower_case_tokens:
                Type = 'UNKNOWN'

            elif token_length == 3:
                Type = 'ALIAS'

            elif token_length > 3 and lower_case_tokens[-1] == '?':
                if 'how' ==  lower_case_tokens[0]:
                    Type = 'QUESTION'
                else:
                    Type = 'UNKNOWN'

            elif token_length > 3:
                Type = 'TRADE'

            yield Type, tokens
				
	

if __name__ == '__main__':
    p = Parser( sys.argv[1] )
    for Type, tokens in p.parse_single_line():
        print Type, tokens
	
