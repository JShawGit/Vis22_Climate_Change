from data_preprocessing import *
from termcolor import colored
from processing import *
import traceback
import os

if __name__ == "__main__":
    """ Preprocesses the data. """

    # Get program configuration
    config = parser.get_config('../config/setup_configuration.json')

    # Read in the data files
    data = config['data_types'].copy()

    # Preprocess the data
    preprocess_data.preprocess(config["data_types"], config["data_locations"], config["coordinate_ranges"])

    """
    land = read_data.get_directory_files(os.path.join(config["data_locations"]["preprocessed"], data['land']))
    for l in land:
        print(pd.read_hdf(l))

    item = read_data.read_modis(land[0])
    print("-------\n")
    """

    # https://rspatialdata.github.io/land_cover.html
    # print(MODIS.MODIStsp_get_prodlayers("MCD12Q1"))

    # https://github.com/dominiktraxl/firetracks/blob/master/02_create_land_cover_table.py
    # https://lpdaac.usgs.gov/documents/875/MCD64_User_Guide_V6.pdf
    # https://appeears.earthdatacloud.nasa.gov/task/area
    # https://disc.gsfc.nasa.gov/datasets/ACOS_L2S_9r/summary


    exit(0)
