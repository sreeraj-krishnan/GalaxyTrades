import copy
from json_parser import JSONReader
import collections

class RomanSymbol(object):
	#SymbolsMap={}
	symbols = {}
        decimal_to_roman_helper={}

	def __init__(self,name,value,repeatable=False,repeat=0,next_allowed_for_subtraction=[]):
		self.name   = name
		self.value  = int(value)
		self.repeat = int(repeat)

                self.repeatable = False
                if repeatable == 'True':
                    self.repeatable = True
                
                self.next_allowed_for_subtraction = []
                if len( next_allowed_for_subtraction ) > 0:
    		    self.next_allowed_for_subtraction = copy.deepcopy(next_allowed_for_subtraction)
	        
                self.symbols [ name ] = self

		#RomanSymbols.SymbolsMap[name] = self
		
	def get_name(self):
		return self.name
	
	def get_value(self):
		return self.value
	
	def get_repeatable(self):
		return self.repeatable
	
        def set_repeatable(self, val):
		self.repeatable = val
	
        def get_repeat(self):
		return self.repeat
        
        def set_repeat(self,val):
		self.repeat = val
		
	def get_allowed_transitions(self):
		return self.next_allowed_for_subtraction
	
       
        @staticmethod
        def init_decimal_to_roman_helper(conf):
            if len(RomanSymbol.decimal_to_roman_helper) > 0:
                return
            
            for decimal, symbol in conf.get_json()['decimal_to_roman'].iteritems():
                RomanSymbol.decimal_to_roman_helper[ int(decimal) ] = symbol
                #print decimal , symbol
            RomanSymbol.decimal_to_roman_helper = collections.OrderedDict(sorted(RomanSymbol.decimal_to_roman_helper.items()))
            
            #for key in RomanSymbol.decimal_to_roman_helper.keys():
            #    print key

            

        @staticmethod
        def clear():
            RomanSymbols.symbols.clear()

        @staticmethod
        def invalidate_all_higher_literals( current_literal, symbol_map ):
            current_symbol = symbol_map[current_literal]
            current_val = current_symbol.get_value()
            
            mark_for_delete = []

            for sym, symbolobj in symbol_map.iteritems():
                if symbolobj.get_value() > current_val:
                    mark_for_delete.append( sym )

            for item in mark_for_delete:
                del symbol_map[ item ]

        @staticmethod
        def roman_to_decimal( roman_value ):
            length = len(roman_value)

            if length == 0:
                # error , invald input
                return 0

            decimal_value = 0
            index = 0
            succession_count = 1

            prev     = None
            prev_obj = None
            
            symbols_repeat_count_table  = {}
            letter_used_for_subtraction = {}

            # using deepcopy because we are changing the repeat value during parsing
            symbol_reference = copy.deepcopy( RomanSymbol.symbols )

            while index < length:
                current_letter = roman_value[index]
                if current_letter not in symbol_reference.keys():
                    return 0
                
                if current_letter not in symbols_repeat_count_table.keys() :
                    symbols_repeat_count_table[ current_letter ] = 1
                else:
                    val = symbols_repeat_count_table[ current_letter ]
                    symbols_repeat_count_table[ current_letter ] = val + 1
                
                if prev != None and prev == current_letter:
                    if current_letter in letter_used_for_subtraction.keys():
                        return 0
                    succession_count += 1
                    RomanSymbol.invalidate_all_higher_literals(current_letter, symbol_reference )
                else:
                    succession_count = 1
                

                current_obj =  copy.deepcopy(symbol_reference[ current_letter ])
               
                if succession_count > current_obj.get_repeat():
                    return 0
                
                if prev != None and prev in symbol_reference.keys():
                    prev_obj = copy.deepcopy(symbol_reference [ prev ])


                # Only one small-value symbol may be subtracted from any large-value symbol.
                if succession_count > 1 and prev_obj.get_value() < current_obj.get_value():
                    # Invalid , for eg : IIX , it's actually VIII 
                    return 0
                
                # check literals which cannot be repeated and exit
                if not current_obj.get_repeatable() and symbols_repeat_count_table[ current_letter ] > 1:
                    return 0
                
                val=0
                if current_obj:
                    val = current_obj.get_value()
                
                if current_letter in letter_used_for_subtraction.keys() and  current_obj.get_value() < prev_obj.get_value() :
                    return 0
                
                #if current_letter in letter_used_for_subtraction.keys() and  current_letter == prev :
                #    return 0
                
                elif prev_obj != None and prev_obj.get_value() < current_obj.get_value():
                    
                    if current_letter not in prev_obj.get_allowed_transitions():
                        # cannot subtract prev from current_letter as its not allowed as per definition
                        return 0
                    else:
                        # that which is subtracted cannot come again, eg MMMCMC -> invalid , here last C is not valid
                        # however XLIX is valid and is 49 , here X is subtracted from L but X is not used its actually 9 IX

                        #del symbol_reference[ prev ]
                        #letter_used_for_subtraction[ prev ] = True
                        #letter_used_for_subtraction[ current_letter ] = True

                        if current_obj.get_repeatable():
                            #del symbol_reference[current_letter]
                            
                            current_obj.set_repeat ( current_obj.get_repeat() + 1)
                            temp = copy.deepcopy(current_obj)
                            # update dictionary with increment of the repeat
                            del symbol_reference[ current_letter ]
                            symbol_reference[ current_letter ]  = temp
                            
                        # actual operation was a- b, but we had done a+b in the last iteration , so now a-2b as corrective action
                        decimal_value = decimal_value - (2*prev_obj.get_value() ) 

                
                elif symbols_repeat_count_table[ current_letter ] > current_obj.get_repeat() :
                    return 0

                decimal_value = decimal_value + val
                prev = current_letter
                index = index + 1


            return decimal_value
        
        @staticmethod
        def decimal_to_roman(decimal):
            roman  = ''
            index  = 0
            if decimal == 0 :
                return roman
            
            while decimal > 0:
                key = 1
                for k in RomanSymbol.decimal_to_roman_helper.keys():
                    #print 'key : ', k , ' decimal : ' , decimal
                    if k <= decimal:
                        key = k
                        continue
                    else:
                        break
                        
                decimal = decimal - key
                roman = roman + RomanSymbol.decimal_to_roman_helper[key]
            
            return roman


def test_value(val):
    out = RomanSymbol.roman_to_decimal(val)
    print val , ' : ', out
    return out 

def init_roman_symbols(conf):
		
    try:
	symbols = conf.get_json()['symbols']
	for symbol in symbols:
		name   = str(symbol['name'])
		value  = str(symbol['value'])
		repeatable = str(symbol['repeatable'])
		repeat = str(symbol['repeat'])
		next_allowed_for_subtraction = symbol['next_allowed_for_subtraction']
		transitions = []
		for transition in next_allowed_for_subtraction:
			transitions.append(str(transition))
	                #print transition	
		roman = RomanSymbol(name,value,repeatable,repeat,transitions)
			
		
				
    except Exception as e:
	print e 
	    


def test_decimal_to_roman():
    for i in range(1,4000):
        yield RomanSymbol.decimal_to_roman(i)

def test_roman_to_decimal(roman):
    return RomanSymbol.roman_to_decimal(roman)


def test_all():
    i = 1
    ob = open('roman_to_decimal.json', 'w')
    d = open('decimal_to_roman.json', 'w')
    ob.write('{\n\t"roman_to_decimal" : {\n')
    d.write('{\n\t"decimal_to_roman" : {\n')
    for roman in test_decimal_to_roman():
        if i != test_roman_to_decimal ( roman ):
            print 'test failed for ', i
        else:
            #print 'test passed for ', i , ' : ' , roman
            s = '\t"' + roman  + '"' + " : " +  str(i) + ','
            da = '\t"' + str(i)  + '" : "' +  roman + '" , \n'
            ob.write('\n' + s )
            d.write( da )
        i += 1

    ob.write('\n}\n}')
    d.write('\n}\n}')
    ob.close()
    d.close()

if __name__ == '__main__':
    conf = JSONReader('./configuration/roman_symbols.json')
    init_roman_symbols(conf)
    RomanSymbol.init_decimal_to_roman_helper(conf)

    test_all()
    #test_decimal_to_roman()
    #print RomanSymbol.decimal_to_roman(100)
    #print RomanSymbol.decimal_to_roman(2)
    #print RomanSymbol.decimal_to_roman(3)

