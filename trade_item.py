
from roman_symbol import RomanSymbol


class TradeItem(object):
	tradedunits={}
	
	def __init__(self, name, unit, total_value, quantity):
		
		self.name        = name    # item name like Silver
		self.unit        = unit    # unit of measurement like Credits
		self.total_value = int(total_value)    # value of total trade
		self.quantity    = int(quantity)     # total quantity traded
                
		# price per unit traded
		self.unit_price = 0
		if self.quantity != 0:
			if self.total_value%self.quantity != 0:
				pass
				# assert or warn
			
                        # floating not supported	
			self.unit_price  = float( float(self.total_value) / self.quantity) 
		
		key = str(name+unit)
		
		# Below check brings consistency of Silver priced in Credits 
		# cannot have 2 trades with different prices of Silver priced in Credits
		# or can override previous price with latest trade price
		if key in self.tradedunits.keys() and self.tradedunits[key] != self.unit_price:
			# log or warn
			pass
			
		self.tradedunits[key] = self.unit_price
	
	@staticmethod
	def get_unit_price_per_item_using_given_measurement(item_name, unit_of_measurement):
		key = item_name+unit_of_measurement
		if key in TradeItem.tradedunits.keys():
			return TradeItem.tradedunits[key]
		
		return 0
	
        @staticmethod
        def parse_measure_and_unit_of_measure( input_string , trade_symbols ):
                    measure = ''
                    unit_of_measure = ''
                    roman_string=''
                    measure = 0
                    parsed_quantity = False

                    for word in input_string.split():
                        if parsed_quantity:
                            return ('error', 'item name has multiple words and is not supported')
                        
                        unicode_val = unicode(word, 'utf-8')
                        
                        if word in trade_symbols.keys():
                            roman_string = roman_string + trade_symbols[ word ].get_value()
                        
                        elif unicode_val.isnumeric():
                            measure = int(word)
                        
                        else:
                            parsed_quantity = True
                            unit_of_measure = word
                    
                    if measure != 0 and len(roman_string) > 0:
                        return ('error', 'Cannot give both roman and arabic numerals')
                    
                    if measure == 0:
                        measure = RomanSymbol.roman_to_decimal( roman_string ) 
                    
                    if measure == 0:
                        return ('error', 'Invalid roman numeral representation')

                    return ( measure , unit_of_measure )
        
        
        @staticmethod
        def get_trade_item(tok1, tok2 , trade_symbols ):
                quantity_n_item , value_n_measurement = tok1, tok2
                
                quantity , item = TradeItem.parse_measure_and_unit_of_measure( quantity_n_item, trade_symbols )
                total_value , unit_of_measure = TradeItem.parse_measure_and_unit_of_measure( value_n_measurement, trade_symbols )
                
                if quantity != 'error' and total_value != 'error':
                    return TradeItem(item, unit_of_measure , total_value , quantity )
                
                elif quantity == 'error':
                    print item
                    return item
                    
                else:
                    print unit_of_measure
                    return unit_of_measure
                    
                return None
        
        @staticmethod
        def parse_trade_item(tokens , trade_symbols): 
                    toks = tokens.split(' is ')
                    if len(toks) != 2 :
                        return None
                    
                    trade_items = []
                    
                    trade_items.append( TradeItem.get_trade_item( toks[0] , toks[1] , trade_symbols) )  
                    trade_items.append( TradeItem.get_trade_item( toks[1] , toks[0] , trade_symbols) )  

                    return trade_items
                    


        
        def print_unit_value(self):
		return str(self.unit_price) + " " + self.unit 
		
	def get_name(self):
		return self.name
	
	def get_unit(self):
		return self.unit
	
	def get_total_value(self):
		return self.total_value
		
	def get_quantity(self):
		return self.quantity 
	
	def get_unit_price(self):
		return self.unit_price
		
