
from roman_symbol import RomanSymbol

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
                
                if rvalue not in RomanSymbol.symbols.keys():
                    return rvalue + ' is not a valid roman numeral'
                
                if rvalue in RomanSymbol.symbols.keys() and lvalue in RomanSymbol.symbols.keys():
                    return 'Cannot assign one roman literal to another'
                
                return TradeSymbol(lvalue, rvalue)
                    
