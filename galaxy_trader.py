import sys

from parser       import Parser
from json_parser  import JSONReader
from roman_symbol import RomanSymbol
from trade_symbol import TradeSymbol
from trade_item   import TradeItem
from question     import Question


class GalaxyTrader(object):
	
	def __init__(self, input_filename, system_configuration):
		
                self.parser        = Parser(input_filename)
		self.configuration = JSONReader(system_configuration)
		self.roman_symbols  = {}
		self.trade_symbols = {}
		self.trade_items   = {}
		
		RomanSymbol.init_roman_symbols( self.configuration )
                RomanSymbol.init_decimal_to_roman_helper( self.configuration )		
	
        def parse_input_process_output(self):
            
            for type_of_token, tokens in self.parser.parse_single_line():
                line = ''
                for i in tokens:
                    line = line + i + ' '
                #print line 
                if type_of_token == 'ALIAS':
                    trade_symbol = TradeSymbol.parse_trade_symbol(tokens)
                    if isinstance(trade_symbol, str):
                        print trade_symbol , ' -> ' , line
                    else:
                        self.trade_symbols [ trade_symbol.get_name() ] = trade_symbol

                elif type_of_token == 'TRADE':
                    
                    trade_items = TradeItem.parse_trade_item( line , self.trade_symbols)
                    error_logged = False
                    for trade_item in trade_items:
                        if isinstance(trade_item,str) or trade_item == None:
                            if not error_logged:
                                print "Failed to parse line -> " , line
                                error_logged = True
                        else: 
                            self.trade_items[ trade_item.get_name() ] = trade_item

                elif type_of_token == 'UNKNOWN':
                        print "I have no idea what you are talking about -> " , line
                
                elif type_of_token == 'QUESTION':
                    q = Question(line)
                    q.parse_question(  self.trade_symbols, self.trade_items )
                    if not q.is_valid():
                        print q.get_answer() + ' -> ' + q.get_question()
                    else:    
                        print q.get_answer() 


if __name__ == '__main__':
    g = GalaxyTrader(sys.argv[1], sys.argv[2])
    g.parse_input_process_output()


