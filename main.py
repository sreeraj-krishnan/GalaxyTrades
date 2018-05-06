import sys
import os
from galaxy_trader import GalaxyTrader 

if __name__ == '__main__':
    if len(sys.argv) >= 2:
        input_filename = sys.argv[1]
        cwd = os.getcwd()
        configuration_file = os.path.join(cwd,"configuration", "roman_symbols.json")
        if not os.path.isfile(configuration_file):
            print "cannot access file ", configuration_file
            sys.exit(1)

        g = GalaxyTrader(input_filename, configuration_file )
        g.parse_input_process_output()

    else:
        print "usage : python main.py <input-file-name>"

