
from roman_symbol import RomanSymbol
from trade_symbol import TradeSymbol
from trade_item   import TradeItem

class Question(object):
        def __init__(self, question):
            self.question = question
            self.answer = str()
            self.is_valid_question = False

        def get_question(self):
            return self.question

        def is_valid(self):
            return self.is_valid_question

        def parse_question(self, trade_symbols, trade_items ):
            split_question =  self.question.split(' is ')

            if len(split_question) != 2:
                self.answer = "I have no idea what you are talking about"
                return

            lvalue = split_question[0]
            rvalue = split_question[1]
            
            unit_of_measurement = None
            Found = False

            for tok in lvalue.split():
                
                if tok == None:
                    continue
                elif Found:
                    self.answer = 'Invalid token "' + tok + '"'
                    return 

                if tok.lower() in ['how' , 'many' , 'much' ]:
                    if Found:
                        self.answer = " Invalid question or statement"
                        return
                    else:
                        continue

                elif tok in trade_items.keys():
                    unit_of_measurement = tok
                    Found = True
                else:
                    self.answer = 'Invalid token "' + tok + '"'
                    return
            
            # no unit of measure found on left side of the question, means right side is a value

            if True:
                roman_string = str()
                decimal = 0
                end = False
                which_item = None
                answer = ''
                for tok in rvalue.split():
                    
                    unicode_val = unicode(tok, 'utf-8')

                    if end:
                        self.answer = " Not a proper question , so cannot answer"
                        return 
                    
                    elif tok == '?':
                        end = True
                    
                    elif tok in trade_symbols.keys():
                        answer = answer + tok + ' '
                        roman_string = roman_string + trade_symbols[tok].get_value()
                    
                    elif tok in trade_items.keys():
                        answer = answer + tok + ' '
                        which_item = tok

                    elif unicode_val.isnumeric():
                        answer = answer + tok + ' '
                        decimal = int(tok)
                    
                    else:
                        self.answer = 'Invalid token "' + tok + '"'
                        return


                if decimal == 0 and len(roman_string) == 0:
                    decimal = 1

                elif decimal > 0 and len(roman_string) > 0:
                    self.answer = 'Provide either roman number or hindu-arabic number, but not both'
                    return 
                
                if len(roman_string) > 0:
                    decimal = RomanSymbol.roman_to_decimal( roman_string )
                    if decimal == 0:
                        self.answer = 'Invalid number system , cannot answer your question'

                if which_item == None: # only roman numbe value asked
                    self.answer = answer + 'is ' + str(decimal)
                    self.is_valid_question = True
                else:
                    val = 0
                    unit = unit_of_measurement
                    trade_key = which_item
                    if unit_of_measurement != None:
                        trade_key = which_item + unit_of_measurement

                    for key in TradeItem.tradedunits.keys():
                        if key.startswith(trade_key):
                            val = TradeItem.tradedunits[key] 
                            if unit_of_measurement == None:
                               unit = key.replace(which_item,"")
                            break

                    if val > 0:
                        self.answer = answer + 'is ' + str( int(decimal*val)) + ' ' + unit
                        self.is_valid_question = True
                    else:
                        # how much Silver is Gold ?
                        # asked question does not have direct relationship
                        # so find trades which has a common denomitator
                        # check test.input , if you see Silver is 17 credits , Gold is 14450 
                        # so Gold = 850 Silver 
                        from_item = False
                        to_item   = False
                        exchange_medium_item1 = {}
                        exchange_medium_item2 = {}
                        val1 = None
                        val2 = None
                        for key in TradeItem.tradedunits.keys():
                            
                            if key.startswith(which_item):
                                
                                from_item = True
                                val1 = TradeItem.tradedunits[key]
                                exchange_medium_item1[ key.replace(which_item, "") ] = val1

                            elif key.startswith(unit_of_measurement):
                                to_item = True
                                val2 = TradeItem.tradedunits[key]
                                exchange_medium_item2 [ key.replace(unit_of_measurement,"") ] = val2

                        if from_item and to_item:
                            val = 0
                            k = None
                            for k in exchange_medium_item1.keys():
                                if k in exchange_medium_item2.keys():
                                    val = float(exchange_medium_item1[k]* decimal) / exchange_medium_item2[k]
                                    medium = k
                            if val > 0:
                                self.answer = answer + 'is ' + str( int(val) ) + ' ' + unit
                                self.is_valid_question = True
                             
                        
                        elif which_item != None:
                            self.answer  = 'No trades found using ' + which_item
                            if unit_of_measurement != None:
                                self.answer  = self.answer + ' and ' + unit_of_measurement 


                


        def get_answer(self):
            return self.answer
