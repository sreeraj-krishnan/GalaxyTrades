INSTRUCTIONS TO RUN

python main.py <input-file>   # input file can be file in current working directory or full path of the file

You may refer sample test.input file for reference

ASSUMPTIONS MADE:

1. Any valid statement should have the word 'is' and it is case sensitive
2. All aliases consist of 3 words alias name ,is and roman literal
3. A question will always start with 'how' and end with '?'
4. Answer to the question ignores the floating point and displays the decimal value only
5. If a commodity price is changed , then the latest price is always taken into consideration
6. If a commodity is traded in different units , then if only the price of the commodity is asked but not the unit of measurement, then the unit of measurement will always be that of first trade
   For eg, consider below 2 statements
   
   1. glob glob Silver is 34 Credits
   2. glob glob Silver is 10 bronze

   Now consider the question "how much is Silver ?" answer would be in Credits and not in bronze
   
   Answer - Silver is 17 Credits  # IT WON'T BE Silver is 5 bronze
   

7. Q - how Much Silver is Gold ?
   
   Here both Silver and Gold are priced in Credits as per test.input and do not have direct correlation
	glob glob Silver is 34 Credits
	glob prok Gold is 57800 Credits

   From the above we see that Gold to Silver ratio is 850

	Hence the answer is " Gold is 850 Silver "
	

   
 
