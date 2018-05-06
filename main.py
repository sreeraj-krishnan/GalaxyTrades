import sys
import os
from galaxy_trader import GalaxyTrader 

if __name__ == '__main__':
    if len(sys.argv) >= 2:
        filename = sys.argv[1]
        cwd = os.getcwd()
        configuration_file = os.path.join(cwd,"configuration", "roman_symbols.json")
        if not os.path.isfile(configuration_file):
            print "cannot access file ", configuration_file
            sys.exit(1)

        g = GalaxyTrader(filename, configuration_file )

    else:
        print "usage : python main.py <input-file-name>"

