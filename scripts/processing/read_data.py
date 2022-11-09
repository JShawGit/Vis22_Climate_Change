from termcolor import colored
from pyhdf.SD import SD, SDC
import pandas as pd
import xarray as xr
import netCDF4
import os

# https://geonetcast.wordpress.com/2021/03/26/reading-modis-terra-hdf-files-with-pyhdf/

def read_netcdf(file_path):
    """
        Reads in a netCDF file.
        :param file_path: The file to read.
        :return: An xarray Dataset.
    """
    # Read the NetCDF dataset
    return xr.open_dataset(file_path)

def read_netcdf4(file_path):
    """
        Reads in a netCDF file.
        :param file_path: The file to read.
        :return: A netCDF4 Dataset.
    """
    # Read the NetCDF dataset
    return netCDF4.Dataset(file_path, 'r')


def read_hdf(file_path):
    """
        Reads in an HDF file.
        :param file_path: The file to read.
        :return: An HDF Dataset.
    """
    # Read the HDF dataset
    return SD(file_path, SDC.READ)


def read_file(file_path):
    """
        Reads in a data file.
        :param file_path: The file to read.
        :return: A Dataset.
    """
    # If NetCDF
    if 'nc' in file_path.split('.')[-1]:
        return read_netcdf(file_path)
    # If HDF
    else:
        return read_hdf(file_path)


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
    files = [os.path.abspath(os.path.join(directory_path, s)).replace("\\", "/") for s in os.listdir(directory_path)]

    # Send warning if this is an empty directory
    if len(files) == 0:
        raise Exception(colored(f"Error: '{directory_path}' is an empty directory.", "red"))
    return files


def read_directory_files(directory_path):
    """
        Reads from the files within a directory.
        :param directory_path: A path containing data.
        :return: An array of dataframes.
    """
    files = get_directory_files(directory_path)
    results = []
    for file in files:
        data = read_file(os.path.join(directory_path, file))
        if data is not None:
            results.append(data)
    return results


def read_modis(data_location):
    """
        Gets useful information from MODIS data filenames.
        :param data_location: Location of all the modis files
        :return: A dictionary of filenames and their metadata.
    """
    filepaths = get_directory_files(data_location)
    metadata = {}
    for filepath in filepaths:
        file = filepath.split('/')[-1]
        metadata[file] = {
            'satellite': file[:3],
            'start_time': pd.Timestamp(year=int(file[9:13]), month=1, day=1),
            'end_time': pd.Timestamp(year=int(file[28:32]), month=12, day=31),
            'horiz': file[18:20],
            'vert': file[21:23]
        }
    return metadata
