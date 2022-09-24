from termcolor import colored
import rioxarray as rxr
import xarray as xr
import netCDF4
import h5py
import os
from pyhdf import SD

def read_hdf(file_path):
    """
        Reads in a hdf file.
        :param file_path: The hdf file to read.
        :return: A netCDF4 Dataset.
    """
    return SD.SD(file_path)


def read_netcdf(file_path):
    """
        Reads in a netCDF file.
        :param file_path: The netCDF file to read.
        :return: A netCDF4 Dataset.
    """
    return netCDF4.Dataset(os.path.abspath(file_path), 'r', format='NETCDF4')


def get_directory_files(directory_path):
    """
        Gets all the file paths within a directory.
        :param directory_path: The path to the directory to get files from.
        :return: An array of filepaths.
    """
    # Make this path have all forward-slashes, to make usable with Windows machines
    directory_path = directory_path.replace("\\", "/")

    # Check if the path exists and is a directory
    if not (os.path.exists(directory_path) and os.path.isdir(directory_path)):
        raise Exception(colored(f"Error: The directory does not exist! '{directory_path}'", "red"))

    # Get and return items
    files = [os.path.join(directory_path, s).replace("\\", "/") for s in os.listdir(directory_path)]

    # Send warning if this is an empty directory
    if len(files) == 0:
        raise Exception(colored(f"Error: '{directory_path}' is an empty directory.", "red"))
    return files


def read_data_files(directory_path):
    """
        Reads in all the files from a directory into their data format.
        :param directory_path:
        :return: A list of data files.
    """
    # Get files
    print(colored(f"Trying to read files from: '{directory_path}'...", 'blue'))
    files = get_directory_files(directory_path)

    # Read in each file
    data = []
    for file in files:
        try:
            if file.endswith('.hdf'):
                data.append(read_hdf(file))
            else:
                data.append(read_netcdf(file))
        except:
            print(colored(f"Warning: Unable to read '{file}', data will be ignored.", 'yellow'))

    print(colored(f"Reading successful!\n", 'green'))
    return data
