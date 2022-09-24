from termcolor import colored
from processing import *
from graphing import *
from reading import *
import traceback
import os

if __name__ == "__main__":
    """ The main program. """

    # Get program configuration
    config = parser.get_config()

    # Read in the data files
    data = config['data_types'].copy()
    for key in list(data.keys()):
        try:
            data[key] = read_data.read_data_files(os.path.join(config["data_locations"]["processed"], data[key]))
        except:
            traceback.print_exc()
            print(colored(f"Fatal Error: Unable to read {key} data from '{data[key]}'.\n", 'red'))
            exit(1)

    exit(0)
