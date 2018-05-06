
class TradeSymbol(object):
	
	def __init__(self, name, value):
		self.name  = name
		self.value = value
		
	def get_name(self):
		return self.name
	
	def get_value(self):
		return self.value

        @staticmethod
        def parse_trade_symbol(tokens):
                lvalue = tokens[0]
                rvalue = tokens[-1]
                
                #print lvalue, ' : ', rvalue
                
                return TradeSymbol(lvalue, rvalue)
                    
